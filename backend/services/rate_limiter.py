"""Rate limiter service - 参考 sub2api 的速率限制"""

import time
from collections import defaultdict
from typing import Optional
from .supabase_client import get_supabase_client


class RateLimiter:
    """令牌桶速率限制器"""

    def __init__(self):
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._tokens: dict[str, float] = defaultdict(float)
        self._last_update: dict[str, float] = defaultdict(float)

    def is_allowed(
        self,
        key: str,
        rate: int = 60,  # 每分钟请求数
        burst: int = 10,  # 突发容量
    ) -> bool:
        """检查是否允许请求"""
        now = time.time()
        last = self._last_update.get(key, now)
        elapsed = now - last

        # 更新令牌
        self._tokens[key] = min(
            burst,
            self._tokens.get(key, burst) + elapsed * (rate / 60)
        )
        self._last_update[key] = now

        if self._tokens[key] >= 1:
            self._tokens[key] -= 1
            return True
        return False

    def get_wait_time(self, key: str, rate: int = 60) -> float:
        """获取等待时间（秒）"""
        if self._tokens.get(key, 0) >= 1:
            return 0
        return 60 / rate - self._tokens.get(key, 0) * (60 / rate)


# 全局速率限制器实例
rate_limiter = RateLimiter()


def check_rate_limit(user_id: str, rate: int = 60) -> bool:
    """检查用户速率限制"""
    return rate_limiter.is_allowed(f"user:{user_id}", rate=rate)


def check_key_rate_limit(api_key_id: str, rate: int = 60) -> bool:
    """检查 API Key 速率限制"""
    return rate_limiter.is_allowed(f"key:{api_key_id}", rate=rate)
