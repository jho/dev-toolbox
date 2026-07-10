#!/usr/bin/env bash
set -euo pipefail

repo_url="${AI_TOOLBOX_REPO_URL:-https://github.com/jho/ai-toolbox.git}"
repo_ref="${AI_TOOLBOX_REPO_REF:-main}"

usage() {
  cat <<'EOF'
Usage: install.sh [--surface codex|claude] [--target PATH]

Install the toolbox skills into a Codex or Claude skills directory.

Defaults:
  --surface codex   -> $CODEX_HOME/skills or ~/.codex/skills
  --surface claude  -> $CLAUDE_HOME/skills or ~/.claude/skills

If run outside a cloned checkout, the script clones the toolbox repo into a temporary directory
and installs from there. Override the remote with AI_TOOLBOX_REPO_URL and AI_TOOLBOX_REPO_REF.
EOF
}

target_root=""
surface="codex"

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

resolve_target_root() {
  case "$1" in
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
  exit 0
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

git clone --depth 1 --branch "$repo_ref" "$repo_url" "$workdir/ai-toolbox"
install_from_repo "$workdir/ai-toolbox" "$target_root"
