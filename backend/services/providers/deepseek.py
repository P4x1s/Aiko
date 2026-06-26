import json
import time

import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class DeepSeekProvider(BaseProvider):
    """DeepSeek API provider (OpenAI-compatible)."""

    BASE_URL = "https://api.deepseek.com/v1"

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
            "messages": messages,
            "stream": stream,
        }

        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
            return response.json()

    async def _stream_completion(
        self, payload: dict[str, Any], headers: dict[str, str]
    ) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data.strip() == "[DONE]":
                            break
                        yield json.loads(data)

    def get_model_name(self, model: str) -> str:
        model_map = {
            "deepseek-chat": "deepseek-chat",
            "deepseek-coder": "deepseek-coder",
            "deepseek-v2": "deepseek-chat",
        }
        return model_map.get(model, model)
