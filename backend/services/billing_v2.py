"""Enhanced billing service - 参考 sub2api 的精确计费"""

import time
from datetime import datetime
from typing import Optional
from .supabase_client import get_supabase_client


class BillingService:
    """精确计费服务"""

    def __init__(self):
        self._usage_cache: dict[str, dict] = {}

    def get_balance(self, user_id: str) -> float:
        """获取用户余额"""
        supabase = get_supabase_client()
        result = supabase.table("profiles") \
            .select("balance") \
            .eq("id", user_id) \
            .execute()

        if result.data:
            return float(result.data[0].get("balance", 0))
        return 0.0

    def deduct_balance(self, user_id: str, amount: float, description: str) -> bool:
        """扣除余额"""
        supabase = get_supabase_client()

        # 获取当前余额
        current = self.get_balance(user_id)
        if current < amount:
            return False

        new_balance = round(current - amount, 6)

        # 更新余额
        supabase.table("profiles") \
            .update({
                "balance": new_balance,
                "updated_at": datetime.utcnow().isoformat()
            }) \
            .eq("id", user_id) \
            .execute()

        # 记录交易
        supabase.table("transactions").insert({
            "user_id": user_id,
            "type": "usage",
            "amount": -amount,
            "balance_after": new_balance,
            "description": description,
        }).execute()

        return True

    def record_request(
        self,
        user_id: str,
        api_key_id: str,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        latency_ms: int,
        status: str = "success",
    ) -> str:
        """记录 API 请求"""
        supabase = get_supabase_client()

        result = supabase.table("request_logs").insert({
            "user_id": user_id,
            "api_key_id": api_key_id,
            "provider": provider,
            "model": model,
            "tokens_input": input_tokens,
            "tokens_output": output_tokens,
            "cost": cost,
            "latency_ms": latency_ms,
            "status": status,
        }).execute()

        return result.data[0]["id"] if result.data else ""

    def get_usage_stats(self, user_id: str, days: int = 30) -> dict:
        """获取用户使用统计"""
        supabase = get_supabase_client()

        # 计算日期范围
        from datetime import timedelta
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        # 获取请求日志
        result = supabase.table("request_logs") \
            .select("model, tokens_input, tokens_output, cost, created_at") \
            .eq("user_id", user_id) \
            .gte("created_at", start_date) \
            .execute()

        logs = result.data or []

        # 计算统计
        total_requests = len(logs)
        total_input_tokens = sum(r.get("tokens_input", 0) for r in logs)
        total_output_tokens = sum(r.get("tokens_output", 0) for r in logs)
        total_cost = sum(r.get("cost", 0) for r in logs)

        # 按模型统计
        model_stats = {}
        for log in logs:
            model = log.get("model", "unknown")
            if model not in model_stats:
                model_stats[model] = {
                    "requests": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0,
                }
            model_stats[model]["requests"] += 1
            model_stats[model]["input_tokens"] += log.get("tokens_input", 0)
            model_stats[model]["output_tokens"] += log.get("tokens_output", 0)
            model_stats[model]["cost"] += log.get("cost", 0)

        return {
            "total_requests": total_requests,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_cost": round(total_cost, 4),
            "model_stats": model_stats,
            "period_days": days,
        }


# 全局计费服务实例
billing_service = BillingService()
