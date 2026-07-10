---
name: creating-prd
description: Interviews a product manager, drafts a standard PRD in the repo template, and saves it for design and implementation planning.
metadata:
  short-description: Draft a PRD
---

# Creating a PRD

Use this skill when a product-manager agent needs to turn an idea, problem, or initiative into a clear product requirements document.

## What this skill does

- Clarifies the problem and intended outcome.
- Captures users, scope, success measures, and constraints.
- Produces a repo-local PRD from a template.
- Leaves the PRD ready for design, planning, or stakeholder review.

## Interview flow

Ask one question at a time and keep the discussion concrete.

Start with:

1. What problem are we solving?
2. Who feels that problem most?
3. What does success look like?
4. What is in scope for the first release?
5. What is explicitly out of scope?
6. What dependencies, constraints, or risks matter?
7. What terms in this domain need precise definitions?

If the brief already answers a question, skip it and focus on the gaps.

## Drafting guidance

- Use the repo-local template at `templates/prd_template.md`.
- Keep the PRD focused on one initiative.
- Prefer measurable goals over vague outcomes.
- Use testable acceptance criteria.
- Define domain terms precisely and avoid synonyms.
- Record open questions instead of guessing when something is unresolved.

## Saving the file

Default location: `docs/prds/<slug>.md`

If a repository uses a different convention, confirm the path before saving.

## Review pass

Before writing the file, summarize:

- the problem statement
- the target user
- the success metrics
- the out-of-scope items
- the open questions

Revise the draft if the PM changes direction.

