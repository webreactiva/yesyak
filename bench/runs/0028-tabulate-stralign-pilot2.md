# Run 0028-tabulate-stralign-pilot2

- Source: /Users/Shared/yak-bench/0026-tabulate-floatfmt-pilot @ ca8fbaeeb
- YesYak: v0.4.5-15-g0d54ca3 · model: ollama-cloud/deepseek-v4.1-flash · turns: 4
- Sessions: `ses_e9aaac57bffeVN3B9TM5BAXysw` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_e9aaa98cbffeLl3f951UFzTlYn` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 113141, output 41786, cache_read 5847296, cache_write 0 · ≈ 0.0596 $ (models.dev prices)
- Time: 5 min wall, 5 min of agent work · model steps: 85
- Tool calls: 98 · errors: 1
- Branch: fix/stralign-none
- Skills loaded, in order: yak-pilot → customize-yak → bug-intake → git-commit-organizer → execute-plan-loop → decision-record-log → write-visual-pr → session-retrospective-rules
- Puppet: OpenCode with deepseek-v4.1-flash; YesYak from branch `feat/autopilot-plan` @ 0d54ca3
- Task: a second session in the project of run 0026 (its work counted as merged): first a profile change in plain words ("always ask me before you change output that existing users already get"), then bug #294 (`stralign=None` breaks the table)
- Result: the profile change was committed apart; the new entry stopped the fix before any code. Option A built: closed-box formats pad, the other formats stay byte-identical (64 of 216 format and alignment pairs change, measured). ADR, local PR body, retrospective, two AGENTS.md lines I allowed. Tests (I ran them): 342 passed, 60 skipped; baseline 337
- Interventions: 0 nudges, 0 corrections, 0 rescues

## Autopilot

| Measure | Value |
| --- | --- |
| Skills the user named | 0 |
| Profile change in plain words | written to `.agents/yesyak.json` and committed apart; shown as a diff after the write, not before (F-078) |
| Blocking questions | 0 (it found that `preserve_whitespace=True` already covers the user's case, and said so) |
| Spec and plan sized as | bug report with an assumed contract; change list |
| Planned gates / dynamic gates | 1 (G-01, from the new profile entry) / 0 |
| Profile-rule stops | 2 (changed output; apply retrospective guards) |
| Decisions taken alone | red team skipped with a reason; none to revert |
| Missed gates / gates too many | 0 / 0 |
| Skills planned but not loaded | 0 |
| Extra messages after the gate | 0 |

## HIL stops

| Turn | Where | Kind | Question | My answer |
| --- | --- | --- | --- | --- |
| 3 | yak-pilot, before the branch | profile rule ("change output that existing users already get"), G-01 | pad only closed boxes, every format, or docs only? | "A. Go ahead." |
| 4 | session-retrospective-rules | profile rule ("apply a retrospective guard") | add two AGENTS.md lines (preview before a profile write; cite symbols, not line numbers)? | "Yes to both." |

## Findings

- F-078 (skill, watch): the profile change was written before a preview. `customize-yak` says preview, then write after a yes; the user's words were explicit, and the change narrowed autonomy. Its own retrospective proposed the guard.
- The profile loop works across sessions: a rule said in the chat went to the file, and the next decision of that kind stopped.

## Cost

≈ 0.06 $ for the puppet; ≈ 1.18 $ for the driver.
