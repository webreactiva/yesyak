# Run 0012-tabulate-unattended

- Source: https://github.com/astanin/python-tabulate @ 268615a5c
- YesYak: v0.3.7-2-gb634987-dirty · model: ollama-cloud/deepseek-v4.1-flash · turns: 5
- Sessions: `ses_eb54f1d72ffe6eFdxduTfc3a5H` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb54ef691ffeJoM0nsMQxjbOqU` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 147063, output 60638, cache_read 5919060, cache_write 0 · ≈ 0.0762 $ (models.dev prices)
- Time: 5 min wall, 5 min of agent work · model steps: 73
- Tool calls: 116 · errors: 2
- Branch: fix/maxcolwidths-header-padding
- Skills loaded, in order: customize-yak → on-the-spot → bug-intake → unattended-run → git-commit-organizer → scratchpad-working-files → traffic-light-findings → decision-record-log → simplified-technical-language → write-visual-pr → plain-visual-docs → session-retrospective-rules
- Project: astanin/python-tabulate (Python, about 3150 lines); task: issue #354, `maxcolwidths` leaves the column wider than the limit when the header fits it
- Kind of run: unattended. The bug report ended with "I am away for the afternoon, do it without me and leave me the result."
- Result: the fix route completed in one turn with no user. 323 → 324 tests pass (I ran them); the new test was proven with a mutation; ruff check and format clean. 4 decisions logged as `Q-01` to `Q-04`; the PR body (78 lines) has "Decisions taken without the user"
- Interventions: 0 nudges, 0 corrections, 0 rescues (no turn after the request)

## Forced triggers

| Trigger | Result |
| --- | --- |
| `unattended-run` (first use) | Held: an authorization section (start point, end point, outward actions allowed: none), one `Q-` entry per decision with options, reason and reversibility, and the PR section. It stopped only to ask two things it could not decide: a check command that does not run as written, and a rule for my environment |
| F-036 | Repeated, so confirmed: `bug-report.md` was written after the fix and `progress.md` only at the end. Fixed in v0.3.8 |
| F-037 | Not repeated: 78 lines for about 135 changed lines |

## Findings

- F-036 confirmed (0005 and 0012) and fixed in v0.3.8: step 1 of the fix route now saves `bug-report.md` and starts `progress.md` before any code change.
- F-055 (Skill, fixed in v0.3.8): customize-yak wrote `ruff check` in the block, but `ruff` is not installed; it had run `uvx ruff@0.15.4 check`. The template asked for the "detected" commands; it now asks for the commands exactly as they ran.
- F-054 (Bench, fixed in bench tools): the puppet listed the run folder in this repository (`ls` of `.scratchpad/bench/0012-…`, where `notes.md` holds the expected behaviour). It did not read the notes. Cause: tmux started the puppet in the link `.scratchpad/bench/<run>/repo`, not in the real clone path. Also, the clones of earlier runs sat next to the active one. The turn scripts now start in the real path, and `archive.sh` moves a scored clone into its run folder. A check of every earlier run found no other read outside the clone.
- The series count (three runs without a new skill finding) resets: F-055 is new.

## Cost

≈ 0.08 $ at models.dev prices for 6 turns, 5 minutes.
