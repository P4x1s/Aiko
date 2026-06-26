from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/v1")


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[dict[str, str]]
    stream: bool = False
    temperature: float = 1.0
    max_tokens: int | None = None


@router.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    return {
        "id": "chatcmpl-placeholder",
        "object": "chat.completion",
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a placeholder response. Provider routing will be implemented in a future task.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


@router.get("/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "gpt-4", "object": "model"},
            {"id": "gpt-4o", "object": "model"},
            {"id": "claude-3-opus", "object": "model"},
            {"id": "gemini-pro", "object": "model"},
        ],
    }
