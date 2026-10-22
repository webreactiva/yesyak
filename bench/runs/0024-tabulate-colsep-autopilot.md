# Run 0024-tabulate-colsep-autopilot

- Source: https://github.com/astanin/python-tabulate.git @ 268615a5c
- YesYak: v0.4.5-6-gafad9ba · model: ollama-cloud/deepseek-v4.1-flash · turns: 6
- Sessions: `ses_e9aeee711ffekurM8bev4coNdO` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e9aeea63cffe2yFarjf0KRDf33` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 143628, output 151351, cache_read 24732160, cache_write 0 · ≈ 0.1866 $ (models.dev prices)
- Time: 31 min wall, 28 min of agent work · model steps: 168
- Tool calls: 214 · errors: 1
- Branch: feat/column-separators
- Skills loaded, in order: customize-yak → autopilot-plan → feature-delivery-pipeline → git-commit-organizer → unattended-run → domain-language → on-the-spot → execute-plan-loop → write-visual-pr → plain-visual-docs → pr-reviewer-guide → session-retrospective-rules
- Puppet: OpenCode with deepseek-v4.1-flash; YesYak from branch `feat/autopilot-plan` (issue #1), not released
- Task: feature #357 (column group separators), an ambiguous request that changes a public API, with "Do it on autopilot; stop only where you need me"
- Result: all phases, alone after G-01. Branch `feat/column-separators`, 9 commits; spec, plan, verification (20/20 criteria), red team (1 blocking and 7 orange findings fixed, recheck with mutants), local `pr-body.md`, reviewer guide, retrospective. Tests (I ran them): 364 passed, 60 skipped; baseline 323 passed
- Interventions: 0 nudges, 1 correction (the plan), 0 rescues; 1 gate answer

## Autopilot

| Measure | Value |
| --- | --- |
| Blocking questions | 0 (the request gave the syntax; the open choices went to G-01) |
| Planned gates | 2: plan approval, G-01 at the spec (formats, characters, `showindex`) |
| Dynamic gates | 0 |
| Decisions taken alone | 12 (`Q-01`–`Q-12`, G-01 logged as `Q-07` "Chosen by: user") |
| Missed gates | 2: the plan skipped the phase 4 red team as "optional" (F-071, caught at the plan approval); Q-09 changed the output of existing flat tables, outside the request (F-073) |
| Gates too many | 0 |
| Extra messages after the plan approval | 1 correction at the plan approval ("keep the red team review after the build"); 0 after G-01 |
| Plan shown before work | yes |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 1 | customize-yak, setup | setup | scope, decision records, other steps to change | "1A 2A 3A, go ahead." |
| 4 | autopilot-plan, after the plan | plan approval | approve the plan: feature route, G-01 at the spec, red team skipped as "optional"? | "Approved, with one change: keep the red team review after the build. Skipping the spec challenge is fine." (correction) |
| 5 | write-acceptance-spec approval | planned gate G-01 | which formats show group separators; which characters; `showindex` | "1A 2A 3A." |

## Phases

| Phase | Reached | Artifacts | As the skill asks |
| --- | --- | --- | --- |
| autopilot-plan | yes | `autopilot-plan.md` | gates with reasons; required red team treated as optional (F-071) |
| 0 Starter kit | yes | branch, `progress.md` | yes |
| 1 Grill & sketch | yes, answered alone | `interview-decisions.md`, `domain-language.md` | `on-the-spot` loaded; questions logged as `Q-` |
| 2 Write the contract | yes | `docs/column-separators-spec.md`, plan, ADR 0001 | written without loading `write-acceptance-spec` or `walking-skeleton-plan` (F-074) |
| 3 Make it work | yes | 3 commits, tests per format | `execute-plan-loop` loaded |
| 4 Break it | yes | `verification-report.md`, `redteam-report.md` | done without loading `verify-against-spec` or `red-team-review` (F-074); real findings |
| 5 Sign your work | yes | `change-list.md`, `pr-body.md`, `pr-guide.md` | triage without `triage-findings-list` (F-074); gates listed in the PR body |
| 6 Retrospective | yes | `retrospective.md` | guards left as proposals (`Q-12`) |

## Findings

- F-071 (skill): the plan called the phase 4 red team "optional" and skipped it without a gate. The criterion named only "an optional phase skipped against the request". Fixed on the branch: leaving out a step that the process map does not put in brackets is a gate.
- F-073 (skill, watch): Q-09 applied a fix to existing flat-header output, outside the request, without a dynamic gate; Q-11 deferred another visible change for that same reason. One run, weak model.
- F-074 (skill, open in #1): five phase skills were not loaded; the agent did their work by hand (the reports exist and found real defects). Same pattern as F-056 and F-057 with Sonnet. The plan of skills must name each skill and check that it was loaded.

## Cost

≈ 0.19 $ at models.dev prices for the puppet; ≈ 3.77 $ for the driver.
