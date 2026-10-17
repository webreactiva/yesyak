# Run 0011-retry-split-handoff

- Source: https://github.com/avast/retry-go @ 5bccbfa93
- YesYak: v0.3.6 · model: ollama-cloud/deepseek-v4.1-flash · turns: 11
- Sessions: `ses_eb563b119ffeKj101DKhm1j9iH` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb56387a8ffe3Vuzb0lY5M2q5K` (ollama-cloud/deepseek-v4.1-flash, from turn 2), `ses_eb55ce938ffe60c435rSaP6S6J` (ollama-cloud/deepseek-v4.1-flash, from turn 10)
- Tokens: input 307294, output 126821, cache_read 10221458, cache_write 0 · ≈ 0.1529 $ (models.dev prices)
- Time: 14 min wall, 12 min of agent work · model steps: 147
- Tool calls: 187 · errors: 0
- Branch: feat/retry-on-returned-value
- Skills loaded, in order: customize-yak → feature-delivery-pipeline → git-commit-organizer → scratchpad-working-files → simplified-technical-language → on-the-spot → domain-language → plain-visual-docs → write-acceptance-spec → walking-skeleton-plan → handoff-and-resume → ask-yak → handoff-and-resume → execute-plan-loop → git-commit-organizer → decision-record-log → no-slop-code → scratchpad-working-files → verify-against-spec → write-visual-pr → plain-visual-docs → session-retrospective-rules
- Project: avast/retry-go (Go); task: three pieces of work in one message (feature #107, bugs #137 and #122), with a session cut in the middle
- Result: all phases reached for delivery 1 across two sessions. 32 → 43 Go tests, `go vet` and `gofmt` clean (I ran them). Deliveries 2 and 3 wait in the spec's out-of-scope list and in the handoff
- Interventions: 0 nudges, 0 corrections, 0 rescues

## Forced triggers

| Trigger | Result |
| --- | --- |
| Too big for one iteration | First time exercised, and it held: phase 0 gave the verdict "Split" with three deliveries, a branch for each, the feature first and the two bugs for `bug-intake` later |
| Chat rule (F-051, fixed in v0.3.6) | Verified: the phase 0 checkpoint asked to write "the PR stays local" to AGENTS.md; it went outside the block, in its own commit on `main` |
| Session ends mid-work | First time exercised, and it held: `handoff-and-resume` wrote `docs/handoffs/handoff-2026-10-17-retry-on-returned-value.md` with the goal, state, decisions and who took each, standing instructions and the next step. It found the session id in `OPENCODE_SESSION_ID`, which the skill did not name |
| Resume in a new session | Held: `ask-yak` and `handoff-and-resume` loaded; it checked the note against the branch, last commit, tree and test baseline before it went on, and asked nothing already decided |

## Phases

| Phase | Session | Notes |
| --- | --- | --- |
| customize-yak | 1 | New block line present; checks `go test`, `go vet`, `gofmt -l` named apart; lint needs Docker, said so |
| 0 Starter kit | 1 | Split verdict; the rule commit on `main` before the branch |
| 1 Grill & sketch | 1 | Searched first; one round of four questions with recommendations |
| 2 Write the contract | 1 | Spec 180 lines for an estimated 40 code and 160 test lines; plan 45 lines. Spec and plan shown at one checkpoint, not two |
| 3 Make it work | 2 | 3 steps, 3 commits; an ADR for the new public API (decision records on) |
| 4 Break it | 2 | Verification found a real deviation (sentinel message text) and fixed it; red team skipped on my request |
| 5 Sign your work | 2 | `pr-body.md` local, Mermaid validated |
| 6 Retrospective | 2 | Covered only the second session's two messages; the first session (split, rule, interview) was left out |

## Findings

- F-052 (Bench, fixed in bench tools): the puppet inherited the driver's Claude Code variables through tmux (`CLAUDECODE`, `CLAUDE_CODE_SESSION_ID`, a messaging token). The handoff still chose `OPENCODE_SESSION_ID`, but it could have written the driver's id. `turn.sh` and `turn-claude.sh` now remove every `CLAUDE*` and `AI_AGENT` variable.
- F-053 (Skill, watch): after a resume, the retrospective covered only the current session, not the whole piece of work.
- `handoff-and-resume` named only Claude Code for the session variable; it now also names `OPENCODE_SESSION_ID` (the repository premise asks for more than one option when a tool is named). v0.3.7.

## Cost

≈ 0.15 $ at models.dev prices for 12 turns in two sessions, 14 minutes.
