#!/usr/bin/env python3
"""Readable output of the puppet agent.

report.py turn <turn.jsonl> <model>   one turn as markdown: text, tool calls, skills, tokens and cost
report.py run <run-dir>               facts of a whole run: sessions, tokens, cost, skills, commits, artifacts
"""
import json
import subprocess
import sys
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
    total, cost = dict.fromkeys(TOKEN_KEYS, 0), 0.0
    for session in meta["sessions"]:
        # A pipe cuts the export of a long session; a file keeps it whole, and it stays as the transcript of the run.
        target = run_dir / f"session-{session['id']}.json"
        with target.open("w") as out:
            subprocess.run(["opencode", "session", "export", session["id"]], cwd=repo, stdout=out, stderr=subprocess.DEVNULL)
        exported = json.loads(target.read_text() or "{}")
        t = exported.get("info", {}).get("tokens") or {}
        tokens = {"input": t.get("input", 0), "output": t.get("output", 0) + t.get("reasoning", 0),
                  "cache_read": t.get("cache", {}).get("read", 0), "cache_write": t.get("cache", {}).get("write", 0)}
        for k in TOKEN_KEYS:
            total[k] += tokens[k]
        cost += models.cost_of(session["model"], tokens, data) or 0
    artifacts = sorted(str(p.relative_to(repo)) for pattern in (".scratchpad/*/*", "docs/**/*.md", "AGENTS.md", ".agents/yesyak.json") for p in repo.glob(pattern))
    print(f"# Run {meta['run_id']}\n")
    print(f"- Source: {meta['source']} @ {meta['ref'][:9]}")
    print(f"- YesYak: {meta['yesyak']} · model: {meta['model']} · turns: {meta['turns']}")
    print("- Sessions: " + ", ".join(f"`{s['id']}` ({s['model']}, from turn {s['first_turn']})" for s in meta["sessions"]))
    print(f"- Tokens: " + ", ".join(f"{k} {v}" for k, v in total.items()) + f" · ≈ {cost:.4f} $ (models.dev prices)")
    print(f"- Tool calls: {calls} · errors: {len(errors)}")
    print(f"- Branch: {git(repo, 'branch', '--show-current')}")
    print("- Skills loaded, in order: " + (" → ".join(skills) or "none"))
    print("\n## Commits\n\n```text\n" + git(repo, "log", "--oneline", f"{meta['ref']}..HEAD", "--all") + "\n```")
    print("\n## Artifacts\n\n" + "\n".join(f"- `{a}`" for a in artifacts))
    if errors:
        print("\n## Tool errors\n\n" + "\n".join(f"- {e}" for e in errors))


if __name__ == "__main__":
    {"turn": lambda: turn(sys.argv[2], sys.argv[3]), "run": lambda: run(sys.argv[2])}.get(
        sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
