---
name: creating-adr
description: Record an accepted architecture decision with its rationale, alternatives, consequences, and enforcement implications.
metadata:
  short-description: Create an ADR
---

# Creating an ADR

Use this skill when a product or engineering problem requires a cross-cutting technical decision
that future features must follow.

## Before drafting

- Read the triggering issue or request, relevant PRD or Event Model material, existing ADRs, and
  the project constitution or equivalent engineering policy.
- Check whether the question is already decided or is still only a proposal.
- Keep unresolved alternatives out of the accepted-decision section.

## Decision workflow

1. State the context and the concrete decision that must be made.
2. Compare only the alternatives that could realistically satisfy the constraints.
3. Ask the decision owner for unresolved choices instead of silently selecting one.
4. Record the accepted decision, rationale, rejected alternatives, consequences, and migration or
   follow-up implications.
5. Link the triggering product or architecture issue.
6. Update the constitution or engineering policy with only the concise normative rules agents must
   enforce during planning and implementation.
7. Make the issue, ADR, and policy references discoverable from the repository's architecture index
   when that convention exists.

## Boundaries

An ADR records what and why. It is not a feature specification, implementation plan, or product
backlog. Do not ratify an unresolved question merely to unblock planning. If the decision changes
user-visible scope or behavior, send that part back to the product workflow for the PRD.

## Completion check

The decision is ready for review when a developer can determine the boundary they must follow, a
tech lead can identify its implementation consequences, and a future agent can find the source issue,
ADR, and enforcement rule without relying on conversation history.
