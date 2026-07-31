---
name: working-on-github-issues
description: Take a selected GitHub issue from context and readiness through local implementation, verification, progress reporting, and explicit issue lifecycle updates. Use when the user wants to work on or complete an existing GitHub issue.
---

# Working on GitHub Issues

Use this skill when the user has selected an existing issue and wants the work carried out. It coordinates the issue, local repository, tests, and optional GitHub updates; it does not replace repository-specific implementation or pull-request guidance.

## Prerequisites

- Resolve the repository and exact issue number or URL. If the issue is only described by a phrase, search first and confirm the selected issue when multiple candidates exist.
- GitHub CLI or another repository-supported issue tool must be available for issue context. Local implementation tools and repository guidance must be available.
- Read the issue body, labels, assignees, milestone, linked issues, and relevant comments before changing code.

## Workflow

```text
resolve issue → understand scope → check readiness → implement locally → verify → report → optionally update issue
```

### 1. Understand the issue

Summarize the intended outcome, acceptance criteria, non-goals, constraints, dependencies, and unresolved questions. Check whether the issue is open, already assigned, blocked, superseded, or likely duplicated. Do not begin implementation if the requested outcome cannot be determined safely; surface the specific gap.

### 2. Establish a change plan

Inspect the repository's contribution guidance, relevant code, tests, and current branch state. Keep the implementation focused on the issue's coherent outcome. Identify the files or components likely to change, the verification strategy, and any migration or compatibility risk. Do not broaden scope merely because adjacent cleanup is tempting.

### 3. Implement and verify

Make the smallest complete local change that satisfies the issue. Follow repository conventions and preserve unrelated user changes. Add or update tests at the appropriate level. Run targeted checks first, then the repository's required validation when practical. Treat failures as part of the result: distinguish regressions introduced by the change from pre-existing or environmental failures.

Before claiming completion, map each acceptance criterion to evidence from tests, commands, or inspected behavior. If a criterion is not met, report it plainly and keep the issue open.

### 4. Report progress

Give the user a concise implementation summary, files changed, validation performed, remaining risks, and the next handoff (for example, review or pull request). Never claim that GitHub was updated unless the update succeeded.

### 5. Update GitHub only with authorization

Creating comments, changing labels or assignees, changing state, and closing or reopening an issue are external writes. Perform them only when the user explicitly requests that action or has clearly authorized the update as part of this task. Keep updates factual and include:

- what changed;
- validation evidence;
- remaining work or known limitations;
- links to the relevant branch, commit, or pull request when available.

Do not close an issue just because code changed. Close it only when the acceptance criteria are satisfied and the user authorizes closure. Do not invent labels, milestones, assignees, or status conventions.

## Quality and safety

- Never silently switch repositories, GitHub accounts, branches, or issue numbers.
- Preserve local changes that are unrelated to the selected issue.
- Do not include secrets, tokens, private credentials, or unnecessary command output in issue comments.
- If the issue conflicts with repository guidance or another active change, stop and explain the conflict before making a risky change.
