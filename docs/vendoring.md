# Vendoring Pattern

This repo treats upstream tools and skills as vendored sources plus local wrappers.

## Principles

- Keep the canonical repo content in a subtree under `vendor/`.
- Keep toolbox-facing entrypoints in `skills/`, `plugins/`, `scripts/`, and `README.md`.
- Use `dev-toolbox update` to resync local skills and run dependency hooks.
- Use `scripts/upgrade-*.sh` to refresh vendored subtrees from upstream.
- Use `mise` to expose repo tasks, not as the package store itself.

## Current example

- `vendor/em` is the vendored upstream `milehimikey/em` repo.
- `skills/event-modeling/` is the toolbox-facing overlay that teaches Codex how to use `em`.
- `skills/event-modeling/deps.sh` builds the vendored subtree and installs the `em` CLI.
- `scripts/upgrade-em.sh` refreshes the subtree from upstream.
- `catalog/plugins.yaml` records the first vendored and plugin catalog examples.

## Future vendored plugins or skills

If a vendored asset has dependencies:

1. Put the upstream source in `vendor/<name>`.
2. Add a `deps.sh` next to the skill or plugin wrapper.
3. Let `scripts/run-deps.sh` discover and run the hook.
4. Add a matching `scripts/upgrade-<name>.sh` for subtree refreshes.

This keeps the install path consistent:

```text
upstream subtree -> local overlay -> dev-toolbox update -> dependency hooks -> installed tool
```
