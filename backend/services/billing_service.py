"""Billing service for balance management and transaction recording."""

from datetime import datetime
from typing import Optional
from .supabase_client import get_supabase_client


def get_balance(user_id: str) -> float:
    """Get user's current balance."""
    supabase = get_supabase_client()
    result = supabase.table("profiles") \
        .select("balance") \
        .eq("id", user_id) \
        .execute()

    if result.data:
        return float(result.data[0].get("balance", 0))
    return 0.0


def deduct_balance(user_id: str, amount: float, description: str) -> bool:
    """Deduct balance for API usage. Returns True if successful."""
    supabase = get_supabase_client()

    # Get current balance
    current = get_balance(user_id)
    if current < amount:
        return False

    new_balance = round(current - amount, 6)

    # Update balance
    supabase.table("profiles") \
        .update({"balance": new_balance, "updated_at": datetime.utcnow().isoformat()}) \
        .eq("id", user_id) \
        .execute()

    # Record transaction
    supabase.table("transactions").insert({
        "user_id": user_id,
        "type": "usage",
        "amount": -amount,
        "balance_after": new_balance,
        "description": description,
    }).execute()

    return True


def add_balance(user_id: str, amount: float, payment_method: str, payment_id: str, description: str = "") -> float:
    """Add balance after payment. Returns new balance."""
    supabase = get_supabase_client()

    current = get_balance(user_id)
    new_balance = round(current + amount, 6)

    # Update balance
    supabase.table("profiles") \
        .update({"balance": new_balance, "updated_at": datetime.utcnow().isoformat()}) \
        .eq("id", user_id) \
        .execute()

    # Record transaction
    supabase.table("transactions").insert({
        "user_id": user_id,
        "type": "payment",
        "amount": amount,
        "balance_after": new_balance,
        "payment_method": payment_method,
        "payment_id": payment_id,
        "description": description or f"充值 ¥{amount}",
    }).execute()

    return new_balance


def get_transaction_history(user_id: str, limit: int = 20, offset: int = 0) -> list[dict]:
    """Get user's transaction history."""
    supabase = get_supabase_client()
    result = supabase.table("transactions") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()

    return result.data or []


def record_usage(
    user_id: str,
    api_key_id: str,
    provider: str,
    model: str,
    tokens_input: int,
    tokens_output: int,
    cost: float,
    latency_ms: int,
    status: str = "success",
) -> None:
    """Record API usage in request_logs."""
    supabase = get_supabase_client()
    supabase.table("request_logs").insert({
        "user_id": user_id,
        "api_key_id": api_key_id,
        "provider": provider,
        "model": model,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "cost": cost,
        "latency_ms": latency_ms,
        "status": status,
    }).execute()


def get_usage_stats(user_id: str) -> dict:
    """Get user's usage statistics."""
    supabase = get_supabase_client()

    # Total requests
    total = supabase.table("request_logs") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .execute()

    # Total cost
    result = supabase.table("request_logs") \
        .select("cost") \
        .eq("user_id", user_id) \
        .execute()

    total_cost = sum(r.get("cost", 0) for r in (result.data or []))

    return {
        "total_requests": total.count if hasattr(total, 'count') else 0,
        "total_cost": round(total_cost, 4),
    }
