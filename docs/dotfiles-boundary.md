# Dotfiles Boundary

This repo is `dev-toolbox`. Your private dotfiles repo should stay responsible for machine state and
security-sensitive configuration, while `dev-toolbox` owns reusable workflow assets.

## Keep In Dotfiles

- Shell startup and `PATH`
- Shell aliases and functions that are personal but not reusable assets
- Git identity and signing config
- SSH config and keys
- OS defaults and desktop preferences
- Secret environment variables
- Auth helpers and credential wiring
- Private host-specific configuration
- Terminal/editor launch behavior
- Any bootstrap logic that assumes the private repo already exists

## Move To Dev-Toolbox

- Tool installers and updaters
- Reusable developer scripts
- AI skills
- Codex or Claude plugins
- Catalog/index of skills and plugins
- Vendored tools like `em`
- Task runners and helper wrappers
- Templates and snippets
- Public-safe shell fragments
- Optional generated bootstrap pieces that are safe to share

## Optional Shared Contract

The contract should be one-way:

- `dev-toolbox` may emit a small, public-safe shell fragment or install helper
- dotfiles may source that fragment if it exists
- dotfiles must not be required for `dev-toolbox` to work

Recommended examples of shared contract files:

- `~/.local/share/dev-toolbox/env.sh`
- `~/.local/share/dev-toolbox/path.sh`
- `~/.local/share/dev-toolbox/bin/dev-toolbox`

## Rule Of Thumb

- If it configures the machine, keep it in dotfiles.
- If it configures the workflow, keep it in `dev-toolbox`.
- If it is safe to share and useful to source later, emit it from `dev-toolbox` and consume it from
  dotfiles optionally.
