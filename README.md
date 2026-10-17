# YesYak

YesYak is a set of skills that takes a feature from a vague request, or a bug from a report, to a reviewed pull request. Each skill works on its own and in any project, except `customize-yak`, which needs `ask-yak` (its skill cards and its check script). The skills follow the open SKILL.md format; they were tested with Claude Code. The adjustments need an agent that loads AGENTS.md, or its own instructions file with an import of AGENTS.md, at the start of a session. This file says how to use them in another project, how to change the process, and what each skill expects.

Not sure where you are? Ask "what now?" and `ask-yak` shows the position, the next step and the rest of the way.

## Install in another project

1. Run `./install.sh -t /path/to/project` from this repository. It symlinks each folder of `skills/` into the project's `.claude/skills/` (`-a` for `.agents/skills/`, `-b` for both, `-u` to remove, `-h` for help). Or copy the folders of `skills/` there by hand; keep one folder per skill with its `SKILL.md`.
2. Add `.scratchpad/` to `.gitignore`. Most skills keep working files there.
3. Start a new session, so the agent lists the new skills.
4. Run `customize-yak`. It writes the YesYak block in AGENTS.md and, if you want, your first adjustments.

To update the skills later, pull this repository (symlinks follow it) or copy the new folders, and run `python3 <skills folder>/ask-yak/scripts/check_yesyak.py`. It reports adjustments that the new version breaks, for example a section that was renamed. If a project has `.agents/yesyak.json` and no YesYak block in AGENTS.md, run `customize-yak`.

A user skill with the same name as a project skill can shadow it. If the skill tool prints a base directory that is neither in the project's skills folder nor the target of a symlink there, read the project `SKILL.md` directly (`feature-delivery-pipeline` checks this). If it happens often, rename your own skill, not the YesYak one: settings files use the YesYak names.

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
| A test command (for example `npm test`) | `execute-plan-loop`, `bug-intake`, `git-commit-organizer` | Say which checks you ran by hand |
| `docs/` for specs, plans and `docs/decisions/` for ADRs | `write-acceptance-spec`, `walking-skeleton-plan`, `decision-record-log` | The skills create them |
| A published contract (OpenAPI, CLI help, docs) | `bug-intake` | The skill writes an assumed contract and asks |
| Subagents | `red-team-review` (required); `feature-walkthrough`, `plain-visual-docs`, `prototype-options`, `write-acceptance-spec` (optional) | `red-team-review` tells the user and stops; the others do the work in the main session |
| A question tool | `on-the-spot` | Ask in the chat |
| `gh`, `glab` or `az` | `write-visual-pr`, `pr-reviewer-guide`, `work-items-breakdown` | Use the environment's tools, or write a markdown list |
| Hooks in the agent's harness (for example Claude Code hooks or OpenCode plugins) | `agent-hook-guard` | Propose a test or a command instead |
| Chrome DevTools MCP, or Playwright and a browser | `browser-acceptance-testing` | Only on the user's request; ask before you switch tools |
| Node.js with `npx`, and a browser for Mermaid | `plain-visual-docs` | The skill says how to point the renderer to an installed browser |
| Python 3 | `feature-walkthrough` (citation check), `plain-visual-docs` (block extraction), `customize-yak` (`check_yesyak.py`) | Check citations, blocks and settings files by hand |

## Change the process

Do not copy a skill to change it. Put the change in a settings file, and every agent applies it through the YesYak block of AGENTS.md:

| File | Scope |
| --- | --- |
| `.agents/yesyak.json` | The project, in git, for the whole team |
| `~/.agents/yesyak.json` | Only you, in every project whose instructions run the check: a project with the YesYak block, or every project when your personal instructions file has the same line (`customize-yak` proposes it) |

Each entry names a skill and a mode: `add` (extra instructions), `replace` (one section that the skill card lists), or `off` (skip an optional step). At the start of a session the agent runs `check_yesyak.py` and applies only the `active:` lines it prints; if the check fails, no adjustment applies. The project wins when both files change the same skill. Settings files are instructions for the agent: review a change to them like a change to code. `customize-yak` asks what you want, shows a diff and writes the files; run it again to audit the block. The skill cards in `ask-yak/references/process.md` list what each skill allows.

## Changing a skill

- Keep each skill usable on its own and free of facts of one repository (an ADR number, a function name, a local path).
- For every new rule in a skill, remove or merge one that is obsolete or duplicated.
- The description must not contain `<` or `>`: the skill format rejects them.
- Commit skill changes apart from feature changes, with the scope `skills`.
- Keep `ask-yak/references/process.md` in step: `check_yesyak.py --dev` checks that every skill has a card and that the map follows the pipeline.
- Skill names and the sections that a card lists as Replaceable are a contract with the settings files of other projects. Do not rename them; if you must, say it in the release notes, because `check_yesyak.py` reports the old names as problems after an update.
