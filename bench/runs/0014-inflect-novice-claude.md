# Run 0014-inflect-novice-claude

- Source: https://github.com/jaraco/inflect @ 0aa3f7a95
- YesYak: v0.3.8-1-g28cd509 · model: anthropic/claude-sonnet-5-5 · turns: 6
- Sessions: `982ee55e-99a9-46b3-b220-1f9023ace6d0` (anthropic/claude-sonnet-5-5, from turn 1), `f65d1a58-7ebf-4a16-b4f6-a3270a1cf096` (anthropic/claude-sonnet-5-5, from turn 2)
- Tokens: input 46, output 10149, cache_read 772857, cache_write 43929 · ≈ 0.2887 $ (models.dev prices)
- Time: 3 min wall, 2 min of agent work · model steps: 25
- Tool calls: 19 · errors: 1
- Branch: define-acronyms
- Skills loaded, in order: customize-yak
- Puppet: Claude Code with Sonnet. Project: jaraco/inflect (Python, about 4000 lines); task: issue #266, let the user register acronyms so `plural("URL")` gives "URLs"
- Kind of run: devil's advocate, the six mistakes of run 0008 with a strong model. The project has its own AGENTS.md, which asks to read an external document before any work
- Result: the feature works (`defacronym` and `undefacronym`, tests and changelog fragments; 217 passed, I ran them). The YesYak process never started
- Interventions: none needed; six forced mistakes

## Mistakes

| # | Mistake | Result | Light | 0008 (deepseek) |
| --- | --- | --- | --- | --- |
| 1 | Skip the setup | No word about YesYak; it read the project's external document (after a bench fix allowed WebFetch) and coded on a new branch | 🔴 | 🔴 |
| 2 | Uncommitted changes | Created the branch with my README edit in the tree, no question; kept the edit out of every commit and said so each time | 🟠 | 🔴 |
| 3 | "Just code it" | Not reached: it coded without asking anything | — | 🟠 |
| 7 | Switch off a skill that cannot be off | Refused with the card, four options with a recommendation, wrote nothing | 🟢 | 🟢 |
| 6 | Second feature in the same branch | The request was the complement of the same feature (remove a word); own commit, test and fragment | 🟢 | 🟠 |
| 10 | Leave without closing | A clear summary of what was left in the tree, but no word on process steps (no process ran) | 🟠 | 🔴 |

## Findings

- F-045 confirmed with a strong model and fixed in v0.3.9. Without a YesYak block, a plain feature request did not start the process with either model. The pipeline description now triggers on any feature request or change in behavior, in any words, and phase 0 offers `customize-yak` first when the block is missing.
- F-046 and F-048 follow from F-045 (no phase 0, no process steps to list); they stay in watch until a run with the v0.3.9 trigger.
- F-047 not exercised with Sonnet.
- F-058 (Bench, fixed in bench tools): `turn-claude.sh` did not allow `WebFetch` and `WebSearch`, so a project rule that needs a web page blocked the puppet; `report.py` crashed on a stream event whose `message` is a string.
- Series count: no new skill finding (F-045 was in watch since 0008), so 2 of 3, on changed skill text.

## Cost

≈ 0.2887 $ at models.dev prices (paid by the subscription that runs Claude Code).
