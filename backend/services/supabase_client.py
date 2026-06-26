from supabase import create_client, Client
from .database import settings

_client: Client | None = None


def get_supabase_client() -> Client:
    """Get a Supabase client instance (singleton)."""
    global _client
    if _client is None:
        _client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    return _client
