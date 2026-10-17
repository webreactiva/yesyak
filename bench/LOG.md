# YesYak benchmark log

Each run drives a puppet agent (OpenCode) through the YesYak process on a small real project, with Claude Code as the human user. The procedure lives in `.claude/skills/yak-bench/SKILL.md`. One file per run in `runs/`. Run folders stay in `.scratchpad/bench/` (not in git).

## Runs

| Run | Date | YesYak | Project · task | Model | Sessions | Reached | Interventions (nudge/correction/rescue) | Cost ≈ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0000](runs/0000-pilot.md) | 2026-10-17 | 7c48557 (pre 0.1.0) | tempopod (local copy) · feature `--json` | openai/gpt-5.6-sol | `ses_eb7033533ffekA0DFyUq18fLtY` (failed: gpt-5.5 not allowed), `ses_eb702b60bffezWdNrdrCOwevSH` | 2 Write the contract (stopped) | 0/0/0, unattended | not measured |
| [0001](runs/0001-candlestick-lines.md) | 2026-10-17 | v0.1.0 | BoboTiG/py-candlestick-chart · feature #44 (chart lines) | openai/gpt-6-luna | `ses_eb6f88379ffedZji6QZ14HqhQj` (work), 3 probe sessions | 6 Retrospective (all phases) | 3/5/1 | 0.73 $ |
| [0002](runs/0002-sjson-empty-key.md) | 2026-10-17 | v0.2.0 | tidwall/sjson · bug #77 (delete an empty key) | openai/gpt-6-luna | `ses_eb6c7d954ffef4eMk69SYt66i5` (work), 1 probe session | fix route complete | 2/0/1 | 0.05 $ |
| [0003](runs/0003-markdown-nbsp.md) | 2026-10-17 | v0.3.0 | thephpleague/html-to-markdown · feature #258 (keep non-breaking spaces) | ollama-cloud/deepseek-v4.1-flash | `ses_eb6aef4efffessgcw9rHdUKN8n` (work), 2 probe sessions | 6 Retrospective (all phases) | 0/3/0 | 0.22 $ |
| [0004](runs/0004-pmemoize-while-pending.md) | 2026-10-17 | v0.3.1 | sindresorhus/p-memoize · feature #53 (`cache: 'while-pending'`) | ollama-cloud/glm-5.3 | `ses_eb6488a4effeCMZNyqQMzguBzN` (work), 1 probe session | 6 Retrospective + agent hook | 0/0/0 | 5.63 $ |
| [0005](runs/0005-vivid-theme-panic.md) | 2026-10-17 | v0.3.2 | sharkdp/vivid · bug #242 (panic on malformed theme values) | ollama-cloud/deepseek-v4.1-flash | `ses_eb5f1ed03ffeR1Tj8yGoAeajlI` (work), 1 probe session | fix route complete | 0/0/0 | 0.05 $ |
| [0006](runs/0006-serialize-nonobject.md) | 2026-10-17 | v0.3.2 | sindresorhus/serialize-error · feature #25 (`onNonObject` option) | ollama-cloud/minimax-m2.7 | `ses_eb5c24a03ffe5wm2uvRxCQ3cDl` (work), 1 probe session | 6 Retrospective (all phases) | 1/4/0 | 0.29 $ |
| [0007](runs/0007-filenamify-entry.md) | 2026-10-17 | v0.3.3 | sindresorhus/filenamify · feature #43 (`filenamify/path` entry) | ollama-cloud/deepseek-v4.1-flash | `ses_eb5a30ed1ffefpJkQlv7BzSrLr` (work), 1 probe session | 6 Retrospective (all phases) | 0/1/0 | 0.12 $ |
| [0008](runs/0008-retry-novice.md) | 2026-10-17 | v0.3.4 | avast/retry-go · feature #107 (retry on a rejected value), devil's advocate user | ollama-cloud/deepseek-v4.1-flash | `ses_eb591dddfffes1fAciXxlNwClE` (work), 1 probe session | feature built; process never started | 6 user mistakes: 🟢1 🟠2 🔴3 | 0.05 $ |
| [0009](runs/0009-filenamify-claude.md) | 2026-10-17 | v0.3.4 | sindresorhus/filenamify · feature #43, same as 0007 | anthropic/claude-sonnet-5-5 (Claude Code) | `0521d082-9033-4725-b0ed-a3fe5e8dfdd8` (work), 1 probe session | feature built; process skipped | 0/0/0 (no checkpoint reached) | 0.32 $ |

## Metrics

From `report.py metrics .scratchpad/bench <claude-transcript.jsonl>`. Puppet: Turns are human messages, Steps are model calls, Wall is session time including the waits for the human, Agent is model time only. Driver: the Claude Code session that plays the human (and its subagents), in the time window of the run's sessions only; setup and scoring outside the window are not counted. Prices from models.dev; a 1-hour cache write is priced as a normal cache write, so the driver cost is a little low.

| Run | Model | Turns | Steps | Wall | Agent | Input | Output | Cache read | Cost $ | Driver steps | Driver tokens (out) | Driver $ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0000-pilot | openai/gpt-5.6-sol | 2 | 56 | 16 min | 16 min | 130759 | 34638 | 4528640 | 3.03 | 109 | 25851644 (64936) | 7.35 |
| 0001-candlestick-lines | openai/gpt-6-luna | 35 | 443 | 46 min | 35 min | 903309 | 210103 | 53797120 | 0.73 | 129 | 40080259 (51978) | 9.84 |
| 0002-sjson-empty-key | openai/gpt-6-luna | 10 | 74 | 6 min | 4 min | 109861 | 14385 | 2722560 | 0.05 | 29 | 12767107 (10208) | 2.86 |
| 0003-markdown-nbsp | ollama-cloud/deepseek-v4.1-flash | 19 | 176 | 65 min | 18 min | 384216 | 150705 | 22311168 | 0.21 | 57 | 28780251 (21180) | 6.42 |
| 0004-pmemoize-while-pending | ollama-cloud/glm-5.3 | 15 | 140 | 35 min | 32 min | 260144 | 157745 | 17595776 | 5.63 | 42 | 23736753 (13243) | 5.18 |
| 0005-vivid-theme-panic | ollama-cloud/deepseek-v4.1-flash | 7 | 74 | 7 min | 5 min | 85386 | 50313 | 3847946 | 0.05 | 21 | 1843729 (8667) | 0.66 |
| 0006-serialize-nonobject | ollama-cloud/minimax-m2.7 | 13 | 103 | 11 min | 8 min | 123495 | 28417 | 3700423 | 0.29 | 17 | 2353051 (9774) | 0.78 |
| 0007-filenamify-entry | ollama-cloud/deepseek-v4.1-flash | 15 | 103 | 16 min | 13 min | 171722 | 113137 | 9395826 | 0.12 | 20 | 3254531 (8285) | 1.16 |
| 0008-retry-novice | ollama-cloud/deepseek-v4.1-flash | 5 | 27 | 5 min | 4 min | 152304 | 35841 | 1367424 | 0.05 | 6 | 1513658 (3899) | 0.42 |
| 0009-filenamify-claude | anthropic/claude-sonnet-5-5 | 7 | 25 | 4 min | 3 min | 46 | 12647 | 796241 | 0.32 | 7 | 2014066 (5447) | 0.56 |

## Findings

Status: `watch` (seen once), `confirmed`, `fixed in vX.Y.Z`, `verified in run NNNN`.

| Id | Class | Status | Finding | Evidence |
| --- | --- | --- | --- | --- |
| F-001 | Skill | fixed in v0.3.4 | A spec of 146 lines for one CLI flag: write-acceptance-spec does not scale the spec to the size of the change (no-slop-code says a spec longer than the code is suspect) | 0000: `docs/json-output-spec.md`; 0001: 207-line spec for about 60 lines of code; 0003: 230-line spec for 37 lines of `src`, after the v0.2.0 rule (second model). The rule became a count reported at the checkpoint; 0004 reported 160 vs about 110 and cut; 0006: counted, did not cut until told (minimax); 0006 and 0007 (deepseek): counted and cut a little, then argued for a long spec; the rule now names the sections that stay |
| F-002 | Bench | fixed in bench tools | The pilot ran with the user's global OpenCode config (other skills, a browser MCP server) and symlinked skills | 0000: `opencode.json` of the user; now `turn.sh` isolates the config and `prepare.sh` copies the skills |
| F-003 | Bench | fixed in bench tools | The clone kept `origin` pointing to the original repository | 0000; now `prepare.sh` removes the remote |
| F-004 | Skill | verified in runs 0002 and 0003 (baseline held at every commit) | customize-yak detected only the test command, so AGENTS.md named pytest alone; the loop, verify-against-spec and red-team-review never ran lint or types, and the branch added 13 ruff errors that only the human found. The command it later wrote fixed files in place | 0001 turns 16, 24, 28, 30, 31 |
| F-005 | Skill | verified in run 0003 | progress.md marked 5 Sign your work done without `pr-body.md`; ask-yak trusted it and pointed to the retrospective | 0001 turn 33 |
| F-006 | Skill | fixed in v0.2.0 | session-retrospective-rules named only the Claude Code and Codex transcript paths; on OpenCode the agent said "no transcript" and wrote the retrospective without quotes | 0001 turns 34-36 |
| F-007 | Skill | verified in run 0003 | verify-against-spec heading "Close the gaps now" made the agent write and commit tests during verification | 0001 turn 26 |
| F-008 | Model | watch | on-the-spot ran five rounds for a small feature; the last ones only confirmed defaults | 0001 turn 14; not repeated in 0003 with deepseek (three scaled rounds): likely the model |
| F-009 | Skill | watch | walking-skeleton-plan: step 1 correct, but later steps bundled several capabilities | 0001 turn 21 |
| F-010 | Model | watch | Optional steps not offered (spec review), and fixes offered before triage-findings-list | 0001 turns 17, 29; not repeated in 0003 (both optional steps offered) |
| F-011 | Skill | fixed in v0.3.0 | No gitmoji in commits. Both projects use another convention in their history, so the real gap was that nothing detected the project's own convention; customize-yak now detects it and writes it to AGENTS.md | 0001 turns 16-30; 0002 turn 7 |
| F-012 | Skill | watch | customize-yak searched for `check_yesyak.py` with a glob; the skills folder was git-ignored, so the search found nothing and the required first line was dropped | 0001 turn 4 |
| F-013 | Skill | watch | on-the-spot recommended options wider than the request (a removal API) | 0001 turn 12 |
| F-014 | Skill | verified in run 0003 | session-retrospective-rules: first pass covered only the last turns; chose an AGENTS.md rule for a mistake a machine can check | 0001 turn 35; 0002 turn 11 (missed the turn-3 nudge); 0006: missed messages and the chat rules (minimax) |
| F-015 | Skill | watch | ask-yak showed the whole entry-point table although the message was already a feature request | 0001 turn 6 |
| F-016 | Model | watch | gpt-6-luna loads unrelated skills each turn and sometimes leaks reasoning text into the answer | 0001 turns 10-13 |
| F-017 | Harness | noted | `opencode run` cancels the question tool; the skills fell back to questions in the chat, as on-the-spot allows | 0001 turns 4, 9 |
| F-018 | Bench | fixed in bench tools | Isolation: OpenCode reads `.agents/skills` in every parent folder and the shared service uses the user's config; clones now live outside home, with a fake HOME and a per-run server | 0001 turns 1-3 |
| F-019 | Bench | fixed in bench tools | Background subagents died with a per-turn `--standalone` server; now one password-protected `opencode serve` per run | 0001 turns 26-28 |
| F-020 | Bench | fixed in bench tools | The project virtual environment was not on the puppet's PATH; a piped session export was cut at 256 KB | 0001 turns 15, 36 |
| F-021 | Skill | verified in run 0003 | customize-yak never commits the settings file and AGENTS.md; they stay untracked for many turns | 0001 turns 5-17; 0002 turn 5 |
| F-022 | Skill | fixed in v0.3.0 | The short PR body for a bug was written only in bug-intake; write-visual-pr, the skill loaded at that step, used the feature template | 0002 turn 9 |
| F-023 | Skill | verified in run 0003 | The fix route never checked the git host; at the PR step the agent blocked waiting for a remote | 0002 turn 10; 0005: checked the remote only at the PR step, did not block |
| F-024 | Skill | watch | customize-yak showed only the settings diff, not the AGENTS.md diff, until asked | 0002 turn 3 |
| F-025 | Model | watch | Bug fix covered by one test case; siblings (`DeleteBytes`, JSON without the key) not tested | 0002 turn 7; not repeated in 0005 (deepseek tested seven cases) |
| F-026 | Bench | fixed in bench tools | The puppet blocked on publishing a PR; the bench now tells it in the first request that PRs stay local (user rule: never publish) | 0002 turn 10 |
| F-027 | Skill | verified in run 0004 | The AGENTS.md line "run the check before every commit" cannot hold when the default branch already fails; it now says "add no new failures" and where the known failures are | 0003 turns 4-5 |
| F-028 | Harness | fixed in bench tools | OpenCode's question-cancel message tells the agent to assume and go on, so it wrote files without the yes customize-yak asks for; the bench now disables the question tool, so questions go to the chat | 0003 turn 2 |
| F-029 | Model | watch | on-the-spot put the recommended option first but did not mark it "(Recommended)" | 0003 turn 7; marked in 0004; 0006 (minimax) |
| F-030 | Skill | watch | An ADR for a routine fix (keep a converter usable without configuration); decision-record-log says no ADR for routine fixes, but it fixes a public contract | 0003 turn 16; not repeated in 0005 (no ADR for a fix) |
| F-031 | Bench | noted | OpenCode Zen had no funds; composer could not authenticate with the user's stale global GitHub token. Runs use ollama-cloud models and an empty COMPOSER_HOME | 0003 setup |
| F-032 | Skill | fixed in v0.3.2 | `npm test 2>&1 | tail -5 && git commit` passed a failing check: the pipe returns the exit code of `tail`. git-commit-organizer now says to read the check's own exit code | 0004 turns 10, 13; 0005: not exercised (git-commit-organizer not loaded; checks run apart, read through `grep`); 0006: loaded; checks in separate calls through `tail`, read as text; no failing commit |
| F-033 | Skill | verified in run 0007 | The phase 0 proposal to write chat rules to AGENTS.md put the rule inside the YesYak block; project rules belong outside it | 0004 turn 5; 0006 (second model): rules written inside the block after a nudge; phase 0 did not propose them. Pipeline step now says outside the block; verified in 0007 (forced) |
| F-034 | Skill | fixed in v0.3.5 | A known failure that stops an `&&` check chain hides the later steps; "add no new failures" then checks nothing after it. The agent ran the tests apart, but no skill says to | 0004 turns 3-4, 10; 0006 (forced): `npm test` = `xo && ava && tsd`, xo fails on main, no lint ran on new code. customize-yak now runs each step apart; verified in 0007 (forced); 0009 (Sonnet): ran the steps apart but named the chain in the block. The template's check line now asks for one command per step |
| F-035 | Skill | verified in run 0004 | agent-hook-guard, first use: diagram and yes first, script plus OpenCode plugin, forced error, false positives, real run blocked | 0004 turns 14-15 |
| F-036 | Skill | watch | Fix route: `bug-report.md`, `progress.md` and `loop-log.md` written after the last commit; bug-intake writes the report before the fix route, and execute-plan-loop updates `progress.md` per step | 0005 turn 6; 0006 feature route: `progress.md` updated once, at the end; not repeated in 0007 |
| F-037 | Skill | watch | write-visual-pr asks for a "short body" for a bug fix with no measure; 123 lines for about 110 changed lines | 0005 turn 6 |
| F-038 | Bench | fixed in bench tools | The fake HOME hid rustup: no Rust toolchain for the puppet. `turn.sh` now passes the real `RUSTUP_HOME`, a per-run `CARGO_HOME` and `RUSTUP_TOOLCHAIN` when set | 0005 setup |
| F-039 | Skill | watch | Phase 5 skipped: "the PR stays local" read as "no PR body"; went to the retrospective | 0006 turn 10; not repeated in 0007 (same no-PR line) |
| F-040 | Model | watch | Steps 1-3 of the plan in one commit | 0006 turn 10 |
| F-041 | Bench | verified in run 0007 | The bench's `chore:` commit made the puppet detect Conventional Commits in a project that does not use them; `prepare.sh` now writes `.git/info/exclude` and commits nothing | 0006 turn 3 (0005 had a mixed history, so no evidence there); verified in 0007 |
| F-042 | Skill | fixed in v0.3.4 | The coverage check of walking-skeleton-plan used `seq -w 1 NN`, which does not pad below 10 on macOS, so it printed every criterion as missing | 0007 retrospective; reproduced |
| F-043 | Skill | watch | A red-team probe subagent left a symlink loop in the working tree that broke the suite; the orchestrator did not check the tree after the missions | 0007 turn 11 |
| F-044 | Bench | fixed in bench tools | With no bench commit, `prepare.sh` recorded `HEAD~1` as the base ref | 0007 setup |
| F-045 | Skill | watch | Skills installed but no YesYak block: a plain feature request never engaged the process (no ask-yak, no phase 0, no PR body, no retrospective). The pipeline description triggers on "end to end", and no skill checks for a missing block. `install.sh` now prints the next step | 0008 turns 2-5; same gap as F-049, seen with the block in place in 0009 |
| F-046 | Skill | watch | The user's uncommitted changes went into the new branch without a question (phase 0 did not run) | 0008 turn 3 |
| F-047 | Skill | watch | "Just code it, no spec" followed without one line on the risk or a short safe route | 0008 turn 3 |
| F-048 | Skill | watch | The user left early; the agent did not say which steps were left | 0008 turn 5 |
| F-049 | Skill | fixed in v0.3.5 | Nothing in the YesYak block says that a feature request or a bug report starts the process; Sonnet judged a breaking change "small", skipped every phase and answered "what now?" without ask-yak. The block template now has the line, and "ask before you skip a phase" | 0009 turns 4-5; 0008 (weak model, no block) |
| F-050 | Bench | fixed in bench tools | The bench drove only OpenCode. `turn-claude.sh` drives Claude Code, `prepare.sh` copies the skills to `.claude/skills` too, `report.py` reads Claude Code's stream JSON and transcripts | 0009 setup |
