"""Payment service for Alipay, WeChat Pay, and Crypto."""

import hashlib
import secrets
import time
from typing import Optional
from .database import settings


class PaymentService:
    """Handle payment integrations."""

    def __init__(self):
        self.alipay_app_id = getattr(settings, 'alipay_app_id', '')
        self.alipay_private_key = getattr(settings, 'alipay_private_key', '')
        self.wechat_app_id = getattr(settings, 'wechat_app_id', '')
        self.wechat_mch_id = getattr(settings, 'wechat_mch_id', '')
        self.wechat_api_key = getattr(settings, 'wechat_api_key', '')

    def create_alipay_order(
        self,
        order_id: str,
        amount: float,
        subject: str,
        return_url: str,
    ) -> dict:
        """Create Alipay payment order."""
        # TODO: Implement actual Alipay SDK integration
        # For now, return mock data
        return {
            "order_id": order_id,
            "payment_url": f"https://openapi.alipay.com/gateway.do?mock=true&order={order_id}",
            "qr_code": f"https://qr.alipay.com/mock_{order_id}",
            "status": "pending",
        }

    def create_wechat_order(
        self,
        order_id: str,
        amount: float,
        description: str,
    ) -> dict:
        """Create WeChat Pay order."""
        # TODO: Implement actual WeChat Pay SDK integration
        # For now, return mock data
        return {
            "order_id": order_id,
            "qr_code": f"weixin://wxpay/mock_{order_id}",
            "status": "pending",
        }

    def create_crypto_order(
        self,
        order_id: str,
        amount: float,
        currency: str = "USDT",
    ) -> dict:
        """Create crypto payment order."""
        # TODO: Implement actual crypto payment (e.g., NOWPayments, CoinGate)
        # For now, return mock data
        wallet_addresses = {
            "USDT": "TYourUsdtWalletAddress",
            "BTC": "1YourBtcWalletAddress",
            "ETH": "0xYourEthWalletAddress",
        }
        return {
            "order_id": order_id,
            "currency": currency,
            "amount_usd": amount,
            "wallet_address": wallet_addresses.get(currency, ""),
            "status": "pending",
        }

    def verify_alipay_callback(self, params: dict) -> bool:
        """Verify Alipay payment callback."""
        # TODO: Implement actual signature verification
        return params.get("trade_status") == "TRADE_SUCCESS"

    def verify_wechat_callback(self, params: dict) -> bool:
        """Verify WeChat Pay callback."""
        # TODO: Implement actual signature verification
        return params.get("return_code") == "SUCCESS"


# Pricing tiers for quick purchase
PRICING_TIERS = [
    {"id": "tier_1", "amount": 10, "bonus": 0, "label": "¥10"},
    {"id": "tier_2", "amount": 50, "bonus": 5, "label": "¥50 + ¥5"},
    {"id": "tier_3", "amount": 100, "bonus": 15, "label": "¥100 + ¥15"},
    {"id": "tier_4", "amount": 200, "bonus": 40, "label": "¥200 + ¥40"},
    {"id": "tier_5", "amount": 500, "bonus": 120, "label": "¥500 + ¥120"},
]


def get_pricing_tiers() -> list[dict]:
    """Get available pricing tiers."""
    return PRICING_TIERS


def generate_order_id(user_id: str) -> str:
    """Generate unique order ID."""
    timestamp = int(time.time())
    random_str = secrets.token_hex(4)
    return f"order_{user_id[:8]}_{timestamp}_{random_str}"
