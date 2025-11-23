from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from .settings import settings

app = FastAPI(
    title="Sandbox Proxy",
    version="1.0.0",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}

@app.get("/{path:path}")
async def serve_sandbox_file(request: Request, path: str):
    host = request.headers.get("host", "")
    
    # Extract task_id from subdomain
    # Expected format: {task_id}.localhost:3000 or {task_id}.sandbox.yfe.app
    if not host:
        raise HTTPException(status_code=400, detail="Missing Host header")
        
    # Remove port if present
    hostname = host.split(":")[0]
    
    # Check if it matches our domain suffix
    if not hostname.endswith(settings.DOMAIN_SUFFIX):
        # If accessing directly (e.g. localhost:3000), show welcome or 404
        if path == "" or path == "/":
            return {"message": "Sandbox Proxy Running. Access via {task_id}.localhost:3000"}
        raise HTTPException(status_code=404, detail="Domain not recognized")
        
    # Extract task_id
    # e.g. "task-123.localhost" -> "task-123"
    suffix_len = len(settings.DOMAIN_SUFFIX)
    # Handle the dot if DOMAIN_SUFFIX doesn't have it (though settings.py has it)
    if settings.DOMAIN_SUFFIX.startswith("."):
         task_id = hostname[:-len(settings.DOMAIN_SUFFIX)]
    else:
         # Fallback logic if needed, but we control settings
         task_id = hostname.replace(f".{settings.DOMAIN_SUFFIX}", "")

    if not task_id:
        raise HTTPException(status_code=400, detail="Invalid task ID in subdomain")

    # Sanitize task_id to prevent directory traversal
    if ".." in task_id or "/" in task_id:
         raise HTTPException(status_code=400, detail="Invalid task ID")

    # Construct file path
    task_root = settings.WORKSPACE_ROOT / task_id
    
    # Default to index.html if path is empty
    if path == "" or path.endswith("/"):
        file_path = task_root / path.strip("/") / "index.html"
    else:
        file_path = task_root / path

    # Security check: ensure file_path resolves to within task_root
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(task_root.resolve())):
             raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
         raise HTTPException(status_code=404, detail="File not found")

    if not file_path.exists() or not file_path.is_file():
        # Try adding .html if missing
        if not path.endswith(".html"):
             alt_path = file_path.with_suffix(".html")
             if alt_path.exists() and alt_path.is_file():
                 return FileResponse(alt_path)
        
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
