"""Multi-account manager - 参考 sub2api 的多账号轮询"""

import os
import random
from typing import Optional, List
from dataclasses import dataclass
from .providers import (
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    BaiduProvider,
    AlibabaProvider,
    ZhipuProvider,
    DeepSeekProvider,
)
from .providers.base import BaseProvider


@dataclass
class AccountInfo:
    """账号信息"""
    provider_name: str
    account_id: str
    api_key: str
    is_active: bool = True
    priority: int = 0  # 优先级，越大越优先
    weight: int = 1  # 权重，用于加权轮询


class MultiAccountManager:
    """多账号管理器"""

    def __init__(self):
        self._accounts: dict[str, List[AccountInfo]] = {}
        self._providers: dict[str, BaseProvider] = {}
        self._current_index: dict[str, int] = {}
        self._init_accounts()

    def _init_accounts(self):
        """从环境变量初始化账号"""
        # OpenAI
        openai_keys = self._get_multi_keys("OPENAI_API_KEY")
        for i, key in enumerate(openai_keys):
            self._add_account("openai", f"openai_{i}", key)

        # Anthropic
        anthropic_keys = self._get_multi_keys("ANTHROPIC_API_KEY")
        for i, key in enumerate(anthropic_keys):
            self._add_account("anthropic", f"anthropic_{i}", key)

        # Google
        google_keys = self._get_multi_keys("GOOGLE_API_KEY")
        for i, key in enumerate(google_keys):
            self._add_account("google", f"google_{i}", key)

        # Baidu
        baidu_keys = self._get_multi_keys("BAIDU_API_KEY")
        baidu_secrets = self._get_multi_keys("BAIDU_SECRET_KEY")
        for i, key in enumerate(baidu_keys):
            secret = baidu_secrets[i] if i < len(baidu_secrets) else ""
            self._add_account("baidu", f"baidu_{i}", key, secret=secret)

        # Alibaba
        alibaba_keys = self._get_multi_keys("ALIBABA_API_KEY")
        for i, key in enumerate(alibaba_keys):
            self._add_account("alibaba", f"alibaba_{i}", key)

        # Zhipu
        zhipu_keys = self._get_multi_keys("ZHIPU_API_KEY")
        for i, key in enumerate(zhipu_keys):
            self._add_account("zhipu", f"zhipu_{i}", key)

        # DeepSeek
        deepseek_keys = self._get_multi_keys("DEEPSEEK_API_KEY")
        for i, key in enumerate(deepseek_keys):
            self._add_account("deepseek", f"deepseek_{i}", key)

    def _get_multi_keys(self, env_var: str) -> List[str]:
        """获取多个 API Key（逗号分隔）"""
        value = os.getenv(env_var, "")
        if not value:
            return []
        return [k.strip() for k in value.split(",") if k.strip()]

    def _add_account(
        self,
        provider_name: str,
        account_id: str,
        api_key: str,
        priority: int = 0,
        weight: int = 1,
        **kwargs,
    ):
        """添加账号"""
        if provider_name not in self._accounts:
            self._accounts[provider_name] = []

        account = AccountInfo(
            provider_name=provider_name,
            account_id=account_id,
            api_key=api_key,
            priority=priority,
            weight=weight,
        )
        self._accounts[provider_name].append(account)

        # 创建 Provider 实例
        provider = self._create_provider(provider_name, api_key, **kwargs)
        if provider:
            self._providers[account_id] = provider

    def _create_provider(
        self, provider_name: str, api_key: str, **kwargs
    ) -> Optional[BaseProvider]:
        """创建 Provider 实例"""
        if provider_name == "openai":
            return OpenAIProvider(api_key=api_key)
        elif provider_name == "anthropic":
            return AnthropicProvider(api_key=api_key)
        elif provider_name == "google":
            return GoogleProvider(api_key=api_key)
        elif provider_name == "baidu":
            return BaiduProvider(api_key=api_key, secret_key=kwargs.get("secret", ""))
        elif provider_name == "alibaba":
            return AlibabaProvider(api_key=api_key)
        elif provider_name == "zhipu":
            return ZhipuProvider(api_key=api_key)
        elif provider_name == "deepseek":
            return DeepSeekProvider(api_key=api_key)
        return None

    def get_provider(self, provider_name: str) -> Optional[BaseProvider]:
        """获取 Provider（轮询方式）"""
        accounts = self._accounts.get(provider_name, [])
        if not accounts:
            return None

        # 过滤活跃账号
        active_accounts = [a for a in accounts if a.is_active]
        if not active_accounts:
            return None

        # 轮询选择
        index = self._current_index.get(provider_name, 0) % len(active_accounts)
        account = active_accounts[index]
        self._current_index[provider_name] = (index + 1) % len(active_accounts)

        return self._providers.get(account.account_id)

    def get_provider_by_weight(self, provider_name: str) -> Optional[BaseProvider]:
        """获取 Provider（加权随机方式）"""
        accounts = self._accounts.get(provider_name, [])
        if not accounts:
            return None

        # 过滤活跃账号
        active_accounts = [a for a in accounts if a.is_active]
        if not active_accounts:
            return None

        # 加权随机选择
        total_weight = sum(a.weight for a in active_accounts)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for account in active_accounts:
            cumulative += account.weight
            if r <= cumulative:
                return self._providers.get(account.account_id)

        return self._providers.get(active_accounts[0].account_id)

    def list_accounts(self) -> dict:
        """列出所有账号"""
        result = {}
        for provider_name, accounts in self._accounts.items():
            result[provider_name] = [
                {
                    "account_id": a.account_id,
                    "is_active": a.is_active,
                    "priority": a.priority,
                    "weight": a.weight,
                }
                for a in accounts
            ]
        return result


# 全局多账号管理器实例
multi_account_manager = MultiAccountManager()
