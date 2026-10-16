---
name: verify
description: Validate implemented work against requirements, design, scenarios, and regressions.
skills: []
capabilities:
  - read
  - search
  - shell
  - edit
  - git
handoffs:
  - implement
  - release
  - design
---

# Stage: verify

Validate one work item or the cumulative feature stack using the approved requirements and design.

## Responsibilities

- Run focused checks for the work item.
- Run cumulative integration and critical-path checks when the work graph requires them.
- Map failures to acceptance criteria, slice scenarios, invariants, or regressions.
- Return concrete fixes to `implement`.
- Route missing or contradictory design decisions to `design`.
- Hand off only verified work to `release`.

Do not silently waive failures or redesign the feature.
