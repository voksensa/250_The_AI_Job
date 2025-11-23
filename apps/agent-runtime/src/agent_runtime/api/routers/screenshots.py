import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/{filename}")
async def get_screenshot(filename: str):
    """Serve a screenshot file."""
    # Ensure we only serve from the screenshots directory
    # and prevent directory traversal
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = f"screenshots/{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Screenshot not found")

    return FileResponse(path)
