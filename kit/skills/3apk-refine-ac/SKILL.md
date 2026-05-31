---
name: 3apk-refine-ac
description: Converts an approved user story into testable acceptance criteria for the 3APK backlog. Second step in the 4-step refinement chain; enforces human-in-the-loop approval before estimate refinement.
---

# 3APK Refine Acceptance Criteria

Convert an **approved user story** (from [`3apk-refine-story`](../3apk-refine-story/SKILL.md)) into **testable acceptance criteria** ready to paste into the Notion Backlog. This skill is **step 2** of the 4-step refinement chain (F2). Do not proceed to estimation until the user explicitly approves the AC list.

<HARD-GATE>
Do NOT invoke `3apk-refine-estimate`, suggest estimate ranges, or mark `testable_ac` as satisfied until the user **explicitly approves** the acceptance criteria list.
Do NOT skip clarification questions when the user story leaves success conditions ambiguous — ask one question at a time until AC can be written without guessing.
Do NOT output the final Paste Block until the user selects **Approved** on the approval prompt.
Do NOT bundle multiple questions in one message — **one question per turn** is mandatory.
Do NOT invent estimates, dependencies, or risks in this step — those belong to downstream skills.
This applies to EVERY user story regardless of perceived simplicity.
</HARD-GATE>

## Purpose

- **Input:** Approved `user_story` text (from the story skill Paste Block) plus optional backlog `id` and `title`.
- **Output:** `acceptance_criteria` array compatible with [`kit/notion/schema/backlog-item.json`](../../notion/schema/backlog-item.json).
- **DoR gate:** Approved AC enable the facilitator to check **`testable_ac`** on the DoR checklist ([`dor-checklist.json`](../../notion/schema/dor-checklist.json)).
- **Next step after approval:** Hand off to [`3apk-refine-estimate`](../3apk-refine-estimate/SKILL.md) with the approved AC list.

## Required Inputs

- **Approved user story** — the `### user_story` paragraph from the story skill Paste Block (must already be human-approved in step 1).
- **Optional:** Backlog item `id` (e.g. `nova-003`) and `title` for traceability in the output block.

If the user provides a draft or unapproved story, stop and ask them to complete **`3apk-refine-story`** first.

## AC Quality Rules

Every acceptance criterion MUST pass this checklist before presentation for approval:

| # | Rule | Pass criteria |
|---|------|---------------|
| 1 | **Testable** | A reviewer can verify pass/fail without reading the implementer's mind |
| 2 | **Observable** | Describes user-visible or system-measurable outcome (not internal refactor) |
| 3 | **No vague terms** | Forbidden without measurable bounds: *fast*, *quick*, *user-friendly*, *easy*, *robust*, *scalable*, *seamless*, *intuitive*, *performant* |
| 4 | **No implementation leakage** | No framework, library, or schema names unless the story explicitly requires them |
| 5 | **Single behavior** | One outcome per AC line — split compound sentences |
| 6 | **Story traceability** | Each AC maps to the stated user capability or benefit |
| 7 | **Given/When/Then preferred** | Use *Given … when … then …* or an unambiguous checklist bullet |
| 8 | **Minimum coverage** | Produce **≥3** AC items for typical stories (fewer only if user confirms narrow scope) |
| 9 | **Edge paths when implied** | Include error, empty, or permission-denied paths when the story implies them |
| 10 | **No duplicates** | No overlapping AC that test the same outcome twice |

### Vague-term rewrite examples

| Forbidden (vague) | Allowed (testable) |
|-------------------|-------------------|
| "Login is fast" | "Given valid credentials, when the user submits login, then the portal shows the dashboard within 3 seconds on a standard broadband connection" |
| "User-friendly export" | "Given DoR-passed stories, when I export CSV, then the file opens in Excel without encoding errors and lists all 13 columns from COLUMNS.md" |
| "System is robust" | "Given a webhook delivery fails, when the retry window opens, then the system retries up to 3 times before marking the invoice sync failed" |

## Asking Questions

When this skill instructs you to ask the user a question:

1. Use your runtime's **interactive question tool** if available — the mechanism that **pauses until the user responds**.
2. If no such tool exists, send **one question** as your complete message and **stop generating**. Do not answer your own question or continue without user input.

### One question per message (strict)

- Your message must contain **exactly one** clarifying question.
- After asking, **STOP**. No follow-up questions, "also" prompts, or "additionally" in the same message.

**Anti-pattern (FORBIDDEN):**

> "Should AC cover error cases? Also, do you need performance bounds?"

Split into two separate turns.

### Multiple-choice format

- Prefer **labeled options A, B, C, D** so the user can reply with a single letter.
- Always include a fallback: **D) Other — describe briefly**.
- Focus on **success boundaries** (in-scope behaviors, measurable thresholds, edge cases), not implementation.

### When to ask

Ask when any of these are unclear from the approved user story:

- Measurable success threshold (time, count, format, allowed error rate)
- In-scope vs out-of-scope behavior for this story
- Required edge or failure behavior (empty state, permission denied, retry)

Stop asking once you can draft ≥3 AC items that pass the quality checklist without guessing.

## Workflow

1. **Acknowledge input** — restate the user story in one sentence; note backlog `id` if provided.
2. **Clarify (if needed)** — ask one multiple-choice question per turn until success conditions are measurable.
3. **Draft acceptance criteria** — produce a numbered list of strings; each string is one AC line (schema: array of strings).
4. **Self-check** — run every row of the AC Quality Rules table; rewrite any failing line before showing the user.
5. **Present for approval** — show the draft list and ask:

   > **Approve these acceptance criteria?**
   > - **A)** Approved — output is final; ready for estimate refinement
   > - **B)** Revise specific AC items (tell me which numbers to change)
   > - **C)** Add or remove scope (tell me what to include/exclude)
   > - **D)** Reject — restart clarification from user story

6. **On A only** — emit the **Paste Block** (below) and document handoff to `3apk-refine-estimate`.
7. **On B/C** — apply edits, re-run self-check, present approval prompt again (step 5).
8. **On D** — return to step 2 with a fresh clarification question.

## Output Contract

Field shapes are defined in [`backlog-item.json`](../../notion/schema/backlog-item.json):

| Field | Schema | Skill output |
|-------|--------|--------------|
| `acceptance_criteria` | array of strings | Required in Paste Block — one AC per list item |
| `dor.testable_ac` | boolean (facilitator sets in Notion) | Facilitator may set `true` after pasting approved AC |

Do **not** invent `estimate_hours`, `estimate_points`, `dependencies`, or `risks` in this step.

### Paste Block (emit only after approval)

Use this exact structure so the facilitator can paste into Notion without renaming fields:

```markdown
## 3APK Refine AC — Approved Output

**id:** <backlog-id or TBD>
**status:** Refining

### acceptance_criteria
- Given <context>, when <action>, then <observable outcome>
- Given <context>, when <action>, then <observable outcome>
- Given <context>, when <action>, then <observable outcome>
```

**Notion paste:** Copy each bullet into the Backlog **Acceptance Criteria** field (multi-line text or bullet list). The field maps to the schema `acceptance_criteria` array — one string per line/bullet.

**CSV export:** When the worksheet is exported, AC lines are joined with newlines into the `acceptance_criteria` column per [`COLUMNS.md`](../../exports/COLUMNS.md).

### DoR `testable_ac` gate

After pasting approved AC, the facilitator checks **Testable AC** on the DoR checklist when:

- Every AC line is verifiable pass/fail (rules 1–2 above)
- No vague terms remain without measurable criteria (rule 3)
- ≥3 AC items cover the story scope (rule 8), unless the user explicitly approved fewer

See [`dor-checklist.json`](../../notion/schema/dor-checklist.json) — property `testable_ac`.

## Handoff to Estimate Refinement

After the user approves and you emit the Paste Block:

1. Tell the user: *"AC approved. Next step: run the **`3apk-refine-estimate`** skill with the approved `acceptance_criteria` (and same backlog `id`)."*
2. Provide the path: [`kit/skills/3apk-refine-estimate/SKILL.md`](../3apk-refine-estimate/SKILL.md).
3. Do **not** generate estimate hints in this skill — that violates the chain boundary.

## Anti-Patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Skipping approval because AC "look obvious" | HARD-GATE; bad AC drive bad estimates |
| Writing estimates or dependencies in step 2 | Downstream skills + DoR gates own those fields |
| Technical AC ("use Redis cache") | Implementation leakage unless story requires it |
| Multiple questions per message | Breaks interactive protocol and facilitator timing |
| Single vague AC ("works correctly") | Fails `testable_ac` DoR gate |

## Skill Smoke Test Checklist

Run manually in any LLM chat (no vendor APIs required):

- [ ] Attach or paste this `SKILL.md` and the DoR_Pass fixture `user_story` from [`refine-ac-example.md`](../../fixtures/refine-ac-example.md) (`nova-003`).
- [ ] Agent asks **at most one** multiple-choice question before first draft (or explains why zero questions were needed).
- [ ] Agent produces **≥3** testable AC items passing the quality checklist.
- [ ] Agent presents **A/B/C/D approval** prompt and stops until user selects **A**.
- [ ] Paste Block uses `acceptance_criteria` bullets — no renamed fields.
- [ ] Agent points to `3apk-refine-estimate` after approval and does **not** output estimates.
- [ ] Approved AC would enable facilitator to set DoR **`testable_ac: true`**.

## HARD-GATE Verification Steps

Use these steps to confirm the gate works before marking a run complete:

1. **Block test:** After draft AC, attempt to continue without user reply — the agent must **not** emit Paste Block or mention estimate refinement.
2. **Approval test:** User selects **B** or **C** — agent revises and re-prompts approval; Paste Block appears only after **A**.
3. **Chain boundary test:** After **A**, agent handoff references `3apk-refine-estimate` only; no `estimate_hours` or range content.
4. **Question discipline test:** Send a deliberately ambiguous user story — verify each agent message contains a single question with A/B/C/D options.
5. **Quality test:** Draft AC must not contain vague terms from rule 3 without measurable rewrite.

## Appendix: Example Run

See [`kit/fixtures/refine-ac-example.md`](../../fixtures/refine-ac-example.md) for a redacted transcript using fixture `nova-003` (DoR_Pass worksheet export story).
