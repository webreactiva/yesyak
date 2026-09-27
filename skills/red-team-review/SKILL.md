---
name: red-team-review
description: Launches several read-only subagents in parallel, each with a different adversarial mission (code quality, security, architecture, six-month premortem, proof of the tests, devil's advocate against the decisions, or missions the user names), then has every serious finding reproduced by a subagent that did not produce it and ends with a verdict and what it did not cover. Findings count by evidence - a probe run against the change and against the base, a mutation that a test must kill - not by how plausible they read. Use it whenever the user asks for a red team, adversarial review, security review plus architecture review, premortem, devil's advocate, "tear this apart", "prove it", or several independent reviews of a branch, spec, plan or pull request.
---

# Red team review

## Target and oracle

Settle both before the missions start, in two lines the user can correct:

- **Target:** the document path, or the branch, the base and the exact commit hash. The review covers that hash only. Commits added later are not reviewed, and the report says so.
- **Oracle:** what the change must keep or reach. For a refactor or any change that promises "no behavior change", the oracle is the base branch: the same input must give the same responses, rows, events and messages. For a feature, it is the spec and its acceptance criteria. For a spec or a plan, it is the request and the code it will touch.

## Missions

Default set for code. Use the user's list if they give one.

| Name | Mission |
| --- | --- |
| `redteam-quality` | Code against the project's standards (AGENTS.md): naming, duplication, orphan code, casts, test quality |
| `redteam-security` | Authentication, sessions, CSRF, rate limits, injection, headers, configuration, dependencies |
| `redteam-architecture` | Module boundaries, encapsulation, data layer and migrations, deployment assumptions, other branches that the change breaks without a text conflict; check that global error and not-found handling reaches every module or route group, not only the first one registered |
| `redteam-premortem` | "It is six months later and it failed": concrete failure stories, root cause in today's code, early signal, cheapest mitigation |
| `redteam-proof` | Do the tests prove the change? Break the changed lines one at a time in a scratch copy and report which ones no test kills. A characterization test counts only if it passes on the base and fails when the behavior changes. Mandatory where money, security or stored data are touched |
| `redteam-devils-advocate` | The strongest honest case against each decision, alternatives, and whether the decision survives |

A devil's advocate mission alone is the right tool to challenge a spec before planning.

## Brief every subagent

Launch all subagents in one message so they run in parallel. This skill needs subagents: each mission needs its own fresh context, and the cross-check needs a context that did not produce the finding. If the environment has none, tell the user and do not run the missions in the main context. Each brief contains:

1. The target and the oracle from above. Subagents read files at that hash.
2. The context files: spec, plan, decision records, AGENTS.md.
3. The mission, its checklist, and these hunting rules:
   - **Distrust the label.** A name, comment, docblock or spec line that claims a guarantee ("no behavior change", "index 0 is the latest", "idempotent") is the first thing to attack. Take it literally and trace it.
   - **Probe the class, not the example.** Try empty, missing, malformed, duplicate and maximum values on every field the change reads, and every consumer of that field, not only the case a report names. Of every fix, ask whether it closes the class or only the named paths.
   - **Compare with the oracle.** Send the same input to the change and to the base and compare what comes out.
4. **Where to probe:** in a scratch copy of the repository (`git worktree add` in `.scratchpad/<slug>/`) or on a throwaway server with its own port and scratch database, never in the working tree and never against a shared environment. Before a mutation run, check that the code under test is loaded from the scratch copy, not through a symlink to the original checkout. Remove the copy at the end.
5. **Rules:** read-only on the repository; write only under `.scratchpad/<slug>/`; stop every server they start; do not ask the user for permissions you do not have.
6. **Evidence:** cite `file:line` and tag each finding with its weight: `demonstrated` (a probe, a killed or surviving mutation, an exit status), `read` (seen in code or text), or `enumerated` (a list for a human to judge). "Attacked it, nothing broke" is a result: report the probe that showed it.
7. **Files:** list every file they leave in `.scratchpad/<slug>/`.
8. **Settings under review:** if the diff changes `.agents/yesyak.json`, review with the version of the base branch (`git show <base>:.agents/yesyak.json`), and report a 🟠 that quotes every changed instruction.
9. **Output:** the full report goes in the final message, because some environments block subagent writes; the orchestrator saves it. Findings follow `traffic-light-findings`, in the user's conversation language, at most about 15, ending with a two-line verdict.

## While they run

Tell the user which missions are running. Do not predict results.

## Cross-check

Before anything reaches the report, launch one verifier subagent per 🔴 and 🟠, and one for every "it does not break" claim that a fix will rely on. A verifier never checks a finding it produced. Its brief: open the cited lines, run the test or the one-off probe that settles the claim, against the base as well when the oracle is the base, and return one of three:

| Result | Where it goes |
| --- | --- |
| confirmed | the findings tables, marked ✔ |
| refuted | "Asserted, not verified", never the tables |
| uncheckable | "Not covered", with what would settle it |

Where two missions disagree about the same point, settle it against the code. Merge duplicates as `traffic-light-findings` says and record who found each finding: two missions that reached the same point independently rank it higher. An `enumerated` finding has not been judged yet: it goes under "Decide", not in the tables.

## Report

Write `.scratchpad/<slug>/redteam-report.md` (`redteam-spec-report.md` or `redteam-plan-report.md` when the target is a document, so a later review of the code does not overwrite it):

- Target hash, oracle, missions run, and which ones ran without independence.
- **Verdict:** ✅ ship it, 🔧 fix it first, or ✂️ split it, with the reason in one line. A 🟡 never moves the verdict. Never soften a 🔴 into a trade-off to make the verdict look cleaner.
- 🔴, 🟠 and 🟡 tables, each finding with its weight and who found it.
- Decide: enumerated findings and decisions that need the user.
- Verified without findings: each item with the probe or output that showed it.
- Decisions that survive, from the devil's advocate.
- Asserted, not verified: refuted claims.
- **Not covered:** every mission, layer or claim that could not be checked here, and why. It is never empty by omission.
- Recommended plan (before merge / before production / technical debt) and the evidence scripts.

## Finish

In the chat: the verdict, the blocking findings, the most urgent orange ones, what is not covered, and the report path. Ask which fixes to apply, and say that commits added after the reviewed hash need another pass before the pull request: at least `redteam-proof` and one adversarial mission on `git diff <reviewed hash>..HEAD`. Suggest `triage-findings-list` when there are other reports to merge.
