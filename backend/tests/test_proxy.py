import pytest
from unittest.mock import AsyncMock, patch
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


@pytest.mark.asyncio
async def test_chat_completions_invalid_request():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [{"role": "invalid", "content": "Hi"}],
            },
        )
    assert response.status_code == 422
