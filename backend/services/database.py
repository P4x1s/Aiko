from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Gateway"
    debug: bool = False

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""

    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    supabase_jwt_secret: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
