# YesYak benchmark log

Each run drives a puppet agent (OpenCode) through the YesYak process on a small real project, with Claude Code as the human user. The procedure lives in `.claude/skills/yak-bench/SKILL.md`. One file per run in `runs/`. Run folders stay in `.scratchpad/bench/` (not in git).

## Runs

| Run | Date | YesYak | Project · task | Model | Sessions | Reached | Interventions (nudge/correction/rescue) | Cost ≈ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0000](runs/0000-pilot.md) | 2026-10-17 | 7c48557 (pre 0.1.0) | tempopod (local copy) · feature `--json` | openai/gpt-5.6-sol | `ses_eb7033533ffekA0DFyUq18fLtY` (failed: gpt-5.5 not allowed), `ses_eb702b60bffezWdNrdrCOwevSH` | 2 Write the contract (stopped) | 0/0/0, unattended | not measured |
| [0001](runs/0001-candlestick-lines.md) | 2026-10-17 | v0.1.0 | BoboTiG/py-candlestick-chart · feature #44 (chart lines) | openai/gpt-6-luna | `ses_eb6f88379ffedZji6QZ14HqhQj` (work), 3 probe sessions | 6 Retrospective (all phases) | 3/5/1 | 0.73 $ |

## Findings

Status: `watch` (seen once), `confirmed`, `fixed in vX.Y.Z`, `verified in run NNNN`.

| Id | Class | Status | Finding | Evidence |
| --- | --- | --- | --- | --- |
| F-001 | Skill | fixed in v0.2.0 | A spec of 146 lines for one CLI flag: write-acceptance-spec does not scale the spec to the size of the change (no-slop-code says a spec longer than the code is suspect) | 0000: `docs/json-output-spec.md`; 0001: 207-line spec for about 60 lines of code |
| F-002 | Bench | fixed in bench tools | The pilot ran with the user's global OpenCode config (other skills, a browser MCP server) and symlinked skills | 0000: `opencode.json` of the user; now `turn.sh` isolates the config and `prepare.sh` copies the skills |
| F-003 | Bench | fixed in bench tools | The clone kept `origin` pointing to the original repository | 0000; now `prepare.sh` removes the remote |
| F-004 | Skill | fixed in v0.2.0 | customize-yak detected only the test command, so AGENTS.md named pytest alone; the loop, verify-against-spec and red-team-review never ran lint or types, and the branch added 13 ruff errors that only the human found. The command it later wrote fixed files in place | 0001 turns 16, 24, 28, 30, 31 |
| F-005 | Skill | fixed in v0.2.0 | progress.md marked 5 Sign your work done without `pr-body.md`; ask-yak trusted it and pointed to the retrospective | 0001 turn 33 |
| F-006 | Skill | fixed in v0.2.0 | session-retrospective-rules named only the Claude Code and Codex transcript paths; on OpenCode the agent said "no transcript" and wrote the retrospective without quotes | 0001 turns 34-36 |
| F-007 | Skill | fixed in v0.2.0 | verify-against-spec heading "Close the gaps now" made the agent write and commit tests during verification | 0001 turn 26 |
| F-008 | Skill | watch | on-the-spot ran five rounds for a small feature; the last ones only confirmed defaults | 0001 turn 14 |
| F-009 | Skill | watch | walking-skeleton-plan: step 1 correct, but later steps bundled several capabilities | 0001 turn 21 |
| F-010 | Skill | watch | Optional steps not offered (spec review), and fixes offered before triage-findings-list | 0001 turns 17, 29 |
| F-011 | Skill | watch | No gitmoji in commits until change-list mode; git-commit-organizer loaded but the format was not followed | 0001 turns 16-30 |
| F-012 | Skill | watch | customize-yak searched for `check_yesyak.py` with a glob; the skills folder was git-ignored, so the search found nothing and the required first line was dropped | 0001 turn 4 |
| F-013 | Skill | watch | on-the-spot recommended options wider than the request (a removal API) | 0001 turn 12 |
| F-014 | Skill | watch | session-retrospective-rules: first pass covered only the last turns; chose an AGENTS.md rule for a mistake a machine can check | 0001 turn 35 |
| F-015 | Skill | watch | ask-yak showed the whole entry-point table although the message was already a feature request | 0001 turn 6 |
| F-016 | Model | watch | gpt-6-luna loads unrelated skills each turn and sometimes leaks reasoning text into the answer | 0001 turns 10-13 |
| F-017 | Harness | noted | `opencode run` cancels the question tool; the skills fell back to questions in the chat, as on-the-spot allows | 0001 turns 4, 9 |
| F-018 | Bench | fixed in bench tools | Isolation: OpenCode reads `.agents/skills` in every parent folder and the shared service uses the user's config; clones now live outside home, with a fake HOME and a per-run server | 0001 turns 1-3 |
| F-019 | Bench | fixed in bench tools | Background subagents died with a per-turn `--standalone` server; now one password-protected `opencode serve` per run | 0001 turns 26-28 |
| F-020 | Bench | fixed in bench tools | The project virtual environment was not on the puppet's PATH; a piped session export was cut at 256 KB | 0001 turns 15, 36 |
