---
name: autopilot-plan
description: Prepares the run that delivers one requirement with as few interruptions as possible. It reads the requirement and the project, asks only the questions that block an autonomous run, plans the phases, and decides where a human must decide (human-in-the-loop gates) and why. After the user approves the plan once, the pipeline runs alone with unattended-run and stops only at those gates. Use it whenever the user says "autopilot", "run it alone but stop where you need me", "decide when you need me", "prepare the run", "human in the loop", or gives a requirement and wants the smallest number of questions that is still safe.
---

# Autopilot plan

The user decides once how much autonomy the run gets. This skill decides where the user's attention is necessary, and nowhere else.

The skill only plans. `feature-delivery-pipeline` or `bug-intake` runs the phases. `unattended-run` answers every question that is not a gate and keeps the decision log.

## 1. Read the requirement and the state

1. Find the position with the state signals of `ask-yak` (`references/process.md`). If work for this slug has started, plan only the phases that are still to run.
2. Choose the route: a feature request goes to `feature-delivery-pipeline`, a bug report to `bug-intake`.
3. Read the code that the requirement touches and give the "does it fit in one iteration?" verdict of the pipeline. A split is a gate: the user chooses the first delivery.

## 2. Ask only what blocks the run

A question blocks the run when both are true:

- The request, the code and the project docs do not answer it.
- A wrong guess changes a result that a user can see, or makes more than one phase run again.

Ask all blocking questions in one round, in the format of `on-the-spot` ("How to ask"). Write the answers to `.scratchpad/<slug>/interview-decisions.md`, so phase 1 does not ask them again. If no question blocks the run, say so and ask nothing.

## Gate criteria

The stop rules of `unattended-run` ("When to stop anyway") always apply. A decision is also a gate when one of these is true:

| Criterion | For example |
| --- | --- |
| It changes a contract that other people or programs use | a public API, a file format, a data schema, command options |
| It changes security, access or private data | permissions, secrets, what a log keeps |
| It cuts the scope or changes the requirement | a dropped acceptance criterion, a split, an optional phase skipped against the request |
| No source decides it, and the options give users different results | the behavior in an edge case that the requirement does not name |
| It costs money or time over what the user set | a paid service, a long job |

Every other decision is autonomous: `unattended-run` takes it and logs it as a `Q-` entry.

## 3. Place the gates

1. Go through the planned phases and their checkpoints. Mark each decision that you can see now and that meets a criterion.
2. Put each gate at the earliest point where the agent can show the decision with its options. For example, an assumed behavior is a gate at the spec approval, not at the pull request.
3. Do not add a gate "to be safe". A gate without a criterion costs the user time and teaches them to approve without reading.
4. The hands-off point is the last planned gate. After it, the run goes to the end point with no planned stop.

## 4. Write the plan and ask once

Write `.scratchpad/<slug>/autopilot-plan.md`:

```markdown
# Autopilot plan: orders-cancel

- Requirement: customers can cancel an order before it ships
- Route: feature-delivery-pipeline
- Start point: main → feat/orders-cancel
- End point: PR open, not merged; retrospective done
- Outward actions allowed: push the branch, open the PR
- Phases: 0-6; prototype-options skipped (no user interface); red-team-review on the spec (refunds)

## Gates

| Id | Where | Decision | Criterion |
| --- | --- | --- | --- |
| G-01 | write-acceptance-spec, approval | refund rule for a paid order | no source decides it |
| G-02 | walking-skeleton-plan, approval | new field in the orders table | data schema |

- Hands-off from: G-02
- Stop also: the stop rules of unattended-run; dynamic gates
```

Copy the start point, end point and outward actions to the top of `unattended-decisions.md`, where `unattended-run` expects them.

Show the user the plan in five lines or fewer: route, number of gates and where, hands-off point, end point. Ask one question: approve the plan? This approval is the only gate that every plan has. A change from the user changes the file; show it again.

## 5. Run

Load the route skill and `unattended-run`, and start.

- **At a planned gate**: stop. Ask the question with its options and the recommended option first, and wait. Log the answer as a `Q-` entry with "Chosen by: user".
- **Dynamic gate**: before `unattended-run` answers a question alone, check it against the gate criteria. If it meets one, add a row `G-NN (dynamic)` to the plan, stop and ask. Do not guess to keep the run going.
- **Between gates**: send the status line of `unattended-run` at each phase end, so the user can interrupt.

## At the end

- Tell the user: planned gates, dynamic gates, decisions taken alone, and where the logs are.
- In the "Decisions taken without the user" section of the pull request (`unattended-run`), add one line per gate with who decided.
- A decision taken alone that the user later reverts is a missed gate. Give it to `session-retrospective-rules`; the guard can be an `add` entry for this skill (`customize-yak`) with the criterion that was missing.
