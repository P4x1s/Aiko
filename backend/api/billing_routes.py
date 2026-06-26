"""Billing API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.auth import get_current_user
from services.billing_service import (
    get_balance,
    get_transaction_history,
    get_usage_stats,
)
from services.payment_service import (
    get_pricing_tiers,
    generate_order_id,
    PaymentService,
)

router = APIRouter(prefix="/api/billing")
payment_service = PaymentService()


class CreatePaymentRequest(BaseModel):
    tier_id: str
    payment_method: str  # alipay, wechat, crypto


@router.get("/balance")
async def get_user_balance(user: dict = Depends(get_current_user)):
    """Get user's current balance."""
    balance = get_balance(user["sub"])
    return {"balance": balance}


@router.get("/history")
async def get_user_history(
    limit: int = 20,
    offset: int = 0,
    user: dict = Depends(get_current_user),
):
    """Get user's transaction history."""
    history = get_transaction_history(user["sub"], limit, offset)
    return {"transactions": history}


@router.get("/stats")
async def get_user_stats(user: dict = Depends(get_current_user)):
    """Get user's usage statistics."""
    stats = get_usage_stats(user["sub"])
    return stats


@router.get("/pricing")
async def get_pricing():
    """Get available pricing tiers."""
    return {"tiers": get_pricing_tiers()}


@router.post("/create-payment")
async def create_payment(
    request: CreatePaymentRequest,
    user: dict = Depends(get_current_user),
):
    """Create a payment order."""
    tiers = get_pricing_tiers()
    tier = next((t for t in tiers if t["id"] == request.tier_id), None)

    if not tier:
        raise HTTPException(status_code=400, detail="Invalid tier")

    order_id = generate_order_id(user["sub"])
    amount = tier["amount"] + tier["bonus"]

    if request.payment_method == "alipay":
        result = payment_service.create_alipay_order(
            order_id=order_id,
            amount=amount,
            subject=f"艾柯 Aiko 充值 ¥{tier['amount']}",
            return_url="https://aiko-qjp6.vercel.app/dashboard/billing",
        )
    elif request.payment_method == "wechat":
        result = payment_service.create_wechat_order(
            order_id=order_id,
            amount=amount,
            description=f"艾柯 Aiko 充值 ¥{tier['amount']}",
        )
    elif request.payment_method == "crypto":
        result = payment_service.create_crypto_order(
            order_id=order_id,
            amount=amount,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    return {
        "order_id": order_id,
        "amount": tier["amount"],
        "bonus": tier["bonus"],
        "total": amount,
        **result,
    }
