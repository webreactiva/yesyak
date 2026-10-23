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

# OpenCode looks for skills in every parent folder, so a clone inside the user's home would see ~/.agents/skills.
# The clone lives outside home; the run folder links to it, so everything stays reachable from this repository.
work=${YAKBENCH_WORK:-/Users/Shared/yak-bench}/$run_id
[ -e "$work" ] && { echo "exists: $work" >&2; exit 1; }
mkdir -p "$(dirname "$work")"
git clone -q "$source" "$work"
ln -s "$work" "$run/repo"
cd "$work"
[ -n "$ref" ] && git checkout -q "$ref"
# A commit ref leaves a detached HEAD; a real checkout is on a branch.
git symbolic-ref -q HEAD >/dev/null || git switch -q -C main
git remote remove origin  # the agent must never reach the original repository

# Frozen copy, not symlinks: an edit to YesYak during the run must not change the run.
# .agents/skills for OpenCode, .claude/skills for Claude Code (turn-claude.sh).
mkdir -p .agents/skills .claude/skills
cp -R "$yesyak"/skills/* .agents/skills/
cp -R "$yesyak"/skills/* .claude/skills/
# No commit: a bench commit in the history misleads the detection of the project's commit convention.
printf '.scratchpad/\n.agents/skills/\n.claude/skills/\n' >> .git/info/exclude

# Isolated OpenCode config: no global skills, plugins or MCP servers. Auth lives in the data dir and stays shared.
mkdir -p "$bench/opencode-config"
# The question tool is off: in a non-interactive run its cancel message tells the agent to assume and go on.
[ -f "$bench/opencode-config/opencode.json" ] || printf '{\n  "$schema": "https://opencode.ai/config.json",\n  "autoupdate": false,\n  "tools": { "question": false }\n}\n' > "$bench/opencode-config/opencode.json"

python3 - "$run/run.json" <<EOF
import json, sys, datetime
json.dump({
  "run_id": "$run_id",
  "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
  "source": "$source",
  "ref": "$(git rev-parse HEAD)",
  "yesyak": "$(git -C "$yesyak" describe --tags --always --dirty)",
  "model": None,
  "sessions": [],
  "turns": 0
}, open(sys.argv[1], "w"), indent=2)
EOF
echo "$run"
