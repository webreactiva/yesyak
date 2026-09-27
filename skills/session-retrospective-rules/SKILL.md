---
name: session-retrospective-rules
description: Reviews the current session for moments where the user had to correct the assistant or where it did something unexpected, and proposes for each one a guard in the first place that fits - a test, a command, a rule in AGENTS.md, a YesYak adjustment for this project, or the skill - without applying anything until the user approves; can also archive the session transcripts. Use it whenever the user asks for a retrospective, lessons learned, "where did I have to correct you", "how do we avoid this next time", or to capture the session's transcripts.
---

# Session retrospective rules

## 1. Find the moments

Read the whole session, not only the end. Look for three kinds of moments:

| Kind | Signals |
| --- | --- |
| The user corrected you | "no", "stop", "don't", a repeated instruction, a clarification after your action |
| You did something unexpected | An action the user did not ask for, a lost or damaged file, a wrong number or id in a question, a tool you opened without being asked |
| Others found your mistake | Findings from reviews, verification or tests that trace back to your own design or code |

Be honest. Include your own mistakes even if the user did not notice them.

## 2. Propose a guard for each moment

For each moment give:

- **What happened**, in two or three sentences, with the step or commit.
- **The guard**, in the best place: the first row of this table that fits. Say why the rows above it did not fit.

| Order | Place | Fits when |
| --- | --- | --- |
| 1 | 🧪 A test | The mistake shows in behavior that a test can check |
| 2 | ⌨️ A command or script | A check before a commit can catch it |
| 3 | 📏 AGENTS.md | It matters even when no skill is loaded, and it fits in one or two lines |
| 4 | An adjustment in `.agents/yesyak.json` | It changes how one skill works in this project only (`customize-yak`) |
| 5 | The skill | It improves the skill in every project |

Tests and commands come first because they do not depend on memory. A rule for AGENTS.md goes in the section where it belongs (for example "Git"), not in the YesYak block. An adjustment is written by `customize-yak`: propose the entry and let it write the file. Skills stay complete, because other projects may load them without this AGENTS.md.

Skills must not only grow. For every new rule in a skill, remove or merge one that is obsolete, duplicated or never used. Record the total size of the skills before and after (`wc -l .claude/skills/*/SKILL.md | tail -1`) in the retrospective.

## 3. Propose the plan, do not apply it

End with a short plan: which files change and in how many commits. Then stop and ask. The user decides what to apply.

In an unattended run (`unattended-run`), apply only the guards that the user allowed (for example, skill edits) and log the choice as a `Q-` entry. List the other guards in the pull request as proposals.

Save the answer to `.scratchpad/<slug>/retrospective.md` when the user asks, or at the end of the session.

## 4. Archive transcripts (on request)

Session transcripts are JSONL files under `~/.claude/projects/<project-folder>/`:

- The main session: `<session-id>.jsonl`.
- Its subagents: `<session-id>/subagents/agent-*.jsonl` with a `.meta.json` each.

A session can span more than one main file (for example after a clear or a resume). Identify the files that belong to this session by the first user prompt, the timestamps and the subagent team name. Exclude other sessions that ran in parallel on the same project, and tell the user about them.

Copy the files to `.scratchpad/<slug>/transcripts/` and write an `INDEX.md` with file, lines, size and a one-line description. Say that the main transcript is a snapshot if the session is still running.
