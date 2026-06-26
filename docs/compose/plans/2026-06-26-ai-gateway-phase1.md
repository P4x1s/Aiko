# AI Gateway Phase 1: Core Proxy + Provider Adapters

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working API proxy that routes OpenAI-compatible requests to multiple AI providers, deployed on Vercel with Supabase for data storage

**Architecture:** FastAPI backend on Vercel serverless with modular provider adapters. Supabase for PostgreSQL database and authentication. GitHub for version control.

**Tech Stack:** Python 3.11, FastAPI, httpx, pydantic, Supabase, Vercel

---

## File Structure

```
ai-gateway/
├── backend/
│   ├── api/                    # Vercel serverless functions
│   │   ├── index.py           # Main FastAPI app entry point
│   │   ├── v1/
│   │   │   └── [...slug].py   # Proxy endpoints (/v1/*)
│   │   └── auth/
│   │       └── [...slug].py   # Auth endpoints
│   ├── services/
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Abstract provider interface
│   │   │   ├── openai.py      # OpenAI adapter
│   │   │   ├── anthropic.py   # Anthropic adapter
│   │   │   └── google.py      # Google adapter
│   │   ├── database.py        # Supabase client
│   │   └── auth.py            # Supabase auth service
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_proxy.py
│   │   └── test_providers/
│   │       ├── __init__.py
│   │       ├── test_openai.py
│   │       ├── test_anthropic.py
│   │       └── test_google.py
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env.example
├── frontend/                  # Nuxt app (separate)
├── supabase/
│   └── migrations/
│       └── 001_initial.sql
├── .gitignore
└── README.md
```

---

## Task 1: Project Scaffolding

**Covers:** [S3, S6]

**Files:**
- Create: `backend/api/index.py`
- Create: `backend/services/providers/__init__.py`
- Create: `backend/services/providers/base.py`
- Create: `backend/services/providers/openai.py`
- Create: `backend/services/providers/anthropic.py`
- Create: `backend/services/providers/google.py`
- Create: `backend/services/database.py`
- Create: `backend/services/auth.py`
- Create: `backend/requirements.txt`
- Create: `backend/vercel.json`
- Create: `backend/.env.example`
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Create project directory structure**

```bash
mkdir -p ai-gateway/backend/api/v1
mkdir -p ai-gateway/backend/services/providers
mkdir -p ai-gateway/backend/tests/test_providers
mkdir -p ai-gateway/supabase/migrations
```

- [ ] **Step 2: Create requirements.txt**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
supabase==2.3.0
python-jose[cryptography]==3.3.0
pytest==7.4.4
pytest-asyncio==0.23.3
```

- [ ] **Step 3: Create .env.example**

```env
# Application
APP_NAME=AI Gateway
DEBUG=true

# API Keys (provider credentials)
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GOOGLE_API_KEY=xxx

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx
SUPABASE_SERVICE_KEY=eyJxxx
```

- [ ] **Step 4: Create vercel.json**

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

- [ ] **Step 5: Create main FastAPI app (api/index.py)**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import routes as v1_routes

app = FastAPI(
    title="AI Gateway",
    description="Unified AI API proxy for Chinese developers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_routes.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 6: Create .gitignore**

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.env
.venv/
venv/

# Node
node_modules/
.nuxt/
.output/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Vercel
.vercel/
```

- [ ] **Step 7: Create README.md**

```markdown
# AI Gateway

Unified AI API proxy for Chinese developers. Access OpenAI, Anthropic, Google, and more through a single OpenAI-compatible endpoint.

## Features

- OpenAI-compatible API format
- Support for multiple AI providers
- User authentication via Supabase
- Deployed on Vercel

## Quick Start

1. Clone the repository
2. Copy `backend/.env.example` to `backend/.env` and add your keys
3. Deploy to Vercel

## API Usage

```bash
curl https://your-app.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```
```

- [ ] **Step 8: Initialize git and commit**

```bash
cd ai-gateway
git init
git add .
git commit -m "feat: project scaffolding for Vercel deployment"
```

---

## Task 2: Pydantic Schemas

**Covers:** [S2, S4]

**Files:**
- Create: `backend/api/schemas.py`

- [ ] **Step 1: Create request/response schemas**

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: Optional[float] = Field(None, ge=0, le=2)
    top_p: Optional[float] = Field(None, ge=0, le=1)
    max_tokens: Optional[int] = Field(None, ge=1)
    stream: bool = False


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list["Choice"]
    usage: Usage


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[Literal["stop", "length"]] = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: list["ChunkChoice"]


class ChunkChoice(BaseModel):
    index: int
    delta: dict
    finish_reason: Optional[Literal["stop", "length"]] = None


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelList(BaseModel):
    object: str = "list"
    data: list[ModelInfo]
```

- [ ] **Step 2: Commit**

```bash
git add backend/api/schemas.py
git commit -m "feat: add Pydantic schemas for chat completions"
```

---

## Task 3: Provider Base Interface

**Covers:** [S4]

**Files:**
- Create: `backend/services/providers/base.py`

- [ ] **Step 1: Create abstract provider interface**

```python
from abc import ABC, abstractmethod
from typing import AsyncIterator
from api.schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChunk,
)


class BaseProvider(ABC):
    """Abstract base class for AI provider adapters."""

    provider_name: str
    supported_models: list[str]

    @abstractmethod
    async def chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """Send a chat completion request."""
        pass

    @abstractmethod
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[ChatCompletionChunk]:
        """Send a streaming chat completion request."""
        pass

    def supports_model(self, model: str) -> bool:
        """Check if this provider supports the given model."""
        return model in self.supported_models
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/providers/base.py
git commit -m "feat: add abstract provider interface"
```

---

## Task 4: OpenAI Provider Adapter

**Covers:** [S4]

**Files:**
- Create: `backend/services/providers/openai.py`
- Create: `backend/tests/test_providers/test_openai.py`

- [ ] **Step 1: Write failing test for OpenAI adapter**

```python
import pytest
from services.providers.openai import OpenAIProvider


@pytest.fixture
def provider():
    return OpenAIProvider(api_key="test-key")


def test_supports_model(provider):
    assert provider.supports_model("gpt-4") is True
    assert provider.supports_model("gpt-3.5-turbo") is True
    assert provider.supports_model("claude-3") is False


def test_provider_name(provider):
    assert provider.provider_name == "openai"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_openai.py -v
# Expected: FAIL with "ModuleNotFoundError"
```

- [ ] **Step 3: Implement OpenAI provider**

```python
import httpx
from typing import AsyncIterator
from services.providers.base import BaseProvider
from api.schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChunk,
)


class OpenAIProvider(BaseProvider):
    provider_name = "openai"
    supported_models = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.AsyncClient()

    async def chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        payload = {
            "model": request.model,
            "messages": [m.model_dump() for m in request.messages],
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.top_p is not None:
            payload["top_p"] = request.top_p
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return ChatCompletionResponse(**response.json())

    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[ChatCompletionChunk]:
        payload = {
            "model": request.model,
            "messages": [m.model_dump() for m in request.messages],
            "stream": True,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.top_p is not None:
            payload["top_p"] = request.top_p
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        async with self.client.stream(
            "POST",
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"},
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    import json
                    yield ChatCompletionChunk(**json.loads(data))
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_openai.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add backend/services/providers/openai.py backend/tests/test_providers/test_openai.py
git commit -m "feat: add OpenAI provider adapter"
```

---

## Task 5: Anthropic Provider Adapter

**Covers:** [S4]

**Files:**
- Create: `backend/services/providers/anthropic.py`
- Create: `backend/tests/test_providers/test_anthropic.py`

- [ ] **Step 1: Write failing test for Anthropic adapter**

```python
import pytest
from services.providers.anthropic import AnthropicProvider


@pytest.fixture
def provider():
    return AnthropicProvider(api_key="test-key")


def test_supports_model(provider):
    assert provider.supports_model("claude-3-opus-20240229") is True
    assert provider.supports_model("claude-3-sonnet-20240229") is True
    assert provider.supports_model("gpt-4") is False


def test_provider_name(provider):
    assert provider.provider_name == "anthropic"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_anthropic.py -v
# Expected: FAIL with "ModuleNotFoundError"
```

- [ ] **Step 3: Implement Anthropic provider**

```python
import httpx
import time
import uuid
from typing import AsyncIterator
from services.providers.base import BaseProvider
from api.schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChunk,
    Choice,
    Message,
    Usage,
)


class AnthropicProvider(BaseProvider):
    provider_name = "anthropic"
    supported_models = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.client = httpx.AsyncClient()

    def _convert_messages(self, messages):
        system = None
        anthropic_messages = []
        for msg in messages:
            if msg.role == "system":
                system = msg.content
            else:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content,
                })
        return system, anthropic_messages

    async def chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        system, messages = self._convert_messages(request.messages)
        payload = {
            "model": request.model,
            "messages": messages,
            "max_tokens": request.max_tokens or 1024,
        }
        if system:
            payload["system"] = system
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.top_p is not None:
            payload["top_p"] = request.top_p

        response = await self.client.post(
            f"{self.base_url}/messages",
            json=payload,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        response.raise_for_status()
        data = response.json()

        content = data["content"][0]["text"] if data["content"] else ""
        return ChatCompletionResponse(
            id=f"msg_{uuid.uuid4().hex[:24]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=content),
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=data["usage"]["input_tokens"],
                completion_tokens=data["usage"]["output_tokens"],
                total_tokens=(
                    data["usage"]["input_tokens"]
                    + data["usage"]["output_tokens"]
                ),
            ),
        )

    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[ChatCompletionChunk]:
        system, messages = self._convert_messages(request.messages)
        payload = {
            "model": request.model,
            "messages": messages,
            "max_tokens": request.max_tokens or 1024,
            "stream": True,
        }
        if system:
            payload["system"] = system
        if request.temperature is not None:
            payload["temperature"] = request.temperature

        msg_id = f"msg_{uuid.uuid4().hex[:24]}"
        async with self.client.stream(
            "POST",
            f"{self.base_url}/messages",
            json=payload,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        ) as response:
            response.raise_for_status()
            import json
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if data["type"] == "content_block_delta":
                        yield ChatCompletionChunk(
                            id=msg_id,
                            created=int(time.time()),
                            model=request.model,
                            choices=[
                                {
                                    "index": 0,
                                    "delta": {"content": data["delta"]["text"]},
                                    "finish_reason": None,
                                }
                            ],
                        )
                    elif data["type"] == "message_stop":
                        break
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_anthropic.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add backend/services/providers/anthropic.py backend/tests/test_providers/test_anthropic.py
git commit -m "feat: add Anthropic provider adapter"
```

---

## Task 6: Google Provider Adapter

**Covers:** [S4]

**Files:**
- Create: `backend/services/providers/google.py`
- Create: `backend/tests/test_providers/test_google.py`

- [ ] **Step 1: Write failing test for Google adapter**

```python
import pytest
from services.providers.google import GoogleProvider


@pytest.fixture
def provider():
    return GoogleProvider(api_key="test-key")


def test_supports_model(provider):
    assert provider.supports_model("gemini-1.5-pro") is True
    assert provider.supports_model("gemini-1.5-flash") is True
    assert provider.supports_model("gpt-4") is False


def test_provider_name(provider):
    assert provider.provider_name == "google"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_google.py -v
# Expected: FAIL with "ModuleNotFoundError"
```

- [ ] **Step 3: Implement Google provider**

```python
import httpx
import json
import time
import uuid
from typing import AsyncIterator
from services.providers.base import BaseProvider
from api.schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChunk,
    Choice,
    Message,
    Usage,
)


class GoogleProvider(BaseProvider):
    provider_name = "google"
    supported_models = [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro",
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.client = httpx.AsyncClient()

    def _convert_messages(self, messages):
        contents = []
        for msg in messages:
            contents.append({
                "role": "model" if msg.role == "assistant" else "user",
                "parts": [{"text": msg.content}],
            })
        return contents

    async def chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        contents = self._convert_messages(request.messages)
        payload = {"contents": contents}
        if request.temperature is not None:
            payload["generationConfig"] = {"temperature": request.temperature}
        if request.max_tokens is not None:
            payload.setdefault("generationConfig", {})["maxOutputTokens"] = (
                request.max_tokens
            )

        model = request.model
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage_data = data.get("usageMetadata", {})

        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=text),
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=usage_data.get("promptTokenCount", 0),
                completion_tokens=usage_data.get("candidatesTokenCount", 0),
                total_tokens=usage_data.get("totalTokenCount", 0),
            ),
        )

    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[ChatCompletionChunk]:
        contents = self._convert_messages(request.messages)
        payload = {"contents": contents, "stream": True}
        if request.temperature is not None:
            payload["generationConfig"] = {"temperature": request.temperature}

        model = request.model
        url = f"{self.base_url}/models/{model}:streamGenerateContent?key={self.api_key}"
        chunk_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"

        async with self.client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    if "candidates" in data:
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        yield ChatCompletionChunk(
                            id=chunk_id,
                            created=int(time.time()),
                            model=request.model,
                            choices=[
                                {
                                    "index": 0,
                                    "delta": {"content": text},
                                    "finish_reason": None,
                                }
                            ],
                        )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ai-gateway/backend
pytest tests/test_providers/test_google.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add backend/services/providers/google.py backend/tests/test_providers/test_google.py
git commit -m "feat: add Google Gemini provider adapter"
```

---

## Task 7: Provider Registry

**Covers:** [S4]

**Files:**
- Create: `backend/services/providers/__init__.py`

- [ ] **Step 1: Create provider registry**

```python
import os
from typing import Optional
from services.providers.base import BaseProvider
from services.providers.openai import OpenAIProvider
from services.providers.anthropic import AnthropicProvider
from services.providers.google import GoogleProvider


class ProviderRegistry:
    """Registry for managing AI providers and routing requests."""

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}
        self._model_map: dict[str, str] = {}

    def register(self, provider: BaseProvider):
        self._providers[provider.provider_name] = provider
        for model in provider.supported_models:
            self._model_map[model] = provider.provider_name

    def get_provider(self, model: str) -> Optional[BaseProvider]:
        provider_name = self._model_map.get(model)
        if provider_name:
            return self._providers.get(provider_name)
        return None

    def list_models(self) -> list[dict]:
        models = []
        for provider in self._providers.values():
            for model in provider.supported_models:
                models.append({
                    "id": model,
                    "object": "model",
                    "created": 0,
                    "owned_by": provider.provider_name,
                })
        return models


registry = ProviderRegistry()

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    registry.register(OpenAIProvider(api_key=openai_key))

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    registry.register(AnthropicProvider(api_key=anthropic_key))

google_key = os.getenv("GOOGLE_API_KEY")
if google_key:
    registry.register(GoogleProvider(api_key=google_key))
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/providers/__init__.py
git commit -m "feat: add provider registry for routing"
```

---

## Task 8: Proxy Routes

**Covers:** [S2, S4]

**Files:**
- Create: `backend/api/v1/__init__.py`
- Create: `backend/api/v1/routes.py`
- Create: `backend/tests/test_proxy.py`

- [ ] **Step 1: Write failing test for proxy endpoints**

```python
import pytest
from httpx import AsyncClient
from api.index import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_models_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert isinstance(data["data"], list)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ai-gateway/backend
pytest tests/test_proxy.py -v
# Expected: FAIL
```

- [ ] **Step 3: Implement proxy routes**

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.schemas import ChatCompletionRequest
from services.providers import registry

router = APIRouter()


@router.get("/v1/models")
async def list_models():
    models = registry.list_models()
    return {"object": "list", "data": models}


@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    provider = registry.get_provider(request.model)
    if not provider:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model}' is not supported",
        )

    try:
        if request.stream:
            return StreamingResponse(
                provider.chat_completion_stream(request),
                media_type="text/event-stream",
            )
        else:
            return await provider.chat_completion(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ai-gateway/backend
pytest tests/test_proxy.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add backend/api/v1/__init__.py backend/api/v1/routes.py backend/tests/test_proxy.py
git commit -m "feat: add proxy routes for chat completions and models"
```

---

## Task 9: Supabase Integration

**Covers:** [S3, S5]

**Files:**
- Create: `backend/services/database.py`
- Create: `backend/services/auth.py`
- Create: `supabase/migrations/001_initial.sql`

- [ ] **Step 1: Create Supabase database service**

```python
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase: Client = create_client(url, key)


def get_supabase() -> Client:
    return supabase
```

- [ ] **Step 2: Create Supabase auth service**

```python
from services.database import get_supabase
from fastapi import HTTPException


async def get_current_user(token: str) -> dict:
    """Verify JWT token and return user data."""
    supabase = get_supabase()
    try:
        user = supabase.auth.get_user(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user.model_dump()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


async def create_api_key(user_id: str, name: str) -> dict:
    """Create a new API key for a user."""
    import secrets
    import hashlib

    supabase = get_supabase()
    raw_key = f"ag-{secrets.token_hex(32)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    key_prefix = raw_key[:8]

    result = supabase.table("api_keys").insert({
        "user_id": user_id,
        "key_hash": key_hash,
        "key_prefix": key_prefix,
        "name": name,
    }).execute()

    return {"key": raw_key, "id": result.data[0]["id"]}
```

- [ ] **Step 3: Create database migration**

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles table (extends Supabase auth.users)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    balance DECIMAL(10,4) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(8) NOT NULL,
    name VARCHAR(100),
    rate_limit INTEGER DEFAULT 60,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE
);

-- Request Logs table
CREATE TABLE request_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id),
    api_key_id UUID REFERENCES api_keys(id),
    provider VARCHAR(50),
    model VARCHAR(100),
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost DECIMAL(10,6),
    latency_ms INTEGER,
    status VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id),
    type VARCHAR(20),
    amount DECIMAL(10,4),
    balance_after DECIMAL(10,4),
    description TEXT,
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE request_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can view own API keys" ON api_keys
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own API keys" ON api_keys
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own API keys" ON api_keys
    FOR DELETE USING (auth.uid() = user_id);

-- Function to create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email)
    VALUES (new.id, new.email);
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/database.py backend/services/auth.py supabase/migrations/001_initial.sql
git commit -m "feat: add Supabase integration for auth and database"
```

---

## Task 10: Integration Tests

**Covers:** [S2, S4, S5]

**Files:**
- Modify: `backend/tests/test_proxy.py`

- [ ] **Step 1: Add integration test with mock provider**

```python
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from api.index import app
from api.schemas import (
    ChatCompletionResponse,
    Choice,
    Message,
    Usage,
)


@pytest.mark.asyncio
async def test_chat_completions_with_mock_provider():
    mock_response = ChatCompletionResponse(
        id="chatcmpl-test123",
        created=1234567890,
        model="gpt-4",
        choices=[
            Choice(
                index=0,
                message=Message(role="assistant", content="Hello!"),
                finish_reason="stop",
            )
        ],
        usage=Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )

    with patch(
        "api.v1.routes.registry.get_provider"
    ) as mock_get:
        mock_provider = AsyncMock()
        mock_provider.chat_completion.return_value = mock_response
        mock_get.return_value = mock_provider

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/v1/chat/completions",
                json={
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": "Hi"}],
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "chatcmpl-test123"
    assert data["choices"][0]["message"]["content"] == "Hello!"


@pytest.mark.asyncio
async def test_chat_completions_unsupported_model():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/chat/completions",
            json={
                "model": "unsupported-model",
                "messages": [{"role": "user", "content": "Hi"}],
            },
        )
    assert response.status_code == 400
```

- [ ] **Step 2: Run all tests**

```bash
cd ai-gateway/backend
pytest -v
# Expected: ALL PASS
```

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_proxy.py
git commit -m "feat: add integration tests with mock provider"
```

---

## Task 11: Vercel Deployment Verification

**Covers:** [S3]

**Files:**
- None (verification only)

- [ ] **Step 1: Verify vercel.json configuration**

```bash
cd ai-gateway/backend
cat vercel.json
# Should show correct build configuration
```

- [ ] **Step 2: Test local development**

```bash
cd ai-gateway/backend
pip install -r requirements.txt
uvicorn api.index:app --port 8000 &
sleep 2
curl http://localhost:8000/health
# Expected: {"status": "ok"}
curl http://localhost:8000/v1/models
# Expected: {"object": "list", "data": [...]}
kill %1
```

- [ ] **Step 3: Push to GitHub**

```bash
cd ai-gateway
git add .
git commit -m "feat: complete Phase 1 - core proxy with Vercel deployment"
# Create GitHub repo and push
```

---

## Summary

This plan implements Phase 1 of the AI Gateway:

1. **Project scaffolding** - FastAPI app configured for Vercel
2. **Pydantic schemas** - Request/response models
3. **Provider base interface** - Abstract adapter pattern
4. **OpenAI adapter** - Full chat completion support
5. **Anthropic adapter** - Claude model support
6. **Google adapter** - Gemini model support
7. **Provider registry** - Model routing logic
8. **Proxy routes** - OpenAI-compatible API endpoints
9. **Supabase integration** - Database and auth setup
10. **Integration tests** - Mock-based testing
11. **Vercel verification** - Deployment readiness

After completing this phase, the API gateway can:
- Accept OpenAI-format requests
- Route to OpenAI, Anthropic, or Google
- Stream responses
- List available models
- Deploy on Vercel with GitHub integration
- Store user data in Supabase
