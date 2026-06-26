from supabase import create_client, Client
from .database import settings


def get_supabase_client() -> Client:
    """Get a Supabase client instance."""
    return create_client(
        settings.supabase_url,
        settings.supabase_key
    )
