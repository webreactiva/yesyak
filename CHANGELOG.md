# Changelog

Versions follow semantic versioning. Before 1.0, a minor version can change a contract that settings files in other projects use (a skill name, a Replaceable heading, a phase number); its entry says so.

## 0.1.0 · 2026-10-17

First tagged version.

- Phases named after the "Resuelve, rompe, repite" workflow: 0 Starter kit, 1 Grill & sketch, 2 Write the contract, 3 Make it work, 4 Break it, 5 Sign your work, 6 Retrospective, 7 Later. **Contract change:** the numbers of the old Build, Validate, Fix and Deliver phases changed; `ask-yak` maps the old names of an existing `progress.md`.
- Phase 0 asks whether the request fits in one iteration.
- New skills: `prototype-options` (optional, Grill & sketch) and `agent-hook-guard` (optional, Break it).
- `decision-record-log`: four questions decide an ADR; dependencies and patterns always get one, routine fixes and linter preferences never. A project can switch it off.
- `execute-plan-loop`: `loop-log.md`, an AGENTS.md review at the end, a look at every user interface step, one branch for the whole plan.
- `bug-intake`: a read-only triage first; checks in proportion to the light of the bug.
- `session-retrospective-rules`: session insights and agent hooks as guards.
- Smaller lessons in `write-acceptance-spec`, `write-visual-pr`, `no-slop-code`, `on-the-spot`, `customize-yak`.
