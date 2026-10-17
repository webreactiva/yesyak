# Next runs

Plans for the next runs. A run moves to `LOG.md` and `runs/` when it is done; delete its section here.

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
