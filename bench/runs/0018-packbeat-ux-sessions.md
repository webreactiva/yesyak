# Run 0018-packbeat-ux-sessions

- Source: /Users/daniel/Sites/lab/packbeat @ a51e7fde8
- YesYak: v0.4.1 (bench fixes in the working tree) · model: ollama-cloud/deepseek-v4.1-flash · turns: 30
- Sessions: `ses_eb4d524bfffe6J6QGTBpf1eFPO` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb4d43a20ffe3q3lzEhRA3PbZm` (ollama-cloud/deepseek-v4.1-flash, from turn 2), `ses_eb4c5a9b9ffetW63IeGV4ErZVX` (ollama-cloud/deepseek-v4.1-flash, from turn 12), `ses_eb4b735edffeSQszijYZ7KvGFg` (ollama-cloud/minimax-m2.7, from turn 14), `ses_eb46fbf7dffeBvOxvKUSoqLINW` (ollama-cloud/deepseek-v4.1-flash, from turn 29)
- Tokens: input 1349426, output 565622, cache_read 120534888, cache_write 0 · ≈ 2.5839 $ (models.dev prices)
- Time: 164 min wall, 131 min of agent work · model steps: 764
- Tool calls: 750 · errors: 11
- Branch: main
- Skills loaded, in order: customize-yak → feature-delivery-pipeline → on-the-spot → domain-language → write-acceptance-spec → handoff-and-resume → handoff-and-resume → walking-skeleton-plan → verify-against-spec → feature-delivery-pipeline → simplified-technical-language → scratchpad-working-files → git-commit-organizer → traffic-light-findings → red-team-review → triage-findings-list → write-visual-pr → pr-reviewer-guide → session-retrospective-rules → unattended-run → feature-delivery-pipeline → decision-record-log → scratchpad-working-files → git-commit-organizer → simplified-technical-language → write-acceptance-spec → on-the-spot → walking-skeleton-plan → execute-plan-loop → verify-against-spec → red-team-review
- Puppet: OpenCode; deepseek-v4.1-flash for sessions 1, 2 and 4; minimax-m2.7 opened session 3 (turn 14 and turns 23-28; turns 15-22 ran on deepseek through a bench defect, F-064)
- Project: packbeat, the user's own app (live sessions, WebSocket, React), with its own process `delivery-loop` set aside in the clone by one bench commit; YesYak installed with `install.sh -a`
- Task: the owner request in `docs/requirements.md` (product view of the UX). Phase 0 split it into 5 deliveries; the run built delivery 1 (P15 session title and pixel-art avatars) and delivery 2 (P16 who joined, on the presenter lobby)
- Result: both deliveries merged into `main` with their tags, as the project's branch rule says; `pnpm test` 146 → 165 (I ran it), e2e 167 → 186 per the puppet. P15: 13 commits, 4 decisions; P16: 11 commits, 3 decisions, done unattended
- Interventions: 0 nudges, 2 corrections, 1 rescue

## Session cuts

| Cut | How | Resume |
| --- | --- | --- |
| 1 · after the spec checkpoint | "I have to stop for today" | The agent wrote and committed a handoff without being asked, with the interview decisions copied out of `.scratchpad/`. New session (deepseek): read the newest handoff, checked it against the repo, found that the spec still said Draft, then went on with the plan |
| 2 · in the middle of the build loop | I killed the session and its server with step 1 committed and step 2 not committed | New session, other model (minimax): no skill, no handoff check; it called the uncommitted step 2 and the docs "complete", and called a new e2e failure "pre-existing". After a correction it bisected against `main` in worktrees and fixed the cause |
| 3 · between delivery 1 and 2 | New session (deepseek), "take the best decisions yourself and run it to the end without me" | `unattended-run` with an authorization and a decision log; it stopped once while the e2e ran in the background (F-065); after one rescue it finished P16 alone, red team included |

## Phases

| Phase | P15 (sessions 1-3) | P16 (session 4, unattended) |
| --- | --- | --- |
| Setup | `customize-yak`, block kept short because AGENTS.md already holds the conventions | — |
| 0 Starter kit | verdict split, 5 deliveries; branch `phase/<id>` from the project's rule | yes, in the decision log |
| 1 Interview | 4 rounds, 19 decisions, domain terms | defaults logged |
| 2 Contract | spec 283 lines, 18 criteria; plan of 3 steps | spec, plan |
| 3 Make it work | step 1 in session 2; step 2 finished in session 3 with a regression fix | 3 steps |
| 4 Break it | verification yes; red team only after my correction | verification and red team: 2 blocking defects found and fixed, a third from a second premortem |
| 5 Sign your work | change list, PR body, reviewer guide | change list, PR body, reviewer guide |
| 6 Retrospective | yes, but only session 3 from the demo (F-053) | yes |

## Interventions

| Session | Turn | Kind | Words |
| --- | --- | --- | --- |
| 1 | 1 | answer | setup request + browser-acceptance-testing off |
| 1 | 2 | answer | "Yes, but one correction: the load test passes for me. It failed because I was running the browser tests at the same time..." (bench-caused) |
| 1 | 3 | answer | the owner request from requirements.md, "several parts over a few days" + "the PR stays local" |
| 1 | 4 | approve | "Yes to the three." (split, P15 first, branch, AGENTS.md rule) |
| 1 | 5 | answer | "a, a, a, a" (interview round 1) |
| 1 | 6 | answer | "a, a, a, a" (rounds 2-3) |
| 1 | 7 | answer | "a, a, a, a" (round 4) |
| 1 | 8 | approve | "Confirmed. Terms and spec." |
| 1 | 9 | approve | "Agreed, write the spec." |
| 1 | 10 | approve | "Spec approved, defaults 1 to 8 confirmed. I have to stop for today, we go on tomorrow." (cut 1) |
| 2 | 1 | answer | "Hi, I continue with yesterday's work." (new session, same model) |
| 2 | 2 | approve | "Yes, set it to approved and start the plan." |
| 2 | 3 | approve | "Yes to both details. No work items this time. Start the build and go on through the steps." |
| 3 | 1 | answer | "Hi, I continue with the work from before." (new session, minimax-m2.7, after a hard cut mid-step) |
| 3 | 2 | correction | "Wait. The session-close test passed on main before we started this work; only the home code-field test failed then. Check that again before you commit anything." |
| 3 | 3 | approve | "Yes, apply the first option." |
| 3 | 4 | approve | "Yes, the three commits." |
| 3 | 5 | approve | "Continue." |
| 3 | 6 | approve | "Yes, add the gap tests and align the spec. Then tell me how to run the demo, I will do it myself." |
| 3 | 7 | answer | demo result: "Demo done, it works..." (I ran it with a Playwright script, outside the report) |
| 3 | 8 | correction | "Hold on before the next delivery. Did we skip steps? I expected an adversarial review of the code, the PR description and a retrospective before the merge." |
| 3 | 9 | approve | "Yes. Move main back, keep every commit on the branch, and run the missing steps." (minimax from here) |
| 3 | 10 | answer | "Are the reviews done?" |
| 3 | 11 | answer | "The verifier looks finished. Show me the red team result." |
| 3 | 12 | answer | "RT-S1 is an accepted risk: only the host can send it. Go on with the rest." |
| 3 | 13 | answer | "Apply 1 to 4 now, they are cheap. Accept 5 and 6." |
| 3 | 14 | answer | "Only the AGENTS.md line. Then finish this delivery as the project does." |
| 4 | 1 | answer | "Hi. I continue with the UX work: the next delivery. I will be away for some hours, so take the best decisions yourself and run it to the end without me. Leave me a summary." (new session, deepseek, unattended) |
| 4 | 2 | rescue | "I looked in: you stopped while the browser tests were running, and they did not finish. I am still away, go on to the end." |

The turn s1-02 correction ("the load test passes for me") came from the bench: my own e2e baseline ran at the same time. It is not counted.

## Compared with the project's own process

The project built P0-P14 with `delivery-loop` (one skill, 7 subagents, no questions to the owner, merge and tag per phase). From its history: 12-39 commits per phase, 2-10 decision files, 52 min to 2 h 30 per phase, four fixed review angles in parallel.

| | delivery-loop (P0-P14) | YesYak (P15, P16) |
| --- | --- | --- |
| Commits per phase | 12-39 | 13, 11 |
| Decision files per phase | 2-10 | 4, 3 |
| Time per phase | 52 min - 2 h 30 | P15 about 1 h 40 of commits across 3 sessions; P16 52 min unattended |
| Questions to the owner | none by design | P15: 4 interview rounds and the checkpoints; P16: none (unattended) |
| Review | 4 reviewers per round, up to 3 rounds | 4 missions plus a verifier; in P16 a second premortem of the fix |
| Resume after a cut | `.scratchpad/STATE.md` (gitignored; P0-P8 lost) | handoff in `docs/handoffs/` (in git) and `progress.md` |
| Plans in git | no | yes, `docs/<slug>-plan.md` |

Both reach a similar size and pace per phase. YesYak asked the owner more in the attended delivery, kept the plan and the handoff in git, and survived the cuts that the project's own process lost data on. It needed a correction where the project's process has a hard gate (its retro rule and hooks).

## Findings

- F-053 (Skill, fixed in v0.4.2): seen again. The P15 retrospective listed only the messages of session 3 from the demo; sessions 1 and 2 and the regression correction are missing, and it added two user messages that were never sent. The skill said "every message of the user in this session". It now says "in this piece of work" and reads the earlier transcripts when a handoff or `progress.md` shows earlier steps.
- F-064 (Bench, fixed in bench tools): `turn.sh` without `--model` used the first model of the run, not the model of the current session, so session 3 changed model after one turn. The fake HOME also hid Playwright's browsers; `turn.sh` now passes `PLAYWRIGHT_BROWSERS_PATH`.
- F-065 (Skill, fixed in v0.4.2): in an unattended run the agent ended its turn to wait for the e2e suite in the background ("I'll resume automatically"); nobody sends the next message, so the run stalled and the suite died with the turn. `unattended-run` now says to never end a turn to wait for a test run, a build or a subagent.
- F-066 (Model, watch): minimax opened session 3 without any skill (the start-up check failed on a malformed tool call and was not retried), called a new e2e failure pre-existing, rewrote `progress.md` from scratch and lost the plan-step table, and put the `phase-P15` tag before the last two commits.
- F-067 (Skill, watch): after the demo, the agent merged into `main` and tagged without asking, and skipped the red team, the PR body and the retrospective. It followed the project's rule "merge and tag at the end of a phase". The session had never loaded `feature-delivery-pipeline` (it was opened by the model in F-066). After the correction it rolled back cleanly and ran every phase.
- F-068 (Model, watch): a retrospective proposed a `.githooks/pre-merge` guard; git has no hook that runs on a fast-forward merge, so the guard could never fire. The retrospective did not test its guard.
- Good: a handoff without being asked at "I have to stop for today"; a resume that checked the handoff against the repo; a complete unattended delivery whose red team found two real blocking defects.
- Series count: stays at 0 (F-065 is new).

## Cost

≈ 2.58 $ at models.dev prices for the puppet.

## Pull request

The user allowed a real PR on this project: https://github.com/delineas/packbeat/pull/1. Branch `pr/p15-p16-ux` from the project's `main`, 21 commits (without the bench commit, the YesYak setup, the YesYak guard line and the two handoffs), authored by the user. `pnpm check` 165 pass and `pnpm e2e` 186 pass on the branch.
