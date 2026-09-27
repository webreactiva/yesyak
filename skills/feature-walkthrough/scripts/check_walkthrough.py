#!/usr/bin/env python3
"""Check a walkthrough: file:line citations at a commit, Mermaid blocks, length.

Usage: check_walkthrough.py <walkthrough.md> <commit>
Exit code 1 when a citation points to a missing file or past the end of a file,
or when a citation has no file path (`:42` alone).
"""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

FULL_CITATION = re.compile(
    r"`(?P<path>[\w./@-]+\.\w+):(?P<start>\d+)(?:-(?P<end>\d+))?`"
)
SHORT_CITATION = re.compile(r"`:\d+(?:-\d+)?`")


def line_count(path: str, commit: str) -> int | None:
    shown = subprocess.run(
        ["git", "show", f"{commit}:{path}"], capture_output=True, text=True
    )
    if shown.returncode == 0:
        return len(shown.stdout.splitlines())
    # Installed dependencies (node_modules/, vendor/, .venv/) are ignored by git: read them from disk.
    ignored = subprocess.run(["git", "check-ignore", "-q", path]).returncode == 0
    file = Path(path)
    return len(file.read_text().splitlines()) if ignored and file.exists() else None


def main() -> int:
    walkthrough, commit = sys.argv[1], sys.argv[2]
    text = Path(walkthrough).read_text()
    problems = []
    citations = list(FULL_CITATION.finditer(text))
    for match in citations:
        lines = line_count(match["path"], commit)
        end = int(match["end"] or match["start"])
        if lines is None:
            problems.append(f"missing file: {match['path']}")
        elif end > lines:
            problems.append(f"{match['path']}:{end} is past the end ({lines} lines)")
    short = SHORT_CITATION.findall(text)
    if short:
        problems.append(f"{len(short)} citations without a file path, e.g. {short[0]}")

    diagrams = Counter(
        block.split()[0] for block in re.findall(r"```mermaid\n(.*?)```", text, re.S)
    )
    ascii_blocks = len(re.findall(r"```text\n", text))
    print(f"lines: {len(text.splitlines())}")
    print(f"citations checked: {len(citations)}")
    print(f"mermaid blocks: {dict(diagrams) or 'none'}")
    print(f"ascii blocks: {ascii_blocks}")
    for problem in sorted(set(problems)):
        print(f"BAD {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
