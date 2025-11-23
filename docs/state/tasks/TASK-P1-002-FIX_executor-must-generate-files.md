# TASK-P1-002-FIX: Executor Must Generate Real Files

**Priority**: 🔴 **CRITICAL BLOCKER**  
**Status**: Awaiting Owner Approval  
**Estimated**: 1-2 days

---

## Problem Statement

**Current Behavior** (BROKEN):
- Owner submits task: "hello world py"
- Executor calls LLM which returns TEXT EXPLANATION of how to write Python
- "Final Result" shows essay, NOT actual code files
- NO files created, NO app deployed, NO working product

**Required Behavior** (PRODUCTION-GRADE):
- Owner submits task: "hello world py"
- Executor generates ACTUAL FILE: `hello_world.py` with working code
- Files saved to workspace volume
- Owner can download files as ZIP
- Owner Console shows file tree, not just text

---

## Success Criteria

### ✅ File Creation (Docker Proof Required):
```bash
# After task completion:
docker-compose exec agent-runtime ls /workspace/{task_id}/
# MUST show: hello_world.py (or equivalent real files)

docker-compose exec agent-runtime cat /workspace/{task_id}/hello_world.py
# MUST show: print("Hello World")  # Actual code
```

### ✅ Download Endpoint Works:
```bash
curl http://localhost:8002/api/v1/artifacts/{task_id}/download -o artifact.zip
unzip -l artifact.zip
# MUST show: hello_world.py inside ZIP
```

### ✅ Owner Console Shows Files:
- File tree visible in browser
- Download button works
- Can view code in UI (not just "Final Result" text)

---

## Implementation Plan

### Phase A: Backend (File Generation)

**A1: Update executor_node to use file-writing tools**
```python
# File: graph/nodes/execution.py

@tool
def create_file(filename: str, content: str, task_id: str) -> str:
    """Create a file in task workspace."""
    workspace = f"/workspace/{task_id}"
    os.makedirs(workspace, exist_ok=True)
    filepath = os.path.join(workspace, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return f"Created {filename} ({len(content)} bytes)"

async def executor_node(state: AgentState) -> dict:
    """Execute task by generating REAL FILES."""
    task = state["task"]
    task_id = state.get("task_id", "unknown")
    
    # LLM with tool calling to create files
    llm_with_tools = llm.bind_tools([create_file])
    
    prompt = f"""Task: {task}

Generate actual working files for this task.
Use the create_file tool to write each file.
Return structured file list, NOT explanations."""
    
    response = await llm_with_tools.ainvoke(prompt)
    
    # Execute tool calls
    files_created = []
    for tool_call in response.tool_calls:
        result = create_file.invoke(tool_call["args"])
        files_created.append(tool_call["args"]["filename"])
    
    return {
        "result": f"Created {len(files_created)} files",
        "files": files_created
    }
```

**A2: Add workspace volume to docker-compose.yml**
```yaml
services:
  agent-runtime:
    volumes:
      - workspace:/workspace

volumes:
  workspace:
```

**A3: Create artifact download endpoint**
```python
# File: api/routers/artifacts.py
import zipfile
from fastapi import HTTPException
from fastapi.responses import FileResponse

@router.get("/v1/artifacts/{task_id}/download")
async def download_artifact(task_id: str):
    """Download task workspace as ZIP."""
    workspace_path = f"/workspace/{task_id}"
    
    if not os.path.exists(workspace_path):
        raise HTTPException(404, "No files for this task")
    
    zip_path = f"/tmp/{task_id}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, workspace_path)
                zipf.write(filepath, arcname)
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{task_id}.zip"
    )
```

### Phase B: Frontend (File Display)

**B1: Add file tree display to Owner Console**
```tsx
// File: apps/web/src/app/file-tree.tsx
export function FileTree({ taskId }: { taskId: string }) {
  const [files, setFiles] = useState<string[]>([]);
  
  useEffect(() => {
    fetch(`http://localhost:8002/api/v1/artifacts/${taskId}/files`)
      .then(res => res.json())
      .then(data => setFiles(data.files));
  }, [taskId]);
  
  return (
    <div className="file-tree">
      <h3>Generated Files</h3>
      <ul>
        {files.map(file => (
          <li key={file}>{file}</li>
        ))}
      </ul>
      <a 
        href={`http://localhost:8002/api/v1/artifacts/${taskId}/download`}
        className="download-button"
      >
        Download ZIP
      </a>
    </div>
  );
}
```

**B2: Integrate into page.tsx**
```tsx
// Replace or augment "Final Result" section:
{taskId && <FileTree taskId={taskId} />}
```

---

## Verification Steps (Developer MUST Complete)

### Step 1: Unit Test File Creation
```python
# tests/test_executor_file_generation.py
async def test_executor_creates_real_files():
    state = {"task": "hello world py", "task_id": "test-123"}
    result = await executor_node(state)
    
    # Verify file exists
    assert os.path.exists("/workspace/test-123/hello_world.py")
    
    # Verify content
    with open("/workspace/test-123/hello_world.py") as f:
        content = f.read()
        assert "print" in content
        assert "Hello" in content
```

### Step 2: Docker Integration Test
```bash
# Clean workspace
docker-compose down -v
docker-compose up -d

# Submit task via API
curl -X POST http://localhost:8002/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "create hello world python script"}'

# Wait for completion, then verify
TASK_ID="..." # from API response
docker-compose exec agent-runtime ls /workspace/${TASK_ID}/
# MUST show files

# Download artifact
curl http://localhost:8002/api/v1/artifacts/${TASK_ID}/download -o test.zip
unzip -l test.zip
# MUST show files inside
```

### Step 3: Owner Validation (Browser)
1. Navigate to `http://localhost:3000`
2. Submit: "create a simple Python hello world script"
3. Wait for completion
4. **VERIFY**: File tree appears (not just text)
5. **VERIFY**: Download button works
6. **VERIFY**: ZIP contains actual `.py` file with code

---

## Evidence Required for Approval

**G5 (Tests)**: >= 85% coverage for file creation logic  
**G4 (Lint/Type)**: Clean  
**G10 (Owner Validation)**: Screenshots showing:
1. File tree in Owner Console
2. Downloaded ZIP with actual files inside
3. Docker `ls` showing files in container

**Docker Proof**:
```bash
docker-compose exec agent-runtime find /workspace -type f
# Shows actual files, not empty
```

---

## Timeline

- **Phase A (Backend)**: 1 day
  - A1: Executor file tools (4 hours)
  - A2: Workspace volume (1 hour)
  - A3: Download endpoint (3 hours)
- **Phase B (Frontend)**: 4 hours
  - B1: File tree component (2 hours)
  - B2: Integration (2 hours)
- **Verification**: 4 hours
  - Unit tests, Docker proof, Owner validation

**Total**: 1.5-2 days

---

## Risks

**Risk 1**: LLM generates explanations instead of code even with tools  
**Mitigation**: Add explicit prompting: "Use create_file tool for EVERY file. Do NOT explain, just create."

**Risk 2**: Workspace volume permissions  
**Mitigation**: Set correct ownership in Dockerfile: `RUN mkdir /workspace && chown app:app /workspace`

---

## Constitutional Compliance

- ✅ **CLAUDE.md Rule 2** (Docker from Line 1): Workspace volume configured in docker-compose
- ✅ **CLAUDE.md Rule 3** (Evidence-Based): Docker proof required before approval
- ✅ **GOLDEN_RULES Coverage 85%**: Tests for file generation logic
- ✅ **VISION.md** (Real App): Generates actual files, not fake outputs
