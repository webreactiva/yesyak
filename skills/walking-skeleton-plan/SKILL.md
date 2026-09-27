---
name: walking-skeleton-plan
description: Turns an approved spec into docs/SLUG-plan.md - step 1 is a walking skeleton (the main path working end to end with the minimum in each layer), and every later step adds exactly one capability, stays integrated, leaves no orphan code and says what can be tested when it is done. Use it whenever the user asks for an implementation plan, a roadmap, incremental steps, a walking skeleton, vertical slices, or "how would you build this", once a spec or clear requirements exist.
---

# Walking skeleton plan

## Principles

- **Step 1 is a walking skeleton.** It runs the main path of the spec end to end: for example "a customer places an order → it is stored → the order list shows it". Each layer has the minimum: data, logic, routes, views, CLI, tests. It stays in the codebase as the base.
- **One capability per step.** A step adds one thing: cancel an order, validation, edit, delete, a config option.
- **Always integrated.** At the end of every step the app starts, the main path works and the full test suite passes.
- **No orphan code.** Every function, table, dependency and template added in a step has a caller in that same step.
- **Testable.** Every step says what can be tested when it is done: automated tests and one manual check.

## Ordering

1. Walking skeleton first.
2. Next, anything that changes the shape of every later step. Example: the error format of the API before the first endpoints that return errors, so every later endpoint uses it from the start and tests are adapted once.
3. Then features, one per step.
4. Then hardening that does not change routes or forms: rate limits, cookie attributes, headers, configuration.
5. Styles and final documentation review last.

State the ordering decisions in the plan so the user can challenge them.

## Output

`docs/<slug>-plan.md`, in the document language of `simplified-technical-language`:

```markdown
# <Feature> Implementation Plan

| | |
| --- | --- |
| Spec | [<slug>-spec.md](<slug>-spec.md) |
| Branch | `feat/<slug>` |

## Overview           table: step | name | acceptance criteria covered
## Steps
### Step 1 - Walking skeleton
**Adds:** …
**Can be tested when done:** …
```

## Coverage check

Every acceptance criterion must appear in the overview at least once. Check it with a script, not by eye:

```bash
for i in $(seq -w 1 NN); do
  grep -q "AC-$i" <(sed -n '/^## Overview/,/^## Steps/p' docs/<slug>-plan.md) || echo "missing AC-$i"
done
```

Mark criteria that a step covers only partly, and name the step that completes them.

## Finish

Commit the plan (`git-commit-organizer`). In the chat, show the step list grouped by phase and the ordering decisions. Offer `work-items-breakdown` if the user tracks work in a tool. Ask before you start `execute-plan-loop`.
