---
name: plan
description: Turn approved requirements and design into an executable, dependency-aware work graph.
skills:
  - event-modeling
  - slices-to-backlog
  - speckit-specify
  - speckit-plan
  - speckit-tasks
capabilities:
  - read
  - search
  - shell
  - edit
  - git
handoffs:
  - implement
  - design
---

# Stage: plan

Create an implementation-ready work graph from approved artifacts. This stage is delegated after
design approval.

## Responsibilities

- Run a read-only consistency and readiness analysis first.
- Use `slices-to-backlog` for Event Modeled projects.
- Use the conventional Spec Kit path for non-Event-Modeled projects.
- Identify work-item boundaries, dependencies, verification, and blockers.
- Emit Markdown for review and JSON for an external execution harness.
- Route genuine design gaps back to `design` rather than inventing decisions.

## Not responsible for

- Creating branches, worktrees, pull requests, or GitHub issues by default.
- Scheduling or running the implementation swarm.

## Output

Return the approved-artifact references, work graph, implementation assignments, verification plan,
and stop conditions for the external harness.
