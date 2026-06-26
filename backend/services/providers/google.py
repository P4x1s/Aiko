import json
import time

import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class GoogleProvider(BaseProvider):
    """Google AI (Gemini) provider."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        model_name = self.get_model_name(model)
        contents = []

        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        payload = {"contents": contents}
        url = f"{self.BASE_URL}/models/{model_name}:generateContent?key={self.api_key}"

        if stream:
            url = f"{self.BASE_URL}/models/{model_name}:streamGenerateContent?key={self.api_key}"
            return self._stream_completion(payload, url)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120.0,
            )
            response.raise_for_status()
            return self._format_response(response.json())

    async def _stream_completion(
        self, payload: dict[str, Any], url: str
    ) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        event = json.loads(line[6:])
                        yield self._format_response(event)

    def _format_response(self, response: dict[str, Any]) -> dict[str, Any]:
        candidates = response.get("candidates", [])
        if not candidates:
            return {"choices": [{"message": {"role": "assistant", "content": ""}}]}
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        text = "".join(part.get("text", "") for part in parts)
        usage = response.get("usageMetadata", {})
        return {
            "id": f"google-{int(time.time())}",
            "model": response.get("modelVersion", ""),
            "created": int(time.time()),
            "choices": [
                {
                    "message": {"role": "assistant", "content": text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": usage.get("promptTokenCount", 0),
                "completion_tokens": usage.get("candidatesTokenCount", 0),
                "total_tokens": usage.get("totalTokenCount", 0),
            },
        }

    def get_model_name(self, model: str) -> str:
        model_map = {
            "gemini-pro": "gemini-pro",
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
        }
        return model_map.get(model, model)
