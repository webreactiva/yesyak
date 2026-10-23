# Run 0027-humanize-locale-pilot

- Source: https://github.com/python-humanize/humanize.git @ a2006eabf
- YesYak: v0.4.5-12-g2e2ae41 · model: ollama-cloud/deepseek-v4.1-flash · turns: 7
- Sessions: `ses_e9acd0593ffeofDETsdD6ptrCR` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e9accc3f4ffex3tqkrTG6uOH5O` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 85013, output 97763, cache_read 10276992, cache_write 0 · ≈ 0.1022 $ (models.dev prices)
- Time: 15 min wall, 9 min of agent work · model steps: 109
- Tool calls: 143 · errors: 1
- Branch: fix/naturalsize-locale-separator
- Skills loaded, in order: customize-yak → git-commit-organizer → yak-pilot → bug-intake → execute-plan-loop → unattended-run → write-visual-pr → pr-reviewer-guide → session-retrospective-rules
- Puppet: OpenCode with deepseek-v4.1-flash; YesYak from branch `feat/autopilot-plan` @ 2e2ae41
- Task: bug #460 (`naturalsize()` ignores the locale decimal separator), a risky change: existing output in six locales and a hot path where an earlier attempt cost 10%. Profile: `approver`
- Result: fix route complete. It measured three variants before the plan (+8.2% naive, +3.1% chosen) and benchmarked after (+2.2% to +2.7%). Branch `fix/naturalsize-locale-separator`: fix, regression tests, ADR, local PR body and guide, retrospective, and the AGENTS.md guard I allowed. Tests (I ran them): 880 passed
- Interventions: 0 nudges, 0 corrections, 0 rescues

## Autopilot

| Measure | Value |
| --- | --- |
| Skills the user named | 0 |
| Blocking questions | 0 |
| Spec and plan sized as | none; the contract is pinned by `intword`/`intcomma` |
| Planned gates / dynamic gates | 2 (plan, `gnu=True` output) / 0 |
| Profile-rule stops | 1 (apply a retrospective guard) |
| Decisions taken alone | 3 (`Q-01`–`Q-03`: skip verify, red team, work items), none to revert |
| Missed gates / gates too many | 0 / 0 |
| Skills planned but not loaded | 0 |
| Extra messages after the plan approval | 0 |
| PR body "Gates" line | yes (F-072 verified) |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 3 | customize-yak, setup | setup + profile onboarding | scope, decision records, preset, always/never | "ok" |
| 4 | customize-yak, preview | setup | write the three files? | "yes" |
| 6 | yak-pilot, after the plan | plan approval + planned gate G-01 | approve the plan; localize `gnu=True` too, or keep the dot? | "ok" (localize every mode) |
| 7 | session-retrospective-rules | profile rule ("apply a retrospective guard") | apply the AGENTS.md commit with three local-check notes? | "Yes, apply the AGENTS.md commit." |

## Findings

- None new. The +3% cost went without a gate: the user named no budget, and the run measured it and reported it.

## Cost

≈ 0.10 $ for the puppet; ≈ 1.47 $ for the driver.
