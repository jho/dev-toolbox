# Agentic SDLC Design

The toolbox defines a reusable lifecycle contract, not an orchestration product. A Codex, Claude,
or project-specific harness owns session state, delegation, permissions, worktrees, scheduling,
and merge actions.

## Lifecycle

```text
analyze → design → plan → implement → verify → release
```

`analyze` and `design` are human-gated stages. They clarify product intent, resolve architecture,
and establish the Event Model or conventional requirements needed for execution. `plan`,
`implement`, `verify`, and `release` are delegated stages that work from approved artifacts.

“Human-gated” and “delegated” describe workflow behavior, not a special Codex or Claude runtime
mode. Skills provide the procedure; generated stage agents provide the responsibility boundary.

## Stage contracts

| Stage | Inputs | Output | Gate |
|---|---|---|---|
| Analyze | Raw request, PRD, backlog | Reviewed requirements and dependencies | Human approval |
| Design | Accepted requirements, ADRs, model | Reviewed design and slices | Human approval |
| Plan | Approved design and current worktree | Markdown plan and JSON work graph | Harness handoff |
| Implement | One work-graph item | Code, tests, evidence | Verification |
| Verify | Work item or cumulative stack | Evidence or concrete failures | Release readiness |
| Release | Verified work graph | Merge/release status and lifecycle updates | Repository policy |

## Context packet

Every delegated run receives a bounded packet:

```text
Objective: the work-item outcome
Stage: analyze | design | plan | implement | verify | release
Source of truth: approved artifact paths and relevant repository guidance
Constraints: product, architecture, policy, and scope boundaries
Allowed changes: files or artifacts this run may edit
Dependencies: completed work items and branch/PR relationships
Verification: commands, scenarios, and acceptance evidence required
Expected output: artifact, work graph, implementation, evidence, or release status
Stop conditions: blockers that must return to a prior stage or human
```

## Event Model planning

For Event Modeled projects:

```text
approved requirements
  → design updates the Event Model and slice documents
  → plan runs slices-to-backlog against the current worktree
  → external harness executes the work graph
```

The `.em` model and linked slice documents remain authoritative. `em` performs validation,
readiness, export, and lifecycle operations. `slices-to-backlog` does not create a second domain
specification and does not replace the upstream `em` workflow.

For conventional projects:

```text
approved requirements → plan derives conventional specification/plan/tasks
```

The planning stage must not invent Event Model artifacts for a project that does not use Event
Modeling.

## Work-graph contract

The plan stage emits Markdown for humans and JSON for an external harness. The minimum JSON shape
is:

```json
{
  "schemaVersion": "1.0",
  "base": "<merge-base>",
  "head": "<commit>",
  "models": [],
  "eventModelingState": [],
  "workItems": [
    {
      "id": "<stable-id>",
      "stage": "implement",
      "model": "<model-path>",
      "slice": "<slice-path>",
      "dependsOn": [],
      "verification": []
    }
  ],
  "blockers": [],
  "ready": true,
  "orchestration": "external-harness"
}
```

The work graph expresses dependencies and ownership; it does not schedule workers, allocate
worktrees, create PRs, merge branches, or watch CI. Those capabilities remain replaceable harness
adapters and may be evaluated after the workflow has been exercised on real work.

## Escalation

- Requirements gap → `analyze` and the human.
- Architecture or Event Model gap → `design` and the human.
- Planning gap → `plan`.
- Implementation failure → `implement`.
- Verification failure → `implement` or `design` depending on the cause.
- Release failure → `verify` or `implement`.
