#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
surface="auto"
skills_target=""
codex_target=""
claude_target=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --surface) shift; surface="${1:-}" ;;
    --skills-target) shift; skills_target="${1:-}" ;;
    --codex-target) shift; codex_target="${1:-}" ;;
    --claude-target) shift; claude_target="${1:-}" ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; exit 1 ;;
  esac
  shift
done

if [ "$surface" = "auto" ]; then
  if [ -n "${CODEX_HOME:-}" ] && [ -d "${CODEX_HOME:-}" ]; then
    surface="codex"
  elif [ -d "$HOME/.codex" ]; then
    surface="codex"
  elif [ -n "${CLAUDE_HOME:-}" ] && [ -d "${CLAUDE_HOME:-}" ]; then
    surface="claude"
  else
    surface="claude"
  fi
fi

if [ "$surface" = "codex" ] || [ "$surface" = "both" ]; then
  if [ -z "$codex_target" ]; then
    if [ -n "$skills_target" ]; then
      codex_target="$(cd "$(dirname "$skills_target")" && pwd)/agents"
    else
      codex_target="${CODEX_HOME:-$HOME/.codex}/agents"
    fi
  fi
fi
if [ "$surface" = "claude" ] || [ "$surface" = "both" ]; then
  if [ -z "$claude_target" ]; then
    if [ -n "$skills_target" ]; then
      claude_target="$(cd "$(dirname "$skills_target")" && pwd)/agents"
    else
      claude_target="${CLAUDE_HOME:-$HOME/.claude}/agents"
    fi
  fi
fi

args=(--repo-root "$repo_root" --surface "$surface")
[ -n "$codex_target" ] && args+=(--codex-target "$codex_target")
[ -n "$claude_target" ] && args+=(--claude-target "$claude_target")
python3 "$repo_root/scripts/sync-agents.py" "${args[@]}"
