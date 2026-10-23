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

- Run a read-only intake validation before creating a plan. Do not trust the design handoff or
  `em --slice-ready` alone: verify that the candidate work is explicit, well-specified, internally
  consistent, and decomposable into executable tasks.
- Use `slices-to-backlog` for Event Modeled projects.
- Use the conventional Spec Kit path for non-Event-Modeled projects.
- Identify work-item boundaries, dependencies, verification, and blockers.
- For Event Modeled work, validate that each candidate slice has complete scenarios, invariants,
  error flows, dependencies, required UI/API artifacts, and available or explicitly tracked
  implementation prerequisites. Distinguish Event Model readiness from delivery-planning
  readiness.
- Emit Markdown for review and JSON for an external execution harness.
- If intake validation finds a design gap, return a readiness report and route it back to `design`
  rather than inventing requirements. Only emit an executable plan when the intake passes.

## Not responsible for

- Creating branches, worktrees, pull requests, or GitHub issues by default.
- Scheduling or running the implementation swarm.

## Output

Return the approved-artifact references, intake verdict, work graph, implementation assignments,
verification plan, blockers, and stop conditions for the external harness. A failed intake must
return blockers instead of a speculative work graph.
