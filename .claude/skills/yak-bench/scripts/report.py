#!/usr/bin/env python3
"""Readable output of the puppet agent.

report.py turn <turn.jsonl> <model>   one turn as markdown: text, tool calls, skills, tokens and cost
report.py run <run-dir>               facts of a whole run: sessions, tokens, cost, skills, commits, artifacts
report.py metrics <bench-dir> [claude-transcript.jsonl]
                                      one row per run from the saved exports: time, turns, steps, tokens, cost;
                                      with a transcript, also the driver's (Claude Code) usage in each run's time window
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import models  # noqa: E402

TOKEN_KEYS = ("input", "output", "cache_read", "cache_write")


def events(path):
    for line in Path(path).read_text().splitlines():
        if line.startswith("{"):
            yield json.loads(line)


def summarize(path):
    text, calls, skills, errors = [], [], [], []
    tokens = dict.fromkeys(TOKEN_KEYS, 0)
    for e in events(path):
        part = e.get("part", {})
        if e["type"] == "text":
            text.append(part.get("text", ""))
        elif e["type"] == "tool_use":
            state = part.get("state", {})
            args = state.get("input", {})
            if part.get("tool") == "skill":
                skills.append(args.get("name") or args.get("id") or "?")
            short = args.get("command") or args.get("filePath") or args.get("path") or args.get("name") or args.get("id") or args.get("pattern") or ""
            calls.append(f"{part.get('tool')}: {str(short)[:120]}")
            if state.get("status") == "error":
                errors.append(f"{part.get('tool')}: {str(state.get('error', ''))[:200]}")
        elif e["type"] == "step_finish":
            t = part.get("tokens", {})
            tokens["input"] += t.get("input", 0)
            tokens["output"] += t.get("output", 0) + t.get("reasoning", 0)
            tokens["cache_read"] += t.get("cache", {}).get("read", 0)
            tokens["cache_write"] += t.get("cache", {}).get("write", 0)
        elif e["type"] == "error":
            errors.append(json.dumps(e.get("error", e))[:300])
    return text, calls, skills, errors, tokens


def turn(path, model):
    text, calls, skills, errors, tokens = summarize(path)
    cost = models.cost_of(model, tokens, models.catalog())
    out = ["\n\n".join(t for t in text if t.strip()) or "(no text)", ""]
    if skills:
        out.append("Skills: " + ", ".join(skills))
    out.append(f"Tool calls: {len(calls)}")
    out += [f"  {c}" for c in calls[-15:]]
    out += [f"ERROR {e}" for e in errors]
    out.append("Tokens (approximate, the last step is missing): " + ", ".join(f"{k} {v}" for k, v in tokens.items()) + (f" · ≈ {cost:.4f} $" if cost is not None else ""))
    print("\n".join(out))


def session_metrics(exported, model, data):
    """Time, iterations, tokens and cost of one exported OpenCode session."""
    t = exported.get("info", {}).get("tokens") or {}
    tokens = {"input": t.get("input", 0), "output": t.get("output", 0) + t.get("reasoning", 0),
              "cache_read": t.get("cache", {}).get("read", 0), "cache_write": t.get("cache", {}).get("write", 0)}
    messages = exported.get("messages", [])
    steps = [m for m in messages if m.get("type") == "assistant"]
    span = exported.get("info", {}).get("time", {})
    return {
        "start": span.get("created", 0), "end": span.get("updated", 0),
        # Wall time includes the minutes the session waits for the human; agent time counts only model steps.
        "wall_s": (span.get("updated", 0) - span.get("created", 0)) / 1000,
        "agent_s": sum((m["time"].get("completed") or m["time"]["created"]) - m["time"]["created"] for m in steps) / 1000,
        "turns": sum(m.get("type") == "user" for m in messages), "steps": len(steps),
        "tokens": tokens, "cost": models.cost_of(model, tokens, data) or 0,
    }


def driver_usage(transcript, start_ms, end_ms, data):
    """Steps, tokens and cost of the Claude Code session that drove the run, and its subagents, between two times.
    Each API message counts once, priced with its own model."""
    seen, tokens, cost = set(), dict.fromkeys(TOKEN_KEYS, 0), 0.0
    transcript = Path(transcript)
    for f in [transcript, *transcript.with_suffix("").glob("subagents/*.jsonl")]:
        for line in f.read_text().splitlines():
            e = json.loads(line) if line.startswith("{") else {}
            msg = e.get("message") or {}
            if e.get("type") != "assistant" or msg.get("id") in seen or not msg.get("usage"):
                continue
            at = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).timestamp() * 1000
            if not start_ms <= at <= end_ms:
                continue
            seen.add(msg["id"])
            u = msg["usage"]
            used = {"input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0),
                    "cache_read": u.get("cache_read_input_tokens", 0), "cache_write": u.get("cache_creation_input_tokens", 0)}
            for k in TOKEN_KEYS:
                tokens[k] += used[k]
            cost += models.cost_of(f"anthropic/{msg.get('model')}", used, data) or 0
    return len(seen), tokens, cost


def minutes(seconds):
    return f"{seconds / 60:.0f} min"


def metrics(bench_dir, transcript=None):
    data = models.catalog()
    head = "| Run | Model | Turns | Steps | Wall | Agent | Input | Output | Cache read | Cost $ |"
    if transcript:
        head += " Driver steps | Driver tokens (out) | Driver $ |"
    print(head + "\n|" + " --- |" * (head.count("|") - 1))
    for run_dir in sorted(Path(bench_dir).glob("[0-9]*")):
        meta_path = run_dir / "run.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        rows = []
        for session in meta["sessions"]:
            path = run_dir / f"session-{session['id']}.json"
            if path.exists() and path.stat().st_size:
                rows.append(session_metrics(json.loads(path.read_text()), session["model"], data))
        if not rows:
            continue
        total = lambda k: sum(r[k] for r in rows)
        tok = lambda k: sum(r["tokens"][k] for r in rows)
        line = (f"| {meta['run_id']} | {meta['model']} | {total('turns')} | {total('steps')} | {minutes(total('wall_s'))} | "
                f"{minutes(total('agent_s'))} | {tok('input')} | {tok('output')} | {tok('cache_read')} | {total('cost'):.2f} |")
        if transcript:
            n, used, cost = driver_usage(transcript, min(r["start"] for r in rows), max(r["end"] for r in rows), data)
            line += f" {n} | {sum(used.values())} ({used['output']}) | {cost:.2f} |"
        print(line)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()


def run(run_dir):
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "run.json").read_text())
    data = models.catalog()
    skills, calls, errors = [], 0, []
    for path in sorted((run_dir / "turns").glob("*.jsonl")):
        _, c, s, e, _ = summarize(path)
        calls += len(c)
        skills += s
        errors += [f"{path.stem}: {x}" for x in e]
    repo = run_dir / "repo"
    # The JSON stream drops the token count of a turn's last step; the session export has all of them.
    total, cost, wall, agent, steps = dict.fromkeys(TOKEN_KEYS, 0), 0.0, 0.0, 0.0, 0
    for session in meta["sessions"]:
        # A pipe cuts the export of a long session; a file keeps it whole, and it stays as the transcript of the run.
        target = run_dir / f"session-{session['id']}.json"
        with target.open("w") as out:
            subprocess.run(["opencode", "session", "export", session["id"]], cwd=repo, stdout=out, stderr=subprocess.DEVNULL)
        m = session_metrics(json.loads(target.read_text() or "{}"), session["model"], data)
        for k in TOKEN_KEYS:
            total[k] += m["tokens"][k]
        cost += m["cost"]
        wall += m["wall_s"]
        agent += m["agent_s"]
        steps += m["steps"]
    artifacts = sorted(str(p.relative_to(repo)) for pattern in (".scratchpad/*/*", "docs/**/*.md", "AGENTS.md", ".agents/yesyak.json") for p in repo.glob(pattern))
    print(f"# Run {meta['run_id']}\n")
    print(f"- Source: {meta['source']} @ {meta['ref'][:9]}")
    print(f"- YesYak: {meta['yesyak']} · model: {meta['model']} · turns: {meta['turns']}")
    print("- Sessions: " + ", ".join(f"`{s['id']}` ({s['model']}, from turn {s['first_turn']})" for s in meta["sessions"]))
    print(f"- Tokens: " + ", ".join(f"{k} {v}" for k, v in total.items()) + f" · ≈ {cost:.4f} $ (models.dev prices)")
    print(f"- Time: {minutes(wall)} wall, {minutes(agent)} of agent work · model steps: {steps}")
    print(f"- Tool calls: {calls} · errors: {len(errors)}")
    print(f"- Branch: {git(repo, 'branch', '--show-current')}")
    print("- Skills loaded, in order: " + (" → ".join(skills) or "none"))
    print("\n## Commits\n\n```text\n" + git(repo, "log", "--oneline", f"{meta['ref']}..HEAD", "--all") + "\n```")
    print("\n## Artifacts\n\n" + "\n".join(f"- `{a}`" for a in artifacts))
    if errors:
        print("\n## Tool errors\n\n" + "\n".join(f"- {e}" for e in errors))


if __name__ == "__main__":
    {"turn": lambda: turn(sys.argv[2], sys.argv[3]), "run": lambda: run(sys.argv[2]),
     "metrics": lambda: metrics(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)}.get(
        sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
