---
name: yak-bench
description: Internal benchmark of this repository. It takes a small real project, drives a weaker agent (OpenCode in tmux, as a puppet) through the YesYak process to build a feature or fix a bug, acting as the human user, then scores the run, records it in bench/LOG.md, turns the confirmed findings into skill changes and cuts a release. Use it whenever the user asks to run the benchmark, repeat it, "otra vuelta", test YesYak on a project, measure the process, or apply what the last runs found.
---

# Yak bench

The goal is always to improve YesYak. A run is evidence; a skill change is the result.

This skill belongs to this repository only. It is not in `skills/`, so `install.sh` never copies it to other projects.

## Roles

- **You are the human.** You choose the project and the task, answer the agent's questions, approve or reject, and correct it when a real user would. You never do its work, never edit its files, and never name a skill or a step that a real user would not name.
- **The puppet** is OpenCode with a cheaper model. It sees only the project and a frozen copy of `skills/`: no global skills, plugins, MCP servers or CLAUDE.md (`turn.sh` isolates it). A weaker model shows where the skills are not clear enough.

## Tools

All in `scripts/`. Runs live in `.scratchpad/bench/<run-id>/` of this repository (ignored by git). The clone itself lives in `/Users/Shared/yak-bench/<run-id>` and `repo` links to it: OpenCode reads `.agents/skills` in every parent folder, so a clone inside the user's home would see the user's own skills.

| Script | Does |
| --- | --- |
| `models.py list` | Models that OpenCode offers, with models.dev prices, cheapest first. Banned models never appear |
| `models.py check <model>` | Fails for a banned model (any `kimi k-3`, any `astra`) or one over the price cap (`YAKBENCH_MAX_OUTPUT`, 5 $/M output by default). Old models can be expensive: always check |
| `prepare.sh <run-id> <git-url> [ref]` | Clones the project without its remote, copies the skills, writes `run.json` with the YesYak version |
| `turn.sh <run-id> <message-file> [--model m] [--new-session]` | Sends one human message in tmux session `yak-bench`, waits, prints the answer, keeps every session id in `run.json`. Starts one isolated, password-protected `opencode serve` per run, so background subagents survive between turns |
| `report.py run <run-dir>` | Facts of the run: sessions, tokens, equivalent cost, skills loaded, commits, artifacts, tool errors. Saves each session export (the full transcript) in the run folder |

Run `turn.sh` in the background and wait for it to finish; one turn can take many minutes.

## 1. Read the log

Read `bench/LOG.md`: the last version, the models used, and the findings with status `watch` or `fixed`. A `fixed` finding must be checked again in this run; choose a project and task that can show it.

## 2. Choose the project, the task and the model

- **Project.** A public repository from GitHub (`gh api 'search/repositories?q=...'`), small (a few thousand lines at most), with tests that pass on this machine, in a stack that this machine runs (check with `command -v`). Change the stack and the kind of project from run to run. The user can name one.
- **Task.** A feature that fits one iteration, or a real bug (an open issue is best). Alternate features and bugs, so both entry points of `ask-yak` get tested.
- **Model.** Take it from `models.py list`. Prefer cheap and weak models; use OpenAI models with moderation. Ask the user when unsure.
- **Repetitions.** With a weak model (for example a luna, a flash or a nano model), one run proves little. Repeat the same task, or a similar one, before you call a finding confirmed.

## 3. Prepare

1. `prepare.sh <NNNN-short-name> <url>`. Run ids are numbered in the order of the log.
2. Run the project's tests yourself and write the baseline in `.scratchpad/bench/<run-id>/notes.md`.
3. Isolation check: one turn in a throwaway session ("Which skills and instruction files can you see? Only list them."). Only the YesYak skills may appear. Then start the real work with `--new-session`.

## 4. Drive the run

Start the way a real user starts, and let `ask-yak` lead:

1. "I just installed YesYak in this project, set it up." This tests `customize-yak`. Ask it to switch off `browser-acceptance-testing`: browser evidence is out of the benchmark unless the user asks for it.
2. The request in plain words: a feature request, or a bug report as a user would write it. Add one line: "Do not publish pull requests; the PR stays local." The benchmark never publishes a PR, and the clone has no remote.
3. At each checkpoint, answer as the product owner: take the recommended option when it is right, say no when it is wrong. When you do not know what comes next, ask the agent "what now?", as the process says.

Write every intervention in `notes.md`, with the turn number, the kind and your exact words:

| Kind | Meaning |
| --- | --- |
| answer | The agent asked and you answered: expected |
| approve | A checkpoint yes |
| nudge | You told it something the skills should have told it |
| correction | It did something wrong and you stopped it |
| rescue | It was stuck and you unblocked it |

Nudges, corrections and rescues are findings. Stop at the end of the Retrospective phase, after the turn limit (default 30), or when the equivalent cost passes the budget the user set.

## 5. Score

1. Run the tests yourself. Run `report.py run`.
2. Write `bench/runs/<run-id>.md` (committed): the report, then a table per phase of the process map: reached or not, the artifacts, and whether each one does what its skill asks. Then the interventions, the findings and the cost.

## 6. Turn findings into changes

Give each finding a class:

| Class | Action |
| --- | --- |
| Skill | Change the skill, following AGENTS.md (one rule in, one out; generic; no example from the benchmark project) |
| Model | Record it. Change a skill only if a cheap, clear rule would help any model |
| Harness | OpenCode or the puppet setup. Record it; fix the tools here if needed |
| Bench | A defect of this skill or its scripts. Fix it |

A skill finding changes a skill when it is confirmed: seen in two runs, or in one run with a strong model, or plainly wrong in the skill text. Otherwise its status is `watch`. After each skill change, run `python3 skills/ask-yak/scripts/check_yesyak.py --dev`.

## 7. Log, commit and release

1. Add the run to `bench/LOG.md`: one row in the runs table, and new or changed rows in the findings table (`F-NNN`, class, status `watch` / `confirmed` / `fixed in vX.Y.Z` / `verified in run NNNN`, evidence).
2. Commit with `git-commit-organizer`: skill changes (scope `skills`), bench changes (scope `bench`) and the log, each in its own commits.
3. If the skills changed, cut a release: add an entry to `CHANGELOG.md`, bump the version (0.x: minor for a new skill, rule or renamed contract; patch for a fix), and tag `vX.Y.Z` on the commit. Push tags only when the user asks.
4. Tell the user: the run in three lines, the findings, the changes, the new version and the next run you propose.
