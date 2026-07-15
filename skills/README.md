# Skills

Canonical reusable skills live here.

Current skills:

- [event-modeling](event-modeling/SKILL.md)
- [catalog-manager](catalog-manager/SKILL.md)
- [creating-prd](creating-prd/SKILL.md)

## Notes

- Keep each skill self-contained.
- Put reusable references in `reference/` or `references/`.
- Put templates in `templates/`.
- Prefer repo-local source of truth, then sync into `~/.codex/skills` for Codex use.
- If a skill needs dependencies, add an executable `deps.sh` beside it so `dev-toolbox update`
  can install them during sync.
- If a skill is vendored from upstream, keep the upstream source under `vendor/` and refresh it
  with a dedicated `scripts/upgrade-*.sh` helper.
