#!/usr/bin/env python3
"""Tests of check_plan.py on sample plans. Run: python3 test_check_plan.py"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_plan  # noqa: E402

SCRIPT = Path(__file__).parent / "check_plan.py"
ROWS = [
    ("Domain language", "domain-language"), ("Spec", "write-acceptance-spec"), ("Spec challenge", "red-team-review"),
    ("Plan", "walking-skeleton-plan"), ("Build", "execute-plan-loop"), ("Verification", "verify-against-spec"),
    ("Red team", "red-team-review"), ("Triage", "triage-findings-list"), ("Fixes", "execute-plan-loop (change-list mode)"),
    ("Pull request", "write-visual-pr"), ("Reviewer guide", "pr-reviewer-guide"), ("Retrospective", "session-retrospective-rules"),
]


def plan(loaded_until, answer="", rows=ROWS):
    steps = "\n".join(f"| {s} | {k} | yes | required | {'yes' if i < loaded_until else ''} |" for i, (s, k) in enumerate(rows))
    return f"""# Progress: orders-cancel

## Plan

- Route: feature-delivery-pipeline · preset: approver

| Step | Skill | Runs | Why | Loaded |
| --- | --- | --- | --- | --- |
| Interview | on-the-spot | no | answered in section 2 | — |
{steps}

| Gate | Before | Decision | Rule | Answer |
| --- | --- | --- | --- | --- |
| G-01 | Build | new column on orders | contract: data schema | {answer} |

## Phases
"""


class CheckPlan(unittest.TestCase):
    def run_check(self, text, log="", ended=False):
        folder = Path(tempfile.mkdtemp())
        (folder / "progress.md").write_text(text)
        (folder / "unattended-decisions.md").write_text(log)
        if ended:
            (folder / "retrospective.md").write_text("")
        return check_plan.check(folder / "progress.md")

    def test_complete_run_passes(self):
        log = "### Q-03 Phase 2 · plan approval\n- Chosen: add the column\n- Chosen by: user\n"
        self.assertEqual(self.run_check(plan(len(ROWS), "Q-03"), log, ended=True), [])

    def test_open_gate_before_its_step_passes(self):
        self.assertEqual(self.run_check(plan(3)), [])

    def test_gate_without_answer_after_its_step_started(self):
        problems = self.run_check(plan(6))
        self.assertTrue(any("gate G-01 has no answer" in p for p in problems), problems)

    def test_gate_answer_not_chosen_by_user(self):
        log = "### Q-03 Phase 2 · plan approval\n- Chosen: add the column\n"
        problems = self.run_check(plan(6, "Q-03"), log)
        self.assertTrue(any("no 'Chosen by: user'" in p for p in problems), problems)

    def test_skipped_load_before_a_later_load(self):
        text = plan(len(ROWS), "Q-03").replace("| Red team | red-team-review | yes | required | yes |", "| Red team | red-team-review | yes | required | |")
        problems = self.run_check(text, "### Q-03 x\n- Chosen by: user\n")
        self.assertEqual(problems, ["step 'Red team' ran with an empty Loaded cell: load red-team-review and redo its checks, or log the skip"])

    def test_required_step_missing_or_left_out(self):
        rows = [r for r in ROWS if r[1] != "verify-against-spec"]
        problems = self.run_check(plan(0, rows=rows).replace("| Triage | triage-findings-list | yes |", "| Triage | triage-findings-list | no |"))
        self.assertIn("required step verify-against-spec is not in the plan", problems)
        self.assertIn("required step triage-findings-list is left out without a gate that names it", problems)

    def test_hook_exit_codes(self):
        folder = Path(tempfile.mkdtemp())
        (folder / "progress.md").write_text(plan(6))
        run = lambda stdin: subprocess.run([sys.executable, str(SCRIPT), str(folder), "--hook"], input=stdin, capture_output=True, text=True).returncode
        self.assertEqual(run("{}"), 2)
        self.assertEqual(run(json.dumps({"stop_hook_active": True})), 0)


if __name__ == "__main__":
    unittest.main()
