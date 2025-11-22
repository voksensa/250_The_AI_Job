# GOLDEN RULES

**Last Updated**: 2025-11-22  
**Status**: ACTIVE - Enforced for all new code  
**Adopted From**: RB-003 (Tier 1 Immediate Enforcement)

---

## Purpose

These are **non-negotiable practices** that prevent "using diamonds as shovels" - AI developers must follow these rules and push back when instructions violate them.

**Scope**: Apply to **NEW and CHANGED code only**. Do not retroactively rewrite existing code to comply unless it's a critical blocker.

---

## Rule 0: The Diamond Rule (AI Must Push Back)

**If an instruction breaks any rule below, AI developers MUST**:

1. **Flag the conflict clearly**:  
   > "This breaks GOLDEN RULES: [rule name]."

2. **Explain the risk in one sentence**.

3. **Offer a safer alternative**.

4. **Only proceed** if Owner/CEO explicitly confirms:  
   > "I understand the risk, do it anyway."

**This applies even if the Owner sounds 100% certain or is in a rush.**

---

## Rule 1: Test Coverage 85% Minimum

**What**:  
All NEW or CHANGED code must have ≥ **85% line coverage**.

**Applies To**:
- Backend (Python): 85% minimum
- Frontend (TypeScript/React): 85% minimum

**Enforcement**:
- CI must measure coverage on changed files
- PR cannot merge if coverage < 85%
- No waivers by default

**Rationale**: Owner's mandate - "85% MINIMUM front/back. no excuses"

---

## Rule 2: Production From Line 1

**What**:  
There is **only one quality level: production-grade**.

**This Means**:
- No "dev mode" with lower standards
- No hard-coded fake data that wouldn't work in production
- Sandboxes are "not yet exposed to users", NOT "lower quality allowed"

**Enforcement**:
- All code must be written as if already live
- AI devs must reject any "let's make it work in dev first" shortcuts

**Rationale**: AI developers can't differentiate between "dev hacks" and "production code" - they understand only one standard.

---

## Rule 3: No Big-Bang Refactors

**What**:  
Design **domain boundaries early**, make structural changes in **small, tested PRs**.

**This Means**:
- Decide module boundaries up front (e.g., `agent_runtime`, `sandbox`, `owner_console`)
- Enforce those boundaries (no cross-module hack imports)
- When structure needs to change, do it incrementally with tests
- Any "let's rewrite the whole thing" proposal requires research doc + approval

**Forbidden**:
- One giant PR that moves/renames everything
- "Burn it all down and start over" rewrites

**Rationale**: Owner mandate - "I don't want to fucking refactor, cause that shit breaks all code bases"

---

## Rule 4: Modular Monolith (Microservice-Shaped)

**What**:  
Design code as if modules will become separate services, but keep ONE deployable for now.

**This Means**:
- Separate packages/namespaces per domain
- Modules communicate via clear interfaces
- Future microservice split = minimal code changes

**Enforcement**:
- Directory structure reflects domains:  
  `apps/agent-runtime/`, `apps/owner-console/`, etc.
- No random cross-imports between domains

**Rationale**: Prevents massive refactor later while avoiding early microservice complexity

---

## How AI Developers Must Use These Rules

**At the start of every task**:
1. Read this file
2. Check planned changes against all 4 rules
3. Use Rule 0 (Diamond Rule) if ANY conflict exists

**If unsure**, the safe default is:
> "I will follow the Golden Rules and ask Owner/CEO if they want to override."

---

## How Owner/CEO Uses These Rules

**As a checklist**:
- "Did this PR respect all Golden Rules?"

**As a shield**:
- If AI dev suggests breaking a rule:  
  > "No, that breaks GOLDEN RULES (see Rule X). Find another way."

**Violations = process bug**, not normal mistake.

---

## Relationship to Other Constitution Files

**Priority Order**:
1. **GOLDEN_RULES.md** (this file) - highest priority for new code
2. `CLAUDE.md` - quality gates + execution protocol
3. `NOVEMBER_2025_STANDARDS.md` - detailed architecture
4. Other specs - domain-specific details

**If conflict**: GOLDEN_RULES wins for new code decisions.

---

## Future Tiers (Not Yet Enforced)

**Tier 2 (Phase 2+)**:
- OpenAPI specs for all APIs
- Structured logging + metrics
- Security baseline (OWASP ASVS)

**Tier 3 (Guidelines)**:
- File size limits (250/400 lines)
- Function size (30/60 lines)
- PR size preferences

**These will be added when formally adopted.**
