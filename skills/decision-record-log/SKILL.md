---
name: decision-record-log
description: Convention for recording implementation decisions as ADRs (Architecture Decision Records) in docs/decisions/, each with a Type field that says whether the decision is Reversible or Irreversible, plus a README index that lists the decisions of each type. Use it whenever you make or change a design choice during implementation, when a review asks "why was this done", when the user mentions ADRs, decision logs, reversible or irreversible decisions, or asks you to "save each decision". Also use it to record decisions that were taken implicitly and never written down.
---

# Decision record log

If AGENTS.md sets a different convention for this topic, follow AGENTS.md.

## Where

```text
docs/decisions/
├── README.md                          simplified list per type
├── 0001-users-table-schema.md
├── 0002-money-stored-in-cents.md
└── 0003-payment-client-behind-an-interface.md
```

- One file per decision: `NNNN-short-title.md`, with a four-digit number that never repeats.
- All decisions live in the same folder. The type is a field, not a folder.
- If the repository already keeps decision records in another folder or format, use that one.
- When a merge brings clashing numbers, the older branch keeps its numbers. Renumber the other after the highest one and update every reference (`ADR NNNN`, `Superseded by NNNN`, links).

## Reversible or irreversible

| Type | Definition | Examples |
| --- | --- | --- |
| **Irreversible** | Undoing it needs a data migration, breaks stored data, or breaks a contract with users, clients or operators. | Table schema, stored data format, public API ids, an environment variable format, a marker in persisted data |
| **Reversible** | It lives only in code. Undoing it is a normal refactor, even if it has a one-time side effect. | Module layout, a library choice behind an interface, a middleware order, a log format |

Write the one-time side effect in the consequences.

## ADR format

```markdown
# NNNN Short title in sentence case

- **Date**: YYYY-MM-DD
- **Status**: Accepted | Accepted (amended by NNNN: what changed) | Superseded by NNNN | Deprecated
- **Type**: Reversible | Irreversible
- **Source**: plan step, review finding ID or user request

## Context

The problem and the forces. Include measurements when they drove the choice.

## Decision

What was chosen, in the imperative or the present tense. Name the files or settings.

## Consequences

- What becomes easier.
- What becomes harder, and the cost to undo it.
```

Keep each ADR short. Write it in the document language of `simplified-technical-language`.

## README index

Keep `docs/decisions/README.md` in this shape:

```markdown
# Decisions

Decisions of this repository. Numbers are unique across both lists.

## Irreversible

- [0001 Users table schema](0001-users-table-schema.md)
- [0002 Money stored as integer cents](0002-money-stored-in-cents.md)

## Reversible

- [0003 Payment client behind an interface](0003-payment-client-behind-an-interface.md)
```

Update the index in the same commit as the ADR.

## When to write one

- An irreversible decision (see the table above).
- A reversible choice only when a reviewer would really question it. Otherwise write one line in the spec or in the commit body.
- A deviation from the spec or the plan.
- A fix that changes a previous decision. Write a new ADR and keep both. If the new ADR replaces the whole decision, mark the old one `Superseded by NNNN`. If it changes only a part, mark it `Accepted (amended by NNNN: what changed)` and put `> Amended by NNNN.` under each paragraph that no longer holds.
- Implicit decisions that reviews uncover (for example no migration path, an id scheme, a default that someone turned off). Record them even if the answer is "accepted for now".

## Before you commit an ADR

- Compare the Type with the examples in the table above. An environment variable, a public URL or a stored format is Irreversible even when the code change is small.
- Every consequence must be true at the commit of the ADR and proven: run a mutation to show that a named test fails, or grep a named document. Do not write "the tests pin it" or "documented" without that proof, and do not cite files outside the repository, such as `.scratchpad/`.
