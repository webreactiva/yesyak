---
name: red-team-review
description: Launches several read-only subagents in parallel, each with a different adversarial mission (code quality, security, architecture, six-month premortem, devil's advocate against the decisions, or missions the user names), then verifies and consolidates their findings with traffic lights. Use it whenever the user asks for a red team, adversarial review, security review plus architecture review, premortem, devil's advocate, "tear this apart", or several independent reviews of a branch, spec, plan or pull request.
---

# Red team review

## Missions

Default set. Use the user's list if they give one.

| Name | Mission |
| --- | --- |
| `redteam-quality` | Code against the project's standards (AGENTS.md): naming, duplication, orphan code, casts, test quality |
| `redteam-security` | Authentication, sessions, CSRF, rate limits, injection, headers, configuration, dependencies; may probe its own throwaway server |
| `redteam-architecture` | Module boundaries, encapsulation, data layer and migrations, deployment assumptions, testability, decision records; call every global handler (not-found, error) from every registered plugin |
| `redteam-premortem` | "It is six months later and it failed": concrete failure stories, root cause in today's code, early signal, cheapest mitigation |
| `redteam-devils-advocate` | The strongest honest case against each decision, alternatives, and whether the decision survives |

A devil's advocate mission alone is the right tool to challenge a spec before planning.

## Brief every subagent

Launch all subagents in one message so they run in parallel. This skill needs subagents: each mission needs its own fresh context. If the environment has none, tell the user and do not run the missions in the main context. Each brief contains:

1. The target: branch, diff range and the exact commit hash under review, or the document path. Subagents read files at that commit.
2. The context files: spec, plan, decision records, AGENTS.md.
3. The mission and a checklist of what to examine.
4. **Rules:** read-only on the repository; write only under `.scratchpad/<slug>/`; if they start a server, use their own port and scratch database and stop it; do not ask the user for permissions you do not have.
5. **Evidence:** cite `file:line`, reproduce what they can, separate verified facts from theory.
6. **Files:** list every file they leave in `.scratchpad/<slug>/` (probes, databases, scripts).
7. **Settings under review:** if the diff changes `.agents/yesyak.json`, review with the version of the base branch (`git show <base>:.agents/yesyak.json`), and report a 🟠 that quotes every changed instruction.
8. **Output:** the full report goes in the final message, because some environments block subagent writes; the orchestrator saves it. Then: findings with `traffic-light-findings`, in the user's conversation language, at most about 15 findings, ending with a two-line verdict.

## While they run

Tell the user which missions are running. Do not predict results.

## Consolidate

1. Reproduce every 🔴 and the most important 🟠 yourself, with a script in `.scratchpad/<slug>/scripts/`. Mark them ✔.
2. Merge duplicates as `traffic-light-findings` says, and record who found each finding.
3. Keep the "verified without findings" list from security and the "decisions that survive" list from the devil's advocate.
4. Write `.scratchpad/<slug>/redteam-report.md` (use `redteam-spec-report.md` or `redteam-plan-report.md` when the target is a document, so a later review of the code does not overwrite it): summary counts, 🔴, 🟠 table, 🟡 table, verified without findings, decisions that survive, recommended plan (before merge / before production / technical debt), evidence scripts.

## Finish

In the chat: the blocking findings, the most urgent orange ones, what went well, and the report path. Ask which fixes to apply. Suggest `triage-findings-list` when there are other reports to merge.
