#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
PROCESS_FILE = SKILLS_DIR / "ask-yak" / "references" / "process.md"
MODES = {"add", "replace", "off"}
FIELDS = {"mode", "section", "instructions", "why"}
PRESETS = {"collaborator", "approver", "observer"}
PILOT_LISTS = ("always_ask", "never")
MAX_BYTES = 1_000_000
BLOCK = re.compile(r"<!-- yesyak:start -->(.*?)<!-- yesyak:end -->", re.S)
SKILL_NAME = r"[a-z0-9]+(?:-[a-z0-9]+)+"


def project_root():
    if (Path.cwd() / "AGENTS.md").is_file():
        return Path.cwd()
    try:
        output = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
        ).stdout.strip()
        return Path(output)
    except (OSError, subprocess.CalledProcessError):
        return Path.cwd()


def read_text(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("not a regular file")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f"larger than {MAX_BYTES} bytes")
    return path.read_text(encoding="utf-8")


def read_cards():
    process = PROCESS_FILE.read_text(encoding="utf-8")
    if "## Skill cards" not in process:
        sys.exit(f"no '## Skill cards' section in {PROCESS_FILE}")
    cards = {}
    for name, body in re.findall(r"^### (\S+)\n(.*?)(?=^### |\Z)", process.split("## Skill cards", 1)[1], re.M | re.S):
        replaceable = re.search(r"^- Replaceable: (.*)$", body, re.M)
        sections = replaceable.group(1).strip() if replaceable else "none"
        makes = re.search(r"^- Makes: (.*)$", body, re.M)
        cards[name] = {
            "replaceable": set() if sections == "none" else {s.strip() for s in sections.split(",")},
            "off_allowed": re.search(r"^- Off: allowed$", body, re.M) is not None,
            "makes": re.findall(r"`([^`]+)`", makes.group(1)) if makes else [],
        }
    return cards


def headings_outside_code(skill):
    headings, in_code = set(), False
    for line in (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code and re.match(r"#{2,3} ", line):
            headings.add(line.lstrip("#").strip())
    return headings


def load_settings(path, problems):
    repeated = []

    def keep_pairs(pairs):
        keys = [key for key, _ in pairs]
        repeated.extend(key for key in set(keys) if keys.count(key) > 1)
        return dict(pairs)

    try:
        settings = json.loads(read_text(path), object_pairs_hook=keep_pairs)
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as error:
        kind = "invalid JSON" if isinstance(error, json.JSONDecodeError) else "cannot read"
        problems.append(f"{kind}: {path}: {error}")
        return {}
    if not isinstance(settings, dict):
        problems.append(f"invalid settings: the file must hold a JSON object ({path})")
        return {}
    problems.extend(f"repeated key: {key} ({path})" for key in sorted(repeated))
    return settings


def check_entry(skill, entry, card, path):
    if not isinstance(entry, dict):
        return [f"invalid adjustment: {skill} is not an object ({path})"]
    mode = entry.get("mode")
    if not isinstance(mode, str) or mode not in MODES:
        return [f"invalid mode: {skill}.mode = {mode!r} ({path})"]
    problems = [f"unknown field: {skill}.{field} ({path})" for field in sorted(set(entry) - FIELDS)]
    if mode == "off" and not card["off_allowed"]:
        problems.append(f"off not allowed: {skill} ({path})")
    if mode in {"add", "replace"}:
        instructions = entry.get("instructions")
        if not isinstance(instructions, list) or not instructions or not all(isinstance(i, str) for i in instructions):
            problems.append(f"invalid instructions: {skill}.instructions must be a list of strings ({path})")
    if mode == "replace":
        section = entry.get("section")
        if not isinstance(section, str) or not section:
            problems.append(f"missing section: {skill}.section is required with replace ({path})")
        elif section not in card["replaceable"]:
            problems.append(f"section not replaceable: {skill}.section = {section!r} ({path})")
        elif not (SKILLS_DIR / skill / "SKILL.md").is_file():
            problems.append(f"skill not installed: {skill} ({path})")
        elif section not in headings_outside_code(skill):
            problems.append(f"section not found: {skill}.section = {section!r} is not a heading of the skill ({path})")
    return problems


def check_pilot(pilot, path):
    """The yak-pilot profile: a preset and two lists of plain-language entries."""
    if not isinstance(pilot, dict):
        return [f"invalid pilot profile: not an object ({path})"]
    problems = [f"unknown field: pilot.{field} ({path})" for field in sorted(set(pilot) - {"preset", "why", *PILOT_LISTS})]
    if "preset" in pilot and (not isinstance(pilot["preset"], str) or pilot["preset"] not in PRESETS):
        problems.append(f"invalid preset: pilot.preset = {pilot['preset']!r}, use one of {', '.join(sorted(PRESETS))} ({path})")
    for key in PILOT_LISTS:
        value = pilot.get(key, [])
        if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
            problems.append(f"invalid pilot.{key}: must be a list of non-empty strings ({path})")
    return problems


def check_settings(path, cards, problems, pilots=None):
    checked = {}
    for skill, value in load_settings(path, problems).items():
        if skill == "pilot":
            found = check_pilot(value, path)
            problems.extend(found)
            if pilots is not None and not found:
                pilots.append(value)
            continue
        if skill not in cards:
            problems.append(f"unknown skill: {skill} ({path})")
            continue
        entries = value if isinstance(value, list) else [value]
        if not entries:
            problems.append(f"invalid adjustment: {skill} has an empty list ({path})")
        if len(entries) > 1 and any(isinstance(e, dict) and e.get("mode") == "off" for e in entries):
            problems.append(f"off with other entries: {skill} ({path})")
        for entry in entries:
            problems.extend(check_entry(skill, entry, cards[skill], path))
        checked[skill] = [e for e in entries if isinstance(e, dict)]
    return checked


def read_block(root, problems):
    agents = root / "AGENTS.md"
    if not agents.exists():
        return None
    try:
        text = read_text(agents)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        problems.append(f"cannot read: {agents}: {error}")
        return None
    starts, ends = text.count("<!-- yesyak:start -->"), text.count("<!-- yesyak:end -->")
    if (starts, ends) not in {(0, 0), (1, 1)}:
        problems.append(f"broken YesYak markers in {agents}: {starts} start and {ends} end")
        return None
    blocks = BLOCK.findall(text)
    return blocks[0] if blocks else None


def check_adjusted_line(block, project, problems):
    if "check_yesyak.py" not in block:
        problems.append("settings line missing from the YesYak block: run customize-yak")
    match = re.search(r"^- Adjusted skills: (.*)$", block, re.M)
    named = {}
    for skill, modes in re.findall(rf"({SKILL_NAME}) \(([^)]*)\)", match.group(1) if match else ""):
        named[skill] = {m.strip() for m in modes.split(",")}
    expected = {skill: {e.get("mode") for e in entries} for skill, entries in project.items()}
    if named != expected:
        problems.append("adjusted skills line differs from .agents/yesyak.json")


def check_install_block(problems):
    """The minimal block that install.sh writes must use the same lines as the template of customize-yak."""
    install = SKILLS_DIR.parent / "install.sh"
    if not install.exists():
        return
    template = read_text(SKILLS_DIR / "customize-yak" / "SKILL.md")
    block = BLOCK.search(read_text(install))
    for line in (block.group(1).splitlines() if block else []):
        if line.startswith("- ") and "not set up" not in line and line not in template:
            problems.append(f"install.sh block line differs from the customize-yak template: {line[:60]}")


def check_dev(cards, problems):
    check_install_block(problems)
    for folder in sorted(p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")):
        if folder not in cards:
            problems.append(f"missing card: {folder}")
        description = re.search(r"^description: (.*)$", (SKILLS_DIR / folder / "SKILL.md").read_text(encoding="utf-8"), re.M)
        if not description or re.search(r"[<>]|: ", description.group(1)):
            problems.append(f"description missing, or with < > or ': ' (breaks YAML): {folder}")
    for skill, card in cards.items():
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        headings = headings_outside_code(skill) if skill_file.is_file() else set()
        problems.extend(f"card section not found: {skill}: {section}" for section in sorted(card["replaceable"] - headings))
        text = skill_file.read_text(encoding="utf-8") if skill_file.is_file() else ""
        for made in card["makes"]:
            name = made.rstrip("/").split("/")[-1]
            if re.search(r"[<*]|YYYY|NNNN", name) or not name or name == ".scratchpad":
                continue
            if name not in text:
                problems.append(f"card file not in skill: {skill}: {name}")
    pipeline = SKILLS_DIR / "feature-delivery-pipeline" / "SKILL.md"
    if not pipeline.is_file():
        problems.append("missing skill: feature-delivery-pipeline")
        return
    pipeline_phases = phases(re.search(r"```text\n(.*?)```", pipeline.read_text(encoding="utf-8"), re.S).group(1), cards)
    map_phases = phases(re.search(r"## Process map\n.*?```text\n(.*?)```", PROCESS_FILE.read_text(encoding="utf-8"), re.S).group(1), cards)
    for phase in sorted(set(pipeline_phases) | set(map_phases)):
        if pipeline_phases.get(phase) != map_phases.get(phase):
            problems.append(f"map differs in phase {phase}: pipeline {pipeline_phases.get(phase)}, map {map_phases.get(phase)}")


def phases(block, cards):
    result, current = {}, None
    for line in block.splitlines():
        start = re.match(r"^(\d) ", line)
        if start:
            current = start.group(1)
            result[current] = []
        if current is not None:
            result[current] += [s for s in re.findall(SKILL_NAME, line) if s in cards]
    return result


def active_lines(skill, entries, scope):
    for entry in entries:
        mode = entry.get("mode")
        if mode == "off":
            yield f"active: {skill} off ({scope})"
            continue
        section = f" [{entry.get('section')}]" if mode == "replace" else ""
        for instruction in entry.get("instructions") or []:
            yield f"active: {skill} {mode} ({scope}){section}: {instruction}"


def pilot_lines(project_pilot, user_pilot):
    """The project preset wins; the entries of both scopes apply."""
    for scope, pilot in (("project", project_pilot), ("user", user_pilot)):
        if pilot and "preset" in pilot:
            yield f"pilot: preset {pilot['preset']} ({scope})"
            break
    for scope, pilot in (("project", project_pilot), ("user", user_pilot)):
        for key in PILOT_LISTS:
            for entry in (pilot or {}).get(key, []):
                yield f"pilot: {key.replace('_', ' ')}: {entry} ({scope})"


def main():
    parser = argparse.ArgumentParser(description="Check the YesYak settings files and print the adjustments to apply.")
    parser.add_argument("--dev", action="store_true", help="also check skill cards and the process map")
    parser.add_argument("--project", type=Path, help="project settings file")
    parser.add_argument("--user", type=Path, help="user settings file")
    args = parser.parse_args()

    cards = read_cards()
    root = project_root()
    project_file = args.project or root / ".agents" / "yesyak.json"
    user_file = args.user or Path.home() / ".agents" / "yesyak.json"
    problems, notes = [], []
    project_pilot, user_pilot = [], []
    block = read_block(root, problems)
    project = {}
    for option, path in (("--project", args.project), ("--user", args.user)):
        if path is not None and not (path.exists() or path.is_symlink()):
            problems.append(f"file not found: {option} {path}")
    if project_file.exists() or project_file.is_symlink():
        if block is None:
            notes.append("project settings ignored: AGENTS.md has no YesYak block")
        else:
            project = check_settings(project_file, cards, problems, project_pilot)
    user = check_settings(user_file, cards, problems, user_pilot) if user_file.exists() or user_file.is_symlink() else {}
    if block is not None:
        check_adjusted_line(block, project, problems)
    if args.dev:
        check_dev(cards, problems)

    for line in problems + notes:
        print(line)
    if problems:
        print("no adjustment applies until these problems are fixed")
        return 1
    for skill, entries in user.items():
        if skill in project and any(e.get("mode") in {"replace", "off"} for e in entries + project[skill]):
            print(f"user entry not used: {skill}")
            continue
        if skill in project:
            print(f"both scopes adjust {skill}: where their lines conflict, apply the project line")
        for line in active_lines(skill, entries, "user"):
            print(line)
    for skill, entries in project.items():
        for line in active_lines(skill, entries, "project"):
            print(line)
    for line in pilot_lines(next(iter(project_pilot), None), next(iter(user_pilot), None)):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
