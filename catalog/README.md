# Catalog

This directory is the source of truth for dev-toolbox-managed tools and installable assets.

## Purpose

- Track skills, plugins, vendored tools, and their install/update surfaces.
- Keep one canonical place to answer "what do I have?" and "how do I install it?"
- Drive repo-local automation without hardcoding every tool into shell scripts.

## Current entries

- `em` - first non-marketplace example; vendored from upstream and installed via `dev-toolbox update`
- `toolbox-catalog-manager` - catalog manager plugin example for Codex and Claude flows

## Conventions

- Keep entries short and explicit.
- Record the source of truth for each item.
- Record the install command for each surface when it differs.
- Record the update command or script when updates are not automatic.
- Prefer machine-readable YAML so assistants can edit the catalog safely.
