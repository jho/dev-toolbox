# ai-toolbox

Personal repository for reusable AI workflow assets.

This repo is intended to hold:

- role definitions for generic SDLC sub-agents
- reusable skills
- Codex plugins
- MCP server definitions
- helper scripts and templates

The initial role model is intentionally compressed:

- `product-manager`
- `architect`
- `planner`
- `developer`
- `tester`
- `release-manager`

The first mirrored skill is `event-modeling`, adapted to stay generic and reusable.

The role definitions are designed to align with the agentic SDLC model in `~/dev/architecture`, while staying generic enough to reuse outside that repo.

## Repo layout

```text
ai-toolbox/
  roles/
  skills/
  plugins/
  mcp/
  scripts/
  references/
```

See [skills/README.md](skills/README.md) for the current skill index.

## Principles

- Keep role specs short and portable.
- Keep tool-specific packaging separate from the canonical role definitions.
- Avoid secrets, private URLs, and company-specific workflow details in public content.
- Prefer generated wrappers over hand-maintained vendor-specific copies.
