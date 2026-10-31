# Run 0044-tenacity-stats-b

- Source: https://github.com/jd/tenacity @ 32ac68f09
- YesYak: v0.4.5-60-ga31def9 · model: ollama-cloud/deepseek-v4.1-flash · turns: 10
- Sessions: `ses_e707ec1c5ffeCMvA9a9aPi7X7B` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e707e72a0ffe5VGnq8x3uG6uj2` (ollama-cloud/deepseek-v4.1-flash, from turn 2), `ses_e7060de69ffex0XB1y6WL2mnwl` (ollama-cloud/deepseek-v4.1-flash, from turn 7)
- Tokens: input 617801, output 211638, cache_read 24492018, cache_write 0 · ≈ 0.2931 $ (models.dev prices)
- Time: 122 min wall, 55 min of agent work · model steps: 223
- Tool calls: 328 · errors: 5
- Branch: fix/zero-multiplier-wait
- Skills loaded, in order: customize-yak → yak-pilot → bug-intake → unattended-run → git-commit-organizer → execute-plan-loop → decision-record-log → no-slop-code → simplified-technical-language → red-team-review → triage-findings-list → write-visual-pr → session-retrospective-rules → yak-pilot → bug-intake → unattended-run → execute-plan-loop → git-commit-organizer → decision-record-log → verify-against-spec → red-team-review → triage-findings-list → write-visual-pr → pr-reviewer-guide → session-retrospective-rules

- Puppet: OpenCode 2.2.5 with ollama-cloud/deepseek-v4.1-flash, skills of `feat/enforced-pilot` (PR #20, with the check fix `a31def9`)
- Series: B of pairs 3 and 4 in [the enforced mode A/B series](../series/0039-enforced-ab.md) (issue #18); A is [0043](0043-tenacity-stats-a.md)
- Project and tasks: the same as 0043
- Result, session 1: fix route with a red team (4 missions + verifier, then a premortem: 3 defects, one blocking, fixed); 3 commits, 185 → 196 tests by its report. Session 2: the rule went to the pilot profile (`.agents/yesyak.json`), committed on the open fix branch; #710 from `main` with G-02 from the new rule, red team (2 defects, fixed), reviewer guide; 4 commits; the rule was not on the new branch
- Interventions: 0 nudges, 0 corrections, 0 rescues. 1 harness action (server restart for the plugin)

## Autopilot

| Measure | Session 1 (#701) | Session 2 (#710) |
| --- | --- | --- |
| Skills the user named besides yak-pilot | 0 | 0 |
| Spec and plan sized as | bug report, change list | bug report, change list |
| Planned gates / dynamic gates | 1 (plan) / 0 | 2 (plan; G-02 from the profile rule) / 0 |
| Missed gates / gates too many | 0 / 0 | 0 / 0 |
| Skills planned but not loaded | 0 (it did the triage before loading `bug-intake`, then loaded it) | 0 |
| `check_plan.py` | run by the model; **the plugin blocked one commit** (empty Loaded cell for the red team); final ok | run by the model; **the plugin blocked one commit** (3 empty Loaded cells); final ok |
| Fresh subagent per phase | no (subagents for the red team only) | no |
| Profile change | — | through `customize-yak` into the pilot profile, with a scope and wording question; committed on the fix branch of session 1, so the #710 branch lost it (F-102); G-02 still fired because the profile was read at the session start |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 2 | customize-yak | setup | preset, always ask + never, decision records, plugin | "yes" |
| 3 | customize-yak, preview | setup | write and commit? | "Yes, write it and commit." |
| 5 | yak-pilot, plan | plan approval (G-01) | approve the plan? | "Yes, approved." |
| 7 | new session | profile change | scope and wording | "Project, and the wording is fine." |
| 9 | yak-pilot, plan | plan approval (G-01) + profile gate (G-02) | approve; the 60 → 0 change for existing users | "Yes to both." |

## Findings

- F-097 confirmed: no fresh subagent per phase in any B run.
- F-102 (new, confirmed with 0043): the rule committed on the open fix branch.
- The profile rule worked as a gate in the same session (G-02).

## Cost

≈ 0.29 $ for the puppet (223 model steps, 55 min of agent work in 122 min wall).
