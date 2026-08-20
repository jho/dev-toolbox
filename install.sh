#!/usr/bin/env bash
set -euo pipefail

repo_url="${DEV_TOOLBOX_REPO_URL:-${AI_TOOLBOX_REPO_URL:-https://github.com/jho/dev-toolbox.git}}"
repo_ref="${DEV_TOOLBOX_REPO_REF:-${AI_TOOLBOX_REPO_REF:-main}}"
command_name="${DEV_TOOLBOX_COMMAND_NAME:-${AI_TOOLBOX_COMMAND_NAME:-dev-toolbox}}"
command_dir="${DEV_TOOLBOX_COMMAND_DIR:-${AI_TOOLBOX_COMMAND_DIR:-$HOME/.local/bin}}"
legacy_command_name="${DEV_TOOLBOX_LEGACY_COMMAND_NAME:-ai-toolbox}"
state_dir="${DEV_TOOLBOX_STATE_DIR:-${AI_TOOLBOX_STATE_DIR:-$HOME/.local/share/dev-toolbox}}"

usage() {
  cat <<'EOF'
Usage: install.sh [--surface auto|codex|claude] [--target PATH] [--verify]

Install the dev-toolbox skills into a Codex or Claude skills directory.

Defaults:
  --surface auto    -> prefer Codex when ~/.codex exists, otherwise Claude when ~/.claude exists
  --surface codex   -> $CODEX_HOME/skills or ~/.codex/skills
  --surface claude  -> $CLAUDE_HOME/skills or ~/.claude/skills

If run outside a cloned checkout, the script clones the dev-toolbox repo into a temporary directory
and installs from there. Override the remote with DEV_TOOLBOX_REPO_URL and DEV_TOOLBOX_REPO_REF
(or the legacy AI_TOOLBOX_* names).
Use --verify to print the installed skill directories after syncing.

The installer also drops a small `dev-toolbox` command into $DEV_TOOLBOX_COMMAND_DIR by
default, plus an `ai-toolbox` compatibility alias. Use `dev-toolbox update` to resync skills
without returning to the repo.

It also writes a small shell contract to `~/.local/share/dev-toolbox/`
so private dotfiles can source a stable PATH/env fragment without depending on the repo layout.
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
  "$repo_root/scripts/sync-skills.sh" "$target"
}

install_deps() {
  local repo_root="$1"
  "$repo_root/scripts/run-deps.sh"
}

install_agents() {
  local repo_root="$1"
  local target_surface="$2"
  "$repo_root/scripts/sync-agents.sh" --surface "$target_surface" --skills-target "$3"
}

install_shell_contract() {
  local contract_dir="$1"
  local command_dir="$2"

  mkdir -p "$contract_dir" "$command_dir"

  cat >"$contract_dir/env.sh" <<EOF
# Managed by dev-toolbox install.sh.
export DEV_TOOLBOX_STATE_DIR="$contract_dir"
export DEV_TOOLBOX_COMMAND_DIR="$command_dir"
EOF

  cat >"$contract_dir/path.sh" <<EOF
# Managed by dev-toolbox install.sh.
_dev_toolbox_path="$(printf '%s' "\${PATH}" | awk -v RS=: -v ORS=: -v dir="$command_dir" '
  $0 != dir && length($0) { print }
')"
_dev_toolbox_path="\${_dev_toolbox_path%:}"
export PATH="$command_dir\${_dev_toolbox_path:+:\${_dev_toolbox_path}}"
unset _dev_toolbox_path
EOF
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
script_name="sync-skills.sh"
agent_script_name="sync-agents.sh"
agent_surface="${surface}"

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
    if [ -f "\$embedded_repo_root/scripts/\$agent_script_name" ]; then
      "\$embedded_repo_root/scripts/\$agent_script_name" --surface "\$agent_surface" --skills-target "\$target_root"
    fi
    return
  fi

  workdir="\$(mktemp -d)"
  trap 'rm -rf "\$workdir"' EXIT

  git clone --depth 1 --branch "\$repo_ref" "\$repo_url" "\$workdir/dev-toolbox" >/dev/null 2>&1
  "\$workdir/dev-toolbox/scripts/\$script_name" "\$target_root"
  if [ -f "\$workdir/dev-toolbox/scripts/run-deps.sh" ]; then
    "\$workdir/dev-toolbox/scripts/run-deps.sh"
  fi
  if [ -f "\$workdir/dev-toolbox/scripts/\$agent_script_name" ]; then
    "\$workdir/dev-toolbox/scripts/\$agent_script_name" --surface "\$agent_surface" --skills-target "\$target_root"
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

script_source="${BASH_SOURCE[0]:-}"
script_dir=""
if [ -n "$script_source" ]; then
  script_dir="$(cd "$(dirname "$script_source")" && pwd)"
fi
installed_command_dir="$command_dir"

if [ -n "$script_dir" ] && [ -f "$script_dir/scripts/sync-skills.sh" ]; then
  install_from_repo "$script_dir" "$target_root"
  install_deps "$script_dir"
  install_agents "$script_dir" "$surface" "$target_root"
  install_command "$script_dir" "$installed_command_dir" "$surface"
  install_shell_contract "$state_dir" "$installed_command_dir"
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

git clone --depth 1 --branch "$repo_ref" "$repo_url" "$workdir/dev-toolbox"
install_from_repo "$workdir/dev-toolbox" "$target_root"
install_deps "$workdir/dev-toolbox"
install_agents "$workdir/dev-toolbox" "$surface" "$target_root"
install_command "$workdir/dev-toolbox" "$installed_command_dir" "$surface"
install_shell_contract "$state_dir" "$installed_command_dir"
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
