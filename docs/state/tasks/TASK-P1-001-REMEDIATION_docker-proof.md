# TASK-P1-001-REMEDIATION: Docker Execution Proof

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL / BLOCKING**  
**Date**: 2025-11-22  
**Blocks**: All Phase 1 work  
**Original Task**: TASK-P1-001_production-toggle-foundation  
**Rejection Reason**: Code not verified in Docker, container crashes, no execution proof

---

## Rejection Summary

**TASK-P1-001 REJECTED** for violating "Production from Line 1" principle.

**Evidence of Failure:**
- Docker container crashes: `ImportError: no pq wrapper available` (psycopg missing libpq)
- Developer tested locally (uvicorn/npm) instead of Docker
- No screenshots of Docker execution
- Frontend Next.js config broken (returns 404 instead of Owner Console)
- No proof system actually works end-to-end in production environment

**Your code files are correct, but execution environment is broken.**

---

## Mandatory Fixes

### Fix 1: Dockerfile Missing PostgreSQL Library

**File**: `apps/agent-runtime/Dockerfile`  
**Line**: 6-9  

**Current (BROKEN)**:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

**Required Fix**:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

**Why**: `psycopg` (imported by `langgraph.checkpoint.postgres`) requires `libpq-dev` to compile binary drivers. Without it, container crashes on startup.

---

### Fix 2: Frontend Docker Configuration

**Current State**: No Dockerfile for `apps/web`  
**Docker Compose**: Not configured for frontend

**Required**:

1. **Create** `apps/web/Dockerfile`:
```dockerfile
FROM node:22-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build Next.js
RUN npm run build

EXPOSE 3000

# Run Next.js in production mode
CMD ["npm", "start"]
```

2. **Update** `docker-compose.yml` to add frontend service:
```yaml
  owner-console:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8002
    depends_on:
      - agent-runtime
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 3s
      retries: 3
```

---

### Fix 3: Execution Proof Requirements

**You MUST provide proof the system works in Docker:**

1. **Start services**:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

2. **Wait for healthy status**:
   ```bash
   docker ps
   # Verify all 3 containers show "healthy" status
   ```

3. **Test backend**:
   ```bash
   curl http://localhost:8002/health
   curl -X POST http://localhost:8002/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"task": "test"}'
   ```

4. **Open browser to frontend**:
   - Navigate to `http://localhost:3000`
   - **SCREENSHOT 1**: Homepage showing Owner Console UI
   - Submit task: "Create a hello world function in Python"
   - **SCREENSHOT 2**: Task submitted, showing task ID
   - Wait 10 seconds for WebSocket events
   - **SCREENSHOT 3**: Live Build Story showing at least 3 events
   - **SCREENSHOT 4**: Browser DevTools console (must show zero errors)

5. **Verify Docker logs**:
   ```bash
   docker logs yfe-agent-runtime | grep -i "llm\|openai\|anthropic"
   # SCREENSHOT 5: Logs showing real LLM API calls
   ```

6. **Container health**:
   ```bash
   docker ps
   # SCREENSHOT 6: All 3 containers healthy
   ```

---

## Verification Requirements

### V1: Docker Build Success

```bash
docker-compose build 2>&1 | tee build.log
```

**Must show**:
- ✅ Backend image built successfully
- ✅ Frontend image built successfully
- ✅ No errors in build.log

---

### V2: Container Health

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**Must show**:
- ✅ `yfe-postgres` - Up, healthy
- ✅ `yfe-agent-runtime` - Up, healthy
- ✅ `yfe-owner-console` - Up, healthy

---

### V3: Backend Functional

```bash
# Health check
curl http://localhost:8002/health

# Task creation
TASK_ID=$(curl -s -X POST http://localhost:8002/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "test"}' | jq -r '.task_id')

echo "Task ID: $TASK_ID"

# Task retrieval
curl http://localhost:8002/api/tasks/$TASK_ID
```

**Must show**:
- ✅ Health returns `{"status":"ok",...}`
- ✅ POST /tasks returns task_id
- ✅ GET /tasks/{id} returns state

---

### V4: Frontend Functional

**Manual browser test** (screenshots required):
1. Open http://localhost:3000
2. Verify Owner Console UI loads (not 404)
3. Submit task
4. Verify WebSocket connects and events stream
5. Verify no console errors

---

### V5: Real LLM Calls

```bash
docker logs yfe-agent-runtime 2>&1 | grep -E "openai|anthropic|gpt|claude"
```

**Must show**: Evidence of actual LLM API calls (not mocks)

---

## Documentation Requirements

### D1: Session Log Update

**File**: `docs/state/SESSIONS/2025-11-22_dev_p1001-remediation.md`

```markdown
# Session Log: TASK-P1-001 Remediation - Docker Execution Proof

## Rejection Root Cause

1. **Docker Build Failure**: Missing `libpq-dev` in Dockerfile
   - Error: `ImportError: no pq wrapper available`
   - Fix: Added `libpq-dev` to apt-get install

2. **No Frontend Docker**: apps/web not containerized
   - Created Dockerfile
   - Added to docker-compose.yml

3. **No Execution Proof**: Tested locally, not in Docker
   - Violated "Production from Line 1" principle

## Fixes Applied

### Fix 1: Backend Dockerfile
- File: apps/agent-runtime/Dockerfile
- Line 7: Added `libpq-dev \`
- Result: Container builds and starts successfully

### Fix 2: Frontend Dockerfile
- File: apps/web/Dockerfile (NEW)
- Build: Multi-stage with npm ci + npm build
- Expose: Port 3000

### Fix 3: Docker Compose
- File: docker-compose.yml
- Added: owner-console service
- Depends: agent-runtime (ensures backend starts first)

## Verification Results

### Docker Build
[paste docker-compose build output showing success]

### Container Health
[paste docker ps output showing all healthy]

### Backend API Test
[paste curl outputs for health + POST /tasks + GET /tasks/{id}]

### Frontend Browser Test
[embed screenshots 1-4 showing UI working]

### LLM Call Proof
[paste docker logs showing real API calls]

## Conclusion
System now fully functional in Docker. All containers healthy. End-to-end flow verified.
```

---

### D2: Evidence Screenshots

Save to `evidence/G10/p1001-remediation/`:
- `01-homepage.png` - Owner Console UI loaded
- `02-task-submitted.png` - Task ID displayed
- `03-events-streaming.png` - Live Build Story with events
- `04-browser-console.png` - DevTools showing zero errors
- `05-docker-logs.png` - LLM API calls in logs
- `06-containers-healthy.png` - All containers up and healthy

---

### D3: Update State Files

**BLOCKERS.md** - Remove this entry after successful remediation

**PROGRESS.md** - Add:
```markdown
- **2025-11-22** – Developer – Remediated TASK-P1-001: Fixed Docker configuration (added libpq-dev), containerized frontend, verified end-to-end in Docker. All services healthy, Owner Console working.
```

---

## Success Criteria

You are DONE when:

### Docker Verification
- [ ] `docker-compose build` completes with zero errors
- [ ] `docker-compose up -d` starts all 3 containers
- [ ] All containers show "healthy" status
- [ ] No container crashes or restarts

### Backend Verification
- [ ] `curl http://localhost:8002/health` returns 200 OK
- [ ] Can POST task and receive task_id
- [ ] Can GET task state from database
- [ ] Docker logs show real LLM API calls (grep for openai/anthropic)

### Frontend Verification
- [ ] http://localhost:3000 loads Owner Console (not 404)
- [ ] Can submit task via UI
- [ ] WebSocket connects and streams events
- [ ] Browser console shows zero errors
- [ ] **6 screenshots** captured and saved to evidence/

### Documentation
- [ ] Session log created with all fixes documented
- [ ] Evidence screenshots in evidence/G10/
- [ ] PROGRESS.md updated
- [ ] Git commit with message: "fix(p1001): remediate Docker execution proof"

---

## CEO Review Checklist

When you resubmit, I will verify:

### I Will Run These Commands
```bash
# Clean slate
docker-compose down
docker system prune -f

# Build fresh
docker-compose build

# Start
docker-compose up -d

# Wait 30 seconds for startup
sleep 30

# Verify health
docker ps
curl http://localhost:8002/health
curl -X POST http://localhost:8002/api/tasks -H "Content-Type: application/json" -d '{"task": "test"}'
docker logs yfe-agent-runtime | grep -i "openai\|anthropic"
```

### I Will Open Browser
- Navigate to http://localhost:3000
- Verify Owner Console loads
- Submit test task
- Verify events stream
- Check console for errors

### I Will Verify Evidence
- [ ] 6 screenshots exist in evidence/G10/
- [ ] Docker logs show real LLM calls (not mocks)
- [ ] Session log documents all fixes
- [ ] Container health confirms all 3 services running

**If ANY check fails, task will be REJECTED again.**

---

## Critical Reminders

1. **DOCKER ONLY**
   - Do NOT test with local `uvicorn` or `npm run dev`
   - ONLY test with `docker-compose up -d`
   - Production from Line 1 = Docker from Line 1

2. **SCREENSHOTS REQUIRED**
   - No screenshots = automatic rejection
   - Must show actual browser UI, not mockups
   - Must show browser console with zero errors

3. **REAL LLM CALLS**
   - Docker logs must prove real API calls
   - Check for environment variables in container:
     ```bash
     docker exec yfe-agent-runtime env | grep API_KEY
     ```

4. **ALL 3 CONTAINERS MUST BE HEALTHY**
   - Postgres
   - Agent Runtime
   - Owner Console (frontend)

---

## Timeline

**Start**: Immediately  
**Expected Duration**: 2-4 hours  
**Deadline**: End of work session

---

## Questions?

**If docker-compose build fails:**
- Share full build output in session log
- Check Dockerfile syntax
- Verify all COPY paths are correct

**If container crashes:**
- Check logs: `docker logs yfe-agent-runtime`
- Verify environment variables in docker-compose.yml
- Ensure database is healthy first

**If frontend shows 404:**
- Check Next.js build output in Docker logs
- Verify src/app/page.tsx exists in container: `docker exec yfe-owner-console ls -la /app/src/app/`
- Check .dockerignore isn't excluding source files

**NO EXCUSES. Docker must work. Period.**
