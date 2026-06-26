import json
import time

import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class BaiduProvider(BaseProvider):
    """Baidu ERNIE API provider."""

    BASE_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop"

    def __init__(self, api_key: str, secret_key: str = ""):
        super().__init__(api_key)
        self.secret_key = secret_key
        self.access_token = None

    async def _get_access_token(self) -> str:
        """Get or refresh access token."""
        if self.access_token:
            return self.access_token

        async with httpx.AsyncClient() as client:
            url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
            response = await client.post(url)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        model_name = self.get_model_name(model)
        token = await self._get_access_token()

        payload = {
            "messages": messages,
            **kwargs,
        }

        url = f"{self.BASE_URL}/{model_name}?access_token={token}"

        if stream:
            return self._stream_completion(payload, url)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120.0,
            )
            response.raise_for_status()
            return self._format_response(response.json(), model)

    async def _stream_completion(
        self, payload: dict[str, Any], url: str
    ) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url,
                json={**payload, "stream": True},
                headers={"Content-Type": "application/json"},
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        event = json.loads(line[5:])
                        if "result" in event:
                            yield {
                                "choices": [{
                                    "delta": {"content": event["result"]},
                                    "finish_reason": event.get("is_end") and "stop" or None,
                                }]
                            }

    def _format_response(self, response: dict[str, Any], model: str) -> dict[str, Any]:
        return {
            "id": f"baidu-{response.get('id', int(time.time()))}",
            "model": model,
            "created": int(time.time()),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.get("result", ""),
                },
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "total_tokens": response.get("usage", {}).get("total_tokens", 0),
            },
        }

    def get_model_name(self, model: str) -> str:
        model_map = {
            "ernie-4.0": "completions_pro",
            "ernie-3.5": "completions",
            "ernie-3.5-8k": "ernie-3.5-8k",
            "ernie-speed": "ernie_speed",
        }
        return model_map.get(model, model)
