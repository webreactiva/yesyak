# Run 0003-markdown-nbsp

- Source: https://github.com/thephpleague/html-to-markdown.git @ 0be46a17d
- YesYak: v0.3.0 · model: ollama-cloud/deepseek-v4.1-flash · turns: 19
- Sessions: `ses_eb6af380effeAPMsoBI4brkTJQ` (ollama-cloud/deepseek-v4.1-flash, from turn 1), `ses_eb6879f12ffebEjCI1oVzz2K54` (ollama-cloud/deepseek-v4.1-flash, from turn 3), `ses_eb6aef4efffessgcw9rHdUKN8n` (ollama-cloud/deepseek-v4.1-flash, from turn 2)
- Tokens: input 384216, output 150705, cache_read 22311168, cache_write 0 · ≈ 0.2150 $ (models.dev prices)
- Tool calls: 221 · errors: 1
- Branch: feat/preserve-nbsp
- Skills loaded, in order: customize-yak → simplified-technical-language → feature-delivery-pipeline → on-the-spot → domain-language → plain-visual-docs → write-acceptance-spec → walking-skeleton-plan → git-commit-organizer → execute-plan-loop → decision-record-log → verify-against-spec → triage-findings-list → traffic-light-findings → write-visual-pr → pr-reviewer-guide → session-retrospective-rules
- Project: thephpleague/html-to-markdown (PHP, 2808 lines in `src`); task: feature from issue #258, keep non-breaking spaces behind an option
- Result: all phases reached; 84 → 91 tests with the same 5 known failures (libxml on this machine), phpstan clean; 37 lines changed in `src`
- Interventions: 3 corrections, 0 nudges, 0 rescues. First run with ollama-cloud/deepseek-v4.1-flash (the user asked for no luna model)

## Phases

| Phase | Reached | Artifacts | Notes |
| --- | --- | --- | --- |
| customize-yak | yes | `AGENTS.md`, `.agents/yesyak.json`, own commit | Full check, commit convention and own commit right. Wrote without a yes and did not run the check until corrected; then a strong baseline per failure cause |
| 0 Starter kit | yes | `progress.md`, branch | "Search whether it exists" found the open upstream PR #280; root cause located before any question |
| 1 Grill & sketch | yes | `interview-decisions.md`, `domain-language.md` | Three rounds, scaled itself (skipped security as not applicable); no "(Recommended)" mark |
| 2 Write the contract | yes | spec (230 → 146 lines, 12 AC), plan (3 steps) | Spec too long again (correction). Offered spec review and work items itself. Walking skeleton end to end |
| 3 Make it work | yes | 3 commits, ADRs 0001-0002, `loop-log.md` | Baseline held at every commit: exactly the 5 known failures |
| 4 Break it | yes | `verification-report.md`, `scripts/verify-gaps.php` | Read-only, no commits (F-007 verified). Red team skipped by the human; the human found a null-config risk in a public class (correction) |
| 5 Sign your work | yes | `change-list.md`, 2 item commits, `pr-body.md`, `pr-guide.md` | Phase marked done only with its files (F-005 verified). No block without a remote |
| 6 Retrospective | yes | `retrospective.md` | All three corrections with quotes, causes and measured numbers (F-014 verified) |

## Interventions

| Turn | Kind | My words | Cause |
| --- | --- | --- | --- |
| 1 | (probe) | isolation probe | only YesYak skills + opencode built-ins |
| 2 | (observation) | — | customize-yak: full check (composer test), mixed commit convention and own commit all correct (F-004 detection, F-011, F-021 OK); but never ran the check, so the 5 failing tests, phpcs and psalm on main went unrecorded; wrote files without a yes after the harness question-cancel message told it to assume (question tool now disabled for the bench) |
| 3 | (probe) | question tool probe | tool disabled; work session restored as current |
| 4 | correction | "Has escrito sin esperar mi sí. Y composer test, ¿pasa en main? Compruébalo y anota lo que ya falla antes de seguir." | skill says write only after a yes, and run the full check once on the default branch |
| 5 | answer | "A, pero phpunit también falla 5 en local: deja esos 5 como fallos conocidos (con el fichero de línea base) y que cada commit no añada fallos nuevos. Haz commit del cambio de AGENTS.md." | after the correction: strong baseline (each failure with its cause: PHP version, psalm version, libxml 2.15), saved in .scratchpad; option A still assumed phpunit passes locally |
| 6 | answer + request | (see msg-06) | check line rewritten to "add no new failures" with the baseline file; it flagged that the baseline in .scratchpad is not versioned (customize-yak does not say where to record it) |
| 7 | approve | "Sí a las dos." | phase 0 excellent: "search whether it exists" found the open upstream PR #280; root cause and second site located; verdict, branch, no remote |
| 8 | answer | "1b, 2a, 3a." | good questions grounded in upstream PR #280 and the code; no "(Recommended)" mark, only the first position; announced "round 1 of 4" for a small feature (F-008 watch) |
| 9 | answer | "4a, 5a, 6a, 7a." | interview scaled itself: skipped the security round as not applicable and merged the rest; real edge cases (NBSP at an emphasis delimiter, runs, U+202F) |
| 10 | answer | "8a, 9a, 10a." | third and last round, useful; scope narrowed with code facts (two sites; TextConverter needs the config). F-008 not repeated with this model |
| 11 | approve | "Sí, todo bien. Sigue con la spec." | phase 1 checkpoint exemplary: artifacts, one-line decisions, central term fixed, prototypes declined with reason, one question |
| 12 | correction | "Son 230 líneas para un cambio de unas 15 líneas de código. Recorta la spec a lo que hace falta para construirlo y probarlo. Sin red team ni work items." | F-001 third run, second model, after the v0.2.0 rule: spec 230 lines, 15 AC (omitted 4 sections, but still long). Offered both optional steps itself (F-010 OK). Verified current behaviour before writing; validated diagrams |
| 13 | approve | "Aprobada. Sigue con el plan." | cut to 146 lines, 12 AC, with a table of what was removed and why; amended the spec commit |
| 14 | approve | "Aprobado. Implementa el plan en un loop hasta completarlo." | plan 3 steps: walking skeleton end to end, emphasis edge, docs; coverage by script; step 1 has 8 AC but one capability (F-009 not repeated) |
| 15 | answer | "Solo la verificación contra la spec. Sin red team ni hook." | loop clean: 3 gitmoji commits, 90 tests with exactly the 5 known failures (baseline held, F-004), phpstan OK, ADRs 0001 and 0002, loop-log; offered phase 4 and suggested agent-hook-guard from the turn-4 correction. Planted check: TextConverter now uses $this->config without a null check (a public class built outside Environment breaks) |
| 16 | correction | "TextConverter es una clase pública. Si alguien la usa sin pasar por Environment, $this->config es null y falla. Compruébalo y, si es así, arréglalo antes de la PR." | F-007 verified: read-only verification, scratch script, no commits, offer to convert gaps into tests. Missed the backward-compatibility risk (red team skipped by the human, so expected) |
| 17 | approve | "Sí." | fix with a failing test first, baseline held (91 tests, 5 known failures), psalm compared to its baseline; ADR 0003 for the contract of a public class (borderline for a fix) |
| 18 | approve | "1 2 3." | triage correct (3 items with lights and sources, accepted items with reasons); progress.md keeps phase 5 as "next", not done |
| 19 | approve | "Bien. Sigue." | F-005 verified: phase 5 marked done only with pr-body.md and pr-guide.md; item commits; local PR without a remote, no block (F-023 fix) |
| 20 | (end) | — | F-014 verified: the retrospective listed all three corrections (turns 4, 12, 16) with quotes, causes and measured numbers (37 lines in src vs a 230-line spec) |
