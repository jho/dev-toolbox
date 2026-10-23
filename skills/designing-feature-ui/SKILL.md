---
name: designing-feature-ui
description: Design a feature's UI flow from an Event Model slice, Spec Kit feature, or conventional requirements artifact, producing a wireframe/prototype and a concise interaction contract.
metadata:
  short-description: Design a feature UI from approved requirements
---

# Designing Feature UI

Turn one approved feature or interaction unit into a reviewable UI design without changing the
product requirements or backend architecture.

## Inputs

Identify the smallest approved unit being designed:

- an Event Model slice and its slice document;
- a Spec Kit feature/spec; or
- a conventional feature brief, issue, or acceptance-criteria document.

Also locate, when present:

- the project's design-system guide and component examples;
- the central prototype or information-architecture reference;
- route/navigation conventions;
- existing wireframes or prototypes for related screens.

Do not assume that an Event Model or Spec Kit is present. If the source artifact is ambiguous or
unapproved, stop and ask for the missing decision rather than inventing product behavior.

## Workflow

1. Establish the user, entry point, primary task, success outcome, and next interaction.
2. Map visible reads, user actions, and navigation to the source artifact. For an Event Model slice,
   distinguish read-model content from commands and do not add domain events from visual design.
3. Reuse the existing design system, information architecture, and interaction patterns. If no
   design system exists, use the project's current conventions and record the missing decision;
   do not silently select a UI library.
4. Design the smallest useful screen or flow. Include the normal state plus relevant loading,
   empty, error, unauthorized, and confirmation states.
5. Create or update the repository's preferred wireframe/prototype format. Prefer source-controlled
   HTML/CSS/SVG or the established project format over an image-only artifact when the screen needs
   interaction or responsive behavior.
6. Add a concise UI/interaction contract to the source feature or slice document, linking the
   wireframe/prototype. Keep visual detail in the visual artifact and behavioral requirements in the
   source document.
7. Render or open the artifact when practical and report unresolved design questions for human
   review.

## Boundaries

- The central prototype is an information-architecture and visual-direction reference, not a
  specification for every screen.
- A screen may introduce a local composition, but a new reusable component or interaction pattern
  needs a design-system update or an explicit human decision.
- Do not change PRD scope, ADRs, Event Model structure, API contracts, or implementation code as a
  side effect of designing the UI.
- If the source artifact exposes a product or architecture gap, record it and hand it back to the
  appropriate human-gated stage.
- For a headless/API-only work item, do not invent a UI; document the absence of a screen and the
  caller-facing interaction contract instead.

## Expected output

Return:

- the wireframe/prototype path;
- the updated source artifact and its interaction contract;
- the states and actions covered;
- the design-system components or tokens used;
- open questions and any handoff needed to product or architecture design.
