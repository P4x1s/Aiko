import json
import time

import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class AlibabaProvider(BaseProvider):
    """Alibaba Tongyi (Qwen) API provider."""

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        model_name = self.get_model_name(model)

        payload = {
            "model": model_name,
            "input": {
                "messages": messages,
            },
            "parameters": {},
        }

        if "temperature" in kwargs:
            payload["parameters"]["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["parameters"]["max_tokens"] = kwargs["max_tokens"]
        if "top_p" in kwargs:
            payload["parameters"]["top_p"] = kwargs["top_p"]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if stream:
            return self._stream_completion(payload, headers)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/services/aigc/text-generation/generation",
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
                f"{self.BASE_URL}/services/aigc/text-generation/generation",
                json={**payload, "parameters": {**payload.get("parameters", {}), "incremental_output": True}},
                headers={**headers, "X-DashScope-SSE": "enable"},
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        event = json.loads(line[5:])
                        if "output" in event:
                            text = event["output"].get("text", "")
                            if text:
                                yield {
                                    "choices": [{
                                        "delta": {"content": text},
                                        "finish_reason": event["output"].get("finish_reason") == "stop" and "stop" or None,
                                    }]
                                }

    def _format_response(self, response: dict[str, Any], model: str) -> dict[str, Any]:
        output = response.get("output", {})
        usage = response.get("usage", {})
        return {
            "id": f"qwen-{response.get('request_id', int(time.time()))}",
            "model": model,
            "created": int(time.time()),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output.get("text", ""),
                },
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
        }

    def get_model_name(self, model: str) -> str:
        model_map = {
            "qwen-max": "qwen-max",
            "qwen-plus": "qwen-plus",
            "qwen-turbo": "qwen-turbo",
            "qwen-long": "qwen-long",
        }
        return model_map.get(model, model)
