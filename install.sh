#!/usr/bin/env bash
set -euo pipefail

repo_url="${AI_TOOLBOX_REPO_URL:-https://github.com/jho/dev-toolbox.git}"
repo_ref="${AI_TOOLBOX_REPO_REF:-main}"
command_name="${AI_TOOLBOX_COMMAND_NAME:-dev-toolbox}"
command_dir="${AI_TOOLBOX_COMMAND_DIR:-$HOME/.local/bin}"
legacy_command_name="${DEV_TOOLBOX_LEGACY_COMMAND_NAME:-ai-toolbox}"

usage() {
  cat <<'EOF'
Usage: install.sh [--surface auto|codex|claude] [--target PATH] [--verify]

Install the dev-toolbox skills into a Codex or Claude skills directory.

Defaults:
  --surface auto    -> prefer Codex when ~/.codex exists, otherwise Claude when ~/.claude exists
  --surface codex   -> $CODEX_HOME/skills or ~/.codex/skills
  --surface claude  -> $CLAUDE_HOME/skills or ~/.claude/skills

If run outside a cloned checkout, the script clones the dev-toolbox repo into a temporary directory
and installs from there. Override the remote with AI_TOOLBOX_REPO_URL and AI_TOOLBOX_REPO_REF.
Use --verify to print the installed skill directories after syncing.

The installer also drops a small `dev-toolbox` command into $AI_TOOLBOX_COMMAND_DIR
by default, plus an `ai-toolbox` compatibility alias. Use `dev-toolbox update` to resync
skills without returning to the repo.
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

install_deps() {
  local repo_root="$1"
  "$repo_root/scripts/run-deps.sh"
}

install_command() {
  local repo_root="$1"
  local command_path="$2/$command_name"

  mkdir -p "$2"

  cat >"$command_path" <<EOF
#!/usr/bin/env bash
set -euo pipefail

repo_url="${repo_url}"
repo_ref="${repo_ref}"
embedded_repo_root="${repo_root}"
script_name="sync-codex-skills.sh"

usage() {
  cat <<'USAGE'
Usage: dev-toolbox update [--target PATH]

Resync the toolbox skills from the canonical source into a Codex or Claude skills directory.

Commands:
  update   Sync the repo's skills into the configured target directory.
  install  Alias for update.
  sync     Alias for update.
  help     Show this help.

Defaults:
  --target  \$CODEX_HOME/skills, then ~/.codex/skills, then \$CLAUDE_HOME/skills, then ~/.claude/skills
USAGE
}

resolve_target_root() {
  local target_root=""
  case "\${1:-auto}" in
    auto)
      if [ -n "\${CODEX_HOME:-}" ] && [ -d "\${CODEX_HOME:-}" ]; then
        target_root="\${CODEX_HOME}/skills"
      elif [ -d "\$HOME/.codex" ]; then
        target_root="\$HOME/.codex/skills"
      elif [ -n "\${CLAUDE_HOME:-}" ] && [ -d "\${CLAUDE_HOME:-}" ]; then
        target_root="\${CLAUDE_HOME}/skills"
      elif [ -d "\$HOME/.claude" ]; then
        target_root="\$HOME/.claude/skills"
      else
        target_root="\${CODEX_HOME:-\$HOME/.codex}/skills"
      fi
      ;;
    *)
      target_root="\$1"
      ;;
  esac

  printf '%s\n' "\$target_root"
}

run_sync() {
  local target_root="\$1"

  if [ -f "\$embedded_repo_root/scripts/\$script_name" ]; then
    "\$embedded_repo_root/scripts/\$script_name" "\$target_root"
    if [ -f "\$embedded_repo_root/scripts/run-deps.sh" ]; then
      "\$embedded_repo_root/scripts/run-deps.sh"
    fi
    return
  fi

  workdir="\$(mktemp -d)"
  trap 'rm -rf "\$workdir"' EXIT

  git clone --depth 1 --branch "\$repo_ref" "\$repo_url" "\$workdir/ai-toolbox" >/dev/null 2>&1
  "\$workdir/ai-toolbox/scripts/\$script_name" "\$target_root"
  if [ -f "\$workdir/ai-toolbox/scripts/run-deps.sh" ]; then
    "\$workdir/ai-toolbox/scripts/run-deps.sh"
  fi
}

subcommand="\${1:-update}"
shift || true

case "\$subcommand" in
  update|install|sync)
    target_root="\$(resolve_target_root "\${1:-auto}")"
    if [ "\${1:-}" = "--target" ]; then
      shift
      target_root="\$(resolve_target_root "\${1:-}")"
    fi
    run_sync "\$target_root"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    printf 'Unknown command: %s\n' "\$subcommand" >&2
    usage >&2
    exit 1
    ;;
esac
EOF

  chmod +x "$command_path"

  if [ "$command_name" != "$legacy_command_name" ]; then
    ln -sf "$command_name" "$2/$legacy_command_name"
  fi
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
installed_command_dir="$command_dir"

if [ -f "$script_dir/scripts/sync-codex-skills.sh" ]; then
  install_from_repo "$script_dir" "$target_root"
  install_deps "$script_dir"
  install_command "$script_dir" "$installed_command_dir"
  if [ "$verify" = "true" ]; then
    printf 'Installed skills:\n'
    list_installed_skills "$target_root"
  fi
  printf 'Installed %s to %s\n' "$command_name" "$installed_command_dir/$command_name"
  if [ "$command_name" != "$legacy_command_name" ]; then
    printf 'Aliased %s to %s\n' "$legacy_command_name" "$installed_command_dir/$legacy_command_name"
  fi
  case ":$PATH:" in
    *":$installed_command_dir:"*) ;;
    *)
      printf 'Note: add %s to PATH to run %s directly.\n' "$installed_command_dir" "$command_name"
      ;;
  esac
  exit 0
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

git clone --depth 1 --branch "$repo_ref" "$repo_url" "$workdir/ai-toolbox"
install_from_repo "$workdir/ai-toolbox" "$target_root"
install_deps "$workdir/ai-toolbox"
install_command "$workdir/ai-toolbox" "$installed_command_dir"
if [ "$verify" = "true" ]; then
  printf 'Installed skills:\n'
  list_installed_skills "$target_root"
fi
printf 'Installed %s to %s\n' "$command_name" "$installed_command_dir/$command_name"
if [ "$command_name" != "$legacy_command_name" ]; then
  printf 'Aliased %s to %s\n' "$legacy_command_name" "$installed_command_dir/$legacy_command_name"
fi
case ":$PATH:" in
  *":$installed_command_dir:"*) ;;
  *)
    printf 'Note: add %s to PATH to run %s directly.\n' "$installed_command_dir" "$command_name"
    ;;
esac
