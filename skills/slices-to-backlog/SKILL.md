---
name: slices-to-backlog
description: Inspect the current Event Model worktree and turn changed, implementation-ready slices into a reviewable work graph for planning agents and external harnesses.
metadata:
  short-description: Plan changed Event Model slices
---

# Slices to backlog

Use this skill during the `plan` stage of an Event Modeled project. It is the toolbox-level
stand-in for a future `/em:plan` workflow; it does not modify the upstream `em` tool.

The planner discovers active `.em` files from the worktree and binds each model to the adjacent
`.event-modeling.md` state file. Deleted or renamed historical paths from Git are traceability
data, not validation targets. Validation uses the repository's pinned `em` command when one is
declared by the repository; otherwise it reports that it fell back to the installed CLI.

## Contract

Inspect the current repository and worktree rather than requiring a model-file argument. Include
committed branch changes, staged and unstaged changes, relevant untracked files, and the current
`.event-modeling.md` state. Conversation context alone is not a machine-readable source.

Use read-only commands such as:

```bash
git status --short --untracked-files=all
git diff --name-status <merge-base>...HEAD
em validate <model>.em
em status <model>.em --json
em export <model>.em
```

The helper at `scripts/slices_to_backlog.py` can produce the standard JSON and Markdown output.

## Planning rules

- A changed `.em` file without changed slice documents is a design blocker, not an invitation to
  invent implementation work.
- Invalid models, missing slice documents, unresolved open questions, and non-ready slice status
  must appear as blockers.
- Draft and reviewed slices may be reported as work items for planning visibility, but they must
  keep the graph `ready: false` until they are ratified and `ready-to-implement`.
- Preserve the Event Model and linked slice documents as the domain source of truth.
- Identify dependencies only when supported by model structure or explicit implementation context;
  mark uncertain relationships for Tech Lead review.
- Do not create branches, worktrees, commits, pull requests, or GitHub issues by default.
- GitHub issue creation is an explicit follow-up using the existing issue-creation skill.
- Parallel execution, worktree allocation, scheduling, CI watching, and merging belong to an
  external Codex/Claude-compatible harness.

## Output

Return both:

1. a concise Markdown plan for the human or Tech Lead; and
2. JSON conforming to the work-graph shape below.

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

The work graph is a handoff contract. It is not a scheduler or an execution engine.
