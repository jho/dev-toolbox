# AGENTS.md

## Purpose

This repository contains reusable AI workflow assets: skills, roles, plugins,
vendored tools, catalogs, scripts, and documentation.

Keep additions portable, concise, public-safe, and useful across projects.

## Before making changes

- Read `README.md` and relevant directory documentation.
- Preserve unrelated user changes.
- Prefer extending an existing pattern before adding a new one.
- Keep secrets, credentials, private URLs, and machine-specific configuration out
  of reusable assets.

## Adding skills

Follow the [skill authoring standards and best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

Repository-specific requirements:

- Put canonical skills under `skills/<skill-name>/SKILL.md`.
- Update `skills/README.md` when adding or removing a skill.
- Put references and supporting material beside the skill.
- Add an executable `deps.sh` beside a skill when it requires dependencies.
- Keep packaged copies synchronized with their canonical source.

## Adding plugins

- Put plugin source under `plugins/<plugin-name>/`.
- Include `.codex-plugin/plugin.json`.
- Record the plugin in `catalog/plugins.yaml`.
- Keep install and update commands explicit for each supported surface.
- Update `plugins/README.md` when adding or removing a plugin.

## Vendored tools

- Put upstream source under `vendor/<name>/`.
- Add a local wrapper or skill under `skills/` or `plugins/`.
- Add `scripts/upgrade-<name>.sh` for upstream refreshes.
- Add dependency installation through a discovered `deps.sh` hook.
- Do not modify vendored code unless the change is intentionally maintained as
  part of the vendored snapshot.

## Validation

Before handing off changes:

- Run the configured pre-commit hooks.
- Run relevant dependency, rendering, or tool checks when practical.
- Review `git diff` and confirm generated or vendored files are intentional.
- Update documentation and catalog metadata when repository structure changes.

## Change boundaries

- Keep reusable workflow assets in this repository.
- Keep machine-specific configuration and security-sensitive wiring in dotfiles.
- Avoid broad refactors or unrelated cleanup.
- Do not claim external installation, publishing, or service updates unless they
  actually succeeded.
