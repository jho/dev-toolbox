---
name: catalog-manager
description: >-
  Manage the dev-toolbox catalog of skills, plugins, vendored tools, and install/update flows.
  Use when the user wants to add something to the catalog, review what is installed, record how a
  skill or plugin should be installed on Codex or Claude, or update catalog metadata for a vendored
  asset. Prefer editing `catalog/plugins.yaml` as the source of truth and keep install/update
  commands explicit.
---

# Catalog Manager

This skill manages the toolbox catalog in `catalog/plugins.yaml`.

## Core behavior

- Treat the catalog as the source of truth for AI-managed tools.
- When the user says "add this to my plugin catalog", update the catalog entry first.
- Do not guess missing install details. Park unknowns in `notes` or ask one focused question.
- Prefer short, explicit entries over clever abstractions.
- Keep `em` as the first non-marketplace example because it proves the vendored path.

## Catalog shape

Each entry should record:

- `name`
- `kind`
- `description`
- `surfaces`
- `source`
- `install`
- `update`
- `status`
- `notes`

Use these source types:

- `subtree` for vendored upstream code
- `local` for repo-local plugin or skill sources
- `marketplace` for Codex marketplace-backed plugins
- `remote` for tools that are not yet vendored or local

## Workflow

1. Read `catalog/plugins.yaml`.
2. Confirm the target item and surface.
3. Update or add the catalog entry.
4. If the item is vendored, ensure the update script exists.
5. If the item is a plugin, make sure the plugin source path is recorded.
6. If the item is meant to be installed on Codex, record the marketplace-based install command.
7. If the item is meant to be installed on Claude, record the Claude plugin install command.
8. If anything is ambiguous, park it in `notes` rather than inventing a flow.

## Defaults

- For vendored items, prefer `dev-toolbox update` as the user-facing sync command.
- For upstream refreshes, prefer a dedicated `scripts/upgrade-<name>.sh`.
- For plugin packaging, keep the source path local and explicit.
- For cross-surface catalog items, record both Codex and Claude install commands when known.

## Current example entries

- `em`
- `toolbox-catalog-manager`
