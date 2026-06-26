import json
import os
import time
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse

from api.schemas import ChatCompletionRequest
from services.providers import (
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    BaiduProvider,
    AlibabaProvider,
    ZhipuProvider,
    DeepSeekProvider,
)
from services.api_key_service import verify_api_key
from services.billing_service import get_balance, deduct_balance, record_usage
from services.token_counter import count_message_tokens, calculate_cost

router = APIRouter(prefix="/v1")

providers = {}
if os.getenv("OPENAI_API_KEY"):
    providers["openai"] = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
if os.getenv("ANTHROPIC_API_KEY"):
    providers["anthropic"] = AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"))
if os.getenv("GOOGLE_API_KEY"):
    providers["google"] = GoogleProvider(api_key=os.getenv("GOOGLE_API_KEY"))
if os.getenv("BAIDU_API_KEY"):
    providers["baidu"] = BaiduProvider(
        api_key=os.getenv("BAIDU_API_KEY"),
        secret_key=os.getenv("BAIDU_SECRET_KEY", ""),
    )
if os.getenv("ALIBABA_API_KEY"):
    providers["alibaba"] = AlibabaProvider(api_key=os.getenv("ALIBABA_API_KEY"))
if os.getenv("ZHIPU_API_KEY"):
    providers["zhipu"] = ZhipuProvider(api_key=os.getenv("ZHIPU_API_KEY"))
if os.getenv("DEEPSEEK_API_KEY"):
    providers["deepseek"] = DeepSeekProvider(api_key=os.getenv("DEEPSEEK_API_KEY"))

model_provider_map: dict[str, str] = {
    # OpenAI
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "gpt-3.5-turbo": "openai",
    # Anthropic
    "claude-3-opus": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-sonnet": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    "claude-3-haiku": "anthropic",
    "claude-3-haiku-20240307": "anthropic",
    # Google
    "gemini-pro": "google",
    "gemini-1.5-pro": "google",
    "gemini-1.5-flash": "google",
    # Baidu
    "ernie-4.0": "baidu",
    "ernie-3.5": "baidu",
    "ernie-3.5-8k": "baidu",
    "ernie-speed": "baidu",
    # Alibaba
    "qwen-max": "alibaba",
    "qwen-plus": "alibaba",
    "qwen-turbo": "alibaba",
    "qwen-long": "alibaba",
    # Zhipu
    "glm-4": "zhipu",
    "glm-4-flash": "zhipu",
    "glm-3-turbo": "zhipu",
    "glm-4-plus": "zhipu",
    # DeepSeek
    "deepseek-chat": "deepseek",
    "deepseek-coder": "deepseek",
    "deepseek-v2": "deepseek",
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

    # Check balance
    user_id = api_key_record["user_id"]
    balance = get_balance(user_id)
    if balance <= 0:
        raise HTTPException(
            status_code=402,
            detail="Insufficient balance. Please recharge.",
        )

    kwargs: dict[str, Any] = {}
    if request.temperature is not None:
        kwargs["temperature"] = request.temperature
    if request.max_tokens is not None:
        kwargs["max_tokens"] = request.max_tokens
    if request.top_p is not None:
        kwargs["top_p"] = request.top_p

    # Estimate input tokens
    messages_dicts = [msg.model_dump() for msg in request.messages]
    input_tokens = count_message_tokens(messages_dicts)

    start_time = time.time()

    try:
        if request.stream:
            async def stream_response():
                nonlocal input_tokens
                output_tokens = 0
                iterator = provider.chat_completion(
                    model=request.model,
                    messages=messages_dicts,
                    stream=True,
                    **kwargs,
                )
                async for chunk in iterator:
                    yield f"data: {json.dumps(chunk)}\n\n"
                    if "choices" in chunk:
                        for choice in chunk["choices"]:
                            if "delta" in choice and "content" in choice["delta"]:
                                output_tokens += count_message_tokens([{"content": choice["delta"]["content"]}])

                yield "data: [DONE]\n\n"

                cost = calculate_cost(request.model, input_tokens, output_tokens)
                latency_ms = int((time.time() - start_time) * 1000)

                deduct_balance(user_id, cost, f"{request.model} ({input_tokens}+{output_tokens} tokens)")
                record_usage(
                    user_id=user_id,
                    api_key_id=api_key_record["id"],
                    provider=provider_name,
                    model=request.model,
                    tokens_input=input_tokens,
                    tokens_output=output_tokens,
                    cost=cost,
                    latency_ms=latency_ms,
                )

            return StreamingResponse(
                stream_response(),
                media_type="text/event-stream",
            )
        else:
            result = await provider.chat_completion(
                model=request.model,
                messages=messages_dicts,
                stream=False,
                **kwargs,
            )

            output_tokens = 0
            if "usage" in result:
                output_tokens = result["usage"].get("completion_tokens", 0)
            elif "choices" in result:
                for choice in result["choices"]:
                    if "message" in choice and "content" in choice["message"]:
                        output_tokens = count_message_tokens([{"content": choice["message"]["content"]}])
                        break

            cost = calculate_cost(request.model, input_tokens, output_tokens)
            latency_ms = int((time.time() - start_time) * 1000)

            deduct_balance(user_id, cost, f"{request.model} ({input_tokens}+{output_tokens} tokens)")
            record_usage(
                user_id=user_id,
                api_key_id=api_key_record["id"],
                provider=provider_name,
                model=request.model,
                tokens_input=input_tokens,
                tokens_output=output_tokens,
                cost=cost,
                latency_ms=latency_ms,
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
