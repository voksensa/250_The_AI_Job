
### User Input

 1. please provide in bulletpoints,from memory, no read files, our operational framework. 2. How we operate, our rules, zero trusts, gates, commands, prodution from line 1, reserach adn discovery are mandatory, always cite evidence direclty from sourece code AND source files/official docs, always use mcp tool docs by langchain to surface offical aptterns, custom are forbidden if native exists, never ever ever ever guess, evidence evidence evidence, all agtes, phase a and b - backend logic immeidate wired to fronted, zero fucking trust paranoiya level shit show, state management, goldfish memory 3. okay, those where what i could remmember, now you take my list rewrte it and include everything i forgot to mention

### Planner Response

## YOUR OPERATIONAL FRAMEWORK (From Memory)

### 1. **Zero Trust Separation of Duties**
- Developer builds → Validator reviews → CEO decides → Owner approves
- No one validates their own work
- No shortcuts, no "trust me", no claims without proof
- Every handoff requires written evidence in repo files

### 2. **Quality Gates (G1-G11)**
- G1: Research (≥3 sources, native-first verification)
- G2: Architecture documented
- G3: Security validated
- G4: Lint/type clean
- G5: Tests ≥85% coverage
- G6: Synthetic QA passed
- G7: Observability (metrics/alerts)
- G8: Privacy validated
- G9: AI risk assessed
- G10: UX/accessibility (Owner browser test, no DevTools errors)
- G11: Operational readiness
- **ALL must pass before approval**

### 3. **Production from Line 1 = Docker from Line 1**
- No stubs, mocks, TODOs, or local-only runs
- Everything runs in `docker-compose`
- Real services, real data paths, real dependencies
- If it doesn't work in Docker, it doesn't exist

### 4. **Evidence-Based Approval = Docker Proof Required**
- Build logs showing `docker-compose build` success
- `docker ps` showing services UP
- `docker logs` excerpts proving functionality
- Browser screenshots of working UI (Owner validation)
- If Docker proof is missing → automatic rejection

### 5. **Research & Discovery Mandatory (Native First)**
- Always search official docs BEFORE coding
- Use MCP tool (`docs-by-langchain`) to verify LangGraph/LangChain patterns
- Custom code FORBIDDEN if native exists
- Must cite source with exact URLs/line numbers
- "I researched X and found Y at [link]" or don't proceed

### 6. **Never Guess - Evidence Only**
- No assumptions, no "probably works", no "should be fine"
- Direct quotes from source code or official docs
- Coverage numbers from actual test runs
- Logs from actual Docker execution
- Screenshots from actual browser tests

### 7. **Phase A + B Together (Backend + Frontend Simultaneously)**
- Every task delivers BOTH backend logic AND frontend UI
- Owner must see and use the feature in browser
- No backend-only deliverables
- No "we'll wire UI later" promises

### 8. **85% Coverage Minimum (Golden Rule 1)**
- Every changed file must hit ≥85% line coverage
- Report actual % in evidence/G5/
- No waivers without explicit Owner approval
- CI must verify automatically

### 9. **State Management (Goldfish Memory)**
- Assume zero context retention between sessions
- Every pass reads: INDEX → CURRENT_TASK → PROGRESS → BLOCKERS
- Update state files after every change
- Task files in `docs/state/tasks/TASK-{ID}.md`
- Evidence in `evidence/G{N}/TASK-{ID}_*`

### 10. **Diamond Rule (Rule 0) - Push Back on Bad Instructions**
- If instruction breaks rules → STOP
- Say: "This breaks GOLDEN RULES: {rule}"
- Explain risk in one sentence
- Offer safer alternative
- Wait for: "I accept the risk; proceed"

---

## COMPLETE FRAMEWORK (Your List + What You Forgot)

### **Constitutional Hierarchy**
1. [GOLDEN_RULES.md](cci:7://file:///Users/Yousef_1/Downloads/250_The_AI_Job/constitution/GOLDEN_RULES.md:0:0-0:0) (law)
2. `ARCHITECTURAL_DECISIONS.md` (enforced patterns)
3. `PROCESS.md` (task workflow)
4. Role manuals ([AGENTS.md](cci:7://file:///Users/Yousef_1/Downloads/250_The_AI_Job/AGENTS.md:0:0-0:0), `VALIDATOR.md`, [CLAUDE.md](cci:7://file:///Users/Yousef_1/Downloads/250_The_AI_Job/CLAUDE.md:0:0-0:0))
5. `NOVEMBER_2025_STANDARDS.md` (tool versions)

### **Architectural Patterns (ARCHITECTURAL_DECISIONS.md)**
- API routes: `/api/v1/` only
- Errors: RFC 9457 ProblemDetail format
- LangGraph state: Additive only (never delete fields)
- Layout: `/src` with clear boundaries
- Naming: `snake_case` everywhere (Python + TypeScript)
- Imports: Absolute only (no `../..`)
- Coverage: Per-file ≥85%, project baseline ≥60%

### **Modular Monolith (Golden Rule 4)**
- Single deployable with separated domains
- Clear module boundaries (agent-runtime, owner-console, sandbox)
- Crossing boundaries without interface = violation
- No Big-Bang refactors (Golden Rule 3)

### **Validator Role**
- Zero-trust gatekeeper
- Writes `docs/state/reports/VALIDATION_TASK-{ID}.md`
- Checks: Golden Rules, Architectural Decisions, Gates, Docker proof
- Verdict: VALIDATED / REJECTED / CONDITIONAL
- Never edits production code
- Never talks directly to Dev/CEO

### **CEO Role**
- Reads Validator report (not raw code)
- Confirms phase alignment
- Checks diamond risks
- Uses mandatory format:
  1. Phase Context
  2. Golden Rules Check
  3. Evidence Review (from Validator)
  4. Decision (APPROVED/REJECTED/ESCALATE)
- Cannot approve work (only Owner can)

### **Developer Role**
- Builds backend + frontend together
- ≥85% coverage on all changes
- Gathers evidence for all gates
- Updates state spine (INDEX, CURRENT_TASK, PROGRESS, BLOCKERS)
- Stops after pass → "ready for validation"
- Never self-validates

### **Owner Role**
- Final authority on everything
- Manually tests in browser (zero DevTools errors)
- Approves/rejects based on evidence
- Can override any rule (but must say so explicitly)

### **Vision Alignment**
- Every decision serves 3 pillars:
  1. Production Toggle
  2. AI Test Users
  3. Build Story
- If not → escalate to Owner

### **Boot Protocols**
- **Developer**: Read VISION → ROADMAP → GOLDEN_RULES → ARCH_DECISIONS → PROCESS → task file → send 1 sentence → wait for YES
- **Validator**: Read Validator manual → task file → evidence → gates → write report
- **CEO**: Read CLAUDE.md → VISION → GOLDEN_RULES → Validator report → write decision

### **Task Workflow (PROCESS.md)**
1. Pre-Work: branch, update state, list gates
2. Implementation: code + tests + evidence in parallel
3. Handoff: update PROGRESS, signal "ready for validation"
4. Validation: Validator writes report
5. CEO Decision: reads report, writes verdict
6. Owner Approval: tests in browser, final YES/NO

### **Evidence Structure**
- `evidence/.template/G{N}/README.md` = gate checklist
- `evidence/G{N}/TASK-{ID}_*` = actual artifacts
- Required: lint output, test coverage, Docker logs, screenshots

### **Diamond Risks (Typical)**
- "Skip tests" → burn quality
- "Rewrite everything" → burn time
- "Ship with mocks" → burn production readiness
- "Custom stack" → burn maintainability
- Must offer Option A (safe) vs Option B (risky)

---

**THIS IS THE COMPLETE OPERATIONAL FRAMEWORK. EVERY PASS MUST FOLLOW THIS.**