import os
import zipfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from ...utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/v1/artifacts/{task_id}/download")
async def download_artifact(task_id: str):
    """Download task workspace as ZIP."""
    workspace_path = f"/workspace/{task_id}"

    if not os.path.exists(workspace_path):
        raise HTTPException(404, "No files for this task")

    zip_path = f"/tmp/{task_id}.zip"
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            has_files = False
            for root, _dirs, files in os.walk(workspace_path):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, workspace_path)
                    zipf.write(filepath, arcname)
                    has_files = True

            if not has_files:
                 raise HTTPException(404, "Workspace exists but is empty")

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"{task_id}.zip"
        )
    except Exception as e:
        logger.error("artifact_download_error", task_id=task_id, error=str(e))
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(500, f"Failed to create zip: {str(e)}") from e

@router.get("/v1/artifacts/{task_id}/files")
async def list_files(task_id: str):
    """List files in task workspace."""
    workspace_path = f"/workspace/{task_id}"

    if not os.path.exists(workspace_path):
        return JSONResponse({"files": []})

    files_list = []
    for root, _dirs, files in os.walk(workspace_path):
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, workspace_path)
            files_list.append(relpath)

    return JSONResponse({"files": files_list})
