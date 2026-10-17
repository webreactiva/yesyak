<p align="center"><img src="assets/logo.webp" alt="YesYak logo" width="240"></p>

# YesYak

YesYak is a set of agent skills that takes a feature from a vague request, or a bug from a report, to a reviewed pull request. The agent asks before it builds, writes the contract before the code, builds in small integrated steps, tries to break its own work, and ends with a retrospective that turns your corrections into guards.

The skills follow the open SKILL.md format. They are tested with Claude Code and OpenCode (see [the benchmark](#benchmark)). Each skill works on its own, except `customize-yak`, which needs `ask-yak` (its skill cards and its check script).

## Install

In the root of your project:

```bash
npx skills add delineas/yesyak
```

The command asks which skills and which agents. Take all the skills. To install everything for one agent without questions:

```bash
npx skills add delineas/yesyak --skill '*' --agent claude-code -y
```

Use the project scope (the default inside a project), so the skills go to the project's skills folder (for example `.claude/skills/`) and the team gets the same process. `npx skills update` updates them later. After an update, run `python3 <skills folder>/ask-yak/scripts/check_yesyak.py`. It reports adjustments that the new version breaks, for example a section that was renamed.

The skills do nothing until the project has the YesYak block in AGENTS.md. Step 2 of the user journey writes it. Without the block, agents often skip the skills for a small change.

Alternative: clone this repository and run `./install.sh -t /path/to/project`. It links the skills and also writes a minimal YesYak block, `@AGENTS.md` in CLAUDE.md and `.scratchpad/` in `.gitignore`. Then the agent offers step 2 by itself. `./install.sh -h` lists the options.

## User journey

1. **Install the skills** with `npx skills add delineas/yesyak` (see [Install](#install)).
2. **Set up YesYak.** Start a new session in the project and say "set up YesYak". `customize-yak` detects the check commands (tests, lint, types), the commit convention, the docs folder and the agent's instructions file. It asks only what it cannot detect, shows a preview, and after your yes it writes the YesYak block in AGENTS.md (and `@AGENTS.md` in CLAUDE.md for Claude Code) in its own commit. You do this once per project.
3. **Ask for work in your own words.**
   - A feature: "Let customers cancel an order before it ships." The agent runs `feature-delivery-pipeline`.
   - A bug: "Cancelling a shipped order returns a 500." The agent runs `bug-intake`.
4. **Answer at each checkpoint.** The agent stops after every phase with a short summary, the file it wrote, the defaults it took and one question. Each question has a recommended option.

   | Phase | What you get | Your part |
   | --- | --- | --- |
   | 0 Starter kit | A branch, a progress file, "does it fit in one iteration?" | Confirm the branch, or choose what goes first |
   | 1 Grill & sketch | Rounds of multiple-choice questions | Pick options |
   | 2 Write the contract | `docs/<slug>-spec.md` with acceptance criteria, then a step plan | Approve or change |
   | 3 Make it work | One commit per step, each with tests and a manual check | Approve the build |
   | 4 Break it | A verification against the spec, an optional red team | Choose the fixes |
   | 5 Sign your work | A pull request with a plain-language summary and diagrams | Review it |
   | 6 Retrospective | What you corrected, and a guard for each (test, hook, rule) | Approve the guards |

5. **When you are lost**, ask "what now?". `ask-yak` shows where the work is and the next step.
6. **When you stop**, say "we stop here". `handoff-and-resume` writes a dated note in `docs/handoffs/`. In the next session, say "let's continue" and the agent checks the note against the repository before it goes on.
7. **When the process does not fit your team**, ask `customize-yak` to change it ("we never test in a browser", "use my spec template"). It writes the change to `.agents/yesyak.json`; no skill is edited.

## Use cases

| You want | Say | What happens |
| --- | --- | --- |
| A new feature from a vague idea | "Customers should be able to cancel an order." | The full pipeline: questions, spec, plan, steps, verification, PR, retrospective |
| A bug fixed | "Cancelling a shipped order returns a 500." | Read-only triage first (severity, layers with file and line, root cause), a failing test, the fix, a short PR |
| More than one thing at once | "Add cancellation, refunds and an order export." | Phase 0 says "split", proposes deliveries and their order, and starts with the first |
| Work done while you are away | "I am away this afternoon, do it without me." | `unattended-run` answers each checkpoint with the recommended option and logs every decision with its reason in the PR |
| A pause and a resume | "We stop here." Next day: "Let's continue." | A handoff note with the decisions and who took them; the next session resumes at the right step |
| A teammate takes over | "Prepare this for a colleague." | The same handoff note, plus a reviewer guide for the pull request (`pr-reviewer-guide`) |
| Only one step | "Write a spec for this." "Review this branch like an attacker." "Write the PR description." | The skill for that step alone (`write-acceptance-spec`, `red-team-review`, `write-visual-pr`) |
| A mistake that must not happen again | "How do we avoid this next time?" | `session-retrospective-rules` proposes the cheapest guard that a machine can check: a test, a command or an agent hook (`agent-hook-guard`) |
| A different process for your team | "Skip work items here." "Verify with Playwright too." | `customize-yak` writes an adjustment that every agent applies; `python3 <skills folder>/ask-yak/scripts/check_yesyak.py` validates it |

A user skill with the same name as a project skill can shadow it. If the skill tool prints a base directory that is neither in the project's skills folder nor the target of a symlink there, read the project `SKILL.md` directly (`feature-delivery-pipeline` checks this). If it happens often, rename your own skill, not the YesYak one, because settings files use the YesYak names.

## Entry points

| Start from | Skill |
| --- | --- |
| "What now?", "where am I?", "which skill?" | `ask-yak` |
| Change the process, or a first install | `customize-yak` |
| A feature request | `feature-delivery-pipeline` |
| A bug report | `bug-intake` |
| A run without questions | `unattended-run`, together with one of the two above |
| A pause, or work that passes to someone else | `handoff-and-resume` (writes `docs/handoffs/`, and resumes from it) |
| One task only | the phase skill for it, for example `write-visual-pr` or `red-team-review` |

## Owner skills

Each topic has one owner skill. It keeps the full rule, even when the project's AGENTS.md repeats it, because other projects may not have that AGENTS.md. When the project's AGENTS.md says something different, the project wins. Other skills name the owner instead of copying its rules.

| Topic | Owner |
| --- | --- |
| Branches, slugs, commits | `git-commit-organizer` |
| Working files, reports, manual test helpers | `scratchpad-working-files` |
| Language and writing style | `simplified-technical-language` |
| Findings and severities | `traffic-light-findings` |
| Decision records | `decision-record-log` |
| Plain-language openings and diagrams | `plain-visual-docs` |
| The process map, skill cards and state signals | `ask-yak` (`references/process.md`); the pipeline's phase block lists the same skills |
| Slop in code, tests and docs | `no-slop-code` |

## What the skills expect from the project

| Need | Used by | Without it |
| --- | --- | --- |
| A full check: tests, plus lint and types if the project has them (for example `npm test` and `npm run lint`) | `execute-plan-loop`, `bug-intake`, `git-commit-organizer` | Say which checks you ran by hand |
| `docs/` for specs, plans and `docs/decisions/` for ADRs | `write-acceptance-spec`, `walking-skeleton-plan`, `decision-record-log` | The skills create them |
| A published contract (OpenAPI, CLI help, docs) | `bug-intake` | The skill writes an assumed contract and asks |
| Subagents | `red-team-review` (required); `feature-walkthrough`, `plain-visual-docs`, `prototype-options`, `write-acceptance-spec` (optional) | `red-team-review` tells the user and stops; the others do the work in the main session |
| A question tool | `on-the-spot` | Ask in the chat |
| `gh`, `glab` or `az` | `write-visual-pr`, `pr-reviewer-guide`, `work-items-breakdown` | Use the environment's tools, or write a markdown list |
| Hooks in the agent tool (for example Claude Code hooks or OpenCode plugins) | `agent-hook-guard` | Propose a test or a command instead |
| Chrome DevTools MCP, or Playwright and a browser | `browser-acceptance-testing` | Only on the user's request; ask before you switch tools |
| Node.js with `npx`, and a browser for Mermaid | `plain-visual-docs` | The skill says how to point the renderer to an installed browser |
| Python 3 | `feature-walkthrough` (citation check), `plain-visual-docs` (block extraction), `customize-yak` (`check_yesyak.py`) | Check citations, blocks and settings files by hand |

## Change the process

Do not copy a skill to change it. Put the change in a settings file, and every agent applies it through the YesYak block of AGENTS.md:

| File | Scope |
| --- | --- |
| `.agents/yesyak.json` | The project, in git, for the whole team |
| `~/.agents/yesyak.json` | Only you, in every project whose instructions run the check: a project with the YesYak block, or every project when your personal instructions file has the same line (`customize-yak` proposes it) |

Each entry names a skill and a mode: `add` (extra instructions), `replace` (one section that the skill card lists), or `off` (skip an optional step). At the start of a session the agent runs `check_yesyak.py` and applies only the `active:` lines it prints; if the check fails, no adjustment applies. The project wins when both files change the same skill. Settings files are instructions for the agent. Review a change to them like a change to code. `customize-yak` asks what you want, shows a diff and writes the files; run it again to audit the block. The skill cards in `ask-yak/references/process.md` list what each skill allows.

## Changing a skill

- Keep each skill usable on its own and free of facts of one repository (an ADR number, a function name, a local path).
- For every new rule in a skill, remove or merge one that is obsolete or duplicated.
- The description must not contain `<` or `>`, because the skill format rejects them.
- Commit skill changes apart from feature changes, with the scope `skills`.
- Keep `ask-yak/references/process.md` in step: `check_yesyak.py --dev` checks that every skill has a card and that the map follows the pipeline.
- Skill names and the sections that a card lists as Replaceable are a contract with the settings files of other projects. Do not rename them. If you must, say it in the release notes, because `check_yesyak.py` reports the old names as problems after an update.

## Benchmark

YesYak is tested on small real projects from GitHub. An internal skill of this repository (`.claude/skills/yak-bench/`, not installed by `npx skills`) drives an agent as a puppet through the process, in tmux, while Claude Code plays the human user: it answers the checkpoints, and it corrects the agent only where a real user would. Each run is scored, every correction becomes a finding, and confirmed findings become skill changes and a release. The full record is in [`bench/LOG.md`](bench/LOG.md) (runs, findings, metrics), [`bench/runs/`](bench/runs/) (one report per run) and [`bench/FLOWS.md`](bench/FLOWS.md) (the skills each run used).

All figures are from 2026-10-17, versions v0.1.0 to v0.4.0.

### In numbers

| | |
| --- | --- |
| Runs | 17 (0000 to 0016) |
| Agents | OpenCode (11 runs), Claude Code (6 runs) |
| Models | 6: deepseek-v4.1-flash, claude-sonnet-5-5, gpt-6-luna, gpt-5.6-sol, glm-5.3, minimax-m2.7 |
| Languages | Python, Go, TypeScript and JavaScript, PHP, Rust |
| Routes | 11 features, 4 bugs, 2 runs as a user who does not know YesYak |
| Findings | 60: skill, model, agent and benchmark defects |
| Releases | 13 tags, v0.1.0 to v0.4.0 |
| Puppet time | 178 minutes of model work, 1,685 model steps, 192 human turns |
| Puppet cost | 14.68 $ for all runs |
| Driver cost | 41.48 $ for Claude Code (Opus) as the human, in the time of the runs |

Costs are the equivalent at the prices of the [models.dev API](https://models.dev/api.json). The Claude Code runs used a subscription. The driver cost does not include the time spent writing the skills.

### By model

| Model | Agent | Runs | Turns | Model steps | Model time | Output tokens | Cache read | Cost $ | $ per run |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash | OpenCode | 6 | 62 | 600 | 57 min | 537k | 53.1M | 0.66 | 0.11 |
| claude-sonnet-5-5 | Claude Code | 6 | 55 | 269 | 26 min | 155k | 13.3M | 4.29 | 0.71 |
| gpt-6-luna | OpenCode | 2 | 45 | 517 | 39 min | 224k | 56.5M | 0.78 | 0.39 |
| glm-5.3 | OpenCode | 1 | 15 | 140 | 32 min | 158k | 17.6M | 5.63 | 5.63 |
| gpt-5.6-sol | OpenCode | 1 | 2 | 56 | 16 min | 35k | 4.5M | 3.03 | 3.03 |
| minimax-m2.7 | OpenCode | 1 | 13 | 103 | 8 min | 28k | 3.7M | 0.29 | 0.29 |
| **All** | | **17** | **192** | **1,685** | **178 min** | **1,138k** | **148.7M** | **14.68** | **0.86** |

What the models did with the same process:

- **deepseek-v4.1-flash** was the best value: complete runs for 0.05 to 0.22 $, with real findings from its red team, and the first unattended run.
- **claude-sonnet-5-5** gave the best code and retrospectives, but it skips steps that it thinks a change does not need. Without the YesYak block it skipped the whole process (runs 0009, 0014, 0015). With the block, it ran every phase (0010, 0016).
- **gpt-6-luna** needed the most corrections and loaded skills it did not need.
- **glm-5.3** ran every phase with no intervention and built the first agent hook, at the highest cost per run.
- **minimax-m2.7** needed four corrections and one nudge, in setup, in the spec and at the pull request.

### By run

| Run | Agent · model | Project · task | Result | Nudges / corrections / rescues | Model time | Cost $ |
| --- | --- | --- | --- | --- | --- | --- |
| 0000 | OpenCode · gpt-5.6-sol | local CLI · feature | pilot, stopped at the spec | unattended | 16 min | 3.03 |
| 0001 | OpenCode · gpt-6-luna | py-candlestick-chart · feature | all phases | 3 / 5 / 1 | 35 min | 0.73 |
| 0002 | OpenCode · gpt-6-luna | sjson (Go) · bug | fix route | 2 / 0 / 1 | 4 min | 0.05 |
| 0003 | OpenCode · deepseek-v4.1-flash | html-to-markdown (PHP) · feature | all phases | 0 / 3 / 0 | 18 min | 0.21 |
| 0004 | OpenCode · glm-5.3 | p-memoize (TypeScript) · feature | all phases + agent hook | 0 / 0 / 0 | 32 min | 5.63 |
| 0005 | OpenCode · deepseek-v4.1-flash | vivid (Rust) · bug | fix route | 0 / 0 / 0 | 5 min | 0.05 |
| 0006 | OpenCode · minimax-m2.7 | serialize-error (JavaScript) · feature | all phases | 1 / 4 / 0 | 8 min | 0.29 |
| 0007 | OpenCode · deepseek-v4.1-flash | filenamify (JavaScript) · feature | all phases | 0 / 1 / 0 | 13 min | 0.12 |
| 0008 | OpenCode · deepseek-v4.1-flash | retry-go (Go) · feature, user who does not know YesYak | feature built, no process | 6 forced mistakes | 4 min | 0.05 |
| 0009 | Claude Code · claude-sonnet-5-5 | filenamify · feature, as 0007 | process skipped | 0 / 0 / 0 | 3 min | 0.32 |
| 0010 | Claude Code · claude-sonnet-5-5 | filenamify · feature, as 0007 | all phases | 0 / 0 / 0 | 7 min | 1.86 |
| 0011 | OpenCode · deepseek-v4.1-flash | retry-go · three requests, session cut | split, handoff, resume, all phases | 0 / 0 / 0 | 12 min | 0.15 |
| 0012 | OpenCode · deepseek-v4.1-flash | python-tabulate · bug, unattended | fix route, no user | 0 / 0 / 0 | 5 min | 0.08 |
| 0013 | Claude Code · claude-sonnet-5-5 | humanize (Python) · bug with a design choice | fix route | 0 / 0 / 0 | 4 min | 0.63 |
| 0014 | Claude Code · claude-sonnet-5-5 | inflect (Python) · feature, user who does not know YesYak | feature built, no process | 6 forced mistakes | 2 min | 0.29 |
| 0015 | Claude Code · claude-sonnet-5-5 | gomodifytags (Go) · feature, no setup | code on main, no process | 0 / 0 / 0 | 1 min | 0.12 |
| 0016 | Claude Code · claude-sonnet-5-5 | gomodifytags · as 0015, new install | all phases | 0 / 1 / 0 | 9 min | 1.07 |

A nudge means the user told the agent something that a skill should have told it; a correction stopped a wrong action; a rescue unblocked a stuck agent.

### What the benchmark changed

- **Setup decides everything.** Without the YesYak block, no model started the process for a plain request. With it, a strong model ran every phase. That is why `install.sh` writes a minimal block and the user journey starts with "set up YesYak".
- **Checks must be real.** Setup now detects the full check (tests, lint, types), runs it once, records the failures that are already there, and names each step as it ran. A pipe in front of a check once let a failing commit through.
- **Specs stay short.** Four runs wrote specs several times longer than the code. The spec skill now keeps only what a reviewer needs.
- **Retrospectives turn corrections into guards.** They start from every user message, and prefer a test, a command or an agent hook to a written rule.
- **Some skills still have no run that used them for their job**: `browser-acceptance-testing`, `feature-walkthrough`, `production-readiness-review`, `prototype-options` and `work-items-breakdown`.
