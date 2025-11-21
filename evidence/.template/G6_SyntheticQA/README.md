# Gate G6: Synthetic QA (AI Test Users)

## Purpose
Catch end-to-end issues by having AI agents exercise the app in realistic flows.

## Required Evidence Files

- `TASK-{TASK_ID}-synthetic-runs.json` - Structured test run data
- `TASK-{TASK_ID}-synthetic-report.md` - Human-readable summary

## Standards

For every build with user-visible changes:
- At least one **happy-path** scenario
- At least one **negative-path** scenario (invalid input/permissions)
- Synthetic tests must pass without critical failures for core flows
- Re-run after bug fixes affecting those flows

## CEO Checklist

- [ ] At least one happy-path and one negative-path synthetic journey executed
- [ ] No unresolved critical synthetic failures on core flows
- [ ] Any waivers are explicit, time-bounded, and justified

## Automation

CI or post-deploy hooks trigger synthetic runs in sandbox. Production toggle blocked if fails without waiver.
