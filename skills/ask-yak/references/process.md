# YesYak process

## Process map

```text
0 Starter kit         branch → slug → .scratchpad/<slug>/ → progress.md → does it fit in one iteration?
1 Grill & sketch      on-the-spot → (prototype-options) → domain-language
2 Write the contract  write-acceptance-spec → (red-team-review: devil's advocate on the spec)
                      → write-acceptance-spec (refine) → walking-skeleton-plan → (work-items-breakdown)
3 Make it work        execute-plan-loop
4 Break it            verify-against-spec → (browser-acceptance-testing) → red-team-review → (agent-hook-guard)
5 Sign your work      triage-findings-list → execute-plan-loop (change-list mode)
                      → write-visual-pr → pr-reviewer-guide → (feature-walkthrough)
6 Retrospective       session-retrospective-rules → (handoff-and-resume, when the work pauses)
7 Later               production-readiness-review, when a deploy is near
```

Steps in parentheses are optional.

Fix route, for a bug report:

```text
bug-intake (triage, then contract and reproduction) → branch fix/<slug> → execute-plan-loop (change-list mode)
→ checks by the light of the bug: (verify-against-spec) → (red-team-review) → (browser-acceptance-testing)
→ write-visual-pr (short) → session-retrospective-rules
```

Conventions that every phase loads: `simplified-technical-language`, `scratchpad-working-files`, `git-commit-organizer`, `no-slop-code`, `decision-record-log`, `traffic-light-findings`, `plain-visual-docs`. Entry: `yak-pilot` plans the skills and the stops for any feature or bug. Modes: `unattended-run` (no questions), `ask-yak` (where am I), `customize-yak` (change the process).

## State signals

Find the slug first. Take it from the branch: `feat/<slug>` or `fix/<slug>`. On another branch name, take it from `docs/<slug>-spec.md` or `docs/<slug>-plan.md` in `git diff --name-only <default branch>...HEAD`, then from the only folder in `.scratchpad/` with a `progress.md`. Without git, take it from the only `docs/<slug>-spec.md` in the folder. On the default branch, take it from a `docs/<slug>-spec.md` or `docs/<slug>-plan.md` that the last five commits changed. If more than one slug fits, list them and ask which one; do not choose.

The strongest signal found sets the position. Show the others; do not use them.

A `progress.md` written before the phases got their names can use the old ones: Prepare is 0, Define is 1 and 2, Build is 3, Validate is 4, Fix and Deliver are 5, Learn is 6.

| Signal | Position | Next step |
| --- | --- | --- |
| `docs/handoffs/handoff-YYYY-MM-DD-<slug>.md` or `handoff-YYYY-MM-DD-<slug>-N.md`, added by the last commit that changes more than handoffs, or by a later commit that only adds handoffs | Resume | `handoff-and-resume` with that file |
| The pull request of the branch is merged or closed | Done | the entry points |
| `.scratchpad/<slug>/retrospective.md` | 6 Retrospective done | `handoff-and-resume` if the work pauses; otherwise the entry points |
| `.scratchpad/<slug>/progress.md` | the phase and step it records | that step if it is not done; otherwise the step after it |
| `.scratchpad/<slug>/pr-guide.md` | 5 Sign your work done | `session-retrospective-rules` |
| An open pull request for the branch | 5 Sign your work | `pr-reviewer-guide` |
| `.scratchpad/<slug>/change-list.md` | 5 Sign your work | `execute-plan-loop` (change-list mode) |
| `verification-report.md`, `browser-test-report.md`, `redteam-report.md` or `hook-report.md` in `.scratchpad/<slug>/` | 4 Break it | the next Break it step, or `triage-findings-list` |
| `docs/<slug>-plan.md` | 3 Make it work | `execute-plan-loop` |
| `docs/<slug>-spec.md` | 2 Write the contract | `walking-skeleton-plan` |
| `.scratchpad/<slug>/interview-decisions.md` | 1 Grill & sketch | `domain-language` |
| A branch `fix/<slug>` | the fix route | the first fix step without its file |
| A branch `feat/<slug>` | 0 Starter kit not finished | create `progress.md` (`feature-delivery-pipeline`, phase 0) |
| `.scratchpad/<slug>/retrospective.md` older than `progress.md` | not a signal: an earlier piece of work with the same slug | |
| None of the above | No work started | the entry points |

Other report names do not move the position. In 2 Write the contract, a `redteam-spec-report.md` means the spec may still need `write-acceptance-spec` (refine): offer both next steps and let the user choose.

A conflict exists only when the strongest signal lacks the file that its phase needs, or when later work contradicts it:

| Strongest signal | Missing | Conflict |
| --- | --- | --- |
| `progress.md` at phase 3 or later | `docs/<slug>-plan.md` | yes |
| `progress.md` marks a phase done | a file that a card of that phase lists under Makes (for example `pr-body.md` for 5 Sign your work) | yes: the phase is not done |
| An open pull request | `docs/<slug>-spec.md`, on a branch that is not `fix/` | yes |
| `docs/<slug>-plan.md` without `progress.md` | nothing, but commits after the plan change code | yes: ask how far the build got (`.scratchpad/` may be on another machine) |
| A merged or closed pull request | nothing, but the branch has commits after the merge | yes: ask whether this is new work on the same branch |

On a conflict, name both signals, ask which one is right, and show no next step.

## Entry points

| Start from | Skill |
| --- | --- |
| "What now?", "where am I?" | `ask-yak` |
| Change the process, first install in a project | `customize-yak` |
| A feature request or a bug report | `yak-pilot`, which plans the skills and the stops, then runs `feature-delivery-pipeline` or `bug-intake` |
| A run without questions | the observer preset of `yak-pilot`; `unattended-run` answers the questions |
| A pause, or work that passes to someone else | `handoff-and-resume` |
| One task only | the skill of that step |

## Skill cards

Each card says when to use the skill, what it makes, what comes next, the sections that a `replace` adjustment can name, and whether an `off` adjustment is allowed.

### ask-yak
- When: the user does not know the next step, or asks where the work is
- Makes: nothing; an answer in the chat
- Next: the skill it names, after a yes
- Replaceable: none
- Off: not allowed

### customize-yak
- When: first install in a project, or the user wants another process
- Makes: `.agents/yesyak.json`, `~/.agents/yesyak.json`, the YesYak block of AGENTS.md
- Next: `ask-yak`
- Replaceable: none
- Off: not allowed

### feature-delivery-pipeline
- When: a feature from request to pull request
- Makes: `.scratchpad/<slug>/progress.md`, the branch
- Next: `on-the-spot`
- Replaceable: none
- Off: not allowed

### on-the-spot
- When: a vague request; before any spec
- Makes: `.scratchpad/<slug>/interview-decisions.md`
- Next: `prototype-options` (optional), then `domain-language`
- Replaceable: What to cover
- Off: not allowed

### prototype-options
- When: the interview is done and the user wants to see options before the spec
- Makes: `.scratchpad/<slug>/prototypes/`, the choice in `interview-decisions.md`
- Next: `domain-language`
- Replaceable: none
- Off: allowed

### domain-language
- When: after the interview, before the spec
- Makes: `.scratchpad/<slug>/domain-language.md`
- Next: `write-acceptance-spec`
- Replaceable: Template
- Off: not allowed

### write-acceptance-spec
- When: turn decisions into a spec, or refine it after a review
- Makes: `docs/<slug>-spec.md`
- Next: `red-team-review` on the spec (optional), then `walking-skeleton-plan`
- Replaceable: Template, Acceptance criteria
- Off: not allowed

### walking-skeleton-plan
- When: the spec is approved
- Makes: `docs/<slug>-plan.md`
- Next: `work-items-breakdown` (optional), then `execute-plan-loop`
- Replaceable: Ordering, Output
- Off: not allowed

### work-items-breakdown
- When: the user tracks work in a tool
- Makes: issues or tickets, or a task list in the repo; `.scratchpad/<slug>/work-items.md` for a tracker
- Next: `execute-plan-loop`
- Replaceable: 2. Build each item
- Off: allowed

### execute-plan-loop
- When: build the plan, or apply a change list
- Makes: commits, `.scratchpad/<slug>/progress.md`, `.scratchpad/<slug>/loop-log.md`
- Next: `verify-against-spec`, or after a change list `write-visual-pr`
- Replaceable: none
- Off: not allowed

### verify-against-spec
- When: the build is done
- Makes: `.scratchpad/<slug>/verification-report.md`
- Next: `browser-acceptance-testing` (optional), then `red-team-review`
- Replaceable: 2. Classify each criterion, 5. Report
- Off: not allowed

### browser-acceptance-testing
- When: the user asks for tests in a browser, or an unattended run decides that a change with a user interface needs them
- Makes: `.scratchpad/<slug>/browser-test-report.md`
- Next: `red-team-review`
- Replaceable: Edge cases to try, Report
- Off: allowed

### red-team-review
- When: challenge a spec, review the code before the fixes, and again on the commits added after the reviewed hash
- Makes: `.scratchpad/<slug>/redteam-report.md` (code), `redteam-spec-report.md` (spec)
- Next: `triage-findings-list` (code), `write-acceptance-spec` refine (spec)
- Replaceable: none
- Off: not allowed

### agent-hook-guard
- When: a review found a problem that a check of the agent tool could stop
- Makes: an agent hook and its script, `.scratchpad/<slug>/hook-report.md`
- Next: `triage-findings-list`
- Replaceable: none
- Off: allowed

### triage-findings-list
- When: there are reports to merge
- Makes: `.scratchpad/<slug>/change-list.md`
- Next: `execute-plan-loop` in change-list mode
- Replaceable: none
- Off: not allowed

### write-visual-pr
- When: the work is ready to deliver
- Makes: the pull request, `.scratchpad/<slug>/pr-body.md`
- Next: `pr-reviewer-guide`
- Replaceable: 2. Write the body
- Off: not allowed

### pr-reviewer-guide
- When: the pull request exists
- Makes: `.scratchpad/<slug>/pr-guide.md`, optional pull request comment
- Next: `session-retrospective-rules`
- Replaceable: The five questions
- Off: not allowed

### feature-walkthrough
- When: someone who did not build the feature must read its code
- Makes: a walkthrough document
- Next: `session-retrospective-rules`
- Replaceable: none
- Off: allowed

### session-retrospective-rules
- When: the work is delivered, or the user asks what went wrong
- Makes: `.scratchpad/<slug>/retrospective.md`, guards
- Next: `handoff-and-resume` if the work pauses; otherwise the entry points
- Replaceable: none
- Off: not allowed

### handoff-and-resume
- When: a pause, a compaction, or work that passes to someone else; "where were we"
- Makes: `docs/handoffs/handoff-YYYY-MM-DD-<slug>.md`
- Next: the next step that the note names
- Replaceable: none
- Off: not allowed

### production-readiness-review
- When: a deploy is near
- Makes: `.scratchpad/<slug>/production-readiness-report.md`
- Next: `triage-findings-list`
- Replaceable: 2. Review each area
- Off: allowed

### bug-intake
- When: a bug report
- Makes: `.scratchpad/<slug>/bug-report.md`, a failing test
- Next: the fix route
- Replaceable: none
- Off: not allowed

### yak-pilot
- When: any feature request or bug report; the user does not choose the skills
- Makes: the `## Plan` section of `.scratchpad/<slug>/progress.md`
- Next: `feature-delivery-pipeline` or `bug-intake`, with `unattended-run`
- Replaceable: Gate criteria, Presets
- Off: not allowed

### unattended-run
- When: the user wants no questions
- Makes: `.scratchpad/<slug>/unattended-decisions.md`
- Next: the skill it runs with
- Replaceable: none
- Off: not allowed

### simplified-technical-language
- When: always loaded; owns the language rules
- Makes: nothing
- Next: none
- Replaceable: none
- Off: not allowed

### scratchpad-working-files
- When: always loaded; owns working files
- Makes: `.scratchpad/<slug>/`
- Next: none
- Replaceable: none
- Off: not allowed

### git-commit-organizer
- When: always loaded; owns branches, slugs and commits
- Makes: branches, commits
- Next: none
- Replaceable: Message format
- Off: not allowed

### no-slop-code
- When: always loaded; owns slop rules
- Makes: nothing
- Next: none
- Replaceable: none
- Off: not allowed

### decision-record-log
- When: always loaded; owns decision records
- Makes: `docs/decisions/NNNN-*.md`
- Next: none
- Replaceable: ADR format
- Off: allowed

### traffic-light-findings
- When: always loaded; owns findings and severities
- Makes: nothing
- Next: none
- Replaceable: none
- Off: not allowed

### plain-visual-docs
- When: always loaded; owns openings and diagrams
- Makes: nothing
- Next: none
- Replaceable: none
- Off: not allowed
