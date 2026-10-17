# Next runs

Plans for the next runs. A run moves to `LOG.md` and `runs/` when it is done; delete its section here.

Goal of this series: three runs in a row with no new skill finding, at least one with a strong model, and every skill used at least once. The count starts at v0.3.8 (run 0012 found F-055, so it reset). A new skill finding resets the count.

Count: 0 after run 0017 (F-061). Every skill has now been used in at least one run.

## 0018 · a long piece of work across sessions

| | |
| --- | --- |
| Puppet | OpenCode, `ollama-cloud/deepseek-v4.1-flash`; one session cut changes the model (for example minimax) |
| Project | packbeat (the user's own, private, about 64k lines), the owner request for product UX improvements (`a2f271a`) |
| Setup | In the clone only, remove the project's own process (`.claude/skills`, `.claude/agents`, the "How to work" section of AGENTS.md) without a commit, so the puppet's branch starts clean from `main`. Then `install.sh` |
| Session cuts | After the spec checkpoint; in the middle of `execute-plan-loop` with a step not committed; between delivery 1 and 2. Each cut is `--new-session` with a plain "I continue with yesterday's work". One session with `unattended-run` |
| Measures | Resumes at the right step without asking what the files already say; no repeated work; keeps the decisions of earlier sessions; the retrospective covers every session (F-053) |
| Compare | With the project's own `delivery-loop` history (phases, commits, decision files, review findings, time per phase) |
| Exception | The user allows a real PR on this project. The puppet stays without a remote; after scoring, the driver shows the branch and the PR body to the user, then pushes to the project and opens the PR |
