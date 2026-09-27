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

## Using the roles in a harness

The role files are portable agent definitions, not an orchestration engine. A harness—Codex,
Claude Code, or a project-specific runner—owns the conversation, permissions, context selection,
approval gates, and delegation. The role provides the specialist lens and the skills it should use.

Install or refresh the native agents and skills with:

```bash
./install.sh --surface codex
# or
./install.sh --surface claude

dev-toolbox update
```

The sync step generates Codex agents under `~/.codex/agents` and Claude agents under
`~/.claude/agents`. It also copies the canonical skills and vendored Event Modeling skill into the
corresponding skills directory. A local checkout can sync agents directly with
`scripts/sync-agents.sh` when a harness uses a custom target directory.

### Harness responsibilities

For each sub-agent run, the orchestrator should provide a small context packet:

```text
Objective: the question this specialist must answer
Source of truth: paths or URLs the specialist may rely on
Constraints: accepted product, architecture, policy, and scope boundaries
Allowed changes: the artifacts this run may create or edit
Expected output: artifact, decision, review, or plan
Stop conditions: unresolved questions that require the human or another role
```

Then the harness should:

1. Select the role whose responsibility matches the current question.
2. Give it the context packet and the relevant artifacts—not the entire project by default.
3. Let it use the skills named by that role.
4. Review the returned artifact, assumptions, and open questions.
5. Decide whether to accept the result, ask for revision, or invoke the next role.

The `handoffs` in role frontmatter are routing suggestions for the harness. They do not make an
agent autonomous, grant extra permissions, or require a separate sub-agent call. Likewise, a skill
listed by a role is a reusable procedure the agent may load when applicable; it is not a promise
that every host has that skill installed. The harness should stop when a product or architecture
decision needs human acceptance.

### Recommended one-input run

For normal feature work, keep the orchestration shallow:

```text
human input
  → product-manager or architect
  → optional second design role
  → tech-lead
  → developer
  → tester
  → release-manager or human merge
```

Most phases can run as one sub-agent invocation with a focused output. Use another invocation when
the artifact needs revision or when the work crosses a decision boundary; do not split every bullet
into its own agent.

## Worked examples

These examples show the shape of a real run. The exact native invocation syntax varies by host, but
the role, context packet, artifact, and handoff stay the same.

### Example 1: Product request with an architecture dependency

Human input:

> “The system must allow users to sign in without creating a password.”

The harness invokes `product-manager` with the existing PRD path and asks:

```text
Turn this request into a PRD update.
Capture the user journey, supported sign-in behavior, acceptance criteria, MVP exclusions,
and success measure. Do not choose an identity provider or session architecture.
Return the PRD diff and list any architecture dependencies separately.
```

Expected product-manager output:

```text
Artifact: docs/prds/account-access.md
Product decisions: passwordless sign-in is in scope; account recovery and provider-specific
behavior are defined at the product level.
Architecture dependency: choose the identity-provider boundary, callback/session handling,
and account-linking strategy.
Open product question: none.
```

The harness presents the accepted PRD and dependency list to `architect`:

```text
Using the attached PRD update, create the smallest ADR needed for passwordless authentication.
Compare realistic alternatives, record the accepted boundary and consequences, and state the
constitution rules future features must follow. Do not expand the product scope.
```

After the human accepts the PRD and ADR, the harness invokes `tech-lead`:

```text
Plan this feature using the accepted PRD and ADR.
This project does not use Event Modeling, so use the conventional Spec Kit path:
specify → plan → tasks. Return implementation boundaries, dependencies, and verification work.
```

The resulting flow is:

```text
human request
  → product-manager: PRD update + architecture dependency
  → architect: accepted ADR
  → tech-lead: spec, plan, tasks
  → developer: implementation PR
  → tester: acceptance and regression evidence
```

The product manager identifies the architectural question, the architect resolves it, and the tech
lead consumes both decisions. No role silently makes a decision owned by another role.

### Example 2: Event Model slice to implementation plan

Assume the project already has a ratified Event Model and the user says:

> “Implement the slice where a user confirms a suggested category for a transaction.”

The harness gives `tech-lead` the model path, slice inventory, relevant PRD, and accepted ADRs:

```text
Select and detail the Event Model slice for confirming a suggested transaction category.
Use em to produce the implementation-ready slice document. Preserve the model's command,
event, views, invariants, and alternate paths. Do not invent new domain behavior.
```

The tech lead then runs the bridge with the selected slice:

```text
Bridge this ratified slice into the project's Spec Kit workflow.
Carry commands, events, projections/views, translations or automations, invariants, scenarios,
and failure paths into planning context. Link the governing PRD and ADRs, then produce the inputs
for speckit-plan and speckit-tasks.
```

Expected handoff packet:

```text
Slice: slices/confirm-transaction-category.md
Spec Kit context: feature intent, command/event contract, projection requirements, invariants,
and test scenarios
Next: /speckit-plan, then /speckit-tasks
Blocked: none
```

The developer receives the generated plan and tasks—not a transcript of the modeling session—and
implements the slice. If the slice exposes a missing product rule or cross-cutting technical
choice, the tech lead stops and routes that question back to `product-manager` or `architect`.

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

Input in Codex:

> “The system must allow the user to log in with passwordless authentication.”

The product manager runs `/creating-prd` for a new product area, or `/updating-prd` when the
project already has a relevant PRD. The workflow clarifies users, behavior, acceptance criteria,
scope, and non-goals, then produces a reviewable PRD change and any needed product backlog issue.

The product manager also identifies architectural implications without resolving them. If the feature
requires a new cross-cutting technical decision, the flow continues through the architect before
planning:

```text
/creating-prd or /updating-prd
  → identify architecture dependencies
  → /creating-adr when a decision is needed
  → accepted PRD + ADR context
  → tech lead planning
```

For example, passwordless authentication may require product decisions about the sign-in experience
and an architecture decision about identity-provider integration, session handling, and account
mapping. Both artifacts should be accepted before implementation planning begins.

### Architecture-driven work

Input in Codex:

> “The system must support multiple notification providers without coupling the domain to one vendor.”

The architect uses `/listing-github-issues` to find or confirm the architecture backlog item, then
runs `/creating-adr`. That workflow researches the alternatives, records the accepted boundary,
updates the constitution or engineering policy, and opens one reviewable decision PR.

The tech lead then uses the accepted ADR as planning context; the ADR is not itself an implementation
plan.

The reusable role and skill surfaces for this flow are:

- `product-manager` → `creating-prd`, `updating-prd`
- `architect` → `creating-adr`
- `tech-lead` → `event-modeling`, `em-sdd-bridge`, and the Spec Kit planning skills

These are portable instructions, not autonomous ownership. The human orchestrator still decides
when a PRD or ADR is accepted and when work is ready to move to the next phase.

In a harness, the product-manager run should return two things: the PRD change and a short list of
architecture dependencies. The architect is invoked only for those dependencies. Once the PRD and
any required ADR are accepted, the tech-lead receives their paths as planning context rather than
reconstructing the prior conversations.

Product and architecture work may both be needed. The human orchestrator decides which question must
be resolved first.

## Planning paths

The tech lead selects one of two planning paths.

### Event-modeled project

When a canonical Event Model exists:

```text
Ratified Event Model
  → /event-modeling slice
  → implementation-ready slice document
  → /em-sdd-bridge
  → /speckit-plan
  → /speckit-tasks
```

The Event Model remains authoritative for commands, events, views, translations, automations, and
invariants. The slice document is the feature specification; Spec Kit adds implementation planning
without becoming a second domain model.

### Conventional project

When no Event Model exists:

```text
Approved requirements or PRD
  → /speckit-specify
  → /speckit-plan
  → /speckit-tasks
```

The tech lead should not invent Event Model artifacts merely to satisfy the workflow. Conventional
Spec Kit planning is a supported first-class path.

For either path, the developer uses `/speckit-implement` or the project’s equivalent implementation
workflow, then opens the focused pull request. The tester runs the relevant checks and sends failures
back to the developer; the release manager verifies CI and merges when ready.

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
