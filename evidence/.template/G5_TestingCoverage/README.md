# Gate G5: Testing & Coverage

## Purpose
Ensure robust automated tests with meaningful coverage.

## Required Evidence Files

- `TASK-{TASK_ID}-pytest.txt` - Backend test output
- `TASK-{TASK_ID}-frontend-tests.txt` - Frontend test output
- `TASK-{TASK_ID}-coverage-summary.txt` - Coverage summary
- `TASK-{TASK_ID}-coverage-html/` - HTML coverage report (directory or archive)

## Tools

- Backend: `pytest` 9.0.x + `coverage.py` 7.11/7.12
- Frontend: Jest 30.x or Vitest 4.x with integrated coverage

## Coverage Thresholds

- New/changed backend code: **≥80% line coverage**
- New/changed frontend logic: **≥70% line coverage**
- Overall project: **≥60% line coverage** (baseline, plan to raise to 80%)

These values reflect industry recommendations where 80% is considered a good target (Google: 60% acceptable, 75% commendable, 90% exemplary).

## CEO Checklist

- [ ] All tests pass (no failures, flakes documented)
- [ ] New/modified backend code ≥80% line coverage
- [ ] New/modified frontend logic ≥70% line coverage
- [ ] Overall project coverage ≥60% (or higher if phase policy increases threshold)

## Automation

CI fails if coverage thresholds not met for new code or if overall coverage dips below baseline.
