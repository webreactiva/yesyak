#!/usr/bin/env python3
"""Check that a run follows its yak-pilot plan.

Usage: check_plan.py [<progress.md or .scratchpad/<slug>/>] [--hook]

Reads the `## Plan` of progress.md, the process map and unattended-decisions.md, and reports:
- a required step of the route that is not in the plan, or that the plan leaves out without a gate;
- a planned step with an empty Loaded cell after a later step loaded its skill, or at the end of the run;
- a gate with no answer of the user when the step after it has started, or at the end of the run.

Without a path, it checks the most recently changed .scratchpad/*/progress.md that has a `## Plan`.
Exit code 1 on a problem. With --hook, exit code 2 (the code that blocks in agent hooks), and exit 0
when the hook input says that the hook already blocked once (`stop_hook_active`), so the agent cannot loop.
"""

import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
PROCESS_FILE = SKILLS_DIR / "ask-yak" / "references" / "process.md"
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)+")
EMPTY = {"", "—", "-"}
# yak-pilot "Optional steps": the blocking round of its section 2 can stand in for the interview.
PILOT_OPTIONAL = {"on-the-spot"}


def required_steps(route):
    """Skill names that a route always runs, from the text blocks of the process map."""
    process = PROCESS_FILE.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)```", process, re.S)
    text = blocks[1] if route == "bug-intake" else blocks[0].split("\n7 ")[0]
    known = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    required = set(SKILL_NAME.findall(re.sub(r"\([^)]*\)", "", text))) & known
    return required - PILOT_OPTIONAL


def tables(text):
    """Every markdown table in text, as a list of dicts keyed by the header cells."""
    found, rows = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif rows:
            found.append([dict(zip(rows[0], r)) for r in rows[2:]])
            rows = []
    return found


def skills_in(cell):
    return SKILL_NAME.findall(re.sub(r"\([^)]*\)", "", cell))


def check(progress):
    folder = progress.parent
    text = progress.read_text(encoding="utf-8")
    if "## Plan" not in text:
        return [f"{progress}: no '## Plan' section"], []
    plan = re.split(r"^## ", text.split("## Plan", 1)[1], maxsplit=1, flags=re.M)[0]
    route = "bug-intake" if re.search(r"^- Route:.*bug-intake", plan, re.M) else "feature-delivery-pipeline"
    found = tables(plan)
    steps = next((t for t in found if t and "Skill" in t[0]), [])
    gates = next((t for t in found if t and "Gate" in t[0]), [])
    log_path = folder / "unattended-decisions.md"
    log = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    ended = (folder / "retrospective.md").exists()
    problems, notes = [], []

    required = required_steps(route)
    planned = {s: row for row in steps for s in skills_in(row.get("Skill", ""))}
    gate_text = " ".join(g.get("Decision", "") for g in gates)
    for skill in sorted(required):
        row = planned.get(skill)
        if row is None:
            problems.append(f"required step {skill} is not in the plan")
        elif row.get("Runs", "").lower().startswith("no") and skill not in gate_text:
            problems.append(f"required step {skill} is left out without a gate that names it")

    # A plan written before the Loaded and Answer columns existed: say so once, and check only what it has.
    if steps and "Loaded" not in steps[0]:
        notes.append("the step table has no Loaded column (an older plan): loads not checked")
    if gates and "Answer" not in gates[0]:
        notes.append("the gate table has no Answer column (an older plan): gates not checked")
        gates = []
    loaded = [row.get("Loaded", "") not in EMPTY for row in steps]
    for i, row in enumerate(steps):
        runs = row.get("Runs", "").lower().startswith("yes") and skills_in(row.get("Skill", ""))
        if runs and "Loaded" in row and not loaded[i] and (ended or any(loaded[i + 1:])):
            problems.append(f"step '{row.get('Step')}' ran with an empty Loaded cell: load {row.get('Skill')} and redo its checks, or log the skip")

    # A gate is passed when a step after its Before step has loaded: the Before skill itself can load while the plan is written.
    started = {row.get("Step", "").lower(): any(loaded[i + 1:]) for i, row in enumerate(steps)}
    for gate in gates:
        name, answer = gate.get("Gate", "?"), gate.get("Answer", "")
        if not ended and not started.get(gate.get("Before", "").lower(), False):
            continue
        ids = re.findall(r"Q-\d+", answer)
        if not ids:
            when = "at the end of the run" if ended else f"but a step after '{gate.get('Before')}' has started"
            problems.append(f"gate {name} has no answer in its Answer cell, {when}")
            continue
        for qid in ids:
            entry = re.search(rf"^### {qid}\b.*?(?=^### |\Z)", log, re.M | re.S)
            if not entry:
                problems.append(f"gate {name}: {qid} is not in unattended-decisions.md")
            elif not re.search(r"Chosen by:\s*user", entry.group(0)):
                problems.append(f"gate {name}: {qid} has no 'Chosen by: user'")
    return problems, notes


def find_progress(arg):
    if arg:
        path = Path(arg)
        return path / "progress.md" if path.is_dir() else path
    candidates = [p for p in Path.cwd().glob(".scratchpad/*/progress.md") if "## Plan" in p.read_text(encoding="utf-8")]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def main():
    args = [a for a in sys.argv[1:] if a != "--hook"]
    hook = "--hook" in sys.argv[1:]
    hook_input = {}
    if hook and not sys.stdin.isatty():
        try:
            hook_input = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            pass
    # In a hook, stdout must stay empty: some agents read it as JSON.
    out = sys.stderr if hook else sys.stdout
    progress = find_progress(args[0] if args else None)
    if progress is None:
        print("plan check: no progress.md with a plan; nothing to check", file=out)
        return 0
    if not progress.is_file():
        print(f"plan check: {progress} not found", file=sys.stderr)
        return 1
    problems, notes = check(progress)
    for n in notes:
        print(f"plan check: note: {n}", file=out)
    if not problems:
        print(f"plan check: ok ({progress})", file=out)
        return 0
    print(f"plan check: {len(problems)} problem(s) in {progress}", file=sys.stderr)
    for p in problems:
        print(f"- {p}", file=sys.stderr)
    if hook:
        return 0 if hook_input.get("stop_hook_active") else 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
