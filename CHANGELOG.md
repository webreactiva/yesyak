# Changelog

Versions follow semantic versioning. Before 1.0, a minor version can change a contract that settings files in other projects use (a skill name, a Replaceable heading, a phase number); its entry says so.

## 0.4.0 · 2026-10-17

From benchmark run 0015: without the YesYak block in AGENTS.md, a strong model skipped the skills for a small change, whatever the skill descriptions said (also runs 0009 and 0014). The block is the switch, so the install now writes it.

- `install.sh` writes a minimal YesYak block in AGENTS.md when there is none (the settings line, "a feature request starts the pipeline", and "YesYak is installed but not set up"), `@AGENTS.md` in CLAUDE.md when it installs for Claude Code, and `.scratchpad/` in `.gitignore`. It prints each file it writes. `-u` removes the block while it is still the minimal one.
- `customize-yak` treats the minimal block as a first install and replaces it with the full one. `feature-delivery-pipeline` offers `customize-yak` first when the block says YesYak is not set up.
- `check_yesyak.py --dev` fails when a line of the install block differs from the template of `customize-yak`.
- README: the install steps follow the new flow.

## 0.3.9 · 2026-10-17

From benchmark runs 0013 (Claude Code with Sonnet, a bug with a design choice) and 0014 (Sonnet as a user who does not know YesYak).

- `feature-delivery-pipeline`: the description triggers on any feature request or change in behavior, in any words, not only on "end to end" or "the full process". Phase 0 says when AGENTS.md has no YesYak block and offers `customize-yak` first. Without the block, two models did not start the process.
- `ask-yak`, `bug-intake`, `customize-yak`, `feature-walkthrough`, `handoff-and-resume`, `unattended-run`: the trigger phrases in the descriptions are English only. AGENTS.md says skills hold no words in another language.
- Benchmark: Claude Code puppets may use web tools; `report.py` reads every Claude Code stream event.

## 0.3.8 · 2026-10-17

From benchmark run 0012 (a Python library, a bug, unattended; the first use of `unattended-run`, which held), and an `unslop` review of every skill.

- `bug-intake`: step 1 of the fix route saves `bug-report.md` and starts `progress.md` before any code change. Two runs wrote them after the fix.
- `customize-yak`: the check line of the block holds the check commands exactly as they ran (for example through a tool runner when the tool is not installed).
- All skills: an `unslop` review removed dashes and colons that joined sentences, passive voice where the actor matters, arrows in prose and "harness" as a metaphor. No heading, skill name or card line changed.
- Benchmark: the puppet starts in the real path of its clone, and `archive.sh` moves a scored clone out of the way.

## 0.3.7 · 2026-10-17

From benchmark run 0011 (a request too big for one iteration, and a session cut), which exercised the "Split" verdict and `handoff-and-resume` for the first time; both held.

- `handoff-and-resume`: the session variable example names OpenCode's `OPENCODE_SESSION_ID` next to Claude Code's.
- Benchmark: the turn scripts remove the driver's Claude Code variables before they start the puppet.

## 0.3.6 · 2026-10-17

From benchmark run 0010 (Claude Code with Sonnet), which verified the 0.3.5 fixes.

- `feature-delivery-pipeline`: the phase 0 checkpoint question asks whether to write the working rules from the chat to AGENTS.md. A strong model skipped that step when it was only in the step list.

## 0.3.5 · 2026-10-17

From benchmark runs 0008 (a user who does not know YesYak) and 0009 (Claude Code with Sonnet, the same task as 0007).

- `customize-yak`: the YesYak block says that a feature request starts `feature-delivery-pipeline` and a bug report starts `bug-intake`, whatever the size, and that the agent asks before it skips a phase. A strong model skipped every phase of a breaking change because it looked small.
- `customize-yak`: the check line of the block asks for one command per step, never a chain that stops at a known failure.
- `install.sh` prints the next step when the project has no YesYak block.
- Benchmark: Claude Code can be the puppet (`turn-claude.sh`).

## 0.3.4 · 2026-10-17

From benchmark run 0007 (a JavaScript library, a feature), which also verified the 0.3.3 fixes.

- `write-acceptance-spec`: when the spec is longer than the change, keep only the TL;DR, the interface, the criteria and what is out of scope, and say why if it is still longer. Cutting "what repeats" let four runs keep specs several times longer than the code.
- `walking-skeleton-plan`: the coverage check builds zero-padded ids with `printf`; `seq -w` does not pad on macOS below 10.
- Benchmark: metrics per run (time, model steps, tokens, cost, and the driver's cost), and a plan for the next runs.

## 0.3.3 · 2026-10-17

From benchmark runs 0005 (a Rust tool, a bug) and 0006 (a JavaScript library, a feature, a project whose check already fails), with the findings forced on purpose.

- `customize-yak`: when one step of a chained check command (for example `a && b`) already fails on the default branch, run each step on its own and name the steps in the block. Before, the failing first step hid every step after it.
- `feature-delivery-pipeline`: working rules from the chat go to AGENTS.md outside the YesYak block.
- Benchmark: a run forces the findings that the last run did not exercise; the clone gets no bench commit; Rust toolchains reach the puppet.

## 0.3.2 · 2026-10-17

From benchmark run 0004 (a TypeScript library, a feature, a stronger model).

- `git-commit-organizer`: read the full check's own exit code before a commit; a pipe to another command returns the exit code of the last one.

## 0.3.1 · 2026-10-17

From benchmark run 0003 (a PHP library, a feature, a second weak model).

- `write-acceptance-spec`: before the checkpoint, count the lines of the spec against the estimated lines of code and tests, cut if the spec is longer, and report both counts. The v0.2.0 sentence alone did not stop a 230-line spec for 37 lines of code.
- `customize-yak`: the check line in the AGENTS.md block says "add no new failures" and where the known failures of the default branch are recorded.

## 0.3.0 · 2026-10-17

From benchmark run 0002 (a Go library, a bug, a weak model) and the findings it confirmed from run 0001.

- `customize-yak` detects the project's commit convention and writes it to the AGENTS.md block, and commits its own files apart from feature work.
- `session-retrospective-rules` starts from a list of every user message of the session, marked as request, answer, approval, nudge or correction.
- `write-visual-pr` owns the short body for a bug fix, and stops at the body when there is no remote. `bug-intake` points to it and checks the git host when it creates the branch.

## 0.2.0 · 2026-10-17

From benchmark run 0001 (a Python library, a feature, a weak model).

- `customize-yak` detects the full check (tests, lint, format, types), only with commands that do not change files, runs it once on the default branch and records the failures that are already there. The AGENTS.md block names the check commands. `git-commit-organizer` commits on the full check.
- `ask-yak`: a phase that `progress.md` marks done without the files its cards make is a conflict.
- `session-retrospective-rules` looks for the agent's sessions before it says there is no transcript, with examples for Claude Code, Codex and OpenCode.
- `verify-against-spec`: section 3 is now "Check the gaps with a script" and changes no source file. Not a Replaceable heading.
- `write-acceptance-spec` sizes the spec to the change.
- Benchmark: isolated per-run OpenCode server, clones outside the user's home, full transcripts saved, run 0001 in `bench/`.

## 0.1.0 · 2026-10-17

First tagged version.

- Phases named after the "Resuelve, rompe, repite" workflow: 0 Starter kit, 1 Grill & sketch, 2 Write the contract, 3 Make it work, 4 Break it, 5 Sign your work, 6 Retrospective, 7 Later. **Contract change:** the numbers of the old Build, Validate, Fix and Deliver phases changed; `ask-yak` maps the old names of an existing `progress.md`.
- Phase 0 asks whether the request fits in one iteration.
- New skills: `prototype-options` (optional, Grill & sketch) and `agent-hook-guard` (optional, Break it).
- `decision-record-log`: four questions decide an ADR; dependencies and patterns always get one, routine fixes and linter preferences never. A project can switch it off.
- `execute-plan-loop`: `loop-log.md`, an AGENTS.md review at the end, a look at every user interface step, one branch for the whole plan.
- `bug-intake`: a read-only triage first; checks in proportion to the light of the bug.
- `session-retrospective-rules`: session insights and agent hooks as guards.
- Smaller lessons in `write-acceptance-spec`, `write-visual-pr`, `no-slop-code`, `on-the-spot`, `customize-yak`.
