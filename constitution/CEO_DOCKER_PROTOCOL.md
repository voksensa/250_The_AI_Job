# CEO Constitutional Amendment: Docker-Only Verification

**Date**: 2025-11-22  
**Trigger**: TASK-P1-001 rejection - Developer tested locally, not in Docker  
**Authority**: CEO quality gate enforcement  
**Status**: ✅ RATIFIED

---

## The Lesson

**TASK-P1-001 was REJECTED despite:**
- ✅ Code looking correct in review
- ✅ TypeScript types proper
- ✅ MCP patterns cited
- ✅ No linting errors
- ✅ Session logs created

**But it FAILED because:**
- ❌ Docker container crashed (missing libpq-dev)
- ❌ Developer only tested locally (uvicorn + npm)
- ❌ No Docker execution proof provided
- ❌ Frontend returned 404 in actual runtime
- ❌ CEO almost approved based on "code looks good"

**ROOT CAUSE**: CEO was about to approve without verifying **Docker execution**.

---

## The Amendment

**"Production from Line 1" = "Docker from Line 1"**

### What Changed

**BEFORE (WRONG)**:
- Developer could test locally and claim it works
- "Code looks good" review was acceptable
- Docker was optional for development
- CEO could approve based on code review alone

**AFTER (CORRECT  )**:
- **All testing MUST use `docker-compose up -d`**
- **"Code looks good" without Docker proof = worthless**
- **Docker is mandatory from first line of code**
- **CEO MUST verify by running docker-compose before approval**

---

## Files Modified

### 1. CLAUDE.md (CEO Quality Gates)

**Changes:**
- Line 83-95: "Production from Line 1" → "Production from Line 1 = Docker from Line 1"
  - Added: "Local execution testing (uvicorn, npm run dev)" to FORBIDDEN list
  - Added: Enforcement protocol requiring Docker proof
  
- Line 96-132: "Evidence-Based Approval" → Added mandatory Docker verification
  - CEO MUST run `docker-compose build && up -d` before approval
  - Added 5 required Docker proof artifacts (build log, ps output, screenshots, logs, console)
  
- Line 175-180: Evidence checklist → Added "DOCKER EXECUTION PROOF (MANDATORY)" section
  - 5 checkboxes for Docker artifacts

**Why**: CEO must never approve without seeing Docker execution.

---

### 2. AGENTS.md (Developer Guide)

**Changes:**
- Line 24-30: "Production from Line 1" → Added "Docker from Line 1" clarification
  - Added testing protocol showing CORRECT (docker-compose) vs WRONG (local)
  - Explicitly marked `uvicorn` and `npm run dev` as FORBIDDEN

**Why**: Developer must never test locally, only in Docker.

---

### 3. NEW: CEO_DOCKER_PROTOCOL.md (This File)

**Purpose**: Document the constitutional amendment and rationale permanently.

**Why**: Future CEOs must understand why Docker-only verification is non-negotiable.

---

## Verification Protocol (CEO Checklist)

For **EVERY** task submission, CEO MUST:

### Step 1: Verify Docker Proof Submitted
- [ ] `docker-compose build` log provided
- [ ] `docker ps` output showing healthy containers
- [ ] Screenshots of browser UI working
- [ ] `docker logs` proving real LLM calls
- [ ] Browser console screenshot (zero errors)

**If ANY missing → REJECT immediately, no code review needed**

### Step 2: Reproduce Docker Execution
```bash
cd /path/to/project

# Clean slate
docker-compose down
docker system prune -f

# Build fresh
docker-compose build

# Start
docker-compose up -d

# Wait for healthy
sleep 30
docker ps

# Test backend
curl http://localhost:8002/health
curl -X POST http://localhost:8002/api/tasks -H "Content-Type: application/json" -d '{"task": "test"}'

# Check logs for real LLM
docker logs yfe-agent-runtime | grep -i "openai\|anthropic"
```

**If ANY command fails → REJECT**

### Step 3: Verify Frontend in Browser
- [ ] Navigate to http://localhost:3000
- [ ] UI loads (not 404, not blank)
- [ ] Can interact with UI
- [ ] Browser console shows zero errors

**If ANY check fails → REJECT**

### Step 4: Only Then Review Code

**After** Docker execution verified, review:
- Code quality
- MCP patterns
- Type safety
- Documentation

**But Docker proof is gate #1. Without it, code review is meaningless.**

---

## Rationale: Why This Matters

**The Trap:**
- Code can look perfect in review
- Types can be correct
- Linting can pass
- MCP patterns can be cited
- **But it doesn't matter if Docker crashes**

**Real-World Evidence (TASK-P1-001):**
- Missing `libpq-dev` in Dockerfile → Container crash
- Next.js config issue → 404 instead of UI
- Only found when actually running `docker-compose up`
- Would have shipped broken code if CEO approved based on code review

**The Principle:**
> "Show me it running in Docker, or it doesn't exist."

---

## Enforcement

**Developer violations:**
- Testing locally instead of Docker → REJECTED
- No Docker proof provided → REJECTED
- Claiming "it works locally" → REJECTED

**CEO violations:**
- Approving without running docker-compose → Invalid approval
- Accepting "code looks good" without Docker → Invalid approval
- Skipping Docker verification → Must self-correct and verify

**No exceptions. No shortcuts. Docker proof or rejection.**

---

## Success Metrics

**Before Amendment:**
- CEO almost approved TASK-P1-001 based on code review
- Would have shipped broken Docker configuration
- Would have violated "Production from Line 1"

**After Amendment:**
- CEO MUST verify Docker before approval
- Broken Docker = immediate rejection
- No path to approval without execution proof

**Measurement:**
- Track: How many tasks rejected for missing Docker proof
- Target: Zero tasks approved without Docker verification
- Review: If any task ships broken, check if Docker protocol was followed

---

## Historical Context

**Date**: 2025-11-22  
**Task**: TASK-P1-001 (Production Toggle Foundation)  
**Incident**: CEO was about to approve task based on code quality alone  
**Discovery**: User challenged: "Did you actually run it in Docker?"  
**Result**: Docker container crashed, frontend broken, no execution proof  
**Lesson**: "Never trust without Docker proof"  

**This amendment ensures this never happens again.**

---

## References

- Original rejection: TASK-P1-001-REMEDIATION_docker-proof.md
- Constitutional authority: CLAUDE.md (CEO mandate)
- Developer protocol: AGENTS.md (implementation guide)
- Vision alignment: VISION.md (Production Toggle requires production execution)

---

**Ratified**: 2025-11-22  
**Effective**: Immediately  
**Review**: After Phase 1 completion  
**Status**: ✅ PERMANENT CONSTITUTIONAL LAW
