# Run 0017-mcu-health-readiness

- Source: https://github.com/DiljotSG/MCU-Countdown @ ec5c13040
- YesYak: v0.4.0-5-gef1271a · model: ollama-cloud/deepseek-v4.1-flash · turns: 20
- Sessions: `ses_eb507463dffe5NORskkkHSZHNn` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb50723a6ffetf83ihd3WNF4Un` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 407901, output 225576, cache_read 39820556, cache_write 0 · ≈ 0.3160 $ (models.dev prices)
- Time: 46 min wall, 33 min of agent work · model steps: 226
- Tool calls: 293 · errors: 3
- Branch: feat/json-lists-and-health
- Skills loaded, in order: customize-yak → feature-delivery-pipeline → git-commit-organizer → simplified-technical-language → scratchpad-working-files → on-the-spot → write-acceptance-spec → plain-visual-docs → domain-language → walking-skeleton-plan → work-items-breakdown → execute-plan-loop → decision-record-log → verify-against-spec → red-team-review → traffic-light-findings → triage-findings-list → write-visual-pr → feature-walkthrough → production-readiness-review → session-retrospective-rules → handoff-and-resume
- Puppet: OpenCode with deepseek-v4.1-flash. Project installed with `install.sh -a` on top of the frozen copy, as a user would
- Task: JSON for the named list pages and a health endpoint for the container (the project deploys a Docker image)
- Result: every phase reached, plus the three skills no run had used in this series: `work-items-breakdown`, `feature-walkthrough`, `production-readiness-review`. 17 commits on `feat/json-lists-and-health`; 40 → 60 tests, flake8 0 (I ran both); spec 258 lines, plan, 3 ADRs, verification (22/22 criteria, the 3 container ones run against a real container), red team (4 missions, 1 🔴 kept for a `fix/` branch), change list of 19, PR body 111 lines, walkthrough with 70 checked citations, production readiness report, retrospective with two `add` adjustments and one AGENTS.md line, handoff note
- Interventions: 0 nudges, 0 corrections, 0 rescues. At turn 11 I started Docker Desktop (the puppet could not) so the container criteria could run

## Phases

| Phase | Reached | Artifacts | As the skill asks |
| --- | --- | --- | --- |
| Setup | yes | `.agents/yesyak.json`, YesYak block, setup commit | yes: detection, one round of questions, diff before writing, commands as they ran |
| 0 Starter kit | yes | branch, `progress.md`, chat rule in AGENTS.md | yes |
| 1 Interview | yes | `interview-decisions.md`, `domain-language.md` | yes; domain-language was run late, at the spec step, and the agent said so |
| 2 Contract | yes | spec, plan, `work-items.md` | spec too long (F-001 again); the task list went to `.scratchpad/` only (F-061) |
| 3 Make it work | yes | 6 commits, one per step plus a refactor, ADRs | yes |
| 4 Break it | yes | verification report, red-team report | yes; browser step off as set |
| 5 Sign your work | yes | change list, 4 changes applied, PR body, walkthrough | yes; the reviewer guide skipped at my request |
| 6 Retrospective | yes | retrospective, handoff | yes, without being named: "let's close this piece of work" was enough |
| 7 Later | yes | production readiness report | report before the target questions (F-062) |

## Interventions

| Turn | Kind | Words |
| --- | --- | --- |
| 1 | answer | "I just installed YesYak in this project, set it up. Switch off browser-acceptance-testing, I don't want browser evidence." |
| 2 | approve | "recommended" |
| 3 | approve | "yes" |
| 4 | answer | feature request (named lists as JSON + health endpoint) + "the PR stays local" |
| 5 | approve | "recommended" |
| 6 | answer | "recommended" (interview round 1) |
| 7 | answer | "recommended" (interview round 2) |
| 8 | approve | "recommended" (phase 1 checkpoint) |
| 9 | approve + answer | "1 and 1. For the work items: yes, I keep a plain task list for this project, produce it." (forces work-items-breakdown) |
| 10 | approve | "recommended" (plan, run all steps, check Docker) |
| 11 | answer | "1. About Docker: I started it now, it should be running. Run the two container checks inside the verification." |
| 12 | answer | "1, 1, 2" (add AC-07 test, run red-team, remove the local tag) |
| 13 | approve | "recommended" (triage; RT1 to a separate fix branch; remove image) |
| 14 | answer | "2, and 1 for the fix branch." |
| 15 | approve | "recommended" (write the PR body) |
| 16 | answer | "Skip the guide. Walk me through the branch instead, I want to understand how the code works before I merge it." (forces feature-walkthrough) |
| 17 | answer | "The fix branch can wait for another day. First tell me: is this ready for production? We deploy the Docker image." (forces production-readiness-review) |
| 18 | answer | deployment facts + "add the deploy items to the change list; ... Then let's close this piece of work." |
| 19 | approve | "recommended" (apply the retrospective guards) |

## Forced triggers

| Skill | Result |
| --- | --- |
| work-items-breakdown | Used after "I keep a plain task list for this project". The table followed the skill, but the list went only to `.scratchpad/`, which git ignores (F-061) |
| feature-walkthrough | Used after "walk me through the branch". Subagent writer, `check_walkthrough.py` exit 0 with 70 citations; the agent caught three wrong numbers by hand (F-063) |
| production-readiness-review | Used after "is this ready for production?". Honest verdict (no, with the 🔴 from the red team), deploy gaps found in the repo; the target questions came after the report (F-062) |

## Findings

- F-001 (again, deepseek): spec 258 lines for about 200 lines of code; it reported both counts and cut 36 lines, but kept the sections the rule says to remove.
- F-061 (Skill, fixed in v0.4.1): the user keeps a task list for the project; `work-items-breakdown` wrote it only to `.scratchpad/<slug>/work-items.md`, which git ignores. The step "save the mapping to `.scratchpad/`" read as applying to a local list too. The same loss shows in another project's own process, whose working folder lost the plans of its early phases. Now a task list in the repo goes to the project's task file (or `docs/<slug>-tasks.md`) and is committed with the plan; the scratchpad mapping is for an external tracker only.
- F-062 (Model, watch): `production-readiness-review` wrote the verdict and asked the target questions after it, without options. The skill says to ask first, in one round.
- F-063 (Skill, watch): the walkthrough subagent wrote three wrong counts (criteria, risks); `check_walkthrough.py` checks citations and diagrams, not numbers. Proposed by the puppet's own retrospective.
- Series count: resets to 0 (F-061). Every skill has now been used in at least one run.

## Cost

≈ 0.32 $ at models.dev prices for the puppet; ≈ 2.94 $ for the driver in the run window.
