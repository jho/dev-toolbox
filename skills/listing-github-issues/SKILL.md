---
name: listing-github-issues
description: Find, filter, and summarize GitHub issues for a repository, including backlog triage, assigned work, open work, and related issue discovery. Use for read-only issue discovery before deciding what to create or work on.
---

# GitHub Issue Listing

Use this skill when a user wants to find, inspect, compare, or triage issues without changing GitHub state. It complements `creating-github-issues`: discovery comes first when the user is unsure whether work already exists.

## Prerequisites

- Resolve the target repository from the current directory, an explicit `OWNER/REPO`, or the user's context. Ask when it is ambiguous.
- GitHub CLI or another repository-supported issue tool must be available and authenticated.
- Inspect repository guidance when it defines labels, projects, ownership, or issue conventions.

## Workflow

```text
resolve repository → translate request into filters → list/search → inspect candidates → summarize next actions
```

### 1. Resolve scope and intent

Establish the repository and what the user means by “issues”: open backlog, assigned work, a label, a milestone, a search phrase, recently changed issues, or likely duplicates. Preserve explicit filters. If none are given, prefer open issues and say what default scope was used.

### 2. Query efficiently

Use the repository's supported tool. With GitHub CLI, common read-only operations include:

- `gh issue list --repo OWNER/REPO` for a concise filtered list;
- `gh issue list --search '...' --repo OWNER/REPO` for GitHub search qualifiers;
- `gh issue view NUMBER --repo OWNER/REPO --comments` for a candidate's complete context.

Use narrow searches before broad ones. Combine distinctive terms, labels, assignees, state, milestone, and author as appropriate. Do not dump an unbounded backlog; paginate or cap results and state the limit.

### 3. Inspect and classify

For each relevant candidate, capture only what supports the decision:

- number, title, state, URL, labels, assignees, and milestone;
- a short reason it matches;
- dependencies, blockers, duplicate signals, or recent discussion;
- the next useful action: work it, reference it, update it, or create a separate issue.

Open likely matches before calling them duplicates. Search results alone are not enough to make that determination.

### 4. Report

Return a compact table or grouped list, followed by a short recommendation. Include the exact scope and filters used, the result cap, and any likely duplicates or blocked items. Link to issues using their canonical URLs.

This skill is read-only. Do not create, edit, comment on, label, assign, reopen, or close issues. Hand off to `creating-github-issues` or `working-on-github-issues` when the user chooses a write or implementation action.

## Quality and safety

- Never silently switch repositories, GitHub accounts, or authentication contexts.
- Do not infer ownership from a username or label unless the repository makes it explicit.
- Do not treat a closed issue as irrelevant; it may document a decision, prior fix, or duplicate.
- Avoid exposing secrets, tokens, private credentials, or unnecessary issue-history bulk output.
