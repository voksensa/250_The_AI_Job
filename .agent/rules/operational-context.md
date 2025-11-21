---
trigger: always_on
---

# Operational Context: Navigation Guide

**Version**: 2.0 (Aligned with VISION.md)  
**Date**: 2025-11-20  
**Purpose**: Quick reference for navigating the project

---

## Start Here

**New to the project? Read in this order:**

1. **VISION.md** (2-3 min) - What we're building
2. **STRATEGY.md** (5-7 min) - How we win
3. **ROADMAP.md** (3-5 min) - What ships when
4. **This document** - Where everything is

Total: ~15 minutes to get oriented.

---

## Document Hierarchy

```
VISION.md               ← North Star (what & why)
    ↓
STRATEGY.md             ← Business model & competitive edge
    ↓
ROADMAP.md              ← Execution timeline
    ↓
CLAUDE.md               ← CEO quality gates
AGENTS.md               ← Developer guide
OPERATIONAL_CONTEXT.md  ← This file (navigation)
```

---

## Directory Structure

```
/Users/Yousef_1/Downloads/UMCA_Coding_System-main/
│
├── VISION.md                    # North Star (read first)
├── STRATEGY.md                  # Business & tech details
├── CLAUDE.md                    # CEO governance
├── AGENTS.md                    # Developer guide
├── OPERATIONAL_CONTEXT.md       # This file
│
├── docs/
│   ├── ROADMAP.md               # Execution timeline
│   ├── research/                # Research reports
│   │   ├── AUTONOMOUS_CODING_FUTURE_2026.md
│   │   └── AUTONOMOUS_SYSTEM_SUMMARY.md
│   └── complete_blueprint.md    # Technical blueprint
│
├── apps/
│   └── owner-console/           # Frontend (Next.js)
│       ├── src/
│       │   ├── app/            # Pages
│       │   └── components/      # React components
│       └── package.json
│
├── services/
│   └── data-plane/
│       └── agent-runtime/       # Backend (Python)
│           ├── src/
│           │   ├── engine/      # LangGraph workflows
│           │   ├── tools/       # Sandbox, Docker
│           │   └── api/         # FastAPI routes
│           └── pyproject.toml
│
├── sandboxes/                   # Generated code storage
│   └── phase2/                  # Current sandbox
│
├── docker-compose.yml           # All services
└── archive/                     # Old/legacy docs
```

---

## Key Files

### Governance
- `VISION.md` - What we're building (read this first!)
- `STRATEGY.md` - How we win (business model, pricing, tech)
- `CLAUDE.md` - CEO quality gates (G1-G11)
- `AGENTS.md` - Developer guide (code standards, patterns)

### Planning
- `docs/ROADMAP.md` - Timeline & phases
- `docs/research/AUTONOMOUS_CODING_FUTURE_2026.md` - Market research
- `docs/research/AUTONOMOUS_SYSTEM_SUMMARY.md` - Simple summary

### Code
- `services/data-plane/agent-runtime/src/engine/graph.py` - LangGraph workflows
- `services/data-plane/agent-runtime/src/tools/docker_sandbox.py` - Docker execution
- `apps/owner-console/src/app/page.tsx` - Main UI

---

## Technology Stack

### Backend (`services/data-plane/agent-runtime/`)
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Orchestration**: LangGraph
- **LLMs**: GPT-4, Claude 4.5
- **Database**: PostgreSQL
- **Testing**: Pytest
- **Port**: 8002

### Frontend (`apps/owner-console/`)
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Testing**: Playwright
- **Port**: 3030

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Sandboxes**: `/sandboxes/phase2/`
- **Generated Apps**: Dynamic ports (9000+)

---

## Service Ports

| Service | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------|
| owner-console | 3000 | 3030 | Frontend UI |
| agent-runtime | 8002 | 8002 | Backend API |
| Generated apps | 5000 | 9000+ | Dynamic Docker apps |

**Avoid ports**: 3000, 8000, 8001 (conflicts with other projects)

---

## Common Commands

### Start All Services
```bash
cd /Users/Yousef_1/Downloads/UMCA_Coding_System-main
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f agent-runtime
docker-compose logs -f owner-console
```

### Run Tests
```bash
# Backend
cd services/data-plane/agent-runtime
pytest

# Frontend
cd apps/owner-console
npm test
```

### Quality Gates
```bash
# Lint
flake8 services/data-plane/agent-runtime/src/
npm run lint --prefix apps/owner-console

# Type check
mypy services/data-plane/agent-runtime/src/
npm run type-check --prefix apps/owner-console
```

---

## Environment Variables

### Required
```bash
OPENAI_API_KEY=sk-...        # OpenAI API key
OPENAI_MODEL=gpt-4           # Model to use
POSTGRES_URL=postgresql://... # Database connection
```

### Optional
```bash
ANTHROPIC_API_KEY=sk-...     # For Claude
LOG_LEVEL=INFO               # Logging verbosity
```

**Location**: `.env` (create from `.env.example`)

---

## Workflow for Developers

### 1. Read Documentation
- VISION.md → STRATEGY.md → ROADMAP.md → AGENTS.md

### 2. Pick a Task
- Check ROADMAP.md for current phase
- Tasks defined in developer instructions

### 3. Implement
- Phase A (Backend) + Phase B (Frontend) together
- Follow AGENTS.md code standards
- Write tests as you go

### 4. Validate
- Run quality gates (G1-G11)
- Test Owner workflow
- Create evidence package

### 5. Submit
- CEO reviews (CLAUDE.md)
- Owner approves

---

## The 3 Killer Features (Current Focus)

### 1. Production Toggle
**Goal**: Simple switch for prototype vs production quality  
**Status**: Planning (Phase 3)  
**Files**:
- Backend workflow: `services/data-plane/agent-runtime/src/engine/graph.py`
- Frontend toggle: `apps/owner-console/src/app/page.tsx`

### 2. AI Test Users
**Goal**: Synthetic users test apps before real people  
**Status**: Planning (Phase 4)  
**Files**:
- QA agent: `services/data-plane/agent-runtime/src/tools/synthetic_qa.py` (TBD)
- UI results: `apps/owner-console/src/components/TestResults.tsx` (TBD)

### 3. Build Story
**Goal**: Timeline showing what AI did in plain English  
**Status**: Planning (Phase 5)  
**Files**:
- Event tracking: In all agent nodes
- Timeline UI: `apps/owner-console/src/components/Timeline.tsx` (TBD)

---

## Troubleshooting

### Services won't start
```bash
# Check ports
lsof -i :3030
lsof -i :8002

# Rebuild
docker-compose down
docker-compose build
docker-compose up -d
```

### Frontend not connecting to backend
- Check `http://localhost:8002/health`
- Verify CORS settings in FastAPI
- Check network in Chrome DevTools

### Docker execution fails
- Check Docker daemon running: `docker ps`
- Check socket mount in docker-compose.yml
- Check sandbox permissions: `ls -la sandboxes/`

### LLM API errors
- Verify API keys in `.env`
- Check quota/billing
- Test with `curl` to OpenAI/Anthropic API

---

## Quick Reference

### URLs
- **Frontend**: http://localhost:3030
- **Backend API**: http://localhost:8002
- **API Health**: http://localhost:8002/health
- **API Docs**: http://localhost:8002/docs

### Key Paths
- **Sandboxes**: `/sandboxes/phase2/`
- **Backend code**: `/services/data-plane/agent-runtime/src/`
- **Frontend code**: `/apps/owner-console/src/`
- **Research**: `/docs/research/`

### Important Commands
- Start: `docker-compose up -d`
- Stop: `docker-compose down`
- Logs: `docker-compose logs -f`
- Rebuild: `docker-compose build`

---

## Need Help?

1. **Read VISION.md** - Understand what we're building
2. **Check AGENTS.md** - Code standards and patterns
3. **Read CLAUDE.md** - Quality requirements
4. **Review ROADMAP.md** - Current priorities
5. **Escalate to Owner** - If still unclear

---

**Last Updated**: 2025-11-20  
**Remember: Everything flows from VISION.md**
