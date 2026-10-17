#!/usr/bin/env bash
# Send one human message to the puppet agent (Claude Code) inside tmux and wait for the answer.
# Usage: turn-claude.sh <run-id> <message-file> [--model alias] [--new-session]
# Prints the readable answer. Session ids are kept in run.json, as turn.sh does for OpenCode.
set -euo pipefail

run_id=${1:?run id}
message=${2:?file with the message}
shift 2
model="" new=0
while [ $# -gt 0 ]; do
  case $1 in
    --model) model=$2; shift 2 ;;
    --new-session) new=1; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done

here=$(dirname "$(readlink -f "$0")")
yesyak=$(cd "$here/../../../.." && pwd)
bench=${YAKBENCH_DIR:-$yesyak/.scratchpad/bench}
run="$bench/$run_id"
meta="$run/run.json"
[ -f "$meta" ] || { echo "no run: $run" >&2; exit 1; }
# The real path of the clone: through the link in this repository the puppet would see the run folder and its notes.
repo=$(cd "$run/repo" && pwd -P)

read_meta() { python3 -c "import json,sys;d=json.load(open('$meta'));print(eval(sys.argv[1]))" "$1"; }
[ -z "$model" ] && model=$(read_meta "(d['model'] or '').removeprefix('anthropic/')")
[ -z "$model" ] && { echo "no model: pass --model on the first turn" >&2; exit 2; }
python3 "$here/models.py" check "anthropic/$model"

session=""
[ $new = 0 ] && session=$(read_meta "d['sessions'][-1]['id'] if d['sessions'] else ''")
n=$(printf '%02d' $(( $(read_meta "d['turns']") + 1 )))
cp "$message" "$run/turns/$n-human.md"

# Isolation: only the project's settings (no user skills, hooks, plugins or CLAUDE.md) and no MCP server.
# HOME stays real: the sign-in lives there. The probe turn checks what the puppet can still see.
args=(-p --model "$model" --setting-sources project --strict-mcp-config --no-chrome
      --output-format stream-json --verbose --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write Glob Grep Skill Agent Task TodoWrite")
if [ -n "$session" ]; then
  args+=(--resume "$session")
else
  session=$(python3 -c "import uuid;print(uuid.uuid4())")
  args+=(--session-id "$session")
fi

tmux has-session -t yak-bench 2>/dev/null || tmux new-session -d -s yak-bench -x 200 -y 50
window="$run_id-$n"
done_file="$run/turns/$n.done"
# The tmux server may come from the driver's Claude Code session; its variables (session id, messaging token)
# must not reach the puppet.
driver_vars=$(env | grep -oE '^(CLAUDE[A-Z_]*|AI_AGENT)=' | tr -d = | sed 's/^/-u /' | tr '\n' ' ')
env_vars="env ${driver_vars}GIT_AUTHOR_NAME=yak-puppet GIT_AUTHOR_EMAIL=puppet@yak-bench GIT_COMMITTER_NAME=yak-puppet GIT_COMMITTER_EMAIL=puppet@yak-bench"

# The message goes through a file, so quotes in it never reach the shell.
tmux new-window -d -t yak-bench -n "$window" -c "$repo" \
  "$env_vars claude $(printf '%q ' "${args[@]}") \"\$(cat '$run/turns/$n-human.md')\" > '$run/turns/$n.jsonl' 2> '$run/turns/$n.stderr'; \
   echo \$? > '$done_file'"

while [ ! -f "$done_file" ]; do sleep 5; done
code=$(cat "$done_file")

python3 - "$meta" "$session" "anthropic/$model" "$code" <<'EOF'
import json, sys
meta_path, sid, model, code = sys.argv[1:]
d = json.load(open(meta_path))
if not any(s["id"] == sid for s in d["sessions"]):
    d["sessions"].append({"id": sid, "model": model, "harness": "claude", "first_turn": d["turns"] + 1})
d["model"] = model
d["turns"] += 1
d.setdefault("exit_codes", []).append(int(code))
json.dump(d, open(meta_path, "w"), indent=2)
EOF

python3 "$here/report.py" turn "$run/turns/$n.jsonl" "anthropic/$model" > "$run/turns/$n-agent.md"
cat "$run/turns/$n-agent.md"
[ "$code" = 0 ] || { echo "claude exit $code:"; tail -5 "$run/turns/$n.stderr"; }
