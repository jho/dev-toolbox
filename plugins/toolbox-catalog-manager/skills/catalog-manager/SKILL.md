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

This plugin bundles the catalog manager skill for Codex-facing use.

## Core behavior

- Treat the catalog as the source of truth for AI-managed tools.
- When the user says "add this to my plugin catalog", update the catalog entry first.
- Do not guess missing install details. Park unknowns in `notes` or ask one focused question.
- Keep `em` as the first non-marketplace example because it proves the vendored path.

## Workflow

1. Read `catalog/plugins.yaml`.
2. Confirm the target item and surface.
3. Update or add the catalog entry.
4. If the item is vendored, ensure the update script exists.
5. If the item is a plugin, make sure the plugin source path is recorded.
6. If the item is meant to be installed on Codex, record the marketplace-based install command.
7. If the item is meant to be installed on Claude, record the Claude plugin install command.
8. If anything is ambiguous, park it in `notes` rather than inventing a flow.

## Current example entries

- `em`
- `toolbox-catalog-manager`
