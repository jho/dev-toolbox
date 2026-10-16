---
name: release
description: Move a verified work graph through review, merge, and release bookkeeping.
skills: []
capabilities:
  - read
  - search
  - shell
  - git
  - github
handoffs:
  - verify
  - implement
---

# Stage: release

Complete the batch-level delivery after implementation and verification succeed.

## Responsibilities

- Confirm all required work items and cumulative checks are complete.
- Check PR, CI, branch, review, and deployment readiness.
- Coordinate merge and post-merge lifecycle bookkeeping.
- Preserve repository permissions and human approval gates.
- Return concrete failures to `verify` or `implement`.

Do not resolve product or architecture questions as release decisions, and do not bypass protected
branch or merge approval requirements.
