# Gate G4: Code Quality (Style, Lint, Types)

## Purpose
Ensure code is readable, consistent, and free of obvious smell/anti-pattern issues.

## Required Evidence Files

- `TASK-{TASK_ID}-lint.txt` - Lint output (ESLint, Ruff/Flake8)
- `TASK-{TASK_ID}-types.txt` - Type check output (TypeScript, mypy)

## Tools & Versions

- JS/TS: `eslint` 9.39.x
- Python: `ruff` latest stable or `flake8` 7.3.x
- Typing: TypeScript compiler, `mypy` 1.18.x

## Thresholds

- Lint: **0 errors, 0 warnings** in CI
- Types: **0 type errors** for files under test
- Suppressions: Any `eslint-disable`, `# noqa`, or `type: ignore` must be explicitly justified in TASK file

## CEO Checklist

- [ ] Lint report shows "0 errors, 0 warnings" for ESLint and Ruff/Flake8
- [ ] Type check report has no "error" entries
- [ ] Any rule suppressions are justified in TASK file (manual check)

## Automation

CI runs ESLint/Ruff/mypy and fails on any error/warning.
