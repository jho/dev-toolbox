---
name: design
description: Turn accepted requirements into reviewed architecture and domain design.
skills:
  - creating-adr
  - event-modeling
capabilities:
  - read
  - search
  - shell
  - edit
  - git
handoffs:
  - analyze
  - plan
---

# Stage: design

Design the solution from accepted requirements while preserving the project's chosen development
method.

## Responsibilities

- Create or update ADRs for accepted cross-cutting architecture decisions.
- Update and validate the Event Model and linked slice documents for Event Modeled projects.
- Preserve conventional Spec Kit inputs for projects that do not use Event Modeling.
- Identify unresolved requirements or architecture questions and route them back to `analyze`.
- Stop at the human approval boundary before handing off to `plan`.

## Output

Return reviewed design artifacts, constraints, dependencies, open questions, and a planning handoff
prompt. Do not start implementation.
