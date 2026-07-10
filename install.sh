#!/usr/bin/env bash
set -euo pipefail

repo_url="${AI_TOOLBOX_REPO_URL:-https://github.com/jho/ai-toolbox.git}"
repo_ref="${AI_TOOLBOX_REPO_REF:-main}"

usage() {
  cat <<'EOF'
Usage: install.sh [--surface auto|codex|claude] [--target PATH] [--verify]

Install the toolbox skills into a Codex or Claude skills directory.

Defaults:
  --surface auto    -> prefer Codex when ~/.codex exists, otherwise Claude when ~/.claude exists
  --surface codex   -> $CODEX_HOME/skills or ~/.codex/skills
  --surface claude  -> $CLAUDE_HOME/skills or ~/.claude/skills

If run outside a cloned checkout, the script clones the toolbox repo into a temporary directory
and installs from there. Override the remote with AI_TOOLBOX_REPO_URL and AI_TOOLBOX_REPO_REF.
Use --verify to print the installed skill directories after syncing.
EOF
}

target_root=""
surface="auto"
verify="false"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --surface)
      shift
      surface="${1:-}"
      ;;
    --target)
      shift
      target_root="${1:-}"
      ;;
    --verify)
      verify="true"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

install_from_repo() {
  local repo_root="$1"
  local target="$2"
  "$repo_root/scripts/sync-codex-skills.sh" "$target"
}

list_installed_skills() {
  local target="$1"
  find "$target" -mindepth 1 -maxdepth 1 -type d | sort | while read -r skill_dir; do
    basename "$skill_dir"
  done
}

resolve_target_root() {
  case "$1" in
    auto)
      if [ -n "${CODEX_HOME:-}" ] && [ -d "${CODEX_HOME:-}" ]; then
        printf '%s\n' "${CODEX_HOME}/skills"
      elif [ -d "$HOME/.codex" ]; then
        printf '%s\n' "$HOME/.codex/skills"
      elif [ -n "${CLAUDE_HOME:-}" ] && [ -d "${CLAUDE_HOME:-}" ]; then
        printf '%s\n' "${CLAUDE_HOME}/skills"
      elif [ -d "$HOME/.claude" ]; then
        printf '%s\n' "$HOME/.claude/skills"
      else
        printf '%s\n' "${CODEX_HOME:-$HOME/.codex}/skills"
      fi
      ;;
    codex)
      printf '%s\n' "${CODEX_HOME:-$HOME/.codex}/skills"
      ;;
    claude)
      printf '%s\n' "${CLAUDE_HOME:-$HOME/.claude}/skills"
      ;;
    *)
      printf 'Unknown surface: %s\n' "$1" >&2
      exit 1
      ;;
  esac
}

if [ -z "$target_root" ]; then
  target_root="$(resolve_target_root "$surface")"
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$script_dir/scripts/sync-codex-skills.sh" ]; then
  install_from_repo "$script_dir" "$target_root"
  if [ "$verify" = "true" ]; then
    printf 'Installed skills:\n'
    list_installed_skills "$target_root"
  fi
  exit 0
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

git clone --depth 1 --branch "$repo_ref" "$repo_url" "$workdir/ai-toolbox"
install_from_repo "$workdir/ai-toolbox" "$target_root"
if [ "$verify" = "true" ]; then
  printf 'Installed skills:\n'
  list_installed_skills "$target_root"
fi
