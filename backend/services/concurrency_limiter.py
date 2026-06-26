"""Concurrency limiter service - 参考 sub2api 的并发控制"""

import asyncio
from collections import defaultdict
from typing import Optional


class ConcurrencyLimiter:
    """并发限制器"""

    def __init__(self):
        self._counts: dict[str, int] = defaultdict(int)
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def acquire(self, key: str, max_concurrent: int = 5) -> bool:
        """获取并发槽位"""
        async with self._locks[key]:
            if self._counts[key] < max_concurrent:
                self._counts[key] += 1
                return True
            return False

    async def release(self, key: str):
        """释放并发槽位"""
        async with self._locks[key]:
            self._counts[key] = max(0, self._counts[key] - 1)

    def get_count(self, key: str) -> int:
        """获取当前并发数"""
        return self._counts.get(key, 0)


# 全局并发限制器实例
concurrency_limiter = ConcurrencyLimiter()


class ConcurrencyContext:
    """并发控制上下文管理器"""

    def __init__(self, key: str, max_concurrent: int = 5):
        self.key = key
        self.max_concurrent = max_concurrent

    async def __aenter__(self):
        acquired = await concurrency_limiter.acquire(self.key, self.max_concurrent)
        if not acquired:
            raise ConcurrencyLimitExceeded(f"Concurrency limit exceeded for {self.key}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await concurrency_limiter.release(self.key)


class ConcurrencyLimitExceeded(Exception):
    """并发限制超出异常"""
    pass
