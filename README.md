# Your First Engineer

> **Tell us your idea. We give you a real, working app.**

The first product that turns plain-language ideas into production-ready applications.

## 🎯 The 3 Killer Features

1. **Production Toggle** - Simple switch for prototype vs production quality
2. **AI Test Users** - Synthetic QA crowd tests apps before real users
3. **Build Story** - Explainable timeline of what the AI did

## 🏗️ Project Structure

```
your-first-engineer/
├── apps/
│   ├── web/                    # Owner Console (Next.js 16)
│   ├── agent-runtime/          # LangGraph Agent (Python 3.12)
│   ├── agent-api/              # API Gateway (FastAPI)
│   └── sandbox-manager/        # Execution Environment Manager
├── packages/
│   ├── ui/                     # Shared UI Components (@yfe/ui)
│   ├── config/                 # Shared Configuration
│   ├── contracts/              # API Contracts (TypeScript)
│   └── monitoring/             # Observability Utilities
├── python_packages/
│   ├── yfe_langgraph/          # LangGraph Implementation
│   ├── yfe_domain/             # Domain Models
│   └── yfe_adapters/           # External Service Adapters
├── infra/
│   ├── k8s/                    # Kubernetes Manifests
│   └── terraform/              # Infrastructure as Code
└── constitution/               # Project Documentation
```

## 📚 Documentation

### Read First
1. **[VISION.md](./VISION.md)** - The North Star
2. **[STRATEGY.md](./STRATEGY.md)** - How we win
3. **[COMPLETE_ARCHITECTURE_SPEC.md](./docs/research/COMPLETE_ARCHITECTURE_SPEC.md)** - Technical Blueprint

### For Developers
- **[AGENTS.md](./AGENTS.md)** - Developer Guide & Patterns
- **[CLAUDE.md](./CLAUDE.md)** - Quality Gates (G1-G11)
- **[OPERATIONAL_CONTEXT.md](./OPERATIONAL_CONTEXT.md)** - Navigation Map

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 20.9.0+ LTS
- **Python**: 3.12.x
- **Docker**: Latest stable

### Local Development

```bash
# 1. Install dependencies
npm install

# 2. Start infrastructure (Postgres + pgvector)
docker-compose up -d postgres

# 3. Start all services (Turborepo)
npm run dev
```

**Services:**
- Owner Console: http://localhost:3030
- Agent Runtime: http://localhost:8002
- Postgres: localhost:5432

### Manual Service Startup

```bash
# Frontend (Next.js 16)
cd apps/web
npm run dev

# Backend (Python 3.12 + LangGraph)
cd apps/agent-runtime
uvicorn agent_runtime.main:app --reload --port 8002
```

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 16.0.x (App Router)
- **UI**: React 19.x + Tailwind CSS 4.0+
- **Components**: shadcn/ui (@yfe/ui shared package)
- **Language**: TypeScript (strict mode)

### Backend
- **Runtime**: Python 3.12.x
- **Framework**: FastAPI
- **Orchestration**: LangGraph 1.0.3 (Native StateGraph)
- **Database**: PostgreSQL 16 + pgvector
- **Persistence**: `langgraph-checkpoint-postgres`

### Infrastructure
- **Monorepo**: Turborepo
- **Containers**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)

## 📋 Core Principles

1. **Production from Line 1** - No stubs, no mocks, no TODOs
2. **Phase A + Phase B Together** - Backend + Frontend in every deliverable
3. **Non-Technical Owner First** - Validate features in ≤20 min via browser
4. **Quality Gates (G1-G11)** - All gates must pass before Owner review

## 🔒 Security & Compliance

- **OWASP ASVS 5.0** (Level 2/3)
- **OWASP LLM Top 10** (2025)
- **NIST CSF 2.0** (Identify, Protect, Detect)
- **NIST SSDF** (SP 800-218)
- **ISO/IEC 42001** (AI Management System)
- **EU AI Act** (High-Risk AI System)

## 🧪 Testing

```bash
# Frontend (Playwright)
cd apps/web
npm run test

# Backend (Pytest)
cd apps/agent-runtime
pytest

# All tests
npm run test
```

## 📦 Building

```bash
# Build all packages
npm run build

# Build specific app
cd apps/web
npm run build
```

## 🌍 Environment Variables

Create `.env.local` files in each app directory:

**apps/web/.env.local:**
```
NEXT_PUBLIC_API_URL=http://localhost:8002
```

**apps/agent-runtime/.env:**
```
DATABASE_URL=postgresql://yfe:yfe_dev_pass@localhost:5432/yfe_db
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## 📖 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Next.js 16 Documentation](https://nextjs.org/docs)
- [Tailwind CSS 4.0 Documentation](https://tailwindcss.com/docs)

## 🤝 Contributing

This is the **250th attempt** at building this software. Every line of code matters.

Before contributing:
1. Read [VISION.md](./VISION.md)
2. Review [CLAUDE.md](./CLAUDE.md) for quality gates
3. Follow [AGENTS.md](./AGENTS.md) for patterns

**All contributions must pass G1-G11 gates.**

## 📝 License

Proprietary - All Rights Reserved

---

**Built with conviction. Attempt #250.**
