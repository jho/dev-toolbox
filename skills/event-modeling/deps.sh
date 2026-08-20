#!/usr/bin/env bash
set -euo pipefail

if [ "${DEV_TOOLBOX_SKIP_DEP_INSTALL:-${AI_TOOLBOX_SKIP_DEP_INSTALL:-0}}" = "1" ]; then
  printf 'Skipping em dependency install because dependency installation was disabled\n'
  exit 0
fi

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$skill_dir/../.." && pwd)"
vendored_em_dir="$repo_root/vendor/em"

if ! command -v npm >/dev/null 2>&1; then
  printf 'npm is required to install @milehimikey/em\n' >&2
  exit 1
fi

if [ -d "$vendored_em_dir" ]; then
  printf 'Building vendored em subtree\n'
  (cd "$vendored_em_dir" && npm ci && npm run build)
  printf 'Installing vendored em to the global PATH\n'
  npm install -g "$vendored_em_dir"
else
  printf 'Vendored em subtree not found; falling back to npm install\n'
  npm install -g @milehimikey/em
fi
