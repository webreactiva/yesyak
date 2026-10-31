# Series 0039–: enforced mode A/B (issue #18)

This series is not like the runs before it. Earlier runs measured one version of the skills on one task. This series measures a **change of design**: does the enforced mode of `yak-pilot` (#17, PR #20) reduce the failures of the process, compared to the skills as they are on `main`?

## What is different from earlier runs

| Item | Earlier runs | This series |
| --- | --- | --- |
| Unit of evidence | one run | a **pair** of runs: A and B, same project, ref, task, model and human answers |
| Skills | the current `skills/` | A: `main` (as today). B: branch `feat/enforced-pilot` (PR #20), not released |
| What B adds | — | `yak-pilot/scripts/check_plan.py` run at each phase end; each phase in a fresh subagent; gate table with `Before` and `Answer` columns; `customize-yak` offers the plan check as an agent hook (for OpenCode 2: a plugin that blocks `git commit` and `git push` while the check fails) |
| Cost guard | the driver watched the cost | `report.py budget` stops a turn at 10 $ per run (PR #16, issue #10). **Not active in pair 1**: the driver's checkout was on `feat/enforced-pilot`, which has no budget; from pair 2 on, the bench scripts come from a checkout with PR #16 |
| Human answers | chosen per run | the same answer policy in A and B: the recommended option at every question, the default profile, the same task words. The questions themselves differ between A and B (the model is not deterministic), so the policy is the constant, not the words. A different answer is recorded with its reason |
| Decision | a finding changes a skill | after at least four pairs, a section in `RESULTS.md` decides: keep the enforced mode as an option, make it the default, or drop it (and so whether #19, the outer program, is worth building) |

## Metrics per pair

From the run files, the same for A and B: required steps run, planned skills loaded (the Loaded column and `report.py run`), missed gates, gates too many, interventions (nudge, correction, rescue), real defects caught by the red team, human stops (HIL table), time, cost. For B also: how many times the plan check or the hook blocked, and what the model did then.

## Pairs

| Pair | A | B | Project · task | Model | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | 0039-tenacity-logging-a | 0040-tenacity-logging-b | jd/tenacity @ 32ac68f · issue #644, a `logging` parameter for `@retry` (public API: gates expected) | ollama-cloud/deepseek-v4.1-flash, OpenCode 2.2.5 | done |

Plan for the next pairs: a bug (fix route), a risky change (security or a data contract), and a second session in the same project, as `yak-bench` asks before an autopilot finding is confirmed. The user asked to start with OpenCode and deepseek-v4.1-flash.

## Result of pair 1

| Measure | A (main) | B (enforced) |
| --- | --- | --- |
| Phases reached | all | all |
| Required steps run | all | all |
| Skills planned but not loaded (`report.py`) | 0 | 0 |
| Loaded column | 9 empty cells of 14 that ran (F-092) | complete |
| `check_plan.py` at the end | 9 problems (+2 of the old gate format) | ok |
| Plan check runs by the model / hook blocks | — | 2 at least / 0 |
| Phases in fresh subagents | — (not asked) | no (F-097) |
| Gates | 2 planned (plan, spec), 0 dynamic | 4 planned (plan + 3 blocking answers), 0 dynamic, no spec gate |
| Missed gates / gates too many | 0 / 0 | 0 / 0 |
| Interventions (nudge/correction/rescue) | 0/0/0 | 0/1/0 (setup) |
| Human stops | 6 | 6 + 1 correction |
| Real defects caught by the red team | spec: 2 🔴; code: 1 blocking (a raising `__str__` hid the exception) | spec: 1 blocking (traceback source); code: 0 blocking, 4 edge cases after a second premortem |
| Commits · tests (agent's report) | 12 · 210 | 5 · 210 |
| Time (wall / agent) | 36 / 33 min | 40 / 31 min |
| Cost | 0.16 $ | 0.22 $ |

Reading of pair 1. The enforced mode fixed the record (Loaded complete, the check passes), but not the behaviour, because the behaviour was already right: in A every skill also loaded, and the empty cells were bookkeeping. The new rule "a fresh subagent per phase" was not followed. The hook was installed and active but never had a reason to block. B cost 37 % more (more input tokens). One pair with a weak model proves little: the next pairs must include a task where a skill is likely to be skipped (a bug, the fix route) and a stronger pull to skip, for example a small change.

## Before the series: hooks verified live (issue #17)

In a scratch project with a plan whose gate G-01 had no answer while its Before step had started:

| Agent | Hook | Result |
| --- | --- | --- |
| Claude Code (`claude -p`, Haiku) | `Stop` in `.claude/settings.json` | blocks the end of the turn; the model reads `progress.md` and does not invent the answer; the second stop passes (`stop_hook_active`) |
| OpenCode 2.2.5 (deepseek-v4.1-flash) | v2 plugin, `ctx.tool.hook("execute.before")` | blocks `git commit` while the gate is open; lets it through after a `Q-` answer with "Chosen by: user". The v1 plugin shape loads but never runs in OpenCode 2 (fixed in PR #20) |
| Codex 0.162.1 (gpt-5.6-sol, effort medium) | `Stop` in `.codex/hooks.json` | runs only after the user trusts it in `/hooks`; then blocks, and the model answers "Gate G-01 needs an answer before the Build step can proceed." |

## Log of the series

| When | Event |
| --- | --- |
| 2026-10-31 | Both runs prepared on the same ref. `prepare.sh` copied an untracked `__pycache__` of `skills/yak-pilot/scripts` into run A (a leftover of the branch switch): removed by hand. Bench finding: `prepare.sh` must copy only tracked files |
| 2026-10-31 | The driver's auto mode refused to install and run the project's code (`pip install`, `pytest`) in the clone. The user ran the baseline of A by hand: 184 passed, 1 skipped, 15 subtests passed. The puppet turns themselves were allowed |
| 2026-10-31 | Probe turns: A and B see only the 31 YesYak skills, plus the OpenCode built-ins `opencode` and `report` (known, issue #2); no instruction files |
| 2026-10-31 | A, setup turn: `customize-yak` detects `uv run poe lint/mypy/check`, Conventional Commits, no AGENTS.md; asks the profile round in one message (4 questions). Answer: the recommended options |
| 2026-10-31 | A, turn 3: diff of `.agents/yesyak.json`, AGENTS.md block, `.gitignore`. It moved `publish` out of always ask because the answer put it under never (coherent). Answer: "Yes, write it." |
| 2026-10-31 | B, setup turn: same detection; a profile round in another order, and it says a second short round follows for the safety limit and the plan check hook. Its recommended "always ask" list drops "open a browser" and "apply a retrospective guard": a recommendation that widens what the agent does alone (finding, watch). To keep A and B equal, the answer keeps the default list |
| 2026-10-31 | A, turn 4: setup committed (`2941c0b chore: set up YesYak process for this project`), check prints the profile. It warns that the skills are not in git (true for the bench clone) |
| 2026-10-31 | B, turn 3: second round: the never limit, and the plan check hook ("Yes, for OpenCode (recommended)" with `.opencode/plugins/yesyak-plan-check.js`). Its recommended never answer is "nothing"; A's was "deploy or publish". Answer `1B 2A`: never deploy or publish (same as A), install the hook |
| 2026-10-31 | A, turn 5: the task, the same words for B (`task.txt`) |
| 2026-10-31 | A, turn 5: `yak-pilot` loaded, on main, route feature, fits one iteration; one round of 3 blocking questions (logger name, levels, the last line when no exception), recommended first. Answer `1A 2A 3A`; B gets the same answer when it asks the same |
| 2026-10-31 | A finding (model, watch): the answer "decision records off" was said back ("no decision-records line, since decision-record-log is off") but `.agents/yesyak.json` has no `off` entry for it. Not corrected (already approved; a user reading the diff could miss it). A and B differ here: B wrote the entry |
| 2026-10-31 | B, turn 4: full preview with the OpenCode 2 plugin from the reference, the right skills path (`.agents/skills`). It wrote never `deploy` for the answer "never deploy or publish packages": correction at turn 5 (finding, watch) |
| 2026-10-31 | A, turn 6: plan in `progress.md`: 20 rows (one per step), spec and plan full, data changes none, 2 gates (G-01 plan approval, G-02 spec approval), hands-off from G-02. Loaded filled only for the starter kit so far. Answer: "Yes, approved." |
| 2026-10-31 | B, turn 5: setup committed (`38c63fb`) with never "deploy or publish packages" and the plugin; `check_plan.py` says nothing to check. It says OpenCode loads plugins at startup: the driver restarted B's per-run server (the bench keeps one alive between turns), as a user would restart OpenCode. Harness note: in a real session the user must restart OpenCode after the setup, or the hook is not active for the first piece of work |
| 2026-10-31 | B, turn 6: the task (`task.txt`) |
| 2026-10-31 | Driver mistake found: `report.py budget` is not in this checkout (it is on PR #16), so pair 1 runs without the 10 $ stop. Costs so far: A ≈ 0.05 $, B ≈ 0.03 $; the driver watches them by hand |
| 2026-10-31 | B, turn 6: `yak-pilot` loaded; its own round of 3 blocking questions (bool or logger, traceback on the final failure, a callback that returns a value), recommended first. Answer `1A 2A 3A`, the same policy as A |
| 2026-10-31 | A, turn 7: spec (17 AC) written, devil's advocate on it with a verifier: 9 confirmed findings, two 🔴 fixed (AsyncRetrying has its own `__init__`; `retry_error_callback` wins over `reraise`). Committed `49db79c`. Stops at G-02 spec approval. Answer: "Yes, approved." |
| 2026-10-31 | B, turn 7: plan in the new format: 20 rows, gate table with Before and Answer; its three blocking answers are gates G-02..G-04 with Answer Q-01..Q-03 ("Chosen by: user" in the log). No spec approval gate (A has one): B runs alone from the plan approval. Answer: "Yes, approved." |
| 2026-10-31 | Script finding (watch): `check_plan.py` on B's plan before the approval reports "G-01 has no answer, but the step Branch has started". Branch had Loaded = yes because B loaded `git-commit-organizer` while writing the plan; it was still on main. Loaded means "skill loaded", not "step started": the check reads the first as the second. Harmless here (the answer fills the cell), but a hook at that moment would block a commit of the plan itself |
| 2026-10-31 | A, turn 8 (one turn, 158 tool calls, ≈ 0.11 $): plan, build, verification, code red team (4 missions, 34 findings, one blocking defect fixed with mutation checks), fixes, a second pass, local PR body, reviewer guide, retrospective. 12 commits; 210 tests (+25) by its report (the driver's auto mode refused to run pytest in the clone). Ends at the always ask "apply a retrospective guard" with three proposals |
| 2026-10-31 | A, Loaded column: `check_plan.py` (run by the driver on A's plan) reports 9 steps with an empty Loaded cell, from Plan to Retrospective, while `report.py` shows that every one of those skills loaded. F-092 seen again in the control run: a bookkeeping gap, not a skipped skill. The 2 gate lines are only the old table format of A |
| 2026-10-31 | A, turn 9: retrospective gate. Answer (same policy for B): "None for now, thanks." |
| 2026-10-31 | B, turn 8 (one turn, 207 tool calls, ≈ 0.18 $): spec, devil's advocate + verifier (one blocking issue: the traceback cannot come from `exc_info=True` at the final log), plan, build, verification, code red team (4 missions + verifier), triage, fixes, a second premortem, local PR body, reviewer guide, retrospective. 5 commits; 210 tests by its report. Loaded column complete; `check_plan.py` run by the model after build and at the end: ok both times; the hook never had to block (no commit with a failing plan). Phases did NOT run in fresh subagents: B used subagents only for the red team missions, the same 8 calls as A (finding, watch: the new rule was not followed). The retrospective proposes a `customize-yak` guard from the driver's correction ("copy an always ask or never answer verbatim") |
| 2026-10-31 | B, turn 9: retrospective gate. Answer: "None for now, thanks." |
| 2026-10-31 | Both runs scored: `bench/runs/0039-tenacity-logging-a.md`, `bench/runs/0040-tenacity-logging-b.md`; LOG rows and findings F-096..F-100 |
