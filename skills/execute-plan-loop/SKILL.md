---
name: execute-plan-loop
description: Implements a plan step by step in a loop until the end - one capability per step, tests and a manual check for each, decision records, docs kept in sync, atomic commits and a progress file that allows a resume after any interruption. Also applies a triaged change list by item id. Use it whenever the user asks to implement the plan, "run the loop", continue from a step, resume after a break, or apply a numbered list of changes or review fixes.
---

# Execute plan loop

Load and follow these conventions during the whole loop: `git-commit-organizer`, `no-slop-code`, `decision-record-log`, `scratchpad-working-files`, `simplified-technical-language`.

## Before the first step

1. Read the plan and the spec. Read `.scratchpad/<slug>/progress.md` if it exists and continue from the first step that is not done.
2. Run the full test suite and record the baseline (number of tests, all passing).
3. Prepare the smallest way to run the change by hand, isolated from real data (for example a server on its own port with a scratch database, or a CLI call on a scratch folder). Put its start and stop commands in `.scratchpad/<slug>/manual-env.sh`.

## For each step

1. **Implement the minimum** that the step describes. Nothing from later steps.
2. **Test.** Add or update tests for the criteria of the step. For fixes, check that the new test fails without the fix, then passes with it.
3. **Run the full check** of the project (for example types, lint and all tests).
4. **Manual check.** Do the check that the plan lists, in the manual environment. Stop everything you started.
5. **Record and commit.** Write the ADRs that `decision-record-log` asks for (if the project switched it off, the reason goes in the commit body), sync the docs the change affects, and commit as `git-commit-organizer` says.
6. **Update `progress.md`** with the status and the commit hashes. Do not start the next step before `progress.md` shows the commit of this one.

Keep the output of each step short in the chat: what was added, test count, manual check result, commit hash.

## When reality differs from the plan

- If a library does not work as the plan assumed, choose the smallest change that keeps the spec true, record it in an ADR and say it in the step summary.
- If the spec itself looks wrong or a step cannot stay integrated, stop and ask. Do not silently change the behavior the user approved.
- Do not open a browser for checks unless the user asked for browser testing. Use the test client, direct calls or static checks, and say what stays unverified.

## Change-list mode

When the input is a numbered change list (from `triage-findings-list`) instead of a plan:

- Treat each item id as a step, in the order the user approved.
- Use the item id in the commit body or the ADR source field. When two items change the same code, fix them in one commit and name both ids.
- Reproduce the problem before you fix it, and keep the reproduction as a test.
- Update the change list with the status of each item.

## At the end

Write `.scratchpad/<slug>/progress.md` in its final state and give a report: steps done, commits, tests before and after, decisions recorded, anything left or skipped and why.

If the session stops before the end, say what is done, what is left and which step to resume from.
