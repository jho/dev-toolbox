#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target_root="${1:-$codex_home/skills}"

mkdir -p "$target_root"

for skill_dir in "$repo_root"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  dest_dir="$target_root/$skill_name"
  mkdir -p "$dest_dir"
  rsync -a --exclude '.DS_Store' "$skill_dir/" "$dest_dir/"
done

printf 'Synced skills from %s to %s\n' "$repo_root/skills" "$target_root"

