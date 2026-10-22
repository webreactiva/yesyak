# Flows of the benchmark runs

How each run went through the YesYak process, and which skills the puppet used, in order. Regenerate the skills column with `python3 .claude/skills/yak-bench/scripts/report.py flows .scratchpad/bench`. It reads the turns of the work session (not the isolation probe). A skill counts when the puppet loads it with the skill tool, or reads its `SKILL.md` by hand (marked `*`). The number is the turn of first use.

Last update: run 0028, YesYak v0.4.5 + yak-pilot (branch).

## The runs

| Run | Puppet | Entry | Route | How far | Main thing the run showed |
| --- | --- | --- | --- | --- | --- |
| 0000 | OpenCode, gpt-5.6-sol | feature | feature | 2 Write the contract (stopped) | Pilot; isolation leaks; no turn files |
| 0001 | OpenCode, gpt-6-luna | feature | feature | 6 Retrospective | First full run; check and lint not detected, spec too long; the model loaded unrelated skills |
| 0002 | OpenCode, gpt-6-luna | bug | fix | complete | Fix route works; blocked on a missing remote |
| 0003 | OpenCode, deepseek-v4.1-flash | feature | feature | 6 Retrospective | Second model; spec still too long; an ADR for a routine fix |
| 0004 | OpenCode, glm-5.3 | feature | feature | 6 Retrospective + hook | Zero interventions; first agent hook; a pipe hid a failing check |
| 0005 | OpenCode, deepseek-v4.1-flash | bug | fix | complete | Triage found a case the issue did not name; working files written late |
| 0006 | OpenCode, minimax-m2.7 | feature | feature | 6 Retrospective | Weakest model; forced F-033 and F-034, both confirmed |
| 0007 | OpenCode, deepseek-v4.1-flash | feature | feature | 6 Retrospective | Verified v0.3.3; red team found real defects |
| 0008 | OpenCode, deepseek-v4.1-flash | feature, no setup | none | feature built, no process | A user who does not know YesYak: the process never started |
| 0009 | Claude Code, Sonnet | feature | none | feature built, process skipped | The strong model judged the change small and skipped every phase |
| 0010 | Claude Code, Sonnet | feature | feature | 6 Retrospective | Verified v0.3.5: the same request now ran every phase |
| 0011 | OpenCode, deepseek-v4.1-flash | three requests | feature, split | 6 Retrospective for delivery 1 | "Split" verdict; handoff, then resume in a new session |
| 0012 | OpenCode, deepseek-v4.1-flash | bug, unattended | fix | complete | `unattended-run` held: decisions logged, no user needed |
| 0013 | Claude Code, Sonnet | bug with a design choice | fix | complete | Optional steps answered in the chat, not through their skills |
| 0014 | Claude Code, Sonnet | feature, no setup | none | feature built, no process | The novice with a strong model: same result as 0008 |
| 0015 | Claude Code, Sonnet | feature, no setup | none | code on main, no process | The v0.3.9 trigger did not start the pipeline for a strong model |
| 0016 | Claude Code, Sonnet | feature, after the new install | feature | 6 Retrospective | The minimal block started the process; one correction after a self-chosen short route |
| 0017 | OpenCode, deepseek-v4.1-flash | feature, after `install.sh` | feature + 7 Later | 6 Retrospective + production readiness | Zero interventions; first runs of work items, walkthrough and readiness in this series; a local task list landed in the gitignored folder |
| 0018 | OpenCode, deepseek-v4.1-flash and minimax-m2.7 | feature split in 5, four sessions | feature, twice | 6 Retrospective for 2 deliveries | Handoff and resume held for deepseek; the other model resumed without skills; an unattended run stalled on a background wait |
| 0019 | Claude Code, Sonnet | feature after a handoff | feature, unattended after a cut | 3 Make it work + merge | The handoff left out phases 4-6, and the unattended session merged with a code review in their place |
| 0020 | OpenCode, deepseek-v4.1-flash | feature after a handoff | feature, unattended after a cut | 6 Retrospective | The handoff carried every phase; the unattended session ran them all and left the merge to the user |
| 0021 | OpenCode, deepseek-v4.1-flash | bug | fix | complete | Triage found a second copy of the pattern and a test that ruled out the naive fix |
| 0022 | Claude Code, Sonnet | feature, YesYak already set up | feature, run alone after "go ahead" | 6 Retrospective after a request | Sonnet built the whole delivery in one turn; the retrospective covered both sessions |
| 0023 | OpenCode, deepseek-v4.1-flash | bug, autopilot | fix, alone after the plan approval | complete | A clear bug: 0 questions, 1 gate, ran to the local PR in one turn |
| 0024 | OpenCode, deepseek-v4.1-flash | feature, autopilot | feature, alone after the spec gate | 6 Retrospective | An ambiguous API change: the plan stopped at the spec with real choices; five phase skills done by hand without loading them |
| 0025 | OpenCode, deepseek-v4.1-flash | bug, yak-pilot, observer | fix, no stop | complete | Observer ran to the end in one turn; the retrospective proposed a profile change and waited |
| 0026 | OpenCode, deepseek-v4.1-flash | feature, yak-pilot, approver | feature, plan + contract gate | 6 Retrospective | Every skill of the plan loaded; it ended its turn to wait for subagents (fixed) |
| 0027 | OpenCode, deepseek-v4.1-flash | bug, yak-pilot, approver | fix, plan + output gate | complete | Measured the performance risk before planning; gate on output the request did not name |
| 0028 | OpenCode, deepseek-v4.1-flash | bug, second session, profile change | fix, gate from the new profile entry | complete | A rule said in the chat went to the profile and stopped the next change of that kind |

## Skills used, in order

| Run | Skills (turn of first use) |
| --- | --- |
| 0000-pilot | none |
| 0001-candlestick-lines | customize-yak (4) → simplified-technical-language (5) → ask-yak (6) → feature-delivery-pipeline (7) → scratchpad-working-files (7) → git-commit-organizer (7) → no-slop-code (7) → decision-record-log (7) → traffic-light-findings (7) → plain-visual-docs (7) → on-the-spot (9) → domain-language (11) → bug-intake (12) → write-acceptance-spec (12) → production-readiness-review (12) → prototype-options (13) → execute-plan-loop (13) → red-team-review (18) → walking-skeleton-plan (20) → verify-against-spec (25) → triage-findings-list (29) → write-visual-pr (33) → pr-reviewer-guide (33) → session-retrospective-rules (34) |
| 0002-sjson-empty-key | customize-yak (2) → simplified-technical-language (2) → bug-intake (5) → scratchpad-working-files (5) → git-commit-organizer (5) → no-slop-code (5) → execute-plan-loop (6) → ask-yak (7) → write-visual-pr (8) → plain-visual-docs (8) → session-retrospective-rules (10) |
| 0003-markdown-nbsp | customize-yak (2) → simplified-technical-language (2) → feature-delivery-pipeline (6) → on-the-spot (6) → domain-language (10) → plain-visual-docs (11) → write-acceptance-spec (11) → walking-skeleton-plan (13) → git-commit-organizer (14) → execute-plan-loop (14) → decision-record-log (14) → verify-against-spec (15) → triage-findings-list (17) → traffic-light-findings (17) → write-visual-pr (18) → pr-reviewer-guide (18) → session-retrospective-rules (19) |
| 0004-pmemoize-while-pending | customize-yak (2) → git-commit-organizer (4) → feature-delivery-pipeline (5) → scratchpad-working-files (5) → simplified-technical-language (5) → no-slop-code (5) → plain-visual-docs (5) → traffic-light-findings (5) → on-the-spot (6) → domain-language (7) → write-acceptance-spec (8) → walking-skeleton-plan (9) → execute-plan-loop (10) → verify-against-spec (11) → triage-findings-list (12) → write-visual-pr (12) → pr-reviewer-guide (12) → session-retrospective-rules (13) → agent-hook-guard (14) |
| 0005-vivid-theme-panic | customize-yak (2) → bug-intake (5) → execute-plan-loop (6) → decision-record-log (6) → write-visual-pr (6) → session-retrospective-rules (6) |
| 0006-serialize-nonobject | customize-yak (2) → feature-delivery-pipeline (6) → simplified-technical-language (6) → scratchpad-working-files (6) → git-commit-organizer (6) → no-slop-code (6) → decision-record-log (6) → traffic-light-findings (6) → plain-visual-docs (6) → on-the-spot (7) → write-acceptance-spec (8) → walking-skeleton-plan (9) → execute-plan-loop (10) → verify-against-spec (10) → write-visual-pr (11) → session-retrospective-rules (12) |
| 0007-filenamify-entry | customize-yak (2) → simplified-technical-language (2) → scratchpad-working-files* (2) → git-commit-organizer* (2) → feature-delivery-pipeline (5) → on-the-spot (6) → write-acceptance-spec (8) → domain-language (8) → plain-visual-docs (8) → no-slop-code (8) → traffic-light-findings (8) → walking-skeleton-plan (9) → execute-plan-loop (10) → verify-against-spec (11) → red-team-review (11) → triage-findings-list (12) → write-visual-pr (13) → pr-reviewer-guide (13) → session-retrospective-rules (14) |
| 0008-retry-novice | on-the-spot* (2) → customize-yak* (3) → git-commit-organizer* (3) |
| 0009-filenamify-claude | customize-yak (2) → write-visual-pr (6) → session-retrospective-rules (6) |
| 0010-filenamify-claude-v035 | customize-yak (2) → feature-delivery-pipeline (4) → git-commit-organizer (4) → scratchpad-working-files (4) → on-the-spot (5) → write-acceptance-spec (7) → walking-skeleton-plan (8) → execute-plan-loop (9) → verify-against-spec (10) → red-team-review (10) → write-visual-pr (11) → session-retrospective-rules (11) |
| 0011-retry-split-handoff | customize-yak (2) → scratchpad-working-files* (2) → decision-record-log* (3) → feature-delivery-pipeline (5) → git-commit-organizer (6) → simplified-technical-language (6) → on-the-spot (7) → domain-language (8) → plain-visual-docs (8) → write-acceptance-spec (8) → walking-skeleton-plan (8) → handoff-and-resume (9) → ask-yak (10) → execute-plan-loop (10) → no-slop-code (10) → verify-against-spec (11) → write-visual-pr (11) → session-retrospective-rules (11) |
| 0012-tabulate-unattended | customize-yak (2) → on-the-spot (2) → git-commit-organizer* (3) → bug-intake (5) → unattended-run (5) → scratchpad-working-files (5) → traffic-light-findings (5) → decision-record-log (5) → simplified-technical-language (5) → write-visual-pr (5) → plain-visual-docs (5) → session-retrospective-rules (5) |
| 0013-humanize-sign-claude | customize-yak (2) → bug-intake (4) → session-retrospective-rules (7) |
| 0014-inflect-novice-claude | customize-yak (4) |
| 0015-gomodifytags-lowercase-claude | none |
| 0016-gomodifytags-install-claude | customize-yak (3) → feature-delivery-pipeline (7) → scratchpad-working-files (7) → git-commit-organizer (7) → simplified-technical-language (7) → on-the-spot (8) → domain-language (9) → write-acceptance-spec (10) → walking-skeleton-plan (11) → execute-plan-loop (12) → verify-against-spec (13) → write-visual-pr (13) → session-retrospective-rules (13) |
| 0017-mcu-health-readiness | customize-yak (2) → feature-delivery-pipeline (5) → git-commit-organizer (5) → simplified-technical-language (5) → scratchpad-working-files (5) → on-the-spot (6) → write-acceptance-spec (9) → plain-visual-docs (9) → domain-language (9) → walking-skeleton-plan (10) → work-items-breakdown (10) → execute-plan-loop (11) → decision-record-log (11) → verify-against-spec (12) → red-team-review (13) → traffic-light-findings (13) → triage-findings-list (14) → write-visual-pr (16) → feature-walkthrough (17) → production-readiness-review (18) → session-retrospective-rules (19) → handoff-and-resume (19) |
| 0018-packbeat-ux-sessions | customize-yak (2) → feature-delivery-pipeline (4) → on-the-spot (5) → domain-language (9) → write-acceptance-spec (10) → handoff-and-resume (11) → walking-skeleton-plan (13) → git-commit-organizer* (13) → verify-against-spec (19) → simplified-technical-language (23) → scratchpad-working-files (23) → traffic-light-findings (23) → red-team-review (23) → triage-findings-list (26) → write-visual-pr (27) → pr-reviewer-guide (27) → session-retrospective-rules (27) → unattended-run (29) → decision-record-log (29) → execute-plan-loop (29) |
| 0019-packbeat-reactions-claude | customize-yak (2) → feature-delivery-pipeline (4) → simplified-technical-language (4) → scratchpad-working-files (4) → git-commit-organizer (4) → on-the-spot (5) → domain-language (8) → write-acceptance-spec (8) → walking-skeleton-plan (9) → handoff-and-resume (10) → unattended-run (11) → execute-plan-loop* (11) |
| 0020-packbeat-wordcloud | customize-yak (2) → feature-delivery-pipeline (4) → scratchpad-working-files* (4) → on-the-spot (5) → domain-language (10) → write-acceptance-spec (10) → plain-visual-docs (11) → walking-skeleton-plan (12) → handoff-and-resume (13) → execute-plan-loop (14) → unattended-run (14) → git-commit-organizer (14) → decision-record-log (14) → no-slop-code (14) → simplified-technical-language (14) → verify-against-spec (14) → red-team-review (14) → pr-reviewer-guide (14) → write-visual-pr (14) → session-retrospective-rules (14) |
| 0021-linkify-parens | customize-yak* (2) → on-the-spot* (2) → bug-intake (5) → git-commit-organizer (6) → execute-plan-loop (6) → write-visual-pr (6) → session-retrospective-rules (6) |
| 0022-packbeat-ranking-claude | feature-delivery-pipeline (2) → unattended-run (3) → session-retrospective-rules (5) |
| 0023-humanize-bytes-autopilot | customize-yak (2) → autopilot-plan (5) → bug-intake (5) → unattended-run (5) → execute-plan-loop (6) → git-commit-organizer (6) → write-visual-pr (6) → session-retrospective-rules (6) |
| 0024-tabulate-colsep-autopilot | customize-yak (2) → decision-record-log* (3) → ask-yak* (3) → autopilot-plan (4) → feature-delivery-pipeline (4) → git-commit-organizer (4) → unattended-run (4) → domain-language (5) → on-the-spot (5) → execute-plan-loop (6) → write-visual-pr (6) → plain-visual-docs (6) → pr-reviewer-guide (6) → session-retrospective-rules (6) |
| 0025-tabulate-rowalign-pilot | customize-yak (2) → ask-yak* (2) → yak-pilot* (2) → unattended-run (5) → bug-intake (5) → execute-plan-loop (5) → git-commit-organizer (5) → scratchpad-working-files (5) → write-visual-pr (5) → simplified-technical-language (5) → no-slop-code (5) → plain-visual-docs (5) → session-retrospective-rules (5) |
| 0026-tabulate-floatfmt-pilot | customize-yak (2) → no-slop-code* (4) → yak-pilot (5) → write-acceptance-spec (6) → red-team-review (6) → execute-plan-loop (6) → decision-record-log (6) → git-commit-organizer (6) → verify-against-spec (6) → triage-findings-list (8) → traffic-light-findings (8) → write-visual-pr (8) → pr-reviewer-guide (8) → session-retrospective-rules (8) |
| 0027-humanize-locale-pilot | customize-yak (2) → decision-record-log* (3) → git-commit-organizer (4) → ask-yak* (4) → yak-pilot (5) → bug-intake (5) → execute-plan-loop (6) → unattended-run (6) → write-visual-pr (6) → pr-reviewer-guide (6) → session-retrospective-rules (6) |
| 0028-tabulate-stralign-pilot2 | yak-pilot (2) → customize-yak (2) → bug-intake (2) → git-commit-organizer (3) → execute-plan-loop (3) → decision-record-log (3) → write-visual-pr (3) → session-retrospective-rules (3) |

## The usual order

A complete feature run (0003, 0004, 0007, 0010, 0011) loads the skills in the order of the process map:

```text
customize-yak → feature-delivery-pipeline → on-the-spot → (domain-language) → write-acceptance-spec
  → walking-skeleton-plan → execute-plan-loop → verify-against-spec → (red-team-review → triage-findings-list)
  → write-visual-pr → (pr-reviewer-guide) → session-retrospective-rules
```

A complete fix run (0002, 0005, 0012, 0013):

```text
customize-yak → bug-intake → (unattended-run) → execute-plan-loop → write-visual-pr → session-retrospective-rules
```

The convention skills (`simplified-technical-language`, `scratchpad-working-files`, `git-commit-organizer`, `no-slop-code`, `plain-visual-docs`, `traffic-light-findings`, `decision-record-log`) load where an owner rule is needed, often all at once when the pipeline starts.

## What the flows show

- **Setup is the only step every run took.** `customize-yak` ran in 15 of 16 runs, also in 0014, where the user asked to switch a skill off.
- **Without the YesYak block, nothing starts the process (0008, 0014).** Both models, weak and strong, wrote the feature directly. v0.3.9 made the pipeline trigger on any feature request; run 0015 showed that a strong model still skips it for a small change. The block is the switch: since v0.4.0 `install.sh` writes a minimal one, and run 0016 started the process with the same request.
- **A strong model loads fewer skills.** For the same task, deepseek loaded 19 skills (0007) and Sonnet 12 (0010). Sonnet left out most convention skills and `triage-findings-list`, and in 0013 wrote the PR text without `write-visual-pr`. Its results were good, but the files that `ask-yak` reads to find the position (for example `pr-body.md`) can then be missing.
- **`ask-yak` is rarely loaded (3 of 14 runs).** Agents go from skill to skill through the "Next" of each card. `ask-yak` came in only for "what now?" or a resume (0011). In 0009 "what now?" got an answer without it.
- **Optional steps run when the user or the size asks.** `red-team-review` ran in 3 runs, each time with real findings. `pr-reviewer-guide` ran in 4. `agent-hook-guard` ran once (0004), when the retrospective chose a hook.
- **Weak models load skills they do not need** (0001: `bug-intake`, `production-readiness-review` and `prototype-options` in a feature run), and sometimes read a `SKILL.md` by hand instead of loading it (0007, 0008, 0011).
- **On autopilot, the plan is followed but its skills are not always loaded (0024).** The run reached every phase and its red team found real defects, yet the spec, plan, verification, red team and triage were done without their skills. A plan of skills must name each skill and check that it ran (issue #1).
- **A plan of skills is loaded when it names them (0026).** With each skill in the plan table, every planned skill loaded. The user named no skill in 0025-0028; `yak-pilot` loaded on a plain request in all four.

## Coverage

| Skill | Runs that used it |
| --- | --- |
| `agent-hook-guard` | 1: 0004 |
| `ask-yak` | 3: 0001, 0002, 0011 |
| `autopilot-plan` | 2: 0023, 0024 (renamed `yak-pilot`) |
| `yak-pilot` | 4: 0025, 0026, 0027, 0028 |
| `browser-acceptance-testing` | 0: none (off in every run on purpose) |
| `bug-intake` | 5: 0001, 0002, 0005, 0012, 0013 |
| `customize-yak` | 14: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011, 0012, 0013, 0014 |
| `decision-record-log` | 6: 0001, 0003, 0005, 0006, 0011, 0012 |
| `domain-language` | 5: 0001, 0003, 0004, 0007, 0011 |
| `execute-plan-loop` | 9: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0010, 0011 |
| `feature-delivery-pipeline` | 7: 0001, 0003, 0004, 0006, 0007, 0010, 0011 |
| `feature-walkthrough` | 0: none (0013: asked for, answered in the chat) |
| `git-commit-organizer` | 10: 0001, 0002, 0003, 0004, 0006, 0007, 0008, 0010, 0011, 0012 |
| `handoff-and-resume` | 1: 0011 |
| `no-slop-code` | 6: 0001, 0002, 0004, 0006, 0007, 0011 |
| `on-the-spot` | 9: 0001, 0003, 0004, 0006, 0007, 0008, 0010, 0011, 0012 |
| `plain-visual-docs` | 8: 0001, 0002, 0003, 0004, 0006, 0007, 0011, 0012 |
| `pr-reviewer-guide` | 4: 0001, 0003, 0004, 0007 |
| `production-readiness-review` | 1: 0001 (0001 only as noise: the model loaded it in a feature run; never used for its job) |
| `prototype-options` | 1: 0001 (0001 only as noise; 0013 compared designs with a script instead) |
| `red-team-review` | 3: 0001, 0007, 0010 |
| `scratchpad-working-files` | 8: 0001, 0002, 0004, 0006, 0007, 0010, 0011, 0012 |
| `session-retrospective-rules` | 12: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0009, 0010, 0011, 0012, 0013 |
| `simplified-technical-language` | 8: 0001, 0002, 0003, 0004, 0006, 0007, 0011, 0012 |
| `traffic-light-findings` | 6: 0001, 0003, 0004, 0006, 0007, 0012 |
| `triage-findings-list` | 4: 0001, 0003, 0004, 0007 |
| `unattended-run` | 1: 0012 |
| `verify-against-spec` | 7: 0001, 0003, 0004, 0006, 0007, 0010, 0011 |
| `walking-skeleton-plan` | 7: 0001, 0003, 0004, 0006, 0007, 0010, 0011 |
| `work-items-breakdown` | 0: none |
| `write-acceptance-spec` | 7: 0001, 0003, 0004, 0006, 0007, 0010, 0011 |
| `write-visual-pr` | 11: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0009, 0010, 0011, 0012 |

Never used for their job yet: `browser-acceptance-testing`, `feature-walkthrough`, `production-readiness-review`, `prototype-options`, `work-items-breakdown`. Each needs a run made for it: a project with a user interface, a deployable service, a change with visual options, or a user who tracks work in a tool.
