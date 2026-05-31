---
name: 3apk-refine-risks
description: Surfaces dependencies and risks for a story with approved AC and estimate hints, then produces a paste-ready Notion backlog entry with DoR self-assessment. Fourth and final step in the 4-step refinement chain (F2).
---

# 3APK Refine Dependencies & Risks

Surface **dependencies** and **risks** for a story that already has **approved user story**, **acceptance criteria**, and **estimate hints** (from upstream refinement skills). Run **DoR self-assessment** against the four gates in [`dor-checklist.json`](../../notion/schema/dor-checklist.json). This skill is **step 4** of the 4-step refinement chain (F2) and produces a **paste-ready backlog entry** eligible for Notion DoR evaluation (PRD F3).

<HARD-GATE>
Do NOT emit the final **Notion Paste Block**, mark the story **DoR_Pass**, or instruct the facilitator to paste into Notion until the user **explicitly approves** the dependencies list, risks list, and DoR self-assessment.
Do NOT skip clarification questions when dependency scope or NFR impact is unknown — ask one question at a time until arrays are complete.
Do NOT bundle multiple questions in one message — **one question per turn** is mandatory.
Do NOT invent new user story text, AC lines, or committed sprint estimates — those belong to upstream skills.
Do NOT set `passed: true` in the DoR self-assessment unless all four gates are honestly satisfied; if any gate fails, output `status: DoR_Fail` guidance.
This applies to EVERY story regardless of perceived simplicity.
</HARD-GATE>

## Purpose

- **Input:** Combined refinement outputs — approved `user_story`, `acceptance_criteria`, and estimate hint range (from [`3apk-refine-story`](../3apk-refine-story/SKILL.md), [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md), [`3apk-refine-estimate`](../3apk-refine-estimate/SKILL.md) Paste Blocks).
- **Output:** `dependencies` and `risks` arrays plus DoR self-assessment compatible with [`backlog-item.json`](../../notion/schema/backlog-item.json).
- **DoR gates:** Enables facilitator evaluation of **`dependencies_surfaced`** and **`nfr_flags_set`**, and confirms upstream **`problem_clear`** and **`testable_ac`** readiness.
- **Next step after approval:** Paste into Notion Backlog; set status to **`Refining`** during paste, then **`DoR_Pass`** or **`DoR_Fail`** per gate results. Sprint planning uses [`3apk-plan-sprint`](../3apk-plan-sprint/SKILL.md) only after **`DoR_Pass`**.

## Required Inputs

Collect from upstream Paste Blocks (all must be **human-approved**):

| Input | Source skill | Required |
|-------|--------------|----------|
| `id`, `title`, `user_story` | `3apk-refine-story` | yes |
| `acceptance_criteria` | `3apk-refine-ac` | yes |
| `estimate_hint_hours` (low/high/midpoint) | `3apk-refine-estimate` | yes |
| `raw_request` | facilitator / Notion Backlog | optional (recommended for `problem_clear`) |

If any upstream output is draft or unapproved, stop and ask the facilitator to complete the missing skill first.

## Dependency & Risk Quality Rules

Every dependency and risk line MUST pass this checklist before presentation for approval:

| # | Rule | Pass criteria |
|---|------|---------------|
| 1 | **Specific** | Names a backlog id/title, external system, team, or artifact — not "unknown stuff" |
| 2 | **Actionable** | A facilitator can verify blocked/unblocked state or mitigation |
| 3 | **Story-linked** | Tied to AC, estimate drivers, or integration touchpoints from inputs |
| 4 | **No duplicates** | Same dependency or risk not repeated under different wording |
| 5 | **Empty is valid** | Use `[]` when genuinely none — do not invent filler |
| 6 | **Risk ≠ AC** | Risks are unknowns/threats; AC are success conditions |
| 7 | **Dependency ≠ risk** | Dependencies are prerequisites; risks are what could go wrong |
| 8 | **NFR cross-check** | Performance/security/accessibility concerns appear in risks or explicit NFR notes |

### Dependency vs risk examples

| Type | Good example | Bad example |
|------|--------------|-------------|
| Dependency | `nova-001` OAuth provider (portal login prerequisite) | "Needs backend" |
| Dependency | `kit/exports/COLUMNS.md` frozen before export AC verification | "Documentation" |
| Risk | UTF-8 encoding edge cases on Windows Excel when opening CSV | "Might be hard" |
| Risk | Jira import field mapping differs between cloud vs server | "Integration issues" |

## NFR Flag Prompts (DoR gate 4)

Evaluate **performance**, **security**, and **accessibility** for every story. Ask one multiple-choice NFR question per turn when impact is unclear from AC.

### Performance

Ask when AC imply latency, throughput, data volume, or export/import size:

> **Does this story need explicit performance bounds beyond what AC already state?**
> - **A)** No — AC already include measurable thresholds
> - **B)** Yes — add performance risk flag (describe bottleneck)
> - **C)** Unknown — treat as risk until clarified
> - **D)** Other — describe briefly

### Security

Ask when story touches auth, PII, webhooks, external APIs, or file export:

> **Does this story introduce or change a security-sensitive surface?**
> - **A)** No security-sensitive change
> - **B)** Yes — auth/secrets/PII (describe scope)
> - **C)** Yes — external integration trust boundary (describe)
> - **D)** Other — describe briefly

### Accessibility

Ask when story adds or changes user-facing UI, export formats read by humans, or error messaging:

> **Does this story need accessibility evaluation?**
> - **A)** No user-facing UI change
> - **B)** Yes — UI/export must meet team a11y standard (describe)
> - **C)** Defer — document as risk if standard unknown
> - **D)** Other — describe briefly

Record NFR evaluation in the **`nfr_flags_set`** gate rationale. Set gate **true** when all three areas are explicitly evaluated (even if answer is "not applicable").

## Asking Questions

When this skill instructs you to ask the user a question:

1. Use your runtime's **interactive question tool** if available — the mechanism that **pauses until the user responds**.
2. If no such tool exists, send **one question** as your complete message and **stop generating**. Do not answer your own question or continue without user input.

### One question per message (strict)

- Your message must contain **exactly one** clarifying question.
- After asking, **STOP**. No follow-up questions, "also" prompts, or "additionally" in the same message.

**Anti-pattern (FORBIDDEN):**

> "Any dependencies on other stories? Also, what about Excel encoding risks?"

Split into two separate turns.

### Multiple-choice format

- Prefer **labeled options A, B, C, D** so the user can reply with a single letter.
- Always include a fallback: **D) Other — describe briefly**.
- Focus on **blockers**, **external systems**, **NFR impact**, and **verification unknowns**.

### When to ask (dependency / risk drivers)

Ask when any of these are unclear from approved inputs:

- Other backlog items or teams that must complete first
- External systems, credentials, or environment prerequisites
- Data format, encoding, or cross-platform compatibility unknowns
- NFR impact (performance, security, accessibility) not covered by AC

Stop asking once you can draft complete `dependencies` and `risks` arrays without guessing hidden blockers.

## Workflow

1. **Acknowledge input** — restate backlog `id`, AC count, and estimate hint range; confirm all upstream steps were approved.
2. **Clarify dependencies (if needed)** — one multiple-choice question per turn about blockers or prerequisites.
3. **Clarify risks (if needed)** — one multiple-choice question per turn about unknowns or failure modes.
4. **Run NFR prompts** — evaluate performance, security, accessibility (one question per turn when unclear).
5. **Draft arrays** — produce `dependencies` and `risks` string arrays per schema.
6. **Draft DoR self-assessment** — evaluate all four gates with boolean + one-line rationale each.
7. **Self-check** — run every row of the Dependency & Risk Quality Rules table.
8. **Present for approval** — show draft arrays, NFR summary, and DoR table; ask:

   > **Approve dependencies, risks, and DoR self-assessment?**
   > - **A)** Approved — ready for Notion paste block
   > - **B)** Revise dependencies (tell me what to add/remove)
   > - **C)** Revise risks or NFR flags (tell me what to change)
   > - **D)** Reject — restart clarification from inputs

9. **On A only** — emit the **Notion Paste Block** (below) with status transition guidance.
10. **On B/C** — apply edits, re-run self-check, present approval prompt again (step 8).
11. **On D** — return to step 2 with a fresh clarification question.

## Output Contract

Field shapes are defined in [`backlog-item.json`](../../notion/schema/backlog-item.json) and [`dor-checklist.json`](../../notion/schema/dor-checklist.json):

| Field | Schema | Skill output |
|-------|--------|--------------|
| `dependencies` | array of strings | Required in Paste Block — backlog ids/titles or external prerequisites |
| `risks` | array of strings | Required in Paste Block — unknowns, threats, mitigations-needed |
| `dor.problem_clear` | boolean | Self-assessment gate 1 |
| `dor.testable_ac` | boolean | Self-assessment gate 2 (confirm upstream AC quality) |
| `dor.dependencies_surfaced` | boolean | Self-assessment gate 3 — true when dependencies array is complete |
| `dor.nfr_flags_set` | boolean | Self-assessment gate 4 — true after performance/security/a11y evaluation |
| `dor.passed` | boolean | `true` only when all four gates are `true` |
| `status` | enum | `Refining` during paste; facilitator sets `DoR_Pass` or `DoR_Fail` after checkbox sync |

Do **not** invent `final_estimate_hours` or sprint commitment fields — those belong to planning.

### DoR Self-Assessment Output Template

Use this structure inside the Paste Block (emit only after approval):

```markdown
### dor_self_assessment
| Gate | Schema field | Result | Rationale |
|------|--------------|--------|-----------|
| 1 — Problem clear | `problem_clear` | true / false | <one line> |
| 2 — Testable AC | `testable_ac` | true / false | <one line> |
| 3 — Dependencies surfaced | `dependencies_surfaced` | true / false | <one line> |
| 4 — NFR flags set | `nfr_flags_set` | true / false | <performance / security / a11y summary> |

**Aggregate:** `passed` = true ONLY if all four gates are true.
**Recommended status after paste:** DoR_Pass | DoR_Fail
```

### Notion Paste Block (emit only after approval)

```markdown
## 3APK Refine Risks — Approved Backlog Entry (paste-ready)

**id:** <backlog-id>
**title:** <from story skill>
**status:** Refining

### raw_request
<optional original request>

### user_story
<approved paragraph>

### acceptance_criteria
- <AC line 1>
- <AC line 2>
- <AC line 3>

### estimate_hours
<optional midpoint hint from estimate skill — label as AI hint in Notion notes>

### estimate_points
<optional if provided upstream>

### dependencies
- <dependency 1 or leave section empty with [] noted>
- <dependency 2>

### risks
- <risk 1>
- <risk 2>

### dor_self_assessment
| Gate | Schema field | Result | Rationale |
|------|--------------|--------|-----------|
| 1 — Problem clear | `problem_clear` | true / false | … |
| 2 — Testable AC | `testable_ac` | true / false | … |
| 3 — Dependencies surfaced | `dependencies_surfaced` | true / false | … |
| 4 — NFR flags set | `nfr_flags_set` | true / false | … |

**passed:** true / false
**recommended_status:** DoR_Pass | DoR_Fail
```

### Notion Paste Field Mapping

| Paste Block section | Notion Backlog property | Schema field | Notes |
|---------------------|-------------------------|--------------|-------|
| `id` | ID (or custom id text) | `id` | Match fixture prefix convention (`nova-*`) |
| `title` | Title | `title` | From story skill |
| `raw_request` | Raw Request | `raw_request` | Optional; helps gate 1 |
| `user_story` | User Story | `user_story` | Multi-line text |
| `acceptance_criteria` bullets | Acceptance Criteria | `acceptance_criteria` | One string per bullet |
| `estimate_hours` | Estimate Hours | `estimate_hours` | Optional AI hint — not sprint commitment |
| `estimate_points` | Estimate Points | `estimate_points` | Optional hint |
| `dependencies` bullets | Dependencies | `dependencies` | One prerequisite per line |
| `risks` bullets | Risks | `risks` | One risk per line |
| DoR gate 1 result | Problem Clear | `dor.problem_clear` | Checkbox |
| DoR gate 2 result | Testable AC | `dor.testable_ac` | Checkbox |
| DoR gate 3 result | Dependencies Surfaced | `dor.dependencies_surfaced` | Checkbox |
| DoR gate 4 result | NFR Flags Set | `dor.nfr_flags_set` | Checkbox |
| Aggregate | Passed | `dor.passed` | Checkbox — all four must be checked |
| `recommended_status` | Status | `status` | Set `DoR_Pass` or `DoR_Fail` after checkboxes |

See [`kit/notion/SPEC.md`](../../notion/SPEC.md) §1 for property types and DoR gate implementation.

### Status Transition After Paste

1. Create or update Backlog row with **`status: Refining`** while pasting refinement outputs.
2. Sync the four DoR checkboxes from the self-assessment table.
3. If **`passed`** is true → set **`status: DoR_Pass`** and check **`passed`**.
4. If any gate is false → set **`status: DoR_Fail`**, leave **`passed`** unchecked, and return to the failing upstream skill.
5. Only **`DoR_Pass`** items may enter the Planning Worksheet **Sprint Candidates** view ([`3apk-plan-sprint`](../3apk-plan-sprint/SKILL.md)).

## Four-Skill Refinement Chain Summary

| Step | Skill | Input → Output | DoR gates touched |
|------|-------|----------------|-------------------|
| 1 | [`3apk-refine-story`](../3apk-refine-story/SKILL.md) | Raw request → `title`, `user_story` | `problem_clear` (facilitator) |
| 2 | [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md) | User story → `acceptance_criteria` | `testable_ac` |
| 3 | [`3apk-refine-estimate`](../3apk-refine-estimate/SKILL.md) | AC → estimate hint range | — (hints only; ADR-001) |
| 4 | **`3apk-refine-risks`** (this skill) | Story + AC + hints → `dependencies`, `risks`, DoR assessment | `dependencies_surfaced`, `nfr_flags_set`, aggregate `passed` |

**Chain rule:** Each step requires explicit human approval before the next skill runs. This skill completes F2 refinement; F3 DoR gate is enforced in Notion via checkboxes and status.

## Handoff to Sprint Planning

After the user approves and the facilitator pastes into Notion:

1. If **`DoR_Pass`** — tell the user: *"Backlog entry ready. Next: run **`3apk-plan-sprint`** with DoR-passed items and sprint capacity."*
2. Provide the path: [`kit/skills/3apk-plan-sprint/SKILL.md`](../3apk-plan-sprint/SKILL.md).
3. If **`DoR_Fail`** — name the failing gate(s) and point to the upstream skill or clarification needed; do **not** suggest sprint planning.

## Anti-Patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Pasting to Notion before approval | HARD-GATE violation |
| Marking `passed: true` with a false gate | Breaks worksheet filter and DoR KPI |
| Inventing dependencies "just in case" | Violates quality rule 5; erodes trust |
| Skipping NFR prompts because "backend only" | Fails `nfr_flags_set` gate |
| Multiple questions per message | Breaks interactive protocol |
| Rewriting AC or estimates in step 4 | Upstream skills own those fields |

## End-to-End Chain Test Procedure (Steps 04→07)

Run manually in any LLM chat to validate the full refinement chain:

1. **Fixture:** Use `nova-003` raw request from [`sample-backlog-items.json`](../../fixtures/sample-backlog-items.json): *"We need to push sprint plans into Jira without copy-paste hell"*.
2. **Step 04 — Story:** Run [`3apk-refine-story`](../3apk-refine-story/SKILL.md); approve user story. See [`refine-story-example.md`](../../fixtures/refine-story-example.md).
3. **Step 05 — AC:** Run [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md) with approved story; approve ≥3 testable AC. See [`refine-ac-example.md`](../../fixtures/refine-ac-example.md).
4. **Step 06 — Estimate:** Run [`3apk-refine-estimate`](../3apk-refine-estimate/SKILL.md) with approved AC; approve hint range. See [`refine-estimate-example.md`](../../fixtures/refine-estimate-example.md).
5. **Step 07 — Risks (this skill):** Run with combined Paste Blocks; approve dependencies, risks, and DoR assessment. See [`refine-risks-example.md`](../../fixtures/refine-risks-example.md).
6. **Validate shape:** Extract JSON from the example fixture and validate against [`backlog-item.json`](../../notion/schema/backlog-item.json) (automated in `test_skill.py`).
7. **DoR_Pass path:** All four gates true → `passed: true`, `status: DoR_Pass` — matches fixture `nova-003`.
8. **DoR_Fail path:** Re-run chain on fixture `nova-002` (single vague AC) → `testable_ac: false`, `passed: false`, `status: DoR_Fail`.
9. **Worksheet block test:** Confirm `DoR_Fail` item would not appear in Planning Worksheet Sprint Candidates view per SPEC §3.3.

## Skill Smoke Test Checklist

- [ ] Attach this `SKILL.md` and combined inputs from [`refine-risks-example.md`](../../fixtures/refine-risks-example.md) (`nova-003`).
- [ ] Agent asks **at most one** multiple-choice question per turn before first draft (or explains why zero were needed).
- [ ] Agent produces `dependencies` and `risks` arrays — schema-shaped strings.
- [ ] Agent runs **performance / security / accessibility** NFR evaluation.
- [ ] DoR self-assessment table covers **`problem_clear`**, **`testable_ac`**, **`dependencies_surfaced`**, **`nfr_flags_set`**.
- [ ] Agent presents **A/B/C/D approval** prompt and stops until user selects **A**.
- [ ] **Notion Paste Block** appears only after **A** — includes field mapping alignment.
- [ ] Agent recommends **`DoR_Pass`** or **`DoR_Fail`** consistent with gate booleans.
- [ ] Agent points to **`3apk-plan-sprint`** only when `DoR_Pass`.

## HARD-GATE Verification Steps

1. **Block test:** After draft deps/risks/DoR table, attempt to continue without user reply — agent must **not** emit Notion Paste Block.
2. **Approval test:** User selects **B** or **C** — agent revises and re-prompts; Paste Block appears only after **A**.
3. **Gate honesty test:** Deliberately weak AC input → agent must **not** set `testable_ac: true` or `passed: true`.
4. **NFR test:** Agent documents evaluation for performance, security, and accessibility before approval.
5. **Chain boundary test:** Agent does not rewrite user story, AC, or committed estimates.

## Appendix: Example Run

See [`kit/fixtures/refine-risks-example.md`](../../fixtures/refine-risks-example.md) for a redacted transcript using fixture `nova-003` (DoR_Pass worksheet export story).
