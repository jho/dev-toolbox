#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
default_home="${CODEX_HOME:-$HOME/.codex}"
target_root="${1:-$default_home/skills}"

mkdir -p "$target_root"

for skill_dir in "$repo_root"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  dest_dir="$target_root/$skill_name"
  mkdir -p "$dest_dir"
  cp -R "$skill_dir"/. "$dest_dir"/
done

for vendor_dir in "$repo_root"/vendor/*/; do
  [ -d "$vendor_dir" ] || continue
  vendor_skills_dir="$vendor_dir/.claude/skills"
  [ -d "$vendor_skills_dir" ] || continue
  for skill_dir in "$vendor_skills_dir"/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    dest_dir="$target_root/$skill_name"
    mkdir -p "$dest_dir"
    cp -R "$skill_dir"/. "$dest_dir"/
  done
done

printf 'Synced skills from %s and vendor packages to %s\n' "$repo_root/skills" "$target_root"
