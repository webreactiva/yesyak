# Next runs

Plans for the next runs. A run moves to `LOG.md` and `runs/` when it is done; delete its section here.

Goal of this series: three runs in a row with no new skill finding, at least one with a strong model, and every skill used at least once. The count starts at v0.3.8 (run 0012 found F-055, so it reset). A new skill finding resets the count.

## 0013 · a strong model, the optional steps

| | |
| --- | --- |
| Puppet | Claude Code, Sonnet (`YAKBENCH_ALLOW_EXPENSIVE=1`) |
| Project | Small, a feature with two real design options |
| Covers | `prototype-options`, `work-items-breakdown` (the user tracks work in a plain task list), `feature-walkthrough` (asked at the end), `production-readiness-review` only if the project deploys |
| How | Answer "yes" when the agent offers an optional step; if it does not offer one, ask in plain words ("can we try both designs first?", "I keep a task list", "walk me through the code") |

## 0014 · the novice again, strong model

| | |
| --- | --- |
| Puppet | Claude Code, Sonnet |
| Covers | F-045 to F-048 (watch since 0008, seen with a weak model only) |
| How | The six mistakes of run 0008 on another project |
