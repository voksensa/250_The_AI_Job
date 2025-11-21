"""Main FastAPI application for Agent Runtime."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

from .api.routes import router as tasks_router


class Settings(BaseSettings):
    """Application settings from environment variables."""

    database_url: str = "postgresql://yfe:yfe_dev_pass@localhost:5432/yfe_db"
    environment: str = "development"
    debug: bool = True
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    print(f"🚀 Agent Runtime starting (env={settings.environment})")
    db_url = settings.database_url
    db_host = db_url.split("@")[1] if "@" in db_url else "N/A"
    print(f"📊 Database: {db_host}")

    yield

    # Shutdown
    print("🛑 Agent Runtime shutting down")


app = FastAPI(title="Agent Runtime", version="0.1.0", lifespan=lifespan)

# CORS middleware for Owner Console
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3030", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for Docker and K8s."""
    return {
        "status": "ok",
        "service": "agent-runtime",
        "version": "0.1.0",
        "environment": settings.environment,
    }


# Include API routers
app.include_router(tasks_router, prefix="/api")
