"""Main FastAPI application for Agent Runtime."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from .api.routers.tasks import router as api_router
from .graph.graph import create_graph
from .schemas.api.problem_detail import ProblemDetail
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    print(f"🚀 Agent Runtime starting (env={settings.environment})")
    db_url = settings.database_url
    db_host = db_url.split("@")[1] if "@" in db_url else "N/A"
    print(f"📊 Database: {db_host}")

    async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:
        await checkpointer.setup()
        app.state.graph = create_graph(checkpointer)
        yield

    # Shutdown
    print("🛑 Agent Runtime shutting down")


app = FastAPI(title="Agent Runtime", version="0.1.0", lifespan=lifespan)

# CORS middleware for Owner Console
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js frontend
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Convert HTTPException to RFC 9457 Problem Details."""
    problem = ProblemDetail(
        type=f"https://yfe.app/errors/{exc.status_code}",
        title=exc.detail if isinstance(exc.detail, str) else "Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=f"urn:trace:{request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump()
    )

# Include API router
app.include_router(api_router, prefix="/api")
