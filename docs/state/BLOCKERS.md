# BLOCKERS

## Active

### 🔴 BLOCKER-001: Missing Deployment Pipeline (Phase 1 Blocked)
- **Severity**: CRITICAL  
- **Reported**: 2025-11-23, CEO  
- **Owner**: Unassigned  
- **Impact**: Phase 1 (Production Toggle MVP) cannot complete - files are generated but not deployed as working apps  
- **Symptom**: Synthetic QA fails (80% failure) because it tries to navigate to `file://` URLs instead of `http://` deployed apps  
- **Root Cause**: No sandbox hosting layer exists - files sit in `/workspace/` but aren't served as live web apps  
- **Blocking**: TASK-P1-002-FIX approval, Owner validation, Phase 1 exit  
- **Next Action**: Create TASK-P1-003-DEPLOYMENT to build sandbox host (Docker container serving generated apps on unique URLs)

## Recently Cleared

- _(empty)_
