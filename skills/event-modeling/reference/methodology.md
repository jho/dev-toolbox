# Event Modeling - Methodology Reference

This is the authoritative reference for the 7 steps and 4 patterns of Event Modeling
(Adam Dymitruk's method). Consult it while running any phase of the `event-modeling` skill.
Do not invent domain facts - use the Socratic prompts to extract them from the user.

## Core idea

An event model is a timeline of state changes told as a story. Information only moves
three ways:

1. Into the system via a command (a request to change state) -> produces an event.
2. Out of the system via a read model / view (a projection of past events) -> shown on a UI or
   consumed by an automation.
3. There is no other way for information to flow. Every box on the diagram is one of:
   UI screen, command, event, read model, or automation/processor.

Automations and translations are not exceptions to rule 1. They are reactions - a processor or
an adapter that wakes up, decides something must change, and issues a command. They never record
an event themselves. A reaction box always points at a command (in the next slice), and that
command produces the event. If you ever see a translation or automation wired straight to an
event, the model is wrong.

Events are immutable past-tense facts ("Order Placed", "Payment Captured"). They are the spine
of the model. Everything else hangs off the events.

The unit of delivery is a slice: a thin vertical cut through the swimlanes that delivers
one of the four patterns. A slice is what a developer implements and tests in isolation.

## The 4 patterns

Every slice is exactly one of these. In `em`, each maps to a specific shape (see `em-dsl.md`).

### 1. State Change (Command pattern)
UI -> Command -> Event. A user (or automation) submits a command; the system validates it
against invariants and records one or more events.

### 2. State View (View pattern)
Event(s) -> Read Model -> UI. Past events are projected into a read model that a screen
displays. Read-only; changes no state.

### 3. Automation (Processor pattern)
Read Model -> Processor -> (next slice) Command -> Event. The system reacts on its own: a
processor watches a read model and issues a command. It never records an event directly.

### 4. Translation
Boundary crossing -> command -> event. An adapter translates data across a boundary into the
model's own language. Like an automation, a translation is a reaction: it triggers a command,
never records an event directly. Two trigger forms:

- Externally triggered: external input -> translation -> command -> event. The trigger comes
  from outside the model, so the translation has no internal `from`.
- Internally triggered: read model -> translation -> command -> event. The translation reads a
  view via `from`.

## The 7 steps

Run them in order. The skill groups them into phases: discover = 1-4, model = 5-7, and a
dedicated slice phase deepens step 6 to implementation-ready specs.

### Step 1 - Brainstorm Events
List the domain events as past-tense facts, unordered at first.

### Step 2 - The Plot / Storyboard
Put the events in timeline order to form the narrative. Identify the personas (actors) and
sketch the UI screens that move the story forward.

### Step 3 - Inputs (Commands)
For each event, identify the command that causes it (State Change pattern). Name the intent,
not the outcome.

### Step 4 - Outputs (Read Models)
Identify the read models / views each UI and automation needs (State View pattern). Wire each
view to the events that feed it.

### Step 5 - Swimlanes & Apply the Patterns
Organize elements into swimlanes and classify every slice as one of the 4 patterns. Split every
automation and every translation across two slices.

### Step 6 - Elaborate Scenarios
For each slice, write Given / When / Then scenarios and surface invariants, critical fields,
and alternate / error flows.

### Step 7 - Evaluate Completeness
Walk the whole model with stakeholders and check for loose ends: every command produces an
event, every view has a source, every event is shown or consumed, every UI is reachable, and
automations / translations are split correctly.

## Socratic stance

- Ask one focused question at a time.
- Prefer why, what if, who, what must always be true, and how do you know.
- Mirror the model back after each increment and re-render so the team sees it evolve.
- Park unresolved questions in the state file instead of guessing.
- Name things crisply: events past-tense, commands imperative, views as the thing-shown.

