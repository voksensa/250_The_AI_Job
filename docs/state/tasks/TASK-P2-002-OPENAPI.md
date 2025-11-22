# TASK-P2-002-OPENAPI: Create OpenAPI Specification

**Priority**: MEDIUM  
**Order**: Task 2 of 4 (Phase 2 Foundation)  
**Depends On**: TASK-P2-001-CONST-AUDIT  
**Estimated**: 2 hours

---

## Objective

Create machine-readable OpenAPI spec for existing API to prevent frontend/backend drift.

**Golden Rule**: Rule 4.1 from RB-003 (Tier 2)

---

## Current API Routes

**Backend** (`apps/agent-runtime`):
1. `POST /api/v1/tasks` - Create new task
2. `GET /api/v1/tasks/{task_id}` - Get task status
3. `WS /api/v1/tasks/{task_id}/stream` - Stream task events
4. `GET /health` - Health check (not versioned)

**No OpenAPI spec exists.**

---

## Tasks

### Phase A: Create OpenAPI File (1hr)

**Create**: `openapi/yfe-api-v1.yaml`

**Structure**:
```yaml
openapi: 3.1.0
info:
  title: Your First Engineer API
  version: 1.0.0
  description: Agent runtime API for task execution

servers:
  - url: http://localhost:8000
    description: Local development
  - url: https://api.yfe.app
    description: Production

paths:
  /api/v1/tasks:
    post:
      summary: Create task
      requestBody: [TaskRequest schema]
      responses: [TaskResponse schema]
  
  /api/v1/tasks/{task_id}:
    get: [task status]
  
  /api/v1/tasks/{task_id}/stream:
    get: [WebSocket upgrade]
  
  /health:
    get: [health check]

components:
  schemas:
    TaskRequest: [from schemas/api/tasks.py]
    TaskResponse: [from schemas/api/tasks.py]
    ProblemDetail: [from schemas/api/problem_detail.py]
```

---

### Phase B: Add CI Validation (30min)

**Install**: `openapi-spec-validator` or similar

**CI Step** (`.github/workflows/`):
```yaml
- name: Validate OpenAPI Spec
  run: |
    pip install openapi-spec-validator
    openapi-spec-validator openapi/yfe-api-v1.yaml
```

---

### Phase C: Documentation (30min)

**Update**:
1. `README.md`: Link to OpenAPI spec
2. PR template: "Did you update openapi/ if API changed?"
3. `GOLDEN_RULES.md`: Note Tier 2 rule now enforced

---

## Success Criteria

✅ **File Created**: `openapi/yfe-api-v1.yaml`  
✅ **Valid**: Passes OpenAPI validator  
✅ **Complete**: All 4 routes documented  
✅ **CI**: Validation in pipeline  
✅ **Docs**: README + PR template updated

---

## Next Task

After completion → **TASK-P2-003-LOGGING**
