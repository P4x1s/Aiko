"""Admin API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.auth import get_current_user
from services.supabase_client import get_supabase_client
from services.billing_service import get_balance

router = APIRouter(prefix="/api/admin")


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """Check if user is admin."""
    supabase = get_supabase_client()
    result = supabase.table("profiles") \
        .select("role") \
        .eq("id", user["sub"]) \
        .execute()

    if not result.data or result.data[0].get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.get("/users")
async def list_users(
    limit: int = 20,
    offset: int = 0,
    user: dict = Depends(require_admin),
):
    """List all users."""
    supabase = get_supabase_client()
    result = supabase.table("profiles") \
        .select("*") \
        .order("created_at", desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()

    count = supabase.table("profiles") \
        .select("id", count="exact") \
        .execute()

    return {
        "users": result.data or [],
        "total": count.count if hasattr(count, 'count') else 0,
    }


@router.get("/users/{user_id}")
async def get_user(user_id: str, user: dict = Depends(require_admin)):
    """Get user details."""
    supabase = get_supabase_client()
    result = supabase.table("profiles") \
        .select("*") \
        .eq("id", user_id) \
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    return result.data[0]


@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    data: dict,
    user: dict = Depends(require_admin),
):
    """Update user (role, balance, etc)."""
    supabase = get_supabase_client()
    result = supabase.table("profiles") \
        .update(data) \
        .eq("id", user_id) \
        .execute()

    return {"success": True}


@router.get("/stats")
async def get_system_stats(user: dict = Depends(require_admin)):
    """Get system statistics."""
    supabase = get_supabase_client()

    # Total users
    users = supabase.table("profiles") \
        .select("id", count="exact") \
        .execute()

    # Total API keys
    keys = supabase.table("api_keys") \
        .select("id", count="exact") \
        .execute()

    # Total requests today
    from datetime import datetime, timedelta
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

    # Total balance across all users
    all_balances = supabase.table("profiles") \
        .select("balance") \
        .execute()

    total_balance = sum(float(r.get("balance", 0)) for r in (all_balances.data or []))

    return {
        "total_users": users.count if hasattr(users, 'count') else 0,
        "total_api_keys": keys.count if hasattr(keys, 'count') else 0,
        "today_requests": today_requests.count if hasattr(today_requests, 'count') else 0,
        "today_cost": round(total_cost, 4),
        "total_balance": round(total_balance, 2),
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
        .select("*, profiles!inner(email)") \
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
