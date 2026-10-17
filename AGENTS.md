# AGENTS.md

Guidance for coding agents that work in this repository.

## Premise: generic for any developer

YesYak must work for any developer, in any project, with any stack and any agent. Every change keeps it that way:

- A rule states the principle, not one case of it. It must stay true and clear when you remove its example.
- Do not tie a skill to concrete examples. Add an example only when the rule is hard to read without it, mark it "for example", and give more than one option when it names a tool, language, framework or host.
- Never take an example from a real project: no domain, entity, file, command, incident or decision of the project where a lesson was learned. Write the general lesson instead.
- Do not assume what a project has: a web server, a database, sign-in, a UI, a CLI, a git host, a harness. When a rule needs one of them, say "if the project has …".

## What this repository is

YesYak is a set of agent skills (open SKILL.md format), not an application. There is no build and no test suite. Each skill is `skills/<name>/SKILL.md`, with optional `references/` and `scripts/`. Other projects use the skills through `install.sh`, which symlinks every skill folder into the project's `.claude/skills/` or `.agents/skills/`. An edit here reaches every linked project at once.

## Commands

```bash
python3 skills/ask-yak/scripts/check_yesyak.py --dev   # run after every skill change; must exit 0
./install.sh -h                                          # install, list or remove the skills in another project
python3 skills/feature-walkthrough/scripts/check_walkthrough.py <walkthrough.md> <commit>
```

`check_yesyak.py` finds the skills folder from its own resolved path, so it also works through the symlinks.

## How the pieces fit

- **Process map.** `skills/ask-yak/references/process.md` holds the process map, the state signals and one card per skill. The `text` block of phases in `skills/feature-delivery-pipeline/SKILL.md` lists the same skills per phase. `--dev` fails when the two differ, when a skill has no card, or when a file that a card lists under "Makes" is not named in the skill.
- **Adjustments.** Projects do not edit skills. They write `add`, `replace` or `off` entries to `.agents/yesyak.json` (or `~/.agents/yesyak.json`). `customize-yak` writes these files and the YesYak block of AGENTS.md. `check_yesyak.py` validates them against the cards and prints the `active:` lines that agents apply.
- **Contract with other projects.** Skill names and the headings that a card lists as "Replaceable" are names that settings files in other repositories use. A `replace` entry must match a `##`/`###` heading outside code fences. Do not rename them. If you must, say it in the release notes.
- **Owner skills.** Each topic has one owner skill that keeps the full rule (table in README.md): branches and commits in `git-commit-organizer`, working files in `scratchpad-working-files`, language in `simplified-technical-language`, findings in `traffic-light-findings`, ADRs in `decision-record-log`, openings and diagrams in `plain-visual-docs`, slop in `no-slop-code`. Other skills name the owner and do not copy its rule. Each owner says that AGENTS.md wins when it sets a different convention.

## Benchmark and releases

- `.claude/skills/yak-bench/` is a skill of this repository only (not in `skills/`, so `install.sh` never copies it). It drives OpenCode as a puppet through the YesYak process on a small real project, with you as the human, and turns confirmed findings into skill changes.
- `bench/LOG.md` keeps every run and every finding; `bench/runs/` has one file per run. Run folders stay in `.scratchpad/bench/`.
- Releases: an entry in `CHANGELOG.md` and a tag `vX.Y.Z`. Push tags only when the user asks.

## Rules for changing a skill

- Keep each skill usable on its own (see the premise above). The existing examples share one neutral domain, orders; a new example that needs a domain uses it too.
- Do not write `.claude/skills/` as the only location; say "the skills folder".
- For every new rule, remove or merge one that is obsolete or duplicated.
- The `description` in the frontmatter must not contain `<` or `>`, and must not contain `: ` (it breaks the YAML).
- Before you commit skill text, review it with the `unslop` skill if it is installed (user level). Review scripts with `deslop`.
- Skills are written in English, ASD-STE100 Simplified Technical English. The document language rule of the skills lives only in `simplified-technical-language`: documents in English unless the project names another language; the conversation in the user's language.
- Commits: Conventional Commits with gitmoji, in English, scope `skills` for skill changes, kept apart from other changes.
