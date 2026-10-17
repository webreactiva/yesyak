#!/usr/bin/env bash
# Move the clone of a scored run into its run folder, so the next puppet cannot read it next to its own clone.
# Usage: archive.sh <run-id>
set -euo pipefail
here=$(dirname "$(readlink -f "$0")")
yesyak=$(cd "$here/../../../.." && pwd)
run="${YAKBENCH_DIR:-$yesyak/.scratchpad/bench}/${1:?run id}"
[ -L "$run/repo" ] || { echo "already archived or no run: $run" >&2; exit 1; }
clone=$(cd "$run/repo" && pwd -P)
rm "$run/repo"
mv "$clone" "$run/repo"
echo "$clone -> $run/repo"
