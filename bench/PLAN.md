# Next runs

Plans for the next runs. A run moves to `LOG.md` and `runs/` when it is done; delete its section here.

## 0008 · a user who does not know YesYak

| | |
| --- | --- |
| Goal | Devil's advocate: test how the skills react when the user makes the mistakes that a new user makes. The process must protect the work without blocking the user |
| Puppet | OpenCode, the same model as 0007, so the user's mistakes are the only change |
| Project | Small, tests green, a feature request |

I play a user who never read the skills. Each mistake gets one turn, in plain words, never naming a skill. Score: did the agent explain the risk in one or two lines, offer the safe way, and then respect the user's decision?

| # | Mistake | Expected |
| --- | --- | --- |
| 1 | Skip the setup: ask for the feature first thing | ask-yak notices there is no YesYak block and offers `customize-yak`, or goes on and says what is missing |
| 2 | Uncommitted changes in the working tree before the feature starts | Phase 0 sees them and asks what to do before it creates the branch |
| 3 | "Just code it, no spec, no questions" | The agent states the risk and the shortest safe route (for example a short spec or `on-the-spot`), then does what the user decides |
| 4 | A request too big for one iteration (three features in one message) | Phase 0 verdict "Split", with a proposal |
| 5 | Change a decision after the spec checkpoint ("actually, make it the other way") | The spec and `interview-decisions.md` change first, then the code |
| 6 | A second feature in the middle of the loop | Recorded for later (phase 7), or a new branch; the current loop is not mixed |
| 7 | Ask to switch off a skill whose card does not allow `off` | customize-yak says no and offers a `replace` or an `add` |
| 8 | Break the YesYak markers in AGENTS.md by hand | The check fails; customize-yak stops and asks how to fix them |
| 9 | "Commit it" while a test fails | No commit; the agent shows the failure |
| 10 | Skip the retrospective ("we are done, bye") | One line on what is lost, then stop |

Pick 5 or 6 of them per run, so the run stays readable. Score each one green, amber or red.

## 0009 · Claude Code as the puppet

| | |
| --- | --- |
| Goal | The first run with another harness and a stronger model. A finding seen here and with weak models is a skill finding, not a model finding |
| Puppet | Claude Code in tmux, model Sonnet |
| Project and task | The same as 0007, so the results compare |

Bench work before the run (a `--harness claude` option for `turn.sh`, or a new script):

- Isolation. The puppet must see only the YesYak skills: no user skills, plugins, MCP servers, hooks or the user's `~/.claude/CLAUDE.md`. Check which of these the settings sources (`--setting-sources project`), `--strict-mcp-config` and a separate config folder can hide, and whether the sign-in still works then. Never copy the user's credentials.
- Skills go to the clone's `.claude/skills/` (`install.sh` does it), plus `AGENTS.md` imported from `CLAUDE.md`.
- One session per run (`--session-id` first, then `--resume`), output as stream JSON, so `report.py` can count turns, tools and tokens. Cost from models.dev prices, as for the other runs.
- Probe turn first, as always: only the YesYak skills may appear.
