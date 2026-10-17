# Run 0000 · pilot

- Source: local copy of `tempopod` (a small Node.js CLI, vitest, 14 tests green)
- YesYak: 7c48557 (before v0.1.0), skills symlinked, not isolated
- Model: openai/gpt-5.6-sol, one unattended `opencode run` with `feature-delivery-pipeline` and `unattended-run`
- Sessions: `ses_eb7033533ffekA0DFyUq18fLtY` (failed: `gpt-5.5` is not allowed with a ChatGPT account), `ses_eb702b60bffezWdNrdrCOwevSH`
- Stopped by the human in phase 2, because the model costs 20 $/M output on models.dev

## Phases

| Phase | Reached | Artifacts | Notes |
| --- | --- | --- | --- |
| 0 Starter kit | yes | `progress.md`, `unattended-decisions.md` | Gave the iteration verdict "fits"; baseline green |
| 1 Grill & sketch | yes | `interview-decisions.md`, `domain-language.md` | Unattended: six decisions logged as `Q-` entries |
| 2 Write the contract | partly | `docs/json-output-spec.md` (146 lines), ADR 0001 for the JSON output contract | ADR correct: a CLI output format is a public contract |

## Findings

F-001, F-002, F-003 (see the log).
