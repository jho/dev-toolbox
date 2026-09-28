# dev-toolbox

Personal repository for reusable developer workflow assets, including AI tooling.

This repo is intended to hold:

- role definitions for generic SDLC sub-agents
- reusable skills
- Codex plugins
- MCP server definitions
- helper scripts and templates

The role model is intentionally compressed:

- `product-manager`
- `architect`
- `tech-lead`
- `developer`
- `tester`
- `release-manager`

## Repo layout

```text
dev-toolbox/
  roles/
  skills/
  plugins/
  catalog/
  mcp/
  scripts/
  references/
```

See [skills/README.md](skills/README.md) for the current skill index.
See [plugins/README.md](plugins/README.md) for the current plugin source index.
See [docs/vendoring.md](docs/vendoring.md) for the subtree + dependency pattern.
See [docs/dotfiles-boundary.md](docs/dotfiles-boundary.md) for what stays in dotfiles vs dev-toolbox.
See [catalog/README.md](catalog/README.md) for the dev-toolbox catalog.

## Agentic SDLC

The toolbox provides a lightweight Plan → Execute workflow for human-orchestrated sub-agents:
interactive product, architecture, and tech-lead planning followed by developer, tester, and
release execution. Start with the [agentic SDLC usage guide](docs/agentic-sdlc/README.md); the
[design reference](docs/agentic-sdlc/design.md) explains the underlying harness contract.

The roles are designed to be used as focused sub-agents under a human-orchestrated harness. The
portable definitions are synced into native Codex or Claude agent directories; their `skills` and
`handoffs` metadata describe capabilities and suggested routing, while the harness retains control
of context, permissions, approvals, and delegation. See the usage guide for the context-packet
contract and examples.

## Install

Run `./install.sh` to sync the repo's skills into the current Codex or Claude skills directory.
It also installs a `dev-toolbox` helper into `~/.local/bin` by default and keeps
`ai-toolbox` as a compatibility alias.
`dev-toolbox update` resyncs the skills and runs any vendored dependency hooks.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jho/dev-toolbox/main/install.sh)"
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

After install, use:

```bash
dev-toolbox update
```

You can override the helper install location with `DEV_TOOLBOX_COMMAND_DIR`
or the legacy `AI_TOOLBOX_COMMAND_DIR`.
The installer also writes shell fragments under `~/.local/share/dev-toolbox/`; private dotfiles
can source those to prepend `~/.local/bin` ahead of Homebrew and other system bins so the
toolbox-installed `em` is the one that gets picked up.

The repo uses `mise` for task orchestration around sync and subtree updates.

To refresh the vendored `em` subtree from upstream:

```bash
./scripts/upgrade-em.sh
```

The first catalog examples are:

- `em` for the vendored non-marketplace path
- `toolbox-catalog-manager` for the catalog-management plugin example

## Principles

- Keep role specs short and portable.
- Keep tool-specific packaging separate from the canonical role definitions.
- Avoid secrets, private URLs, and company-specific workflow details in public content.
- Prefer generated wrappers over hand-maintained vendor-specific copies.
