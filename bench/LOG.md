# YesYak benchmark log

Each run drives a puppet agent (OpenCode) through the YesYak process on a small real project, with Claude Code as the human user. The procedure lives in `.claude/skills/yak-bench/SKILL.md`. One file per run in `runs/`. Run folders stay in `.scratchpad/bench/` (not in git).

## Runs

| Run | Date | YesYak | Project · task | Model | Sessions | Reached | Interventions (nudge/correction/rescue) | Cost ≈ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0000](runs/0000-pilot.md) | 2026-10-17 | 7c48557 (pre 0.1.0) | tempopod (local copy) · feature `--json` | openai/gpt-5.6-sol | `ses_eb7033533ffekA0DFyUq18fLtY` (failed: gpt-5.5 not allowed), `ses_eb702b60bffezWdNrdrCOwevSH` | 2 Write the contract (stopped) | 0/0/0, unattended | not measured |

## Findings

Status: `watch` (seen once), `confirmed`, `fixed in vX.Y.Z`, `verified in run NNNN`.

| Id | Class | Status | Finding | Evidence |
| --- | --- | --- | --- | --- |
| F-001 | Skill | watch | A spec of 146 lines for one CLI flag: write-acceptance-spec does not scale the spec to the size of the change (no-slop-code says a spec longer than the code is suspect) | 0000: `docs/json-output-spec.md` |
| F-002 | Bench | fixed in bench tools | The pilot ran with the user's global OpenCode config (other skills, a browser MCP server) and symlinked skills | 0000: `opencode.json` of the user; now `turn.sh` isolates the config and `prepare.sh` copies the skills |
| F-003 | Bench | fixed in bench tools | The clone kept `origin` pointing to the original repository | 0000; now `prepare.sh` removes the remote |
