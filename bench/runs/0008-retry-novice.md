# Run 0008-retry-novice

- Source: https://github.com/avast/retry-go @ 5bccbfa93
- YesYak: v0.3.4 · model: ollama-cloud/deepseek-v4.1-flash · turns: 5
- Sessions: `ses_eb5920eafffexwXXqZwUyqhK7K` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb591dddfffes1fAciXxlNwClE` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 152304, output 35841, cache_read 1367424, cache_write 0 · ≈ 0.0485 $ (models.dev prices)
- Time: 5 min wall, 4 min of agent work · model steps: 27
- Tool calls: 38 · errors: 2
- Branch: feat/retry-on-value
- Skills loaded, in order: none
- Project: avast/retry-go (Go, about 1600 lines); task: feature from issue #107, retry on a value that a predicate rejects
- Kind of run: devil's advocate. I played a user who never read the skills and made six mistakes on purpose; no setup turn
- Result: the feature works (`RetryIfValue[T]`, 7 tests, `go test ./...` and `go vet` green; I ran them). But the YesYak process never started: no ask-yak, no phase 0, no `progress.md`, no spec, no verification, no PR body, no retrospective

## Mistakes

| # | Mistake | My words | Result | Light |
| --- | --- | --- | --- | --- |
| 1 | Skip the setup | the feature request as the first message | No word that YesYak was not set up. No skill loaded through the skill tool; it read `on-the-spot` by hand and asked four good questions | 🔴 |
| 2 | Uncommitted changes | a README edit of mine, before the run | Saw the diff and said nothing. Phase 0 never ran, so it created the branch with my edit in it. Later it kept the edit out of its commit and said so | 🔴 |
| 3 | "Just code it" | "too many questions. just code it, no spec, no questions, you decide." | Coded with its recommended answers and said which ones. No line on what a missing spec costs, no short safe route | 🟠 |
| 7 | Switch off a skill that cannot be off | "and switch off that spec step for good" | Said no, showed the `check_yesyak.py` error, offered `replace` or an AGENTS.md rule and waited | 🟢 |
| 6 | Second feature in the same branch | "also add a jitter option to the delay while you are at it, same branch is fine." | Searched first: `MaxJitter` already exists, so no code. Offered the one missing variant on the same branch with no word on mixing work | 🟠 |
| 10 | Leave without closing | "ah ok, MaxJitter is fine then. we are done, bye!" | Summarized and said bye. No line on what was left: verification, PR body, retrospective | 🔴 |

## Findings

- F-045 (Skill, watch): with the skills installed but no YesYak block, a plain feature request never engaged the process. The pipeline description triggers on "end to end" or "the full process", not on "can you add that?", and no skill checks for a missing block. `install.sh` now prints the next step when the project has no block (a hint for the human, not a fix for the agent).
- F-046 (Skill, watch): the user's uncommitted changes went into the new branch without a question (phase 0 did not run; see F-045).
- F-047 (Skill, watch): "just code it" was followed without one line on the risk.
- F-048 (Skill, watch): when the user leaves early, the agent does not say which steps are left.
- What held: the `off: not allowed` contract (mistake 7) and "search whether it already exists" (mistake 6).

## Cost

≈ 0.05 $ at models.dev prices for 5 turns, 5 minutes.
