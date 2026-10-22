---
name: yak-pilot
description: The one entry point of YesYak. It takes any feature request or bug report in plain words, reads the project state and the user's profile, makes the plan of skills (which skills run, whether a spec and a plan are needed, which optional steps apply), and decides where a human must decide (human-in-the-loop gates) and why. After one approval it runs the plan alone and stops only at those gates. The user never has to know or name a skill. Use it for every feature request or bug report, and whenever the user says "do it", "autopilot", "run it alone but stop where you need me", "decide when you need me", or does not know which skill to use.
---

# Yak pilot

The user asks for a result. You know the skills. Choose them, run them, and ask the user only where a human decision is necessary.

This skill plans and keeps the run on its plan. The phase skills do the work. `unattended-run` answers every question that is not a gate and keeps the decision log. `customize-yak` writes the profile.

## 1. Read the request, the state and the profile

1. Find the position with the state signals of `ask-yak` (`references/process.md`). If work for this slug has started, plan only the steps that are still to run.
2. Read the profile: the `pilot:` lines that `check_yesyak.py` prints. No `pilot:` line means no profile. Then the first message of the run asks the round of `customize-yak` ("Pilot profile") together with the blocking questions of section 2, and says that the run uses the default profile until the answer. `customize-yak` writes the answer.
3. Choose the route: a feature request goes to `feature-delivery-pipeline`, a bug report to `bug-intake`.
4. Read the code that the request touches, and give the "does it fit in one iteration?" verdict of the pipeline. A split is a gate: the user chooses the first delivery.

## 2. Ask only what blocks the run

A question blocks the run when both are true:

- The request, the code and the project docs do not answer it.
- A wrong guess changes a result that a user can see, or makes more than one step run again.

Ask all blocking questions in one round, in the format of `on-the-spot` ("How to ask"), with "use the recommended options" as the first answer. Write the answers to `.scratchpad/<slug>/interview-decisions.md`, so the interview does not ask them again. If no question blocks the run, say so and ask nothing.

## 3. Make the plan of skills

Start from the route and its process map. For each step, decide if it runs, and write the skill that does it.

**Size the artifacts.** Unless the user or the profile asks for them:

| The task | Spec | Plan |
| --- | --- | --- |
| A bug with a clear contract (the code, a test or a document says what is correct) | the bug report of `bug-intake` | the change list of the fix route |
| A small change with one obvious design, no new contract | short (`write-acceptance-spec`, criteria only) | none; build from the criteria |
| A new behavior, a new contract, or more than one way to build it | full | full (`walking-skeleton-plan`) |

Write the choice and its reason in the plan. A spec left out for a change that touches a contract is a gate.

**Optional steps.** Run one when its signal is in the request, the code or the profile:

| Signal | Step |
| --- | --- |
| Open questions remain after section 2, or the profile asks for the interview | `on-the-spot`, answered by `unattended-run` unless a question meets a gate criterion |
| More than one way to show or shape the result, and a person must see them | `prototype-options`, with a gate to choose |
| A public contract, security, private data, or many files | `red-team-review` on the spec (devil's advocate) |
| The user keeps a task list | `work-items-breakdown` |
| A user interface in the acceptance criteria, and the profile does not switch it off | `browser-acceptance-testing` |
| The user wants to understand the change before the merge | `feature-walkthrough` |
| A deploy is near | `production-readiness-review` |

A step that the process map does not put in brackets always runs. To leave one out is a gate.

## Gate rules

Check a decision against these rules, in this order. The first rule that matches decides.

1. **The profile.** An `always ask` entry that matches is a gate. A `never` entry is a limit: do not do it, and say so. No preset changes them.
2. **The gate criteria** below. A match is a gate.
3. **The preset** of the profile.

### Gate criteria

The stop rules of `unattended-run` ("When to stop anyway") always apply. A decision is also a gate when one of these is true:

| Criterion | For example |
| --- | --- |
| It changes a contract that other people or programs use, or behavior that already exists and that the request does not name | a public API, a file format, a data schema, command options, the output of existing calls |
| It changes security, access or private data | permissions, secrets, what a log keeps |
| It weakens a check | a test removed or loosened, a longer timeout, a lint rule switched off, a failure called "already there" |
| It cuts the scope or changes the requirement | a dropped acceptance criterion, a split, a step that the process map does not put in brackets left out |
| No source decides it, and the options give users different results | the behavior in an edge case that the request does not name |
| It costs money or time over what the user set | a paid service, a long job |
| You cannot classify it, or your confidence is low | two options look equal and the cost of a wrong choice is not clear |

### Presets

| Preset | The user's role | Gates |
| --- | --- | --- |
| `collaborator` | decides with you at each phase | every checkpoint of the route skill, plus the gate criteria |
| `approver` (default) | approves the plan and the risky decisions | the plan approval, plus the gate criteria |
| `observer` | watches and can interrupt | only the profile and the stop rules of `unattended-run` |

Without a profile, the default profile is `approver` with these `always ask` entries: push, publish or merge; open a browser; apply a retrospective guard.

## 4. Show the plan and ask once

Write the plan to `.scratchpad/<slug>/progress.md`, under `## Plan`, above the phase table:

```markdown
## Plan

- Request: customers can cancel an order before it ships
- Route: feature-delivery-pipeline · preset: approver
- Start → end: main → feat/orders-cancel → local PR, retrospective done
- Outward actions allowed: push the branch
- Spec: full (new behavior, a refund contract) · plan: full

| Step | Skill | Runs | Why |
| --- | --- | --- | --- |
| Interview | on-the-spot | yes, answered alone | two open points, none meets a criterion |
| Spec challenge | red-team-review | yes | refunds touch money |
| Prototype | prototype-options | no | no user interface |

| Gate | Where | Decision | Rule |
| --- | --- | --- | --- |
| G-01 | spec approval | refund rule for a paid order | no source decides it |
| G-02 | plan approval | new field in the orders table | contract: data schema |

- Hands-off from: G-02
```

Copy the start point, end point and outward actions to the top of `unattended-decisions.md`, where `unattended-run` expects them.

Show the user the plan in five lines or fewer: route, artifacts, number of gates and where, hands-off point, end point. With `collaborator` and `approver`, ask one question: approve the plan? A change from the user changes the plan; show it again. With `observer`, the plan is a status line: start at once.

## 5. Run the plan

Load the route skill and `unattended-run`, and start.

- **Load each skill of the plan when its step comes**, with the skill tool. Do not do a step's work from memory: the skill holds checks that memory loses. At each phase end, compare the skills you loaded with the plan. A skill not loaded is loaded now, or its skip is a gate (it cuts the scope) or a logged `Q-` decision with the reason.
- **At a gate**: stop. Show a short summary, the evidence (diff, test output), and the options, the recommended one first. Also offer "do not ask me this again". Wait. Log the answer as a `Q-` entry with "Chosen by: user", and the gate's status in the plan.
- **Dynamic gate**: before `unattended-run` answers a question or takes an action alone, check it against the gate rules. If it matches, add a row `G-NN (dynamic)` to the plan, stop and ask. Do not guess to keep the run going.
- **Between gates**: send the status line of `unattended-run` at each phase end, so the user can interrupt. A turn ends only at a gate or at the end point: wait for subagents, test runs and builds in the same turn (`unattended-run`, step 4).

## At the end

- Tell the user: planned gates, dynamic gates, decisions taken alone, skills skipped, and where the logs are.
- In the pull request body, put a "Gates" line before "Decisions taken without the user" (`unattended-run`): each gate, its answer and who gave it.
- `session-retrospective-rules` runs its "Gates review" on this plan and proposes changes to the profile.
