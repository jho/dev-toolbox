---
name: designing-api-contract
description: Design a system-organized application API contract from approved Event Model, Spec Kit, or conventional requirements artifacts. Use this whenever a project needs TypeSpec, OpenAPI, REST, MCP, or transport contracts designed or updated, especially when domain/spec contracts must be mapped to HTTP operations without duplicating their models.
metadata:
  short-description: Design system-organized API bindings
---

# Designing API Contracts

Design the application-facing API contract from an approved source of product and domain truth.
Keep the domain/spec contract and the transport contract related but separately owned.

The output is an authored, system-organized API specification—usually TypeSpec—and its generated
OpenAPI artifact. The binding maps application operations to approved source artifacts; it does not
pretend that a domain command is automatically an HTTP route.

## Inputs

Identify the source mode before editing:

- Event Modeled: the relevant `.em` model, slice documents, and generated public contract.
- Spec Kit: the approved feature/specification and project API conventions.
- Conventional: the approved requirements, design document, or issue plus existing API rules.

Also locate:

- the TypeSpec or API source root and compiler configuration;
- generated OpenAPI/client artifacts and their drift checks;
- authentication, authorization, error, pagination, and MCP conventions;
- the system, bounded-context, or namespace ownership map.

If the source artifact or operation ownership is ambiguous, stop and record the gap. Do not invent
routes or domain behavior to make the contract compile.

## Source ownership

Keep these layers distinct:

1. Generated domain/spec contracts own approved commands, events, views, schemas, or requirements.
   Never hand-edit generated files.
2. System API bindings own HTTP routes, verbs, request/response transport shapes, auth policy,
   errors, pagination, async behavior, and MCP exposure metadata.
3. OpenAPI and client artifacts are generated outputs. Never hand-edit them.

When an Event Model project is present, run its generator first—for example,
`em api generate <model>.em`—then import the generated contract into the system binding. When a
project uses another source format, use that project's generated or approved contract instead.

For EM 1.22 or newer, prefer the bindable generated shape:

- use generated formatted scalars such as `Uuid` instead of redeclaring identifier types;
- extend the generated `Commands` and `Views` interfaces when their public operation set matches
  the application boundary;
- redeclare inherited operations with HTTP decorators and transport projections as needed;
- derive request projections from generated command payload models (for example,
  `OmitProperties<CreateThing, "ownerId">` when the owner comes from the authenticated principal);
- use TypeSpec augment decorators for field-level transport metadata instead of copying generated
  models.

Do not expose unrelated generated commands merely to satisfy interface inheritance. If the public
HTTP boundary intentionally combines or branches domain operations, keep those commands internal
to the application translation and use an explicit binding interface with traceable mappings.
Projects on older EM versions should preserve the same ownership and mapping rules, but may need
named handwritten projections until the generated contract supports payload models and bindable
interfaces.

## Workflow

### 1. Build the system inventory

Group operations by system or bounded context, not by technical layer or one flat API file. Record
for each candidate operation:

| Field | Question |
| --- | --- |
| System | Which domain/system owns this capability? |
| Source | Which approved model, slice, feature, or requirement defines it? |
| Intent | Is it a resource read, CRUD mutation, domain command, search, or workflow? |
| Caller | Web client, MCP, worker, integration, or another system? |
| Scope | What principal, tenant, account, or resource scope applies? |

Create one binding entry point per system when the project convention supports it. For a new
TypeSpec project, prefer a self-contained system directory such as
`typespec/<system>/main.tsp`; keep the repository-level `typespec/main.tsp` as the assembly entry
point and shared definitions in common files directly under `typespec/`. Group operations in
named TypeSpec interfaces rather than leaving operations at namespace scope. When a generated
contract exposes an interface in the same namespace, extend it and redeclare operations where
HTTP decorators or transport projections are required. Follow the project's existing layout when
it uses another naming convention.

### 2. Map operations to source behavior

For every operation, identify the source operation explicitly:

- Event Model: model, slice, command/view, and resulting event or read model.
- Spec Kit: feature/spec section, scenario, or approved API requirement.
- Conventional: requirement/design reference and owning capability.

Put the mapping next to the operation in the binding using the project's supported documentation or
metadata convention. A mapping is traceability; it is not a claim that the HTTP operation has the
same signature as the domain operation.

If one HTTP operation branches to multiple domain commands—for example, one OAuth callback that
routes to signup or authentication—document the branch condition and each command. If no clean
source mapping exists, return the operation as a design gap instead of silently creating a new
domain concept.

### 3. Choose direct reuse or a transport projection

Reuse an imported source model directly when its shape and semantics are appropriate for the API.

Create an explicit named request or response projection when transport concerns differ, such as:

- deriving `userId` from the authenticated session instead of accepting it from the client;
- returning a resource after a command whose domain operation has no response body;
- hiding provider subjects, credentials, internal fields, or event metadata;
- adding pagination, envelopes, problem details, or HTTP-only status information.

Name projections after their transport purpose, not after a database table. Document why the
projection exists and which source shape it maps to. Do not create a duplicate model merely to
rename an identical domain view.

### 4. Apply API conventions

Use the project's accepted API standards. If none exist, surface the decision rather than silently
choosing a style. At minimum, resolve:

- plural resource paths and versioning;
- HTTP verbs and status codes;
- typed partial updates versus replacement;
- authentication and authorization scope;
- stable error/problem-details shapes;
- pagination, filtering, and sorting for collections;
- idempotency and async command behavior;
- MCP capability, audience, confirmation, and exposure rules.

Do not expose every event, aggregate, view, or internal operation automatically. Expose a capability
only when the product and security boundary authorize it.

### 5. Compile and validate

Run the repository's equivalent of all applicable checks:

- source-model validation and generated-contract freshness;
- TypeSpec compilation;
- OpenAPI generation and schema validation;
- generated-artifact drift comparison;
- linting/formatting and contract tests where the project requires them.

Never fix generated-artifact failures by editing the generated output. Change the source model,
binding, or compiler configuration and regenerate.

## Expected output

Return:

- the system-organized binding files and source references;
- an operation mapping table or equivalent per-operation documentation;
- direct-reuse and transport-projection decisions;
- auth, error, pagination, async, and MCP behavior;
- generated OpenAPI/client artifact paths and validation commands;
- unresolved mapping or architecture questions;
- a handoff stating whether the API design is ready for planning or needs human decisions.

## Worked example

An Event Model project may have this generated domain contract:

```tsp
namespace Accounts;

@format("uuid") scalar Uuid extends string;

model CreateAccount {
  ownerId: Uuid;
  name: string;
}

interface Commands {
  op createAccount(payload: CreateAccount): void;
}

model Account {
  id: string;
  name: string;
  status: string;
}
```

The system binding imports that contract and defines the actual HTTP API:

```tsp
namespace Accounts {
  model CreateAccountRequest is OmitProperties<CreateAccount, "ownerId">;

  /**
   * HTTP bindings extend the generated domain operation set, then redeclare operations where
   * HTTP decorators or transport projections are required.
   */
  @route("/v1")
  interface HttpApi extends Commands {
    /**
     * EM mapping:
     * - System: accounts
     * - Slice: create-account
     * - Command: Commands.createAccount
     * - Projection: ownerId comes from the authenticated principal
     * - Result: Account
     */
    @route("/accounts")
    @post
    op createAccount(
      @body body: CreateAccountRequest
    ): Account;
  }
}
```

This is a valid binding because the HTTP interface extends the generated `Commands` interface while
making the transport projection explicit. The application layer still adapts the authenticated
principal and returns the resulting read model; interface inheritance provides contract linkage,
not runtime implementation.
