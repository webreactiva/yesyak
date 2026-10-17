#!/usr/bin/env bash
# Send one human message to the puppet agent (OpenCode) inside tmux and wait for the answer.
# Usage: turn.sh <run-id> <message-file> [--model provider/model] [--new-session]
# Prints the readable answer. Session ids are kept in run.json.
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

read_meta() { python3 -c "import json,sys;d=json.load(open('$meta'));print(eval(sys.argv[1]))" "$1"; }
[ -z "$model" ] && model=$(read_meta "d['model'] or ''")
[ -z "$model" ] && { echo "no model: pass --model on the first turn" >&2; exit 2; }
python3 "$here/models.py" check "$model"

session=""
[ $new = 0 ] && session=$(read_meta "d['sessions'][-1]['id'] if d['sessions'] else ''")
n=$(printf '%02d' $(( $(read_meta "d['turns']") + 1 )))
cp "$message" "$run/turns/$n-human.md"

args=(run --standalone -m "$model" --auto --format json)
[ -n "$session" ] && args+=(-s "$session") || args+=(--title "yak-bench $run_id")

tmux has-session -t yak-bench 2>/dev/null || tmux new-session -d -s yak-bench -x 200 -y 50
window="$run_id-$n"
done_file="$run/turns/$n.done"
# Isolation: --standalone skips the shared background service (it runs with the user's config), and a fake HOME
# hides the user's skills (~/.claude, ~/.agents, ~/.config/opencode). Auth and sessions stay in the real data dir.
mkdir -p "$bench/home"
env_vars="HOME='$bench/home' XDG_CONFIG_HOME='$bench/home/.config' XDG_DATA_HOME='$HOME/.local/share' \
  XDG_CACHE_HOME='$HOME/.cache' XDG_STATE_HOME='$HOME/.local/state' OPENCODE_CONFIG_DIR='$bench/opencode-config' \
  OPENCODE_DISABLE_CLAUDE_CODE=1 OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1 OPENCODE_DISABLE_AUTOUPDATE=1 \
  GIT_AUTHOR_NAME=yak-puppet GIT_AUTHOR_EMAIL=puppet@yak-bench GIT_COMMITTER_NAME=yak-puppet GIT_COMMITTER_EMAIL=puppet@yak-bench"
# The message goes through a file, so quotes in it never reach the shell.
tmux new-window -d -t yak-bench -n "$window" -c "$run/repo" \
  "$env_vars opencode $(printf '%q ' "${args[@]}") \"\$(cat '$run/turns/$n-human.md')\" > '$run/turns/$n.jsonl' 2> '$run/turns/$n.stderr'; \
   echo \$? > '$done_file'"

while [ ! -f "$done_file" ]; do sleep 5; done
code=$(cat "$done_file")

python3 - "$meta" "$run/turns/$n.jsonl" "$model" "$code" <<'EOF'
import json, sys
meta_path, jsonl, model, code = sys.argv[1:]
d = json.load(open(meta_path))
sid = next((json.loads(l).get("sessionID") for l in open(jsonl) if l.startswith("{")), None)
if sid and not any(s["id"] == sid for s in d["sessions"]):
    d["sessions"].append({"id": sid, "model": model, "first_turn": d["turns"] + 1})
d["model"] = model
d["turns"] += 1
d.setdefault("exit_codes", []).append(int(code))
json.dump(d, open(meta_path, "w"), indent=2)
EOF

python3 "$here/report.py" turn "$run/turns/$n.jsonl" "$model" > "$run/turns/$n-agent.md"
cat "$run/turns/$n-agent.md"
[ "$code" = 0 ] || { echo "opencode exit $code:"; tail -5 "$run/turns/$n.stderr"; }
