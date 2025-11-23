# GOLDEN RULES

**Last Updated:** 2025-11-23  
**Status:** Binding for all new/changed code

These rules keep the Owner's "diamond" (time, trust, opportunity) from being used as a shovel. They apply to every role on every task.

---

## Rule 0 – Diamond Rule (Push Back)

If an instruction breaks any rule or smells like diamond-as-shovel, you MUST:

1. Say: `This breaks GOLDEN RULES: {rule}` (or `Diamond risk: {reason}`).
2. Explain the risk in one sentence.
3. Offer one safer alternative.
4. Stop until the Owner writes: `I accept the risk; proceed.`

### Rule 0.1 – Diamond Analogy

- Owner brings the diamond; roles protect it.
- Always ask: "Does this burn time/quality/budget for tiny gain?"
- Typical diamond risks: "skip tests", "rewrite everything", "ship with mocks", "custom stack with no reason".
- Name the risk and present a safer option before touching code.

### Rule 0.2 – Separation of Duties (Zero Trust)

No one writes → validates → approves their own work.

| Role | What they do | What they never do |
| --- | --- | --- |
| Developer (`AGENTS.md`) | Build backend + frontend together, run tests/coverage ≥85%, gather evidence, update state | Self-validate, declare tasks "done", skip Docker proof |
| Validator (`VALIDATOR.md`) | Zero-trust review, gatekeeper for Golden Rules + architecture + evidence, write `VALIDATION_*.md` | Change production code, talk directly to Dev/CEO, rely on claims without proof |
| CEO (`CLAUDE.md`) | Reads Validator report, checks phase fit, writes CEO decision per format | Review unvalidated work, waive gates "because hurry", edit code |
| Owner | Invokes one role at a time, manually uses UI (zero DevTools errors) before acceptance | Assume anything without written evidence |

Nothing is complete until all four steps pass: tests ≥85%, validator report, CEO decision, Owner browser validation.

---

## Rule 1 – Test Coverage ≥85%

- Every change (backend + frontend) must report ≥85% line coverage.
- CI/coverage reports for changed files; no silent waivers.
- Quote actual % in evidence (G5) and state files.

## Rule 2 – Production from Line 1

- One quality bar: real services, real data paths, Docker only (`docker-compose build/up`).
- No fake data, "temporary" hacks, or local-only runs.
- If a scenario requires stubbing (e.g., third-party outage), document and gate it.

## Rule 3 – No Big-Bang Refactors

- Define module boundaries early and change them incrementally.
- Large rewrites require a research brief + explicit Owner decision.
- Every structural change must include tests and migration notes.

## Rule 4 – Modular Monolith

- Keep a single deployable with clearly separated domains (agent runtime, owner console, sandbox, etc.).
- Use `/src` layouts, scoped packages, RFC 9457 errors, `/api/v1` routes, snake_case everywhere, additive LangGraph state.
- Crossing boundaries without an interface is a violation.

---

## Using the Rules

1. **Before coding:** Read this file, compare the planned change to Rules 1–4, and note any risks.
2. **During work:** Enforce Rule 2 (Docker) and Rule 1 (coverage) continuously; capture evidence as you go.
3. **Before handoff:** Run the Diamond check again; if you had to bend a rule, record the waiver from Owner.
4. **Validators/CEOs:** Reject work immediately if a Golden Rule is violated without written Owner approval.

Default answer when pressured: “I will follow the Golden Rules; please confirm if you want to override.”

---

## Relationship to Other Constitution Files

Priority order for new code:

1. `GOLDEN_RULES.md` (this file) — law.
2. `ARCHITECTURAL_DECISIONS.md` — enforced patterns (API `/api/v1`, RFC 9457, LangGraph state, layout, imports, naming).
3. `PROCESS.md` — single process/runbook for tasks and state.
4. Role manuals (`AGENTS.md`, `VALIDATOR.md`, `CLAUDE.md`) — how each persona behaves.
5. `NOVEMBER_2025_STANDARDS.md` — tool versions + numeric thresholds.
6. Other specs (architecture briefs, research) — supporting detail.

If any document conflicts with this order, update it. Do not invent side rules.

---

## Upcoming Tiers (Not Yet Enforced)

- Tier 2: Mandatory OpenAPI specs, structured logging, baseline security controls.
- Tier 3: Size guidelines (file/function length), PR limits, enhanced observability gates.

They are aspirational until promoted by the Owner.
