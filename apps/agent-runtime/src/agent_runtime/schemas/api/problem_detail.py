from pydantic import BaseModel


class ProblemDetail(BaseModel):
    """RFC 9457 Problem Details for HTTP APIs."""
    type: str  # URI reference identifying the problem type
    title: str  # Short, human-readable summary
    status: int  # HTTP status code
    detail: str  # Explanation specific to this occurrence
    instance: str | None = None  # URI reference to specific occurrence

    class Config:
        json_schema_extra = {
            "example": {
                "type": "https://yfe.app/errors/task-not-found",
                "title": "Task Not Found",
                "status": 404,
                "detail": "Task a1b2c3d4 was not found in the system",
                "instance": "urn:trace:req-abc123"
            }
        }
