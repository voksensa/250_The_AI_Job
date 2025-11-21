# TASK-P1-001: Production Toggle Foundation (Phase 1 MVP)

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🟢 **HIGH (Phase 1 Kickoff)**  
**Date**: 2025-11-21  
**Epic**: E001 – Foundation  
**Phase**: Phase 1 – MVP  
**Estimated Effort**: 4-6 hours  
**Blocks**: All Phase 1 features - This is the foundation

---

## Objective

Build the **minimal end-to-end Production Toggle proof of concept** where Owner can submit a task via browser UI, see it process through LangGraph, and view results in real-time.

**Non-Negotiable Requirements:**
1. **Phase A + Phase B Together** - Backend capability AND frontend UI in same task
2. **Evidence-Based** - All new patterns verified via MCP queries to official docs
3. **Native over Custom** - Extend existing native LangGraph code, no custom replacements
4. **Production from Line 1** - Real LLM calls, real streaming, no mocks
5. **Owner Can Use It** - ≤20 min browser validation required

---

## Context

**Current State (Post TASK-FIX-001):**
- ✅ `apps/agent-runtime` working with native LangGraph
- ✅ `graph.py` has 2 nodes: planner_node, executor_node
- ✅ `routes.py` has POST /tasks, GET /tasks/{id}, WebSocket /stream
- ✅ PostgresSaver for checkpointing
- ✅ Native astream for events

**What's Missing for Phase 1:**
- ❌ No frontend UI (Owner can't use it)
- ❌ No real-time event display
- ❌ No end-to-end workflow demonstration
- ⚠️ WebSocket endpoint exists but needs testing/refinement

**Goal**: Connect the dots with minimal new code to prove the concept works.

---

## Pre-Work (Research Phase)

### Step 1: Review Existing Implementation

**Before writing ANY new code, document what we have:**

1. **Read current graph.py:**
   - How many nodes? (planner, executor)
   - What state fields? (task, plan, result, messages)
   - How are events emitted? (get_stream_writer)
   
2. **Read current routes.py:**
   - What endpoints exist? (POST /tasks, GET /tasks/{id}, WebSocket /stream)
   - How does WebSocket work? (Receives task, streams via astream)
   - What's the exact flow?

3. **Document in session log** under "Phase 1: Current State Analysis"

**Do NOT skip this.** You must understand what exists before extending it.

---

### Step 2: MCP Research for Frontend Patterns

**You MUST run these MCP queries and document results:**

```python
# Query 1: Next.js 15 App Router basics
mcp0_SearchDocsByLangChain(query="nextjs 15 app router server actions form")

# Query 2: React hooks for streaming
mcp0_SearchDocsByLangChain(query="react hooks useEffect fetch streaming")

# Query 3: WebSocket in React/Next.js
mcp0_SearchDocsByLangChain(query="nextjs websocket client connection react")

# Query 4: Server-Sent Events vs WebSocket
mcp0_SearchDocsByLangChain(query="server sent events vs websocket streaming")

# Query 5: FastAPI CORS for Next.js
mcp0_SearchDocsByLangChain(query="fastapi cors configuration nextjs localhost")
```

**Document findings in:**
`docs/state/SESSIONS/2025-11-21_dev_p1001-research.md`

**Include for each query:**
- Query text
- Key findings (patterns, code examples)
- How it applies to our implementation
- Any gotchas or warnings

---

## Implementation (Execution Phase)

### Part A: Frontend UI (Next.js)

**Directory**: `apps/web/`

#### A1: Verify Next.js Setup

```bash
cd apps/web
# If package.json doesn't exist, initialize:
# npx create-next-app@latest ./ --typescript --tailwind --app --no-src-dir

# Install if needed
npm install
```

**Evidence**: Screenshot of `npm install` success or existing `node_modules/`

---

#### A2: Create Task Submission Page

**File**: `apps/web/app/page.tsx`

**Requirements:**
- Form with textarea for task description
- Submit button
- Display area for task ID and status
- Real-time event stream display
- Uses native Next.js patterns per MCP Query 1

**Example Structure** (verify against MCP findings):
```typescript
'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [task, setTask] = useState('')
  const [taskId, setTaskId] = useState<string | null>(null)
  const [events, setEvents] = useState<any[]>([])
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // POST to backend /api/tasks
    // Pattern from MCP Query 1
  }
  
  useEffect(() => {
    if (!taskId) return
    // WebSocket connection to stream events
    // Pattern from MCP Query 3
  }, [taskId])
  
  return (
    <div className="container mx-auto p-8">
      <h1>Your First Engineer</h1>
      {/* Form and event display */}
    </div>
  )
}
```

**Verification:**
- [ ] Code uses patterns from MCP queries (cite query number in comments)
- [ ] No generic "I think this works" code
- [ ] TypeScript types are correct
- [ ] Tailwind classes for basic styling

---

#### A3: Create API Client

**File**: `apps/web/lib/api.ts`

**Requirements:**
- `submitTask(description: string)` function
- Returns `{ task_id: string, status: string }`
- Uses fetch API (native, no external libs needed)
- Error handling with try/catch

**Pattern** (verify against MCP findings):
```typescript
export async function submitTask(description: string) {
  const response = await fetch('http://localhost:8002/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: description })
  })
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  
  return response.json()
}
```

**Verification:**
- [ ] Error handling included
- [ ] Correct backend URL (port 8002 per TASK-FIX-001)
- [ ] TypeScript types defined

---

### Part B: Backend Refinements

**Directory**: `apps/agent-runtime/src/agent_runtime/`

#### B1: Verify CORS Configuration

**File**: `main.py`

**Current CORS** (from TASK-FIX-001):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # May need to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Action**: 
- Check if localhost:3000 (Next.js dev server) is allowed
- Update if needed per MCP Query 5
- Document decision in session log

---

#### B2: Test WebSocket Endpoint

**File**: `api/routes.py` - WebSocket /tasks/{task_id}/stream

**Current Implementation** (from TASK-FIX-001):
- Accepts WebSocket connection
- Receives task JSON
- Streams via `graph.astream(..., stream_mode=["updates", "custom"])`

**Action**:
1. **Manual Test**: Connect via `websocat` or browser console
2. **Verify**: Events are received and JSON-serializable
3. **Fix if needed**: Handle non-serializable objects
4. **Document**: Test commands and results in session log

**Test Command**:
```bash
# Install websocat if not available: brew install websocat
echo '{"task": "Create a hello world function"}' | \
  websocat ws://localhost:8002/api/tasks/test-123/stream
```

**Expected**: JSON events streamed back

**If errors**: Fix serialization in routes.py, document fix

---

#### B3: Add HTTP Endpoint for Events (Optional Fallback)

**If WebSocket proves problematic**, implement Server-Sent Events as fallback per MCP Query 4.

**File**: `api/routes.py`

```python
from fastapi.responses import StreamingResponse

@router.get("/tasks/{task_id}/events")
async def stream_task_events(request: Request, task_id: str):
    """Stream task events via Server-Sent Events."""
    async def event_generator():
        graph = request.app.state.graph
        config = {"configurable": {"thread_id": task_id}}
        
        # Get existing state and stream
        async for chunk in graph.astream(None, config=config, stream_mode=["updates", "custom"]):
            yield f"data: {json.dumps(str(chunk))}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Document decision**: WebSocket vs SSE in session log with rationale

---

### Part C: Integration Testing

#### C1: Start All Services

```bash
# Terminal 1: Backend
cd apps/agent-runtime
source .venv/bin/activate
uvicorn agent_runtime.main:app --reload --port 8002

# Terminal 2: Frontend
cd apps/web
npm run dev

# Terminal 3: Database (if not already running)
docker-compose up postgres
```

**Evidence**: Screenshots of all three terminals showing services running

---

#### C2: End-to-End Test

**Steps**:
1. Open http://localhost:3000 in browser
2. Enter task: "Create a simple hello world function in Python"
3. Click Submit
4. Observe:
   - Task ID displayed ✅
   - Status shows "running" ✅
   - Events stream in real-time ✅
   - See planner_node events ✅
   - See executor_node events ✅
   - Final result displayed ✅

**Evidence Required**:
- Screenshot of form submission
- Screenshot of event stream (showing at least 3 events)
- Screenshot of final result
- Browser console showing no errors
- Backend logs showing LLM calls

---

#### C3: Owner Validation (≤20 min)

**Owner must be able to:**
1. Start services with simple commands
2. Open browser to localhost:3000
3. Submit a task
4. See it process
5. View results

**Document in session log**:
- Exact commands Owner runs
- What Owner sees at each step
- Total time from "start services" to "see results"
- Any issues encountered

**Success Criteria**: Owner completes flow in ≤20 minutes without touching code

---

## Documentation Requirements

### D1: Session Log

Create: `docs/state/SESSIONS/2025-11-21_dev_p1001-implementation.md`

**Structure:**

```markdown
# Session Log: Production Toggle Foundation (TASK-P1-001)

## Phase 0: Current State Analysis

### Existing graph.py
- Nodes: planner_node, executor_node
- State: AgentState with task, plan, result, messages
- Events: get_stream_writer() used in both nodes
- [Code citations to specific lines]

### Existing routes.py
- POST /tasks: Creates task, runs in background
- GET /tasks/{id}: Returns state from PostgresSaver
- WebSocket /stream: Streams via astream with stream_mode
- [Code citations]

## Phase 1: MCP Research

### MCP Query 1: Next.js App Router
- Query: [paste query]
- Key Finding: [paste code example from docs]
- Applied To: app/page.tsx lines X-Y
- Link: [URL from MCP response]

[Repeat for all 5 queries]

## Phase 2: Implementation

### Frontend: app/page.tsx
- Pattern used: [cite MCP query]
- Key decisions:
  * useState for task/taskId/events
  * useEffect for WebSocket connection
  * Cleanup on unmount
- Code: [lines X-Y]

### Frontend: lib/api.ts
- Pattern used: Native fetch API
- Error handling: try/catch with HTTP status check
- Code: [lines X-Y]

### Backend: CORS Configuration
- Decision: [WebSocket worked/didn't work]
- Fix applied: [if any]
- MCP query reference: Query 5

### Backend: WebSocket Testing
- Test command: [paste exact command]
- Result: [paste output]
- Events received: [list event types]
- Serialization issues: [none / fixed X]

## Phase 3: Integration Testing

### End-to-End Test Results
- Task submitted: "Create a simple hello world function in Python"
- Task ID: [UUID]
- Events received: [count]
- Sample events: [paste 3 events]
- Final result: [paste result]
- LLM called: ✅ (evidence: backend logs show API key usage)

### Owner Validation
- Commands run: [list exact commands]
- Time elapsed: [X minutes]
- Issues: [none / list]
- Owner feedback: [what worked, what didn't]

## Phase 4: Verification

### Code Quality
- Lint (frontend): `npm run lint` → [result]
- Type check (frontend): `npm run type-check` → [result]
- Lint (backend): Already passing from TASK-FIX-001
- No new violations introduced

### Evidence
- [Link to screenshots]
- [Link to browser console logs]
- [Link to backend logs]

## Conclusion
Production Toggle foundation complete. Owner can submit tasks and see results in browser.
```

---

### D2: Update PROGRESS.md

```markdown
- **2025-11-21** – Developer – Completed TASK-P1-001: Production Toggle Foundation. Owner can submit tasks via browser UI, see real-time LangGraph processing, and view results. End-to-end flow validated in ≤20 min.
```

---

### D3: Update BLOCKERS.md

**If any blockers encountered**, document them. Otherwise note "None."

---

## Success Criteria

You are DONE when:

### Code Complete
- [ ] `apps/web/app/page.tsx` exists with task form and event display
- [ ] `apps/web/lib/api.ts` exists with submitTask function
- [ ] CORS configured for localhost:3000
- [ ] WebSocket endpoint tested and working (or SSE fallback implemented)
- [ ] All code cites MCP query patterns in comments

### Quality Gates
- [ ] G3: Frontend lint clean (`npm run lint`)
- [ ] G3: Backend lint still clean (no new violations)
- [ ] G5: TypeScript check passes (`tsc --noEmit`)
- [ ] G6: Both services start successfully
- [ ] G10: Owner validated in ≤20 min

### Evidence
- [ ] 5 MCP queries documented in session log
- [ ] Screenshots of end-to-end test (form, events, result)
- [ ] Browser console showing no errors
- [ ] Backend logs showing real LLM calls
- [ ] Owner validation steps documented with timings

### Documentation
- [ ] Session log complete with all phases
- [ ] PROGRESS.md updated
- [ ] All decisions documented with rationale
- [ ] Git commit with detailed message

---

## Git Commit Message Template

```
feat(phase1): Add Production Toggle foundation (owner console + streaming)

Phase 1 MVP: Owner can submit tasks via browser and see real-time processing.

Frontend (apps/web):
- Created task submission form (app/page.tsx)
- Implemented real-time event streaming via WebSocket
- API client for backend communication (lib/api.ts)
- Patterns verified via MCP queries to Next.js docs

Backend (apps/agent-runtime):
- Verified CORS for localhost:3000
- Tested WebSocket /tasks/{id}/stream endpoint
- [SSE fallback added] (if applicable)

Validation:
- End-to-end test: Task submission → LLM processing → Results display
- Owner validated in <20 minutes
- Real LLM calls confirmed
- Zero mocks/stubs

Evidence: docs/state/SESSIONS/2025-11-21_dev_p1001-implementation.md

Gates: G3 (lint), G5 (types), G6 (builds), G10 (owner can use it)
```

---

## CEO Review Checklist

When you submit, I will verify:

### Code Review
- [ ] MCP queries actually run and documented
- [ ] Frontend code cites MCP query patterns
- [ ] No generic "I think this works" code
- [ ] TypeScript types are proper (not `any` everywhere)
- [ ] WebSocket connection properly cleaned up (no memory leaks)

### Runtime Verification
- [ ] I will open browser to localhost:3000
- [ ] I will submit a task
- [ ] I will verify events stream in real-time
- [ ] I will check backend logs for real LLM calls
- [ ] I will verify no errors in browser console

### Evidence Verification
- [ ] Screenshots show actual UI (not mockups)
- [ ] Browser console screenshot included
- [ ] Backend logs show API key usage (LLM called)
- [ ] Session log has MCP query results
- [ ] Owner validation timing documented

**If any item fails, task will be REJECTED and returned to you.**

---

## Critical Reminders

1. **EXTEND, DON'T REPLACE**
   - Do NOT rewrite graph.py
   - Do NOT replace existing routes
   - BUILD ON what TASK-FIX-001 delivered

2. **EVIDENCE REQUIRED**
   - Every frontend pattern must cite MCP query
   - Every decision must have documented rationale
   - Screenshots must show real working UI, not plans

3. **OWNER MUST VALIDATE**
   - You must actually run the end-to-end test
   - You must document exact steps Owner takes
   - If it takes >20 min, simplify the flow

4. **NO MOCKS**
   - Real LLM calls (evidence: API logs)
   - Real WebSocket/SSE streaming
   - Real Next.js (not static HTML)

5. **MCP QUERIES ARE MANDATORY**
   - Do NOT skip MCP research
   - Do NOT use "I know Next.js" patterns
   - VERIFY against official docs

---

## Timeline

**Start**: After CEO approval  
**Expected Duration**: 4-6 hours focused work  
**Deliverable**: Working Owner Console with real-time task processing

---

## Questions?

**If WebSocket doesn't work:**
- Document the error in session log
- Implement SSE fallback per MCP Query 4
- Explain why WebSocket failed

**If you need to modify routes.py:**
- Document what and why
- Ensure existing POST/GET endpoints still work
- Verify TASK-FIX-001 tests still pass

**If Next.js setup is missing:**
- Initialize with `npx create-next-app@latest`
- Document exact command used
- Ensure TypeScript + Tailwind enabled

**Do NOT guess. Do NOT skip MCP queries. VERIFY everything against official docs.**
