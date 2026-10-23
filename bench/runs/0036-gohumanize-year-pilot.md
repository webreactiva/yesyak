# Run 0036-gohumanize-year-pilot

- Source: https://github.com/dustin/go-humanize @ f5b54ae13
- YesYak: v0.4.5-37-gf5605ee · model: ollama-cloud/deepseek-v4.1-flash · turns: 7
- Sessions: `ses_e98611841ffeaZLv5C4o7cGrdc` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e98602413ffeES07g1HTS2TaRe` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 53484, output 30068, cache_read 2098460, cache_write 0 · ≈ 0.0324 $ (models.dev prices)
- Time: 6 min wall, 3 min of agent work · model steps: 56
- Tool calls: 58 · errors: 3
- Branch: fix/reltime-year
- Skills loaded, in order: customize-yak → git-commit-organizer → yak-pilot → bug-intake → unattended-run → write-visual-pr → session-retrospective-rules

- Puppet: OpenCode with ollama-cloud/deepseek-v4.1-flash, YesYak @ f5605ee (0.5.0 text)
- Project: dustin/go-humanize (Go), baseline `go test ./...` green
- Task: upstream #116, a year counts as 360 days (`Year = 12 * Month`), so relative times over several years drift
- Result: fix route complete in 6 minutes. Plan with every step of the fix route, two gates (exact length of a year; no spec for an exported constant), one commit (`Year = 365 * Day`, a regression test that fails on master), local PR body, retrospective. Tests green
- Interventions: 0 nudges, 0 corrections, 0 rescues

## Phases (fix route)

| Step | Reached | Artifact | Does what its skill asks |
| --- | --- | --- | --- |
| Setup | yes | `.agents/yesyak.json`, `AGENTS.md`, setup commit | yes, with the pilot profile round |
| Triage and bug report | yes | `bug-report.md` | yes; the Reproduction block was first written from predicted output, then corrected (the agent's own retrospective) |
| Branch | yes | `fix/reltime-year` | yes |
| Fix and tests | yes | `dcf588e` | yes, but `execute-plan-loop` never loaded |
| Verification, red team | no (optional) | `Q-02`, `Q-03` in `unattended-decisions.md` | yes, skipped with a reason |
| PR description | yes | `pr-body.md` | yes, local |
| Retrospective | yes | `retrospective.md` | yes, with the gates review |

## Autopilot

| Measure | Value |
| --- | --- |
| Skills the user named besides yak-pilot | 0 |
| Blocking questions | 0 (the two decisions went to gates) |
| Spec and plan sized as | the bug report and the change list |
| Planned gates / dynamic gates | 2 / 0 |
| Decisions taken alone | 3 |
| Missed gates / gates too many | 0 / 0 |
| Approvals without a change per gate kind | plan approval 1 (both gates as recommended) |
| Plan rows against the route | 8 rows, every step of the fix route, optional ones marked "no" (F-089 verified for the fix route) |
| Skills planned but not loaded | 1: `execute-plan-loop` (F-085) |
| Loaded column | empty in every row (F-092) |
| Extra messages after the plan approval | 0 |
| Profile changes proposed | 0 |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 2 | customize-yak, round 1 | setup + profile | scope, preset, decision records, which file the agent reads | "1A 2A 3A 4A" |
| 3 | customize-yak, preview | setup | always ask, never, write the files? | "yes" |
| 5 | yak-pilot, plan | plan approval with G-01 and G-02 | 365 or 365.25 days; no spec for a public constant | "1A 2A" |
| 6 | retrospective | profile rule (retrospective guard) | apply a wording change to `bug-intake`? | "Leave it." |

## Findings

- F-089 verified for the fix route: the plan lists every step.
- F-085 again with a weak model: `execute-plan-loop` planned "yes", the work done without loading it.
- F-092 again: the Loaded column stayed empty in every row, and the phase-end check did not catch it.

## Cost

≈ 0.03 $ for the puppet.
