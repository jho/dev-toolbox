---
name: creating-github-issues
description: Create well-formed GitHub issues for bugs, enhancements, research, and workflow improvements. Searches for related issues before creation and separates user value from implementation notes.
metadata:
  short-description: Create a GitHub issue
---

# GitHub Issue Creation

Use this skill when a user wants to capture work in GitHub as an issue. It follows the same value-first discipline as story creation while adapting it to GitHub's lighter-weight issue model.

## Prerequisites

- The target repository must be clear from the current directory, an explicit repository argument, or the user's context.
- GitHub CLI or another repository-supported issue tool must be available and authenticated.
- External issue creation requires user authorization. A direct request to create the issue is authorization; drafting alone is not.

Repository-specific authentication, account selection, wrappers, labels, and project conventions belong to the repository or account-management workflow. Do not embed them here.

## Workflow

```text
resolve repository → search related issues → draft issue → review/authorize → create → report URL
```

### 1. Resolve the repository

Use the current repository when unambiguous. Otherwise ask for the repository before making a write. Inspect local contribution guidance and `.github/ISSUE_TEMPLATE/` when it exists.

Issue-template precedence:

1. Use the repository's matching issue template or issue form when one exists.
2. If several templates could apply, choose based on the issue type and explain the choice.
3. If no repository template applies, read [references/default-issue-template.md](references/default-issue-template.md) and use it as the fallback structure.

Do not load the bundled fallback reference when a repository template already provides the required structure.

### 2. Search for related issues

Search by the main subject and a few distinctive terms. Review results for:

- duplicates or overlapping work;
- existing issues that should be referenced;
- dependencies, blockers, or prior decisions;
- an established title, label, or formatting convention.

If a likely duplicate exists, tell the user and ask whether to update, reference, or create a separate issue. Do not create duplicate work silently.

### 3. Prepare the issue

Use a concise, action-oriented title. Follow the selected repository template exactly, including required fields, checkboxes, metadata, and instructions. Do not discard useful repository fields merely because they are absent from the fallback template.

When using the fallback, read [references/default-issue-template.md](references/default-issue-template.md). For research, performance, or data work, also apply its guidance on baseline protection, candidate evaluation, promotion criteria, non-goals, and locked evaluation boundaries.

### 4. Review and create

If the user requested a draft, stop after presenting it. If the user authorized creation, create it with the supported tool and apply labels only when their existence and meaning are known. Do not invent labels or add assignees/milestones without instruction.

If no repository issue template exists, use the bundled fallback for the issue body. You may offer to add a repository template under `.github/ISSUE_TEMPLATE/`, but creating or modifying repository files is a separate write and requires explicit authorization. If authorized, adapt the fallback to the repository's conventions, preserve the required issue fields, and show the proposed file change before or as part of implementation.

### 5. Report

Return the created issue number and URL, followed by a short summary. If creation fails, report the failure without switching accounts or bypassing repository controls.

## Quality and safety

- Keep one issue focused on one coherent outcome; split larger initiatives when separate pieces deliver value independently.
- Record important non-goals to prevent scope drift.
- Do not include secrets, tokens, private credentials, or unnecessary bulk output.
- Creating, editing, labeling, closing, or commenting on an issue is an external write; do not perform it without authorization.
