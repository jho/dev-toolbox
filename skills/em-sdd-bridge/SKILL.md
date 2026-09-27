---
name: em-sdd-bridge
description: Convert a ratified Event Model slice into Spec Kit planning context without creating a second domain model.
metadata:
  short-description: Bridge Event Model to Spec Kit
---

# Event Model to Spec Kit Bridge

Use this skill when a feature starts from an implementation-ready slice produced by `em` or the
`event-modeling` skill and needs to enter a Spec Kit workflow.

## Preconditions

- The Event Model is ratified or the user explicitly authorizes work on a draft slice.
- The selected slice document exists and identifies its commands, events, views, translations or
  automations, invariants, scenarios, and boundaries.
- Accepted ADRs and product requirements that constrain the slice are available.

## Workflow

1. Read the selected slice and the relevant model context; do not redesign the domain while
   bridging it.
2. Map the slice's user value and behavior into Spec Kit feature context.
3. Carry forward commands, events, views, translations, automations, invariants, scenarios, and
   failure paths as implementation constraints.
4. Link the relevant PRD and ADRs, preserving their ownership of product and architecture decisions.
5. Create or populate the project's supported bridge artifact, then continue with `/speckit-plan`
   and `/speckit-tasks`.
6. Flag contradictions or missing model detail for the tech lead; do not invent a parallel
   hand-written domain specification.

## Mapping rules

- Events are facts the implementation must record or publish, not commands to execute.
- Commands become write-side behaviors and handler responsibilities.
- Views become read-side projection or query requirements.
- Translations and automations become boundary or reaction behavior; preserve their trigger and
  output.
- Invariants and scenarios become acceptance and test-planning constraints.

The bridge adds implementation context; it does not replace the Event Model or make Spec Kit the
source of domain truth.

