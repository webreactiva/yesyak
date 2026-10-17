# Run 0009-filenamify-claude

- Source: https://github.com/sindresorhus/filenamify @ 2036ef0f9
- YesYak: v0.3.4-2-g4409951-dirty · model: anthropic/claude-sonnet-5-5 · turns: 7
- Sessions: `560eaef7-ef0e-4450-b6ec-f519a981e5ed` (anthropic/claude-sonnet-5-5, from turn 1), `0521d082-9033-4725-b0ed-a3fe5e8dfdd8` (anthropic/claude-sonnet-5-5, from turn 2)
- Tokens: input 46, output 12647, cache_read 796241, cache_write 45444 · ≈ 0.3198 $ (models.dev prices)
- Time: 4 min wall, 3 min of agent work · model steps: 25
- Tool calls: 17 · errors: 1
- Branch: feat/path-entry-point
- Skills loaded, in order: customize-yak → write-visual-pr → session-retrospective-rules
- Harness: Claude Code 2.1.302 in tmux through the new `turn-claude.sh` (`--setting-sources project --strict-mcp-config`); the probe saw only the YesYak skills and Claude Code's built-in skills
- Project and task: the same as run 0007 (filenamify, issue #43), with the same messages where the conversation allowed
- Result: the code works (`npx ava` 18 passed; I ran it), one commit, no dependency, subject under 60 characters. But the process was skipped: no phase 0, no questions, no spec, no plan, no verification, no red team. A breaking API change was decided without the user
- Interventions: 0 nudges, 0 corrections, 0 rescues. The process asks for many checkpoints; this run had none, so the zero does not mean a good run

## Compared with run 0007 (same task, deepseek-v4.1-flash)

| | 0007 deepseek (OpenCode) | 0009 Sonnet (Claude Code) |
| --- | --- | --- |
| Setup | Steps of the check named apart | Ran the steps apart, but named `npm test` in the block with a note |
| Feature request | Phase 0 → 6, every checkpoint | Code and commit in one turn, "small change" |
| Chat rules | Proposed outside the block in phase 0 | Written outside the block only after the retrospective |
| Design questions | 8, each with a recommendation | none; kept `filenamify/browser` as an alias |
| Red team | found an unmarked breaking change and a guard test that could not fail | not run |
| Tests | 16 → 19, each new test proven with a mutation | 16 → 18 |
| "what now?" | — | answered from memory; `ask-yak` not loaded |
| Cost | 0.12 $, 103 steps, 16 min | 0.32 $, 25 steps, 4 min |

## Interventions

| Turn | Kind | My words |
| --- | --- | --- |
| 1 | (probe) | isolation probe |
| 2 | request | "I just installed YesYak in this project, set it up. We do not need browser testing here, switch it off." |
| 3 | answer | "Yes, write them. No decision records." |
| 4 | request | the 0007 feature request, two working rules, no-PR line |
| 5 | answer | "what now?" |
| 6 | answer | "2, then the retrospective." |
| 7 | answer | "Write the three as AGENTS.md lines, the PR rule is permanent. No hooks." |

## Findings

- F-049 (Skill, confirmed: strong model, and the same gap as F-045 with a weak one): nothing in the YesYak block says that a feature request or a bug report starts the process. Sonnet judged the change small and skipped every phase; it also answered "what now?" without `ask-yak`. Fixed in v0.3.5: the block template has the line "A feature request starts `feature-delivery-pipeline` and a bug report starts `bug-intake`, whatever the size. Ask the user before you skip a phase."
- F-034: the v0.3.3 rule was half followed by a strong model (steps run apart, chain named in the block). Fixed in v0.3.5: the template's check line asks for one command per step.
- F-050 (Bench, fixed in bench tools): the bench could drive only OpenCode. `turn-claude.sh` drives Claude Code; `prepare.sh` copies the skills to `.claude/skills` too; `report.py` reads Claude Code's stream JSON and transcripts.
- The retrospective found the skipped steps and the unrecorded rules by itself.

## Cost

≈ 0.32 $ at models.dev prices for 7 turns, 4 minutes (paid by the subscription that runs Claude Code).
