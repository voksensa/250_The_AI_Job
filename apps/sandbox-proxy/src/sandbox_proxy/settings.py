from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    WORKSPACE_ROOT: Path = Path("/workspace")
    HOST: str = "0.0.0.0"
    PORT: int = 3001
    LOG_LEVEL: str = "info"
    
    # Domain suffix to strip (e.g., ".localhost:3000")
    # In local dev: ".localhost"
    # In prod: ".yourdomain.com"
    DOMAIN_SUFFIX: str = ".localhost"

    model_config = SettingsConfigDict(env_prefix="SANDBOX_")

settings = Settings()
