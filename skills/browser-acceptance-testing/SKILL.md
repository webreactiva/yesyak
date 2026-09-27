---
name: browser-acceptance-testing
description: Tests acceptance criteria and edge cases as an end user in a real browser with the Chrome DevTools MCP, then writes a report with findings. Use it only when the user explicitly asks for browser testing, end-user testing, manual QA, "test it like a user", UI validation, or testing with Chrome DevTools. Do not open a browser on your own initiative for other tasks.
---

# Browser acceptance testing

The user decides when a browser opens. If they asked for this skill, go ahead. If a browser tool fails, do not switch to another browser tool without asking.

## Setup

1. Start the app with a scratch database and a dedicated port (`.scratchpad/<slug>/manual-env.sh`). Create test users there; keep credentials in the helper, not in chat messages.
2. Choose the browser tool. Prefer the Chrome DevTools MCP: load the tools you need in one search (navigate, snapshot, screenshot, click, fill, fill form, evaluate script, console messages, network requests, emulate, resize). If the environment has no DevTools MCP but has Playwright and a browser (common in containers and cloud sessions), write one script in `.scratchpad/<slug>/scripts/` that drives the same checks. Record console messages, network status codes and screenshots in `.scratchpad/<slug>/shots/`. This is the tool choice, not a switch after a failure.
3. Look at a few screenshots yourself (desktop, 375 px, one error page). Layout problems such as wrong plurals, missing headings or cut text show there and not in status codes.
4. Keep notes in `.scratchpad/<slug>/browser-test-notes.md` while you test.

## Test the criteria as a user

Walk through the acceptance criteria in the order a user meets them (for example: first visit, sign-in, lists, create, edit, delete). For each check:

- Use the UI like a person: fill the form, click the button. Use scripts only to read state or to type very long input.
- Confirm status codes in the network panel, not only what the page shows.
- Confirm data through the public API when the criterion talks about it.

## Edge cases to try

| Area | Cases |
| --- | --- |
| Input | Only spaces, maximum length and one over, emoji at the limit, a very long word without spaces, HTML and script in every field, quotes in attribute values |
| Navigation | Back button after delete and after sign-out, reload after a failed form, direct URLs to unknown or odd ids (`9999`, `1.5`, `abc`) |
| Timing | Double click on submit, a form left open in one tab while the session changes in another |
| Session | Cookie flags visible to scripts, server restart with the same and a different secret |
| Layout | Desktop and a 375 px mobile viewport; horizontal overflow; hidden actions; dark color scheme if the CSS has one; keyboard focus order |
| Console | CSP violations and script errors after every page |

Never trigger `alert`, `confirm` or `prompt`: they block the browser tools. Use `console.log` to prove script execution. A page with a strict CSP blocks `fetch` from an evaluated script; drive its forms instead.

## Report

Write `.scratchpad/<slug>/browser-test-report.md`:

```markdown
# End-user test report (browser)

## Summary                criteria passed in the browser, not testable in a browser, failed; findings by light
## Criteria tested        AC | What the user did | Result
## Not testable in a browser (and where they were verified)
## Edge cases             case | result
## Findings               H1, H2… with traffic lights (traffic-light-findings)
## Final state            servers stopped, test data left
```

Stop the server and close extra tabs before you report.
