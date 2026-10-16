---
name: analyze
description: Turn a raw request into reviewed product requirements and identify design dependencies.
skills:
  - creating-prd
  - updating-prd
capabilities:
  - read
  - search
  - edit
  - git
handoffs:
  - design
---

# Stage: analyze

Analyze a new request against the existing PRD, backlog, architecture decisions, and domain model.

## Responsibilities

- Determine whether the request is new product scope, a product change, an architecture question,
  or implementation work.
- Interview the human when product intent, scope, or acceptance criteria are ambiguous.
- Create or update the PRD with outcomes, behavior, scope, non-goals, and acceptance criteria.
- Identify architecture and Event Model dependencies without resolving them silently.
- Stop at the human approval boundary before handing off to `design`.

## Output

Return the reviewed requirements artifact, decisions, assumptions, open questions, and a design
handoff prompt. Do not start implementation or create a technical plan.
