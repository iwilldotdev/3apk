---
name: 3apk-refine-story
description: Transforms a raw stakeholder request into an approved user story for the 3APK backlog. First step in the 4-step refinement chain; enforces human-in-the-loop approval before acceptance-criteria refinement.
---

# 3APK Refine Story

Transform a **raw stakeholder request** into a well-formed **user story** ready to paste into the Notion Backlog. This skill is **step 1** of the 4-step refinement chain (F2). Do not proceed to acceptance criteria until the user explicitly approves the story.

<HARD-GATE>
Do NOT invoke `3apk-refine-ac`, suggest AC refinement, or mark the story as DoR-ready until the user **explicitly approves** the generated user story.
Do NOT skip clarification questions when the raw request is ambiguous — ask one question at a time until scope is clear enough to draft.
Do NOT output the final paste block until the user selects **Approved** on the approval prompt.
Do NOT bundle multiple questions in one message — **one question per turn** is mandatory.
This applies to EVERY raw request regardless of perceived simplicity.
</HARD-GATE>

## Purpose

- **Input:** `raw_request` text (and optional backlog `id` / context from the facilitator).
- **Output:** `title` and `user_story` fields compatible with [`kit/notion/schema/backlog-item.json`](../../notion/schema/backlog-item.json).
- **Next step after approval:** Hand off to [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md) with the approved `user_story`.

## Required Inputs

- **Raw request** — verbatim stakeholder text (e.g. from Notion Backlog `raw_request` or a chat paste).
- **Optional:** Backlog item `id` (e.g. `nova-001`) for traceability in the output block.

If the user provides only a vague one-liner, run the clarification protocol before drafting.

## Asking Questions

When this skill instructs you to ask the user a question:

1. Use your runtime's **interactive question tool** if available — the mechanism that **pauses until the user responds**.
2. If no such tool exists, send **one question** as your complete message and **stop generating**. Do not answer your own question or continue without user input.

### One question per message (strict)

- Your message must contain **exactly one** clarifying question.
- After asking, **STOP**. No follow-up questions, "also" prompts, or "additionally" in the same message.

**Anti-pattern (FORBIDDEN):**

> "Who is the primary actor? Also, what is the success outcome?"

Split into two separate turns.

### Multiple-choice format

- Prefer **labeled options A, B, C, D** so the user can reply with a single letter.
- Always include a fallback: **D) Other — describe briefly**.
- Keep options mutually exclusive and business-focused (WHO / WHAT outcome / scope), not implementation (no frameworks, APIs, or schema design).

### When to ask

Ask when any of these are unclear from the raw request:

- Primary user persona or actor
- Desired outcome vs. nice-to-have scope
- Success boundary (in-scope vs. out-of-scope for this story)

Stop asking once you can draft a testable "As a … I want … so that …" without guessing.

## Workflow

1. **Acknowledge input** — restate the raw request in one sentence; note backlog `id` if provided.
2. **Clarify (if needed)** — ask one multiple-choice question per turn until actor and outcome are clear.
3. **Draft user story** — produce:
   - `title` — short, imperative, ≤80 characters where possible (matches schema `title`).
   - `user_story` — single paragraph in classic format: *As a [role], I want [capability] so that [benefit].*
4. **Present for approval** — show the draft and ask:

   > **Approve this user story?**
   > - **A)** Approved — output is final; ready for AC refinement
   > - **B)** Revise title only (tell me what to change)
   > - **C)** Revise user story only (tell me what to change)
   > - **D)** Reject — restart clarification from raw request

5. **On A only** — emit the **Paste Block** (below) and document handoff to `3apk-refine-ac`.
6. **On B/C** — apply edits, present approval prompt again (step 4).
7. **On D** — return to step 2 with a fresh clarification question.

## Output Contract

Field shapes are defined in [`backlog-item.json`](../../notion/schema/backlog-item.json):

| Field | Schema | Skill output |
|-------|--------|--------------|
| `title` | string, short human-readable title | Required in Paste Block |
| `user_story` | string, "As a … I want … so that …" | Required in Paste Block |
| `raw_request` | string | Preserve original in Paste Block for Notion paste |
| `status` | enum | Suggest `Refining` after approval (facilitator updates Notion) |

Do **not** invent `acceptance_criteria`, estimates, `dependencies`, or `risks` in this step — those belong to later skills.

### Paste Block (emit only after approval)

Use this exact structure so the facilitator can paste into Notion without renaming fields:

```markdown
## 3APK Refine Story — Approved Output

**id:** <backlog-id or TBD>
**status:** Refining

### title
<short title>

### raw_request
<verbatim original request>

### user_story
As a <role>, I want <capability> so that <benefit>.
```

## Handoff to Acceptance Criteria

After the user approves and you emit the Paste Block:

1. Tell the user: *"Story approved. Next step: run the **`3apk-refine-ac`** skill with the approved `user_story` (and same backlog `id`)."*
2. Provide the path: [`kit/skills/3apk-refine-ac/SKILL.md`](../3apk-refine-ac/SKILL.md).
3. Do **not** generate acceptance criteria in this skill — that violates the chain boundary and DoR sequencing.

## Anti-Patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Skipping approval because the request "looks simple" | HARD-GATE; rework cost is highest on vague stories |
| Writing AC or estimates in step 1 | Downstream skills + DoR gates own those fields |
| Technical clarification ("OAuth library?") | Stay on user need and outcome |
| Multiple questions per message | Breaks interactive protocol and facilitator timing |

## Skill Smoke Test Checklist

Run manually in any LLM chat (no vendor APIs required):

- [ ] Attach or paste this `SKILL.md` and a Draft fixture `raw_request` (see [`refine-story-example.md`](../../fixtures/refine-story-example.md)).
- [ ] Agent asks **at most one** multiple-choice question before first draft (or explains why zero questions were needed).
- [ ] Agent presents **A/B/C/D approval** prompt and stops until user selects **A**.
- [ ] Paste Block uses `title`, `raw_request`, `user_story` labels — no renamed fields.
- [ ] Agent points to `3apk-refine-ac` after approval and does **not** output AC.
- [ ] User story matches "As a … I want … so that …" and is paste-ready into Notion Backlog `user_story`.

## HARD-GATE Verification Steps

Use these steps to confirm the gate works before marking a run complete:

1. **Block test:** After draft, attempt to continue without user reply — the agent must **not** emit Paste Block or mention AC refinement.
2. **Approval test:** User selects **B** or **C** — agent revises and re-prompts approval; Paste Block appears only after **A**.
3. **Chain boundary test:** After **A**, agent handoff references `3apk-refine-ac` only; no `acceptance_criteria` content.
4. **Question discipline test:** Send a deliberately ambiguous raw request — verify each agent message contains a single question with A/B/C/D options.

## Appendix: Example Run

See [`kit/fixtures/refine-story-example.md`](../../fixtures/refine-story-example.md) for a redacted transcript using fixture `nova-001` (Draft OAuth request).
