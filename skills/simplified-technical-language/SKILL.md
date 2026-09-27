---
name: simplified-technical-language
description: Entry convention for language and writing style. Load it at the start of any task that produces documents, specs, plans, reports, ADRs, pull requests, issue text or code comments, and whenever you are unsure which language to answer in. Deliverables go in English written in ASD-STE100 Simplified Technical English (STE); the conversation stays in the user's language, in Simplified Technical Spanish (ETS) when the user writes in Spanish. Other skills in this workflow depend on it, so apply it even when the user does not mention language or style.
---

# Simplified technical language

## Which language goes where

| Output | Language | Style |
| --- | --- | --- |
| Files in the repository: specs, plans, ADRs, README, AGENTS.md, code, commit messages | English | STE |
| Pull request descriptions, PR comments, issues, work items | English | STE |
| Messages to the user in the conversation | The user's language | STE in English, ETS in Spanish, the same principles in other languages |
| Working notes in `.scratchpad/` | The user's language | Same as the conversation |

Identifiers, commands, file paths, error messages and quoted UI text stay exactly as they are. Do not translate them.

## Style

Write English deliverables in ASD-STE100 Simplified Technical English. Write Spanish in the same spirit (ETS). The rules of the standard are not repeated here.

## Conversation style

- Answer in the user's language. If the user switches language, switch with them.
- Use emojis only when the user asks for them or already uses them in the request.

## Before you deliver

Read the text once as a reviewer who does not know the project:

- Does each sentence say one thing?
- Is every term used with one meaning only?
- Is there a sentence that only a person inside this session would understand? Rewrite it.
