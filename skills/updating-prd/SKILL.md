---
name: updating-prd
description: Update an existing product requirements document when a product request changes scope, behavior, or acceptance criteria.
metadata:
  short-description: Update a PRD
---

# Updating a PRD

Use this skill when a product manager needs to incorporate an approved product change into an
existing PRD without turning technical implementation choices into product requirements.

## Workflow

1. Locate the relevant PRD and read its goals, scope, terminology, acceptance criteria, and open
   questions.
2. Restate the requested change as user value and identify which existing requirements it affects.
3. Ask only the questions needed to resolve product ambiguity: user, behavior, scope, success
   measure, non-goals, or domain terminology.
4. Update the PRD in place, preserving its structure and clearly recording changed behavior.
5. Identify architecture dependencies for the architect; do not resolve them inside the PRD.
6. Record unresolved product questions rather than guessing.

## Boundary with architecture

The PRD owns why the capability exists, who uses it, what the product promises, and how success is
recognized. If the change requires a new cross-cutting technical choice, hand off the dependency to
the architect for an ADR before implementation planning. The PRD may link to the ADR once accepted,
but should not contain its full rationale.

## Review checklist

Before handing off, confirm:

- Existing requirements still agree with the changed behavior.
- Acceptance criteria are observable and testable.
- Scope and non-goals are explicit.
- Product decisions are separated from implementation decisions.
- Architecture dependencies and open questions are visible.

