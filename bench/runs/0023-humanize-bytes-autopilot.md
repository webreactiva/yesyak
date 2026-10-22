# Run 0023-humanize-bytes-autopilot

- Source: https://github.com/python-humanize/humanize.git @ a2006eabf
- YesYak: v0.4.5-6-gafad9ba · model: ollama-cloud/deepseek-v4.1-flash · turns: 6
- Sessions: `ses_e9aef134affe9LLyqlSRK9qliq` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e9aeea63affeaRLTsRW4HxgLJb` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 94153, output 37100, cache_read 3780480, cache_write 0 · ≈ 0.0477 $ (models.dev prices)
- Time: 6 min wall, 5 min of agent work · model steps: 79
- Tool calls: 74 · errors: 0
- Branch: fix/naturalsize-fraction
- Skills loaded, in order: customize-yak → autopilot-plan → bug-intake → unattended-run → execute-plan-loop → git-commit-organizer → write-visual-pr → session-retrospective-rules
- Puppet: OpenCode with deepseek-v4.1-flash; YesYak from branch `feat/autopilot-plan` (issue #1), not released
- Task: bug #459 (`naturalsize()` truncates non-integer byte counts below the base), a clear requirement, with "Do it on autopilot; stop only where you need me"
- Result: fix route complete in one turn after the plan approval. Branch `fix/naturalsize-fraction`, one commit, 7 new and 2 corrected test rows, local `pr-body.md`, retrospective. Tests (I ran them): 753 passed, 132 skipped; baseline 746 passed
- Interventions: 0 nudges, 0 corrections, 0 rescues; 1 gate answer ("Approved.")

## Autopilot

| Measure | Value |
| --- | --- |
| Blocking questions | 0 (expected: the report states the behavior) |
| Planned gates | 1 (plan approval) |
| Dynamic gates | 0 |
| Decisions taken alone | 6 (`Q-01`–`Q-06`) |
| Missed gates | 0 (Q-02 follows the sibling rounding rule; Q-03 leaves the new msgid to Weblate, the project convention) |
| Gates too many | 0 |
| Extra messages after the plan approval | 0 |
| Plan shown before work | yes: route, gates, hands-off point, end point |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 1 | customize-yak, setup | setup | scope of the change, decision records, commit style | "A, A, A. Go ahead." |
| 2 | customize-yak, setup preview | setup | write the three setup files? | "Yes, write them." |
| 4 | autopilot-plan, after the plan | plan approval (G-01) | approve the plan: fix route, 1 gate, hands-off after it? | "Approved." |

## Fix route

| Step | Reached | As the skill asks |
| --- | --- | --- |
| autopilot-plan | yes | plan file, one gate, red team skipped with a reason (optional on the fix route) |
| bug-intake | yes | `bug-report.md`: triage, root cause (`int()` cast), assumed contract |
| execute-plan-loop, change-list mode | yes | failing test first; `loop-log.md` |
| Checks | full suite, `prek`, `tox -e mypy` | as the AGENTS.md block says |
| write-visual-pr | yes, local | "Decisions taken without the user" present; no gate line (F-072) |
| session-retrospective-rules | yes | proposes an AGENTS.md clarification, not applied |

## Findings

- F-072 (skill): the PR body has no gate line. The skill asked to put the gates, which the user decides, in "Decisions taken without the user"; the text contradicted itself. Fixed on the branch: a "Gates" line before that section.
- F-075 (bench): two runs started together raced to create the tmux session; one failed with `duplicate session`. Fixed in `turn.sh` and `turn-claude.sh`.

## Cost

≈ 0.05 $ at models.dev prices for the puppet; ≈ 0.86 $ for the driver.
