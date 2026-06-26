import json
import time
import hashlib
import hmac
import base64
from datetime import datetime

import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class ZhipuProvider(BaseProvider):
    """Zhipu AI (GLM) API provider."""

    BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

    def _generate_token(self) -> str:
        """Generate JWT token for Zhipu API."""
        api_key = self.api_key
        # Zhipu API key format: {id}.{secret}
        if "." not in api_key:
            return api_key

        key_id, secret = api_key.split(".", 1)

        # Header
        header = base64.urlsafe_b64encode(
            json.dumps({"alg": "HS256", "sign_type": "SIGN"}).encode()
        ).rstrip(b"=").decode()

        # Payload
        payload = base64.urlsafe_b64encode(
            json.dumps({
                "api_key": key_id,
                "exp": int(time.time()) + 3600,
                "timestamp": int(time.time()),
            }).encode()
        ).rstrip(b"=").decode()

        # Signature
        signing_input = f"{header}.{payload}"
        signature = base64.urlsafe_b64encode(
            hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
        ).rstrip(b"=").decode()

        return f"{header}.{payload}.{signature}"

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        model_name = self.get_model_name(model)
        token = self._generate_token()

        payload = {
            "model": model_name,
            "messages": messages,
        }

        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        if stream:
            return self._stream_completion(payload, headers)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=120.0,
            )
            response.raise_for_status()
            return self._format_response(response.json(), model)

    async def _stream_completion(
        self, payload: dict[str, Any], headers: dict[str, str]
    ) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                json={**payload, "stream": True},
                headers=headers,
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        event = json.loads(line[5:])
                        if "choices" in event:
                            for choice in event["choices"]:
                                delta = choice.get("delta", {})
                                if "content" in delta:
                                    yield {
                                        "choices": [{
                                            "delta": {"content": delta["content"]},
                                            "finish_reason": choice.get("finish_reason"),
                                        }]
                                    }

    def _format_response(self, response: dict[str, Any], model: str) -> dict[str, Any]:
        usage = response.get("usage", {})
        return {
            "id": response.get("id", f"zhipu-{int(time.time())}"),
            "model": model,
            "created": response.get("created", int(time.time())),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.get("choices", [{}])[0].get("message", {}).get("content", ""),
                },
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
        }

    def get_model_name(self, model: str) -> str:
        model_map = {
            "glm-4": "glm-4",
            "glm-4-flash": "glm-4-flash",
            "glm-3-turbo": "glm-3-turbo",
            "glm-4-plus": "glm-4-plus",
        }
        return model_map.get(model, model)
