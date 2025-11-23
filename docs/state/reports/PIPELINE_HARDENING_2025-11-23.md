# Pipeline Hardening Report — 2025-11-23

## Summary (What changed)
- Locked in acceptance-criteria obedience: Developers must treat task specs as law and pause for Diamond Checks + new tasks before altering designs.
- Added Dev/Validator Done checklists tied to evidence (coverage ≥85%, RFC 9457 errors, Docker/browser proof) so partial work can’t advance.
- Validator flow now starts with Gate 0 (spec match) to reject drift immediately and mandates Diamond Checks for any proposed spec change.
- CEO manual now forbids “do what you think is optimal,” enforces spec & validation confirmation, and limits replies to short formats.
- PROCESS.md encodes the Dev → Validator → CEO pipeline, requires spec alignment, and adds a design-change protocol (new tasks before code).
- EXECUTION_PROTOCOL_SPEC.md references the authoritative checklists and reminds Devs to keep acceptance criteria exact before handoff.
- ARCHITECTURAL_DECISIONS.md clarifies that addressing patterns (ports vs hostnames, etc.) are architectural law requiring explicit change tasks.
- State spine updated: TASK-P1-003-DEPLOYMENT marked REJECTED with remediation steps; BLOCKERS/CURRENT_TASK reflect reality.

## Port/Hostname Example (Before → After)
- **Before:** Developer swapped the acceptance criteria (unique `http://localhost:{port}` per task) for host-based routing without approval; Validator caught it only after work was done.
- **After:** Spec Obedience Rule + Gate 0 mean Dev cannot implement hostnames unless the Owner approves a design-change task; Validator rejects immediately if acceptance criteria aren’t met.

## Files touched
- `AGENTS.md` — Added Spec Obedience Rule + Dev Done checklist.
- `VALIDATOR.md` — Added Gate 0 spec match + Validator Done checklist; Diamond check now mandatory when specs drift.
- `CLAUDE.md` — Added reply boundaries, spec-change rule, and spec & validation confirmation in the CEO Answer Format.
- `constitution/PROCESS.md` — Explicit acceptance-criteria steps, validator spec check, design-change protocol, and CEO spec verification.
- `constitution/EXECUTION_PROTOCOL_SPEC.md` — References Dev/Validator checklists, enforces acceptance-criteria focus, warns against early handoff.
- `constitution/ARCHITECTURAL_DECISIONS.md` — States that addressing patterns belong to acceptance criteria/design law.
- `docs/state/tasks/TASK-P1-003-DEPLOYMENT.md`, `docs/state/CURRENT_TASK.md`, `docs/state/BLOCKERS.md`, `docs/state/PROGRESS.md` — Updated to show deployment task rejected and awaiting remediation.
