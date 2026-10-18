# Run 0021-linkify-parens

- Source: https://github.com/sindresorhus/linkify-urls @ 2d0a5bf0a
- YesYak: v0.4.3-2-gbce7fa9 · model: ollama-cloud/deepseek-v4.1-flash · turns: 7
- Sessions: `ses_eb34317beffeRmJ2xMIMzSAL1A` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb3430398ffe4XfNk9LykqAJ09` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 44260, output 37943, cache_read 2235392, cache_write 0 · ≈ 0.0361 $ (models.dev prices)
- Time: 5 min wall, 4 min of agent work · model steps: 49
- Tool calls: 86 · errors: 0
- Branch: fix/wikipedia-parentheses
- Skills loaded, in order: bug-intake → git-commit-organizer → execute-plan-loop → write-visual-pr → session-retrospective-rules
- Puppet: OpenCode with deepseek-v4.1-flash; YesYak installed with `install.sh -a`
- Task: bug #28 (parentheses in URLs), reported as a user would: a Wikipedia link with `(planet)` is cut
- Result: fix route complete. Triage confirmed the bug, found a second copy of the URL pattern and an existing test that rules out "always include `)`", and stated the assumed contract (balanced parentheses only). Branch `fix/wikipedia-parentheses`: a refactor commit (one shared pattern), the fix with a failing-first test, then two project commits I asked for (the AGENTS.md rule and the `.gitignore` line). `npm test` exit 0, 42 tests (I ran it); the reported input now links in full
- Interventions: 0 nudges, 0 corrections, 0 rescues

## Fix route

| Step | Reached | As the skill asks |
| --- | --- | --- |
| bug-intake | yes | `bug-report.md` before any code; layers, contract, root cause, scope |
| Branch `fix/<slug>` | yes | `fix/wikipedia-parentheses` |
| execute-plan-loop, change-list mode | yes | failing test first, then the fix; `progress.md` and `loop-log.md` |
| Checks by the light of the bug | verify and red team skipped, with a reason (no spec; the suite plus the contract cover it) | optional on the fix route |
| write-visual-pr, short | yes | 74 lines, local |
| session-retrospective-rules | yes | names why no test caught it and proposes a class test; proposes the AGENTS.md rule for the chat instruction |

## Findings

- None new. Setup left the installer's `.gitignore` line uncommitted until I asked (watch only: it said so and asked).
- Series count: 3 of 3 (runs 0019, 0020, 0021 with no new skill finding; 0019 with a strong model; every skill used at least once). The goal of this series is met.

## Cost

≈ 0.04 $ at models.dev prices for the puppet.
