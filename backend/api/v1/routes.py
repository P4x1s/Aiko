"""V1 API routes - 参考 sub2api 重构"""

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
from services.billing_v2 import billing_service
from services.token_counter import count_message_tokens, calculate_cost
from services.rate_limiter import check_rate_limit, check_key_rate_limit
from services.concurrency_limiter import ConcurrencyContext, ConcurrencyLimitExceeded
from services.multi_account import multi_account_manager

router = APIRouter(prefix="/v1")

# 模型到 Provider 的映射
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

# 默认并发限制
DEFAULT_USER_CONCURRENCY = 5
DEFAULT_KEY_CONCURRENCY = 10
DEFAULT_USER_RATE = 60  # 每分钟
DEFAULT_KEY_RATE = 120  # 每分钟


async def verify_api_key_auth(authorization: str = Header(...)) -> dict:
    """验证 API Key"""
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
    """聊天补全接口 - 参考 sub2api 重构"""
    user_id = api_key_record["user_id"]
    api_key_id = api_key_record["id"]

    # 1. 检查模型是否支持
    provider_name = model_provider_map.get(request.model)
    if not provider_name:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model}' is not supported",
        )

    # 2. 速率限制检查
    if not check_rate_limit(user_id, DEFAULT_USER_RATE):
        raise HTTPException(
            status_code=429,
            detail="User rate limit exceeded. Please try again later.",
        )

    if not check_key_rate_limit(api_key_id, DEFAULT_KEY_RATE):
        raise HTTPException(
            status_code=429,
            detail="API key rate limit exceeded. Please try again later.",
        )

    # 3. 余额检查
    balance = billing_service.get_balance(user_id)
    if balance <= 0:
        raise HTTPException(
            status_code=402,
            detail="Insufficient balance. Please recharge.",
        )

    # 4. 获取 Provider（多账号轮询）
    provider = multi_account_manager.get_provider(provider_name)
    if not provider:
        raise HTTPException(
            status_code=500,
            detail=f"Provider '{provider_name}' is not configured",
        )

    # 5. 构建请求参数
    kwargs: dict[str, Any] = {}
    if request.temperature is not None:
        kwargs["temperature"] = request.temperature
    if request.max_tokens is not None:
        kwargs["max_tokens"] = request.max_tokens
    if request.top_p is not None:
        kwargs["top_p"] = request.top_p

    # 6. 估算输入 tokens
    messages_dicts = [msg.model_dump() for msg in request.messages]
    input_tokens = count_message_tokens(messages_dicts)

    start_time = time.time()

    try:
        # 7. 并发控制
        async with ConcurrencyContext(f"user:{user_id}", DEFAULT_USER_CONCURRENCY):
            if request.stream:
                return await _handle_stream(
                    provider, request, messages_dicts, kwargs,
                    user_id, api_key_id, provider_name, input_tokens, start_time
                )
            else:
                return await _handle_sync(
                    provider, request, messages_dicts, kwargs,
                    user_id, api_key_id, provider_name, input_tokens, start_time
                )
    except ConcurrencyLimitExceeded:
        raise HTTPException(
            status_code=429,
            detail="Too many concurrent requests. Please try again later.",
        )
    except Exception as e:
        # 记录失败请求
        latency_ms = int((time.time() - start_time) * 1000)
        billing_service.record_request(
            user_id=user_id,
            api_key_id=api_key_id,
            provider=provider_name,
            model=request.model,
            input_tokens=input_tokens,
            output_tokens=0,
            cost=0,
            latency_ms=latency_ms,
            status="error",
        )
        raise HTTPException(status_code=500, detail="Internal server error")


async def _handle_stream(
    provider, request, messages_dicts, kwargs,
    user_id, api_key_id, provider_name, input_tokens, start_time
):
    """处理流式响应"""
    async def stream_response():
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

        # 计费
        cost = calculate_cost(request.model, input_tokens, output_tokens)
        latency_ms = int((time.time() - start_time) * 1000)

        billing_service.deduct_balance(user_id, cost, f"{request.model} ({input_tokens}+{output_tokens} tokens)")
        billing_service.record_request(
            user_id=user_id,
            api_key_id=api_key_id,
            provider=provider_name,
            model=request.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            latency_ms=latency_ms,
        )

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
    )


async def _handle_sync(
    provider, request, messages_dicts, kwargs,
    user_id, api_key_id, provider_name, input_tokens, start_time
):
    """处理同步响应"""
    result = await provider.chat_completion(
        model=request.model,
        messages=messages_dicts,
        stream=False,
        **kwargs,
    )

    # 计算输出 tokens
    output_tokens = 0
    if "usage" in result:
        output_tokens = result["usage"].get("completion_tokens", 0)
    elif "choices" in result:
        for choice in result["choices"]:
            if "message" in choice and "content" in choice["message"]:
                output_tokens = count_message_tokens([{"content": choice["message"]["content"]}])
                break

    # 计费
    cost = calculate_cost(request.model, input_tokens, output_tokens)
    latency_ms = int((time.time() - start_time) * 1000)

    billing_service.deduct_balance(user_id, cost, f"{request.model} ({input_tokens}+{output_tokens} tokens)")
    billing_service.record_request(
        user_id=user_id,
        api_key_id=api_key_id,
        provider=provider_name,
        model=request.model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
        latency_ms=latency_ms,
    )

    return result


@router.get("/models")
async def list_models() -> dict[str, Any]:
    """列出所有可用模型"""
    models = []
    for model_name, provider_name in model_provider_map.items():
        # 检查 provider 是否有可用账号
        provider = multi_account_manager.get_provider(provider_name)
        if provider:
            models.append({
                "id": model_name,
                "object": "model",
                "created": 0,
                "owned_by": provider_name,
            })
    return {"object": "list", "data": models}
