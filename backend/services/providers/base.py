from abc import ABC, abstractmethod
from typing import AsyncIterator, Any


class BaseProvider(ABC):
    """Base class for AI providers."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        """Send a chat completion request to the provider."""
        ...

    @abstractmethod
    def get_model_name(self, model: str) -> str:
        """Map a generic model name to the provider-specific model name."""
        ...
