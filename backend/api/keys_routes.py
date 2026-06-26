"""Keys API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.auth import get_current_user
from services.api_key_service import create_api_key, list_api_keys, delete_api_key

router = APIRouter(prefix="/api/keys")


class CreateKeyRequest(BaseModel):
    name: str = ""


@router.get("")
async def get_keys(user: dict = Depends(get_current_user)):
    """Get all API keys for the current user."""
    keys = list_api_keys(user["sub"])
    return {"keys": keys}


@router.post("")
async def create_new_key(
    request: CreateKeyRequest,
    user: dict = Depends(get_current_user),
):
    """Create a new API key."""
    result = create_api_key(user["sub"], request.name)
    return result


@router.delete("/{key_id}")
async def delete_key(key_id: str, user: dict = Depends(get_current_user)):
    """Delete an API key."""
    success = delete_api_key(key_id, user["sub"])
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"success": True}
