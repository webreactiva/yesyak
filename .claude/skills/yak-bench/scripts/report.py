#!/usr/bin/env python3
"""Readable output of the puppet agent.

report.py turn <turn.jsonl> <model>   one turn as markdown: text, tool calls, skills, tokens and cost
report.py run <run-dir>               facts of a whole run: sessions, tokens, cost, skills, commits, artifacts
report.py metrics <bench-dir> [claude-transcript.jsonl]
                                      one row per run from the saved exports: time, turns, steps, tokens, cost;
                                      with a transcript, also the driver's (Claude Code) usage in each run's time window
report.py flows <bench-dir>           per run, the YesYak skills the work session used, in order, with the turn of first use
"""
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import models  # noqa: E402

TOKEN_KEYS = ("input", "output", "cache_read", "cache_write")


def parse(line):
    # A transcript can end with a line cut while it was written; skip it instead of failing the whole report.
    try:
        return json.loads(line) if line.startswith("{") else {}
    except json.JSONDecodeError:
        return {}


def events(path):
    for line in Path(path).read_text().splitlines():
        if line.startswith("{"):
            yield parse(line)


def summarize_claude(path):
    """The same facts from Claude Code's stream JSON. Its result event carries the whole turn's usage."""
    text, calls, skills, errors = [], [], [], []
    tokens = dict.fromkeys(TOKEN_KEYS, 0)
    for e in events(path):
        message = e.get("message") if isinstance(e.get("message"), dict) else {}
        content = message.get("content")
        if e["type"] == "assistant" and isinstance(content, list):
            for c in content:
                if c.get("type") == "text":
                    text.append(c["text"])
                elif c.get("type") == "tool_use":
                    args = c.get("input", {})
                    if c["name"] == "Skill":
                        skills.append(args.get("skill") or "?")
                    short = args.get("command") or args.get("file_path") or args.get("skill") or args.get("pattern") or args.get("description") or ""
                    calls.append(f"{c['name']}: {str(short)[:120]}")
        elif e["type"] == "user" and isinstance(content, list):
            errors += [str(c.get("content"))[:200] for c in content if c.get("type") == "tool_result" and c.get("is_error")]
        elif e["type"] == "result":
            u = e.get("usage", {})
            tokens = {"input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0),
                      "cache_read": u.get("cache_read_input_tokens", 0), "cache_write": u.get("cache_creation_input_tokens", 0)}
            if e.get("is_error"):
                errors.append(str(e.get("result"))[:300])
    return text, calls, skills, errors, tokens


def summarize(path):
    first = next(events(path), {})
    if "session_id" in first:
        return summarize_claude(path)
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
    # A session can switch models; price each step with its own model, the session model when a step does not say.
    cost = 0.0
    for m in steps:
        t, own = m.get("tokens") or {}, m.get("model") or {}
        used = {"input": t.get("input", 0), "output": t.get("output", 0) + t.get("reasoning", 0),
                "cache_read": t.get("cache", {}).get("read", 0), "cache_write": t.get("cache", {}).get("write", 0)}
        cost += models.cost_of(f"{own['providerID']}/{own['id']}" if own.get("id") else model, used, data) or 0
    return {
        "start": span.get("created", 0), "end": span.get("updated", 0),
        # Wall time includes the minutes the session waits for the human; agent time counts only model steps.
        "wall_s": (span.get("updated", 0) - span.get("created", 0)) / 1000,
        "agent_s": sum((m["time"].get("completed") or m["time"]["created"]) - m["time"]["created"] for m in steps) / 1000,
        "turns": sum(m.get("type") == "user" for m in messages), "steps": len(steps),
        "tokens": tokens, "cost": cost,
    }


def claude_transcript(repo, session_id):
    """Where Claude Code keeps a session: ~/.claude/projects/<working dir with every other character as ->/<id>.jsonl."""
    import re
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(repo).resolve())) / f"{session_id}.jsonl"


def claude_session_metrics(transcript, run_dir, data):
    """session_metrics for a Claude Code transcript; the agent time comes from the turns' result events."""
    steps, tokens, cost = driver_usage(transcript, 0, float("inf"), data)
    entries = [parse(l) for l in Path(transcript).read_text().splitlines() if l.startswith("{")]
    times = [datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).timestamp() * 1000 for e in entries if "timestamp" in e]
    turns = sum(e.get("type") == "user" and isinstance((e.get("message") or {}).get("content"), str) for e in entries)
    sid = Path(transcript).stem.removeprefix("session-")
    agent = sum(e.get("duration_ms", 0) for p in Path(run_dir, "turns").glob("*.jsonl") for e in events(p)
                if e.get("type") == "result" and e.get("session_id") == sid)
    return {"start": min(times), "end": max(times), "wall_s": (max(times) - min(times)) / 1000, "agent_s": agent / 1000,
            "turns": turns, "steps": steps, "tokens": tokens, "cost": cost}


def driver_usage(transcript, start_ms, end_ms, data):
    """Steps, tokens and cost of the Claude Code session that drove the run, and its subagents, between two times.
    Each API message counts once, priced with its own model."""
    seen, tokens, cost = set(), dict.fromkeys(TOKEN_KEYS, 0), 0.0
    transcript = Path(transcript)
    for f in [transcript, *transcript.with_suffix("").glob("subagents/*.jsonl")]:
        for line in f.read_text().splitlines():
            e = parse(line)
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
            if session.get("harness") == "claude":
                path = run_dir / f"session-{session['id']}.jsonl"
                if path.exists():
                    rows.append(claude_session_metrics(path, run_dir, data))
                continue
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


def skill_uses(path, skills):
    """(skill, how) for every skill the events of one turn load: the skill tool, or a read of its SKILL.md."""
    for e in events(path):
        found = []
        if e.get("type") == "tool_use":
            p = e["part"]
            args = p.get("state", {}).get("input", {})
            if p.get("tool") == "skill":
                found.append((args.get("name") or args.get("id"), "tool"))
            found += [(m, "read") for m in re.findall(r"skills/([a-z-]+)/SKILL\.md", str(args.get("filePath") or args.get("path") or args.get("command") or ""))]
        elif e.get("type") == "assistant" and isinstance(e.get("message"), dict) and isinstance(e["message"].get("content"), list):
            for c in e["message"]["content"]:
                if c.get("type") == "tool_use":
                    args = c.get("input", {})
                    if c["name"] == "Skill":
                        found.append((args.get("skill"), "tool"))
                    found += [(m, "read") for m in re.findall(r"skills/([a-z-]+)/SKILL\.md", str(args.get("file_path") or args.get("command") or ""))]
        yield from ((name, how) for name, how in found if name in skills)


def flows(bench_dir):
    skills = set(p.name for p in (Path(__file__).resolve().parents[4] / "skills").iterdir())
    for run_dir in sorted(Path(bench_dir).glob("[0-9]*")):
        meta_path = run_dir / "run.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        # The first session of a run with several is the isolation probe.
        work = {s["first_turn"] for s in meta["sessions"][1:]} or {1}
        start = min(work)
        seen = {}
        for path in sorted((run_dir / "turns").glob("*.jsonl")):
            if not path.stem.isdigit():  # a killed turn kept aside, for example 08-killed
                continue
            n = int(path.stem)
            if n < start:
                continue
            for name, how in skill_uses(path, skills):
                seen.setdefault(name, f"{name}{'*' if how == 'read' else ''} ({n})")
        print(f"| {meta['run_id']} | {' → '.join(seen.values()) or 'none'} |")


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
        if session.get("harness") == "claude":
            source = claude_transcript(repo, session["id"])
            target = run_dir / f"session-{session['id']}.jsonl"
            if source.exists():  # after archive.sh the clone has moved; keep the copy saved before
                target.write_text(source.read_text())
            elif not target.exists():
                target.write_text("")
            if source.with_suffix("").is_dir():  # the puppet's subagents
                shutil.copytree(source.with_suffix(""), target.with_suffix(""), dirs_exist_ok=True)
            m = claude_session_metrics(target, run_dir, data) if target.stat().st_size else None
            if m:
                for k in TOKEN_KEYS:
                    total[k] += m["tokens"][k]
                cost += m["cost"]
                wall += m["wall_s"]
                agent += m["agent_s"]
                steps += m["steps"]
            continue
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
     "metrics": lambda: metrics(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None),
     "flows": lambda: flows(sys.argv[2])}.get(
        sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
