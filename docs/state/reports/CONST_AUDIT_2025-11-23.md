# Constitutional Audit — 2025-11-23

## Summary (Zero-Trust Findings)
- Re-confirmed hierarchy: GOLDEN_RULES > ARCHITECTURAL_DECISIONS > PROCESS > role manuals > standards.
- Trimmed GOLDEN_RULES to a 2–3 minute read while keeping Rule 0 + duties separation explicit.
- Converted NOVEMBER_2025_STANDARDS into a pure reference (tables + thresholds) with no stray law.
- Updated PROCESS with validator startup + flow so Developer → Validator → CEO chain is unambiguous.
- Added mandatory boot protocols (1–5 handshake) for Developer, Validator, and CEO files.
- Ensured OPERATIONAL_CONTEXT + state docs point new personas straight to the correct reading order.

## File-Level Changes
- `constitution/GOLDEN_RULES.md` – Rewrote for brevity, codified separation of duties, clarified doc precedence, kept Rules 0–4 intact.
- `constitution/NOVEMBER_2025_STANDARDS.md` – Shortened executive summary, replaced prose with tool table, reiterated subordinate status to Golden Rules/Arch/Process.
- `constitution/PROCESS.md` – Added validator startup + flow, clarified developer handoff goes to validation before CEO, renumbered sections.
- `AGENTS.md` – Added boot protocol, explicit “stop at ready for validation”, reinforced repo-only comms.
- `CLAUDE.md` – Added CEO boot protocol referencing validator report before any decision work.
- `VALIDATOR.md` – Replaced rambling intro with strict boot protocol + reminder of evidence-only communication.
- `constitution/OPERATIONAL_CONTEXT.md` – Extended reading order through role manuals to prevent law confusion.
- `docs/state/INDEX.md`, `CURRENT_TASK.md`, `BLOCKERS.md`, `PROGRESS.md` – Verified structure; no content edits required beyond existing task context.

## Remaining Concerns / TODOs
- `EXECUTION_PROTOCOL_SPEC.md` and `STATE_MANAGEMENT.md` still contain legacy prose; future cleanup should remove redundant storytelling once time allows.
- Ensure future CEO edits keep boot protocol + decision format intact; treat `CLAUDE.md` as process enforcement, not another law book.
- CI should enforce presence of validator and CEO reports before marking tasks complete (not yet automated).
