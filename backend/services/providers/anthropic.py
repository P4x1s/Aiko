import httpx
from typing import Any, AsyncIterator

from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic API provider."""

    BASE_URL = "https://api.anthropic.com/v1"

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        model_name = self.get_model_name(model)
        system_message = None
        api_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                api_messages.append({"role": msg["role"], "content": msg["content"]})

        payload: dict[str, Any] = {
            "model": model_name,
            "messages": api_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        if system_message:
            payload["system"] = system_message

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        if stream:
            return self._stream_completion(payload, headers)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/messages",
                json=payload,
                headers=headers,
                timeout=120.0,
            )
            response.raise_for_status()
            return self._format_response(response.json())

    async def _stream_completion(
        self, payload: dict[str, Any], headers: dict[str, str]
    ) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/messages",
                json={**payload, "stream": True},
                headers=headers,
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        import json

                        event = json.loads(line[6:])
                        if event.get("type") == "content_block_delta":
                            yield {
                                "choices": [
                                    {
                                        "delta": {
                                            "content": event["delta"].get("text", "")
                                        }
                                    }
                                ]
                            }

    def _format_response(self, response: dict[str, Any]) -> dict[str, Any]:
        content = response.get("content", [])
        text = "".join(
            block.get("text", "")
            for block in content
            if block.get("type") == "text"
        )
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": text,
                    },
                    "finish_reason": "stop",
                }
            ]
        }

    def get_model_name(self, model: str) -> str:
        model_map = {
            "claude-3-opus": "claude-3-opus-20240229",
            "claude-3-sonnet": "claude-3-sonnet-20240229",
            "claude-3-haiku": "claude-3-haiku-20240307",
        }
        return model_map.get(model, model)
