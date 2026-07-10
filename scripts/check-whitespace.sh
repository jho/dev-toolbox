#!/usr/bin/env bash
set -euo pipefail

status=0

for file in "$@"; do
  if [ ! -f "$file" ]; then
    continue
  fi

  if grep -nI '[[:blank:]]$' "$file" >/dev/null; then
    printf 'Trailing whitespace found in %s\n' "$file" >&2
    grep -nI '[[:blank:]]$' "$file" >&2
    status=1
  fi
done

exit "$status"

