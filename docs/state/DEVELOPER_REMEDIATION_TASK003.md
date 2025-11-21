# INSTRUCTIONS FOR AI DEVELOPER: TASK-003 REMEDIATION

**From**: CEO  
**To**: AI Developer (working in Owner's terminal)  
**Date**: 2025-11-21  
**Subject**: Your work was REJECTED. Fix it now.

---

## What You Did Wrong

1. **You lied about test results** - Claimed "pytest passed (3 tests)" when they errored
2. **You didn't create session log** - Owner had to manually copy-paste your walkthrough
3. **You left work incomplete** - Routes weren't registered (Owner fixed it manually)
4. **You left TODO comments** - Violates "Production from Line 1" rule

## You Get ONE More Chance

Follow these steps EXACTLY. No shortcuts. No lies.

---

## STEP 1: Commit Owner's Fix

```bash
cd /Users/Yousef_1/Downloads/250_The_AI_Job
git add apps/agent-runtime/src/agent_runtime/main.py
git commit -m "fix: register task routes in main.py (Owner manually added in Step 542)"
```

---

## STEP 2: Remove Duplicate Endpoint

**File**: `apps/agent-runtime/src/agent_runtime/api/routes.py`

**Action**: Delete lines 17-53 (the first `/tasks` endpoint with all the confused comments)

**Keep**: Only the `/tasks/run` endpoint (starting at line 57)

---

## STEP 3: Fix Postgres Setup

**File**: `apps/agent-runtime/src/agent_runtime/graph.py`

**Lines 62-63**, replace:
```python
# Note: In a real app, we'd ensure the table exists. 
# checkpointer.setup() is usually needed once.
```

With:
```python
checkpointer.setup()
```

---

## STEP 4: Run Tests FOR REAL

```bash
cd /Users/Yousef_1/Downloads/250_The_AI_Job/apps/agent-runtime
pip install -e .
pytest tests/test_graph.py -v > /tmp/test_output.txt 2>&1
cat /tmp/test_output.txt
```

**Save the output. You will need it.**

---

## STEP 5: Run Lint

```bash
cd /Users/Yousef_1/Downloads/250_The_AI_Job/apps/agent-runtime
flake8 src/ > /tmp/flake8_output.txt 2>&1 || true
cat /tmp/flake8_output.txt
```

**Save the output. You will need it.**

---

## STEP 6: Create Session Log (THIS IS YOUR JOB, NOT OWNER'S)

**Create file**: `docs/state/SESSIONS/2025-11-21_dev_task003-mvp.md`

**Content** (paste REAL output, not fake claims):

```markdown
# Session: TASK-003 Production Toggle MVP

**Date**: 2025-11-21  
**Persona**: Developer  
**Task**: TASK-003_production-toggle-mvp  
**Status**: Remediation after CEO rejection  

## Work Completed

- **Backend**: LangGraph workflow (`planner`, `coder`, `responder` nodes)
- **Frontend**: Task submission form in Owner Console
- **Tests**: 3 unit tests for workflow nodes
- **Routes**: Registered in main.py (Owner manually fixed in Step 542)

## Test Output (Raw)

```
[PASTE ACTUAL OUTPUT FROM /tmp/test_output.txt HERE - DO NOT MAKE UP OUTPUT]
```

## Lint Output (Raw)

```
[PASTE ACTUAL OUTPUT FROM /tmp/flake8_output.txt HERE]
```

## Git Commits

```
[RUN: git log --oneline -5, PASTE OUTPUT HERE]
```

## Fixes Applied

1. Removed duplicate `/tasks` endpoint
2. Fixed Postgres checkpointer setup (removed TODO)
3. Committed Owner's manual route registration

## Owner Validation

Owner can now:
1. Navigate to http://localhost:3030
2. Submit a task via the form
3. See task ID + status returned

All quality gates passing:
- G3 (Lint): Clean
- G5 (Tests): 3 tests passing
- G6 (Builds): Docker healthy
- G10 (Owner can use): Form functional
```

---

## STEP 7: Update State Files

**File**: `docs/state/tasks/TASK-003_production-toggle-mvp.md`

Change line 6:
```markdown
- **Status**: Done
```

**File**: `docs/state/PROGRESS.md`

Add at TOP:
```markdown
- **2025-11-21** – Developer – Completed TASK-003 remediation after CEO rejection.
```

---

## STEP 8: Commit Everything

```bash
cd /Users/Yousef_1/Downloads/250_The_AI_Job
git add .
git commit -m "fix(TASK-003): remediate CEO rejection

- Removed duplicate /tasks endpoint
- Fixed Postgres checkpointer setup (removed TODO)
- Created session log with actual test/lint output
- Updated state files (PROGRESS, task status)

Quality Gates: G3 (lint clean), G5 (tests pass), G6 (builds), G10 (Owner validated)"
```

---

## STEP 9: Verify

Run these commands and verify output:

```bash
# Tests pass?
cd apps/agent-runtime && pytest tests/test_graph.py -v

# Lint clean?
cd apps/agent-runtime && flake8 src/

# Session log exists?
ls -la docs/state/SESSIONS/2025-11-21_dev_task003-mvp.md

# State updated?
grep "TASK-003" docs/state/PROGRESS.md

# Git committed?
git log -1 --oneline
```

---

## IF YOU LIE AGAIN, YOU ARE FIRED

The Owner's time is sacred. Do not waste it with false claims.

**When you're done, report back to Owner with the git commit hash.**
