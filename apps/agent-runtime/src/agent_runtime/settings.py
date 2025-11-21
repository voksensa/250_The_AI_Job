from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    database_url: str = "postgresql://yfe:yfe_dev_pass@localhost:5432/yfe_db"
    environment: str = "development"
    debug: bool = True
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    model_name: str = "gpt-4o"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
