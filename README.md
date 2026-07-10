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

## Install

Run `./install.sh` to sync the repo's skills into the current Codex or Claude skills directory.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jho/ai-toolbox/main/install.sh)"
```

To force a specific surface from a cloned repo:

```bash
./install.sh --surface codex
./install.sh --surface claude
```

To verify what was installed:

```bash
./install.sh --verify
```

## Principles

- Keep role specs short and portable.
- Keep tool-specific packaging separate from the canonical role definitions.
- Avoid secrets, private URLs, and company-specific workflow details in public content.
- Prefer generated wrappers over hand-maintained vendor-specific copies.
