# Agentic SDLC Workflow

This toolbox supports a lightweight, agent-assisted software delivery loop. The human remains the
top-level orchestrator and decision owner. Agents provide focused expertise, produce reviewable
artifacts, and hand work to the next phase when appropriate.

```text
Design → Plan → Implement → Test → Release
             ↑             │
             └─────────────┘
```

The loop is intentionally small. A normal run should produce one coherent change and one focused
pull request rather than forcing every step through a separate ticket or agent conversation.

## Roles

### Product manager

Answers: “What problem are we solving, for whom, and why?”

The product manager frames user value, scope, acceptance criteria, success measures, and non-goals.
Product decisions belong in the product requirements artifact and should not be hidden in an ADR.

### Architect

Answers: “What cross-cutting technical decisions must support this?”

The architect resolves architecture questions, researches meaningful tradeoffs, and records accepted
decisions in ADRs. The constitution or equivalent engineering policy should contain only the concise
rules that future planning and implementation must enforce.

### Tech lead

Answers: “How does this become an implementation-ready feature?”

The tech lead chooses the planning path, defines implementation boundaries, and produces the Spec Kit
artifacts used by development. The tech lead may also coordinate design review when the work crosses
multiple contexts or capabilities.

### Developer

Answers: “How do we implement the approved plan safely?”

The developer works from approved requirements, decisions, and tasks; makes focused changes; runs
targeted validation; and opens the implementation pull request. The developer should surface new
product or architecture questions instead of silently deciding them.

### Tester

Answers: “Does the result satisfy the requirements and remain safe to trust?”

The tester validates acceptance criteria, edge cases, regressions, and relevant architecture or
operational contracts. Failures loop back to development with concrete evidence.

### Release manager

Answers: “Is the change ready to merge and close out?”

The release manager confirms CI and review readiness, coordinates merge or deployment, verifies the
result, and closes the delivery loop.

## Design paths

The user’s initial input determines which specialist is needed first.

### Product-driven work

```text
User problem
  → product manager
  → product requirements and acceptance criteria
  → tech lead
```

Example:

> “Users need a faster way to approve a submitted request.”

The product manager clarifies the users, workflow, success criteria, and scope. Once the product
intent is clear, the tech lead designs the implementation path.

### Architecture-driven work

```text
Architecture question
  → architect
  → research and decision record
  → implementation context
  → tech lead
```

Example:

> “The system needs to support multiple notification providers without coupling the domain to one vendor.”

The architect compares the meaningful alternatives, records the accepted boundary, and updates the
engineering policy that future plans must follow.

Product and architecture work may both be needed. The human orchestrator decides which question must
be resolved first.

## Planning paths

The tech lead selects one of two planning paths.

### Event-modeled project

When a canonical Event Model exists:

```text
Ratified Event Model
  → elaborate and slice with em
  → implementation-ready slice document
  → em-sdd-bridge
  → Spec Kit plan and tasks
```

The Event Model remains authoritative for commands, events, views, translations, automations, and
invariants. The slice document is the feature specification; Spec Kit adds implementation planning
without becoming a second domain model.

### Conventional project

When no Event Model exists:

```text
Approved requirements or PRD
  → Spec Kit specification
  → plan
  → tasks
```

The tech lead should not invent Event Model artifacts merely to satisfy the workflow. Conventional
Spec Kit planning is a supported first-class path.

## Artifact ownership

Keep each question in its appropriate source of truth:

| Question | Artifact |
|---|---|
| What user problem and behavior are in scope? | Product requirements / PRD |
| What technical choice and tradeoff was accepted? | ADR |
| How must future work comply with an accepted architecture choice? | Constitution or engineering policy |
| What domain behavior, commands, events, and views exist? | Event Model |
| How will one feature be implemented? | Spec Kit specification, plan, and tasks |
| What changed in the repository? | Pull request |

Do not use an ADR to pre-decide an unresolved question. Do not copy an entire ADR into the
constitution. Do not let implementation tasks silently change product intent.

## Delivery loop

The default delivery unit is one coherent input through one focused pull request:

```text
Input
  → design artifact(s)
  → approved plan/tasks
  → implementation
  → validation
  → pull request
  → merge and closeout
```

Backlog issues are useful durable records for prioritization, dependencies, and discussion, but they
are not required to become an extra handoff between agents. Link a pull request to the relevant
issue when the project uses issue tracking, and close it only when the acceptance criteria are met.

## Feedback and escalation

- Missing user intent goes to the product manager or back to the human orchestrator.
- An unresolved cross-cutting technical choice goes to the architect.
- An Event Model gap goes to the tech lead and modeling workflow.
- A task or implementation problem goes to the developer.
- A failed acceptance criterion loops from tester to developer.
- A release or environment problem goes to the release manager.

Agents should preserve the current source of truth, state assumptions explicitly, and leave a
reviewable artifact at each meaningful decision boundary.
