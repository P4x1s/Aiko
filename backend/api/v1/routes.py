import json
import os
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse

from api.schemas import ChatCompletionRequest
from services.providers import OpenAIProvider, AnthropicProvider, GoogleProvider
from services.api_key_service import verify_api_key

router = APIRouter(prefix="/v1")

providers = {}
if os.getenv("OPENAI_API_KEY"):
    providers["openai"] = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
if os.getenv("ANTHROPIC_API_KEY"):
    providers["anthropic"] = AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"))
if os.getenv("GOOGLE_API_KEY"):
    providers["google"] = GoogleProvider(api_key=os.getenv("GOOGLE_API_KEY"))

model_provider_map: dict[str, str] = {
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "gpt-3.5-turbo": "openai",
    "claude-3-opus": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-sonnet": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    "claude-3-haiku": "anthropic",
    "claude-3-haiku-20240307": "anthropic",
    "gemini-pro": "google",
    "gemini-1.5-pro": "google",
    "gemini-1.5-flash": "google",
}


async def verify_api_key_auth(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format",
        )
    raw_key = authorization[7:]
    key_record = verify_api_key(raw_key)
    if not key_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key",
        )
    return key_record


@router.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    api_key_record: dict = Depends(verify_api_key_auth),
) -> dict[str, Any]:
    provider_name = model_provider_map.get(request.model)
    if not provider_name:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model}' is not supported",
        )

    provider = providers.get(provider_name)
    if not provider:
        raise HTTPException(
            status_code=500,
            detail=f"Provider '{provider_name}' is not configured",
        )

    kwargs: dict[str, Any] = {}
    if request.temperature is not None:
        kwargs["temperature"] = request.temperature
    if request.max_tokens is not None:
        kwargs["max_tokens"] = request.max_tokens
    if request.top_p is not None:
        kwargs["top_p"] = request.top_p

    try:
        if request.stream:
            async def stream_response():
                iterator = provider.chat_completion(
                    model=request.model,
                    messages=[msg.model_dump() for msg in request.messages],
                    stream=True,
                    **kwargs,
                )
                async for chunk in iterator:
                    yield f"data: {json.dumps(chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                stream_response(),
                media_type="text/event-stream",
            )
        else:
            result = await provider.chat_completion(
                model=request.model,
                messages=[msg.model_dump() for msg in request.messages],
                stream=False,
                **kwargs,
            )
            return result
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/models")
async def list_models() -> dict[str, Any]:
    models = []
    for model_name, provider_name in model_provider_map.items():
        if provider_name in providers:
            models.append({
                "id": model_name,
                "object": "model",
                "created": 0,
                "owned_by": provider_name,
            })
    return {"object": "list", "data": models}
