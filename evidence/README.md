# Evidence Directory

This directory contains all quality gate evidence for the "Your First Engineer" project.

## Structure

```
evidence/
  .template/          # Templates and READMEs for each gate
  G1_Research/        # Research & problem definition evidence
  G2_Architecture/    # Architecture & design evidence
  G3_Security/        # Security & compliance evidence
  G4_CodeQuality/     # Code quality (lint, types) evidence
  G5_TestingCoverage/ # Testing & coverage evidence
  G6_SyntheticQA/     # Synthetic QA (AI test users) evidence
  G7_ObservabilityReliability/ # Observability & reliability evidence
  G8_DataPrivacyCompliance/    # Data, privacy & governance evidence
  G9_AIRiskEthics/    # AI risk & safety evidence
  G10_UXAccessibility/  # UX, accessibility & product fit evidence
  G11_OperationalReadiness/  # Operational readiness & launch evidence
```

## Naming Convention

All evidence files use the format: `TASK-{TASK_ID}-{artifact}.{ext}`

Example:
- `TASK-001-research-report.md`
- `TASK-001-pytest.txt`
- `TASK-001-coverage-html/`

## CI Automation

CI checks verify:
1. Required evidence files exist for gates in scope (from task file)
2. Files are non-empty
3. Structured files (JSON, XML) are valid

## Usage

1. Developer: Creates evidence files during task execution per gate requirements
2. CEO: Reviews evidence files to approve/reject PR per gate checklists
3. CI: Automates checks for file existence and basic validity

See `EXECUTION_PROTOCOL_SPEC.md` for detailed developer/CEO protocols.
