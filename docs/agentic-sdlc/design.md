# Agentic SDLC Design

This document describes the design behind the reusable agentic SDLC assets. For the human-facing
quick start, see [README.md](README.md).

## Operating model

The human is the top-level orchestrator and decision owner. Roles provide focused expertise; they do
not create autonomous ownership or bypass approval gates.

```text
PLAN:    product-manager ↔ human → architect ↔ human → tech-lead ↔ human
EXECUTE: developer → tester → release-manager
```

Planning roles use Socratic interview flows and pause at decision boundaries. Execution roles use
approved artifacts and continue until they finish, fail validation, or hit a genuine blocker.

The default delivery unit is one coherent input through one focused pull request. Issues are useful
durable backlog records, but they are not required to become an extra agent handoff.

## Harness contract

The role files are portable definitions, not an orchestration engine. A Codex, Claude Code, or
project-specific harness owns conversation state, permissions, context selection, approvals, and
delegation.

For each sub-agent run, provide a small context packet:

```text
Objective: the question this specialist must answer
Source of truth: paths or URLs the specialist may rely on
Constraints: accepted product, architecture, policy, and scope boundaries
Allowed changes: artifacts this run may create or edit
Expected output: artifact, decision, review, or plan
Stop conditions: unresolved questions that require the human or another role
```

The harness should select the role, pass only relevant artifacts, review the result, and decide
whether to accept, revise, or hand off. `handoffs` in role frontmatter are routing suggestions; they
do not require a separate call. A listed skill is a procedure the role may load when applicable.

Native installation generates Codex agents under `~/.codex/agents` and Claude agents under
`~/.claude/agents`; it also syncs canonical and vendored skills.

## Planning contract

Planning agents must not silently turn exploration into a committed change. Each returns:

1. A reviewable artifact or proposed artifact change.
2. Decisions, assumptions, and open questions.
3. A suggested next-step prompt requesting approval.

Typical approval gates:

```text
PRD drafted. Shall I lock it in and ask the architect to resolve the identified dependency?

ADR drafted. Shall I lock it in and ask the tech lead to plan implementation?

Plan and tasks are ready. Shall I hand them to the developer for implementation?
```

After approval, pass the artifact paths and approval as the next context packet. Do not repeat the
interview.

### Product manager

Owns user problem, outcomes, scope, acceptance criteria, success measures, and non-goals. Uses
`creating-prd` or `updating-prd`. Identifies architecture dependencies but does not resolve them.

### Architect

Owns cross-cutting technical decisions and tradeoffs. Uses `creating-adr`. Records accepted ADRs
and extracts concise enforcement rules for the constitution or equivalent policy. Does not ratify an
unresolved question merely to unblock planning.

### Tech lead

Owns implementation-ready planning. Chooses the Event Model or conventional Spec Kit path, detects
missing decisions, and prepares boundaries, dependencies, tasks, and verification work. Does not
start implementation automatically.

## Execution contract

- `developer` implements approved plans and reports progress or blockers; it does not renegotiate
  scope.
- `tester` runs planned checks and reports evidence or failures; it does not redesign the feature.
- `release-manager` checks merge/release readiness; it does not resolve product or architecture
  questions.

If execution exposes a real decision gap, return to the appropriate planning role rather than
guessing.

## Planning paths

Event-modeled project:

```text
ratified Event Model
  → em slice
  → em-sdd-bridge
  → Spec Kit plan
  → Spec Kit tasks
```

The Event Model remains authoritative for commands, events, views, translations, automations, and
invariants. The bridge adds implementation context without creating a second domain model.

Conventional project:

```text
approved requirements or PRD
  → Spec Kit specify
  → Spec Kit plan
  → Spec Kit tasks
```

Do not invent Event Model artifacts for a project that does not use Event Modeling.

## Artifact ownership

| Question | Source of truth |
|---|---|
| User problem, promised behavior, and scope | PRD |
| Accepted technical choice and rationale | ADR |
| Normative implementation constraints | Constitution or engineering policy |
| Domain commands, events, views, and invariants | Event Model |
| Feature implementation approach | Spec Kit spec, plan, and tasks |
| Repository change and review | Pull request |

## Escalation rules

- Missing user intent → product manager or human orchestrator.
- Unresolved cross-cutting choice → architect.
- Event Model gap → tech lead and Event Modeling workflow.
- Task or implementation problem → developer.
- Failed acceptance criterion → developer, then tester again.
- Release or environment problem → release manager.

Agents preserve the current source of truth, state assumptions explicitly, and leave a reviewable
artifact at every meaningful decision boundary.
