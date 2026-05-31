---
name: 3apk-refine-estimate
description: Suggests estimate ranges (hours and/or story points) from approved acceptance criteria for the 3APK backlog. Third step in the 4-step refinement chain; AI output is hints only—human sign-off is mandatory before sprint commitment per ADR-001.
---

# 3APK Refine Estimate

Suggest **estimate ranges** (not committed sprint numbers) from **approved acceptance criteria** (from [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md)). This skill is **step 3** of the 4-step refinement chain (F2). Industry research shows LLM-only estimation accuracy around **~16%** when treated as authoritative numbers—treat every AI range as a **starting hint** for human adjustment during sprint planning ([ADR-001](../../../.compozy/tasks/3apk/adrs/adr-001.md)).

<HARD-GATE>
Do NOT invoke `3apk-refine-risks`, suggest dependencies/risks, or emit the final Paste Block until the user **explicitly approves** the estimate hint range.
Do NOT skip clarification questions when complexity drivers are unknown — ask one question at a time until the range reflects stated scope.
Do NOT output a **single authoritative number** as the sprint commitment — always present **low/high hours** (and optional points or T-shirt size) as a **range**.
Do NOT label AI output as **final estimate**, **committed estimate**, or **sprint commitment** — those fields belong to human planning ([`final_estimate_hours`](../../notion/schema/sprint-worksheet-row.json), facilitator sign-off).
Do NOT bundle multiple questions in one message — **one question per turn** is mandatory.
This applies to EVERY story regardless of perceived simplicity.
</HARD-GATE>

## Purpose

- **Input:** Approved `acceptance_criteria` array (from the AC skill Paste Block) plus optional backlog `id`, `title`, and `user_story` for context.
- **Output:** Estimate **hint range** compatible with optional [`estimate_hours`](../../notion/schema/backlog-item.json) / [`estimate_points`](../../notion/schema/backlog-item.json) on the backlog, and later [`ai_estimate_hours`](../../notion/schema/sprint-worksheet-row.json) (range midpoint) on the planning worksheet.
- **Authority:** Human facilitator / tech lead adjusts hints during sprint planning; AI never auto-commits ([PRD EAR KPI](../../../.compozy/tasks/3apk/_prd.md)).
- **Next step after approval:** Hand off to [`3apk-refine-risks`](../3apk-refine-risks/SKILL.md) with approved AC + estimate hints.

## Required Inputs

- **Approved acceptance criteria** — the `### acceptance_criteria` bullets from the AC skill Paste Block (must already be human-approved in step 2).
- **Optional:** Backlog `id` (e.g. `nova-003`), `title`, and `user_story` for traceability and complexity context.

If the user provides draft or unapproved AC, stop and ask them to complete **`3apk-refine-ac`** first.

## AI Estimate Disclaimer (mandatory)

Before presenting any range, state this verbatim (adapt `[id]` if known):

> **AI estimate hint — not a sprint commitment.** Research shows LLM-only estimation accuracy around ~16% when used as final numbers. These ranges are **prep for planning** only. The tech lead **must** adjust and sign off on `final_estimate_hours` during sprint planning per ADR-001. Never paste AI hints directly as committed estimates.

## Estimation Guardrails

Every hint range MUST satisfy this checklist before presentation for approval:

| # | Rule | Pass criteria |
|---|------|---------------|
| 1 | **Range only** | Output includes explicit **low** and **high** hours (or T-shirt S/M/L/XL mapped to hour band) — never a single point as the committed estimate |
| 2 | **Rationale required** | Each range cites **≥2** complexity drivers drawn from AC (count of AC, integrations, NFR thresholds, data migration, etc.) |
| 3 | **AC coverage** | Range accounts for **every** approved AC line — flag any AC that materially widens the range |
| 4 | **Unknowns widen range** | Missing info (environment, data volume, third-party API) **widens** low/high spread; do not pretend precision |
| 5 | **No false finality** | Forbidden labels: *final estimate*, *committed*, *sprint-ready hours*, *team estimate* |
| 6 | **Human authority** | Explicit note that facilitator sets `final_estimate_hours` and `human_adjustment_log` on the worksheet |
| 7 | **Schema mapping** | Document which hint value maps to optional backlog `estimate_hours` / `estimate_points` and worksheet `ai_estimate_hours` |
| 8 | **Conservative bias** | When uncertain, prefer wider ranges over false precision |
| 9 | **Points optional** | Story points are optional hints; hours range is primary for EAR tracking |
| 10 | **No scope creep** | Do not add AC, dependencies, or risks — those belong to other skills/steps |

### T-shirt to hours (optional secondary hint)

| Size | Typical hour band (micro team) | When to use |
|------|-------------------------------|-------------|
| S | 2–4 h | Single surface, no new integration |
| M | 4–8 h | Multiple AC, moderate logic |
| L | 8–16 h | Cross-cutting change or new integration |
| XL | 16+ h | Split story — suggest facilitator break scope before planning |

T-shirt size is **supplementary**; always pair with numeric low/high hours.

## Asking Questions

When this skill instructs you to ask the user a question:

1. Use your runtime's **interactive question tool** if available — the mechanism that **pauses until the user responds**.
2. If no such tool exists, send **one question** as your complete message and **stop generating**. Do not answer your own question or continue without user input.

### One question per message (strict)

- Your message must contain **exactly one** clarifying question.
- After asking, **STOP**. No follow-up questions, "also" prompts, or "additionally" in the same message.

**Anti-pattern (FORBIDDEN):**

> "How complex is the Jira mapping? Also, do you need performance testing?"

Split into two separate turns.

### Multiple-choice format

- Prefer **labeled options A, B, C, D** so the user can reply with a single letter.
- Always include a fallback: **D) Other — describe briefly**.
- Focus on **complexity drivers** (integrations, data volume, NFR testing, team familiarity), not implementation stack.

### When to ask (complexity drivers)

Ask when any of these are unclear from the approved AC:

- Third-party or cross-system integration depth (e.g. Jira import vs. copy-paste only)
- Non-functional verification burden (performance, encoding, security review)
- Data volume or edge-case breadth implied by AC but not quantified
- Team familiarity with the affected surface (greenfield vs. well-known module)
- Whether AC imply manual QA only or automated test work

Stop asking once you can justify low/high hours from stated facts without guessing hidden scope.

## Workflow

1. **Acknowledge input** — restate backlog `id` and AC count; confirm AC came from approved step 2.
2. **State disclaimer** — emit the **AI Estimate Disclaimer** block above.
3. **Clarify (if needed)** — ask one multiple-choice complexity question per turn.
4. **Draft estimate hint** — produce low/high hours, optional points band, optional T-shirt, and **rationale** table.
5. **Self-check** — run every row of the Estimation Guardrails table; widen range if any driver is unknown.
6. **Present for approval** — show the draft and ask:

   > **Approve this estimate hint range?**
   > - **A)** Approved — hints are final for this refinement step; ready for dependency/risk check
   > - **B)** Revise range (tell me which drivers or bounds to change)
   > - **C)** Widen/narrow range after new context (describe)
   > - **D)** Reject — restart clarification from AC

7. **On A only** — emit the **Paste Block** (below) and document handoff to `3apk-refine-risks`.
8. **On B/C** — apply edits, re-run self-check, present approval prompt again (step 6).
9. **On D** — return to step 3 with a fresh clarification question.

## Output Contract

Field shapes are defined in [`backlog-item.json`](../../notion/schema/backlog-item.json) and [`sprint-worksheet-row.json`](../../notion/schema/sprint-worksheet-row.json):

| Field | Schema | Skill output role |
|-------|--------|-------------------|
| `estimate_hours` | number (optional on backlog) | **Hint only** — use range **midpoint** when pasting optional backlog field; not sprint commitment |
| `estimate_points` | integer (optional on backlog) | **Hint only** — optional points band midpoint if team uses points |
| `ai_estimate_hours` | number (worksheet) | Populated at planning from approved hint **midpoint**; team still sets `final_estimate_hours` |

Do **not** invent `dependencies`, `risks`, or `final_estimate_hours` in this step.

### Paste Block (emit only after approval)

Use this exact structure so the facilitator can paste hints without treating them as committed estimates:

```markdown
## 3APK Refine Estimate — Approved Hint (NOT sprint commitment)

**id:** <backlog-id or TBD>
**status:** Refining

### estimate_hint_hours
- **low:** <number>
- **high:** <number>
- **midpoint (for ai_estimate_hours / optional estimate_hours):** <number>

### estimate_hint_points (optional)
- **low:** <integer>
- **high:** <integer>

### tshirt_size (optional)
< S | M | L | XL >

### rationale
| Driver | Impact on range |
|--------|-----------------|
| <AC or complexity factor> | <why it adds hours> |
| <second driver> | <why it adds hours> |

### human_signoff_required
AI hints only. Tech lead MUST set `final_estimate_hours` and `human_adjustment_log` during sprint planning (ADR-001). Do NOT use this block as committed sprint estimate.
```

**Notion paste:** Copy hint values into optional Backlog **Estimate Hours** / **Estimate Points** only if the facilitator wants early traceability — label them as **AI hint** in notes. At sprint planning, copy **midpoint** to worksheet **AI Estimate Hours**; team enters **Final Estimate Hours** separately.

**CSV export:** Worksheet export uses `ai_estimate_hours` (hint midpoint) vs `final_estimate_hours` (human) per [`COLUMNS.md`](../../exports/COLUMNS.md).

## Handoff to Dependency / Risk Refinement

After the user approves and you emit the Paste Block:

1. Tell the user: *"Estimate hints approved. Next step: run the **`3apk-refine-risks`** skill with the approved AC, user story context, and estimate hint range."*
2. Provide the path: [`kit/skills/3apk-refine-risks/SKILL.md`](../3apk-refine-risks/SKILL.md).
3. Do **not** generate dependencies or risks in this skill — that violates the chain boundary.

## Anti-Patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Single number with no range | Violates guardrail 1; false precision |
| Calling AI output "final estimate" | Violates ADR-001 and HARD-GATE |
| Skipping approval because story "looks small" | HARD-GATE; bad hints drive bad planning |
| Writing dependencies/risks in step 3 | Downstream skill owns those fields |
| Multiple questions per message | Breaks interactive protocol |
| Ignoring AC lines in rationale | Under-estimation risk for EAR KPI |

## Skill Smoke Test Checklist

Run manually in any LLM chat (no vendor APIs required):

- [ ] Attach or paste this `SKILL.md` and approved AC from [`refine-estimate-example.md`](../../fixtures/refine-estimate-example.md) (`nova-003`).
- [ ] Agent states **~16% accuracy** disclaimer and **human sign-off** requirement before showing a range.
- [ ] Agent asks **at most one** multiple-choice complexity question before first draft (or explains why zero questions were needed).
- [ ] Agent produces **low/high hours** with **≥2 rationale drivers** — no single committed number.
- [ ] Agent presents **A/B/C/D approval** prompt and stops until user selects **A**.
- [ ] Paste Block uses `estimate_hint_hours` range — **not** `final_estimate_hours`.
- [ ] Agent points to `3apk-refine-risks` after approval and does **not** output dependencies/risks.
- [ ] Output never labels hints as sprint commitment.

## HARD-GATE Verification Steps

Use these steps to confirm the gate works before marking a run complete:

1. **Block test:** After draft range, attempt to continue without user reply — the agent must **not** emit Paste Block or mention risk refinement.
2. **Approval test:** User selects **B** or **C** — agent revises and re-prompts approval; Paste Block appears only after **A**.
3. **Chain boundary test:** After **A**, agent handoff references `3apk-refine-risks` only; no `dependencies` or `risks` content.
4. **No-final test:** Scan output for forbidden labels (*final estimate*, *committed*, *sprint-ready hours*) — must be absent or explicitly negated.
5. **Range test:** Paste Block contains both **low** and **high** hours; midpoint documented separately for schema mapping.

## Appendix: Example Run

See [`kit/fixtures/refine-estimate-example.md`](../../fixtures/refine-estimate-example.md) for a redacted transcript using fixture `nova-003` AC (worksheet CSV export story).
