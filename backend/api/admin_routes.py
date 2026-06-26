"""Admin API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.auth import get_current_user
from services.supabase_client import get_supabase_client

router = APIRouter(prefix="/api/admin")


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """Check if user is admin."""
    role = user.get("user_metadata", {}).get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.get("/users")
async def list_users(
    limit: int = 50,
    offset: int = 0,
    user: dict = Depends(require_admin),
):
    """List all users from auth.users."""
    supabase = get_supabase_client()

    # Use Supabase admin API to list users
    result = supabase.auth.admin.list_users()

    users = []
    for u in (result or []):
        users.append({
            "id": u.id,
            "email": u.email,
            "role": u.user_metadata.get("role", "user"),
            "created_at": str(u.created_at) if hasattr(u, 'created_at') else "",
        })

    return {
        "users": users,
        "total": len(users),
    }


@router.get("/stats")
async def get_system_stats(user: dict = Depends(require_admin)):
    """Get system statistics."""
    supabase = get_supabase_client()

    # List users
    users = supabase.auth.admin.list_users()
    user_count = len(users) if users else 0

    # Total API keys
    keys = supabase.table("api_keys") \
        .select("id", count="exact") \
        .execute()

    # Total requests today
    from datetime import datetime
    today = datetime.utcnow().date().isoformat()
    today_requests = supabase.table("request_logs") \
        .select("id", count="exact") \
        .gte("created_at", today) \
        .execute()

    # Total cost today
    today_cost = supabase.table("request_logs") \
        .select("cost") \
        .gte("created_at", today) \
        .execute()

    total_cost = sum(r.get("cost", 0) for r in (today_cost.data or []))

    return {
        "total_users": user_count,
        "total_api_keys": keys.count if hasattr(keys, 'count') else 0,
        "today_requests": today_requests.count if hasattr(today_requests, 'count') else 0,
        "today_cost": round(total_cost, 4),
    }


@router.get("/requests")
async def list_requests(
    limit: int = 50,
    offset: int = 0,
    user: dict = Depends(require_admin),
):
    """List recent API requests."""
    supabase = get_supabase_client()
    result = supabase.table("request_logs") \
        .select("*") \
        .order("created_at", desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()

    return {"requests": result.data or []}


@router.get("/provider-stats")
async def get_provider_stats(user: dict = Depends(require_admin)):
    """Get stats per provider."""
    supabase = get_supabase_client()
    result = supabase.table("request_logs") \
        .select("provider, model, cost") \
        .execute()

    stats = {}
    for r in (result.data or []):
        provider = r.get("provider", "unknown")
        if provider not in stats:
            stats[provider] = {"requests": 0, "cost": 0}
        stats[provider]["requests"] += 1
        stats[provider]["cost"] += r.get("cost", 0)

    return {"providers": stats}
