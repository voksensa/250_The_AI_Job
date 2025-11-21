# RESEARCH BRIEF: EXECUTION FRAMEWORK & ROADMAP DEFINITION

**Brief ID**: YFE-EXEC-001  
**Date**: 2025-11-21  
**Assigned To**: Owner's Researcher  
**Escalated By**: CEO  
**Urgency**: CRITICAL - All work blocked until delivered  

---

## Context: Why This Research Is Needed

**Current State**: Project has failed 250+ times due to:
1. **No clear roadmap** - What does each phase deliver?
2. **No execution framework** - How do developers execute with zero ambiguity?
3. **No evidence structure** - Where is proof that quality gates passed?
4. **Guessing instead of researching** - Assumptions instead of November 2025 standards

**Owner Mandate** (verbatim):
> "i need all spelled out in detail. i need the how the what the why. you will provide evidence for EVERY fucking claim, task, code block everything! no guessing, november 2025 standards."

**CEO Failure**: Approved TASK-003 without enforcing evidence requirements. This research prevents future failures.

---

## Research Questions

### RQ1: What Is The Goal?

**Question**: What is "Your First Engineer" trying to achieve, specifically?

**Required Outputs**:
- One-sentence mission statement
- 3 measurable success criteria (e.g., "Non-technical founder can build X in Y minutes")
- Target user persona (decision-maker profile, pain points, alternatives they'd use)
- Competitive positioning vs. existing tools (v0, bolt.new, Replit, Cursor, etc.)

**Evidence Requirements**:
- Market research on autonomous coding tools (November 2025 state-of-the-art)
- User research or interviews (if available)
- Competitive analysis with screenshots/demos
- Citations for all claims

---

### RQ2: What Is The Roadmap? What Does Each Phase Bring?

**Question**: What is delivered in each phase, and why is that the right sequence?

**Required Outputs**:

For **EACH** phase (Phase 0-5 or however many exist):

1. **Phase Name** (e.g., "Phase 1: Production Toggle MVP")
2. **Objective** - What capability does this phase unlock?
3. **Success Criteria** - How do we know it worked?
4. **Deliverables** - Specific features/components built
5. **Dependencies** - What must exist before this phase starts?
6. **Owner Validation** - How does Owner verify it works (≤20 min, browser-only)?
7. **Timeline** - Estimated duration (with justification)
8. **Risk** - What could go wrong, mitigation strategy

**Visual Output**: Mermaid roadmap diagram showing phase dependencies

**Evidence Requirements**:
- Industry benchmarks for similar products (e.g., "Bolt.new shipped MVP in X weeks")
- Technical dependencies (e.g., "LangGraph checkpointing required before parallel execution")
- User validation methods (screenshots, user testing protocols)

---

### RQ3: How Do Developers Execute With Zero Ambiguity?

**Question**: What is the step-by-step protocol for a developer to execute ANY task?

**Required Outputs**:

1. **Developer Execution Protocol Template**
   - Pre-work checklist (read task file, understand gates, etc.)
   - Implementation steps (code, test, lint, commit)
   - Evidence collection (what to capture, where to store)
   - Handoff steps (update state files, create session log)

2. **Evidence Directory Structure**
   - Folder organization (e.g., `evidence/G1/`, `evidence/G5/`)
   - File naming conventions
   - Required contents per gate (e.g., G5 needs `pytest_output.txt` + coverage report)

3. **CEO Quality Gate Checklist**
   - Per-gate verification steps
   - Evidence audit process
   - Approval/rejection criteria

**Format**: Executable templates with placeholders (e.g., `{TASK_ID}`, `{PHASE}`)

**Evidence Requirements**:
- Industry best practices for evidence management (FAANG, open-source projects)
- Quality gate frameworks (e.g., Google's launch checklist, AWS Well-Architected)
- November 2025 standards for code quality (latest ESLint, Flake8, coverage tools)

---

### RQ4: What Are November 2025 Standards?

**Question**: What are current industry standards for each quality gate?

**Required Outputs**:

For **EACH** gate (G1-G11):
- **Standard Definition** (e.g., "Lint clean means 0 errors, 0 warnings per tool X version Y")
- **Tool Versions** (e.g., "ESLint 9.x, Flake8 7.x, Mypy 1.x")
- **Thresholds** (e.g., "Test coverage ≥80% for new code, ≥60% overall")
- **Automation** (CI/CD checks, pre-commit hooks)

**Evidence Requirements**:
- Official documentation for each tool (pinned to November 2025 versions)
- Industry benchmarks (e.g., "FAANG requires X% coverage")
- Stack Overflow/GitHub discussions on current best practices

---

## Constraints

From existing constitution:

1. **VISION.md** - Everything must serve the 3 killer features:
   - Production Toggle
   - AI Test Users
   - Build Story

2. **CLAUDE.md** - Quality gates G1-G11 are non-negotiable

3. **STATE_MANAGEMENT_SPEC.md** - Living documents, persona protocols, handoffs

4. **COMPLETE_ARCHITECTURE_SPEC.md** - LangGraph 1.0.3, Next.js 16, etc.

**New Constraint (Owner Mandate)**:
- NO GUESSING. Every claim requires evidence (citation, screenshot, benchmark, or research).

---

## Success Criteria

This research is successful if:

1. ✅ **Zero Ambiguity Roadmap**
   - Owner can read Phase 1-5 descriptions and know exactly what gets built when
   - Each phase has clear entry/exit criteria
   - Timeline is justified with evidence

2. ✅ **Execution Protocol That Prevents All Past Failures**
   - Developer can execute any task by following checklist (no interpretation needed)
   - CEO can verify any task by auditing evidence (no trust required)
   - Evidence structure is automatable (CI can check completeness)

3. ✅ **November 2025 Compliance**
   - All tool versions pinned to latest stable (as of Nov 2025)
   - All thresholds justified with industry evidence
   - All claims cited with sources

4. ✅ **Owner Can Understand Without Reading Code**
   - Roadmap uses plain English
   - Execution protocol is visual (checklists, diagrams)
   - Evidence is browsable (HTML reports, screenshots, not logs)

---

## Research Methodology

**Recommended Approach**:

1. **Market Research** (RQ1, RQ2)
   - Analyze competitors: v0.dev, bolt.new, Replit Agent, Cursor Composer
   - Extract feature timelines, MVP scopes, user validation methods
   - Document with screenshots, feature matrices

2. **Technical Standards Research** (RQ4)
   - Query official docs for tool versions (ESLint, Flake8, Pytest, etc.)
   - Search "November 2025 best practices" for code quality
   - Extract specific version numbers and configuration recommendations

3. **Process Research** (RQ3)
   - Study FAANG launch checklists (Google, AWS, etc.)
   - Review open-source quality gate frameworks (Kubernetes, Django, etc.)
   - Synthesize into executable templates

4. **Validation**
   - Create sample task using new protocol
   - Execute it end-to-end (mock or real)
   - Verify all evidence requirements are clear and automatable

---

## Deliverables

**Files To Create**:

1. `docs/research/ROADMAP_SPEC.md`
   - Detailed phase breakdown (RQ2)
   - Mermaid roadmap diagram
   - Evidence citations

2. `docs/research/EXECUTION_PROTOCOL_SPEC.md`
   - Developer execution template (RQ3)
   - Evidence directory structure
   - CEO gate checklist

3. `docs/research/NOVEMBER_2025_STANDARDS.md`
   - Tool versions and thresholds (RQ4)
   - Configuration examples
   - Industry benchmarks

4. `evidence/.template/`
   - Folder structure template
   - README per gate explaining requirements
   - Sample files (e.g., empty coverage report)

**Format**: All files must include:
- Executive summary (≤200 words)
- Citations for all claims (URLs, version numbers, dates)
- Examples/templates where applicable
- Mermaid diagrams for visual clarity

---

## Timeline

**Urgency**: CRITICAL

**Estimated Duration**: 4-6 hours (comprehensive research)

**Breakdown**:
- Market research (competitors, roadmaps): 1.5 hours
- Technical standards (tool versions, configs): 1.5 hours
- Process frameworks (execution templates): 1.5 hours
- Synthesis and documentation: 1.5 hours

**Deadline**: Owner decides. Recommend delivering in phases if needed:
- Phase 1 (2 hours): Roadmap + Phase definitions (RQ2) - Unblocks planning
- Phase 2 (2 hours): Execution protocol (RQ3) - Unblocks development
- Phase 3 (2 hours): Standards + Evidence (RQ4) - Completes framework

---

## Handoff To Owner's Researcher

**Researcher**: You have full authority to:
- Search web for November 2025 best practices
- Analyze competitor products (screenshots, demos)
- Extract tool versions from official docs
- Create templates and examples

**Do NOT**:
- Guess or assume
- Use outdated information (pre-2025)
- Make recommendations without evidence
- Skip any research question

**When Complete**: Hand deliverables to CEO for validation, then to Owner for approval.

---

## CEO Commitment

Once this research is delivered:
- I will enforce the execution protocol on ALL tasks
- I will audit evidence before ANY approval
- I will reject work that doesn't meet November 2025 standards
- I will never approve based on trust again

**Owner, approve this research brief or modify as needed.**
