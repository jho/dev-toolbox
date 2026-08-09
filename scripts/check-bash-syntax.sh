#!/usr/bin/env bash
set -euo pipefail

status=0

for file in "$@"; do
  if [ ! -f "$file" ]; then
    continue
  fi

  if ! bash -n "$file"; then
    status=1
  fi
done

exit "$status"
