from supabase import create_client, Client
from .database import settings

_client: Client | None = None


def get_supabase_client() -> Client:
    """Get a Supabase client instance with service_role key (bypasses RLS)."""
    global _client
    if _client is None:
        _client = create_client(
            settings.supabase_url,
            settings.supabase_service_key  # 使用 service_role key 绕过 RLS
        )
    return _client
