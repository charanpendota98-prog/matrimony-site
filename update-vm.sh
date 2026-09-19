#!/usr/bin/env bash
# Stable root entrypoint kept for the documented VM command: `bash update-vm.sh`.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$ROOT/scripts/update-vm.sh" "$@"
