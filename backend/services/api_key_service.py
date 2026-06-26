import hashlib
import secrets
from datetime import datetime, timezone
from typing import Optional
from .supabase_client import get_supabase_client


def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key.
    Returns: (raw_key, key_hash, key_prefix)
    """
    raw_key = f"ag-{secrets.token_hex(32)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    key_prefix = raw_key[:11]  # "ag-" + 8 hex chars
    return raw_key, key_hash, key_prefix


def create_api_key(user_id: str, name: str) -> dict:
    """
    Create a new API key for a user.
    Returns: {"id": ..., "key": raw_key, "name": ...}
    """
    raw_key, key_hash, key_prefix = generate_api_key()
    supabase = get_supabase_client()

    result = supabase.table("api_keys").insert({
        "user_id": user_id,
        "key_hash": key_hash,
        "key_prefix": key_prefix,
        "name": name,
    }).execute()

    return {
        "id": result.data[0]["id"],
        "key": raw_key,
        "name": name,
    }


def verify_api_key(raw_key: str) -> Optional[dict]:
    """
    Verify an API key and return the key record if valid.
    """
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    supabase = get_supabase_client()

    result = (
        supabase.table("api_keys")
        .select("*")
        .eq("key_hash", key_hash)
        .eq("is_active", True)
        .execute()
    )

    if result.data:
        supabase.table("api_keys").update(
            {"last_used_at": datetime.now(timezone.utc).isoformat()}
        ).eq("id", result.data[0]["id"]).execute()
        return result.data[0]
    return None


def list_api_keys(user_id: str) -> list[dict]:
    """
    List all API keys for a user.
    """
    supabase = get_supabase_client()
    result = (
        supabase.table("api_keys")
        .select("id, name, key_prefix, is_active, created_at, last_used_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


def delete_api_key(key_id: str, user_id: str) -> bool:
    """
    Delete an API key (only if it belongs to the user).
    """
    supabase = get_supabase_client()
    result = (
        supabase.table("api_keys")
        .delete()
        .eq("id", key_id)
        .eq("user_id", user_id)
        .execute()
    )
    return len(result.data) > 0
