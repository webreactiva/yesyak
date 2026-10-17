#!/usr/bin/env bash
# Prepare one benchmark run: a clean copy of a project with a frozen copy of the YesYak skills.
# Usage: prepare.sh <run-id> <git-url-or-path> [ref]
set -euo pipefail

run_id=${1:?run id, for example 0003-orders-api}
source=${2:?git url or local path of the project}
ref=${3:-}

yesyak=$(cd "$(dirname "$(readlink -f "$0")")/../../../.." && pwd)
bench=${YAKBENCH_DIR:-$yesyak/.scratchpad/bench}
run="$bench/$run_id"
[ -e "$run" ] && { echo "exists: $run" >&2; exit 1; }
mkdir -p "$run/turns"

git clone -q "$source" "$run/repo"
cd "$run/repo"
[ -n "$ref" ] && git checkout -q "$ref"
git remote remove origin  # the agent must never reach the original repository

# Frozen copy, not symlinks: an edit to YesYak during the run must not change the run.
mkdir -p .agents/skills
cp -R "$yesyak"/skills/* .agents/skills/
printf '\n.scratchpad/\n.agents/skills/\n' >> .gitignore
git add .gitignore
git -c user.name=yak-bench -c user.email=yak-bench@localhost commit -q -m "chore: ignore yesyak working folders"

# Isolated OpenCode config: no global skills, plugins or MCP servers. Auth lives in the data dir and stays shared.
mkdir -p "$bench/opencode-config"
[ -f "$bench/opencode-config/opencode.json" ] || printf '{\n  "$schema": "https://opencode.ai/config.json",\n  "autoupdate": false\n}\n' > "$bench/opencode-config/opencode.json"

python3 - "$run/run.json" <<EOF
import json, sys, datetime
json.dump({
  "run_id": "$run_id",
  "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
  "source": "$source",
  "ref": "$(git rev-parse HEAD~1)",
  "yesyak": "$(git -C "$yesyak" describe --tags --always --dirty)",
  "model": None,
  "sessions": [],
  "turns": 0
}, open(sys.argv[1], "w"), indent=2)
EOF
echo "$run"
