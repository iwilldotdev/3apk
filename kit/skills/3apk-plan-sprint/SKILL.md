---
name: 3apk-plan-sprint
description: Drafts a sprint commitment from DoR-passed backlog items and declared team capacity. Produces Planning Worksheet rows with AI estimate hints, mandatory human adjustment logs, and sprint lock ceremony before CSV export (PRD F4).
---

# 3APK Plan Sprint

Draft a **sprint commitment** from **DoR-passed backlog items** and declared **team capacity (hours)**. Produce worksheet rows compatible with [`sprint-worksheet-row.json`](../../notion/schema/sprint-worksheet-row.json), including **`human_adjustment_log`** for every story where the team changes the AI hint. This skill implements **PRD F4** and the primary flow **Sprint Planning**.

<HARD-GATE>
Do NOT emit the **Sprint Lock Block**, instruct the facilitator to **lock the sprint**, or reference **CSV export** until the user **explicitly approves** the sprint draft (committed stories, final estimates, assignments, and capacity balance).
Do NOT accept backlog items where `dor.passed` is not `true` or `status` is not `DoR_Pass` — reject and point to the refinement chain or Notion DoR gate.
Do NOT skip `human_adjustment_log` when `final_estimate_hours` differs from `ai_estimate_hours` — every changed estimate requires a non-empty rationale.
Do NOT bundle multiple questions in one message — **one question per turn** is mandatory.
Do NOT treat AI hint midpoints as committed sprint numbers — only **`final_estimate_hours`** after human sign-off counts toward capacity.
This applies to EVERY sprint regardless of team size or story count.
</HARD-GATE>

## Purpose

- **Input:** Array of **DoR-passed** backlog items (from Notion Backlog **Sprint Candidates** view or approved Paste Blocks from the refinement chain) plus **sprint metadata** (`sprint_id`, capacity hours, optional dates).
- **Output:** Worksheet row drafts per [`sprint-worksheet-row.json`](../../notion/schema/sprint-worksheet-row.json), export-ready when combined with backlog `dependencies` and `status` per [`COLUMNS.md`](../../exports/COLUMNS.md).
- **Authority:** Tech lead / facilitator sets **`final_estimate_hours`**, **`final_estimate_points`**, and **`human_adjustment_log`**; AI provides **`ai_estimate_hours`** hints only ([ADR-001](../../../.compozy/tasks/3apk/adrs/adr-001.md)).
- **Next step after lock:** Export canonical CSV and follow [`jira-recipe.md`](../../exports/jira-recipe.md) or [`trello-recipe.md`](../../exports/trello-recipe.md) (task_09).

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| DoR-passed backlog items | Notion Backlog (`status: DoR_Pass`, `dor.passed: true`) or refinement chain output | yes (≥1; recommend ≥3 for meaningful sprint) |
| `sprint_id` | Notion **Sprints** database | yes |
| `capacity_hours` | Notion **Sprints** → `capacity_hours` | yes |
| `sprint_name`, `start_date`, `end_date` | Notion **Sprints** | optional (recommended for metrics) |
| Team roster | Facilitator | optional (for `assigned_to` prompts) |

### Backlog item minimum fields (per story)

Each item MUST include:

| Field | Required | Rejection if missing |
|-------|----------|----------------------|
| `id` | yes | Cannot build `story_id` |
| `title` | yes | Worksheet denormalisation incomplete |
| `user_story` | yes | Planning discussion lacks context |
| `acceptance_criteria` | yes (≥1 testable line) | Not truly DoR-passed — return to [`3apk-refine-ac`](../3apk-refine-ac/SKILL.md) |
| `dor.passed` | yes, must be `true` | **Reject item** — see Input Validation |
| `status` | yes, must be `DoR_Pass` | **Reject item** |
| `estimate_hours` or upstream hint | recommended | AI uses AC complexity to suggest `ai_estimate_hours` |

Optional but useful: `estimate_points`, `dependencies`, `risks`.

### Input Validation (mandatory first step)

Before drafting worksheet rows, validate **every** backlog item:

```
IF dor.passed != true OR status != "DoR_Pass":
  REJECT item with id + title
  INSTRUCT: complete refinement chain (tasks 04→07) or fix Notion DoR checkboxes
  DO NOT include item in sprint draft
```

**Rejection message template:**

> **Cannot plan:** `{id}` — `{title}` is not DoR-passed (`status: {status}`, `dor.passed: {passed}`). Run the refinement chain or fix Notion gates before sprint planning.

Also reject:

- `Draft`, `Refining`, `DoR_Fail` statuses
- Items with empty `acceptance_criteria`
- Worksheet rows where facilitator manually unchecked `dor_passed`

Reference: [`kit/notion/SPEC.md`](../../notion/SPEC.md) §3.3 **Sprint Candidates** view filter.

## Capacity vs Commitment Balancing

After validating inputs, compute and discuss capacity balance **before** finalising per-story estimates.

### Capacity summary table (present early)

| Metric | Value |
|--------|-------|
| `sprint_id` | … |
| `capacity_hours` | … |
| DoR-passed candidate count | … |
| Sum of backlog `estimate_hours` hints (if present) | … |
| Buffer recommendation | 10–20% of capacity for unknowns |

### Balancing questions (one per turn)

Ask these when commitment total approaches or exceeds capacity:

**Q1 — Scope priority (when candidates exceed capacity):**

> **Which scope reduction approach fits this sprint?**
> - **A)** Commit highest-priority stories until capacity filled; defer remainder
> - **B)** Reduce AC scope on a large story (name which)
> - **C)** Split a story and commit only the smaller slice
> - **D)** Increase capacity (facilitator confirms realistic)
> - **E)** Other — describe briefly

**Q2 — Buffer allocation:**

> **How much capacity should we reserve for unplanned work?**
> - **A)** 0% — commit full capacity
> - **B)** 10% buffer
> - **C)** 20% buffer (recommended for new teams)
> - **D)** Other — specify hours

**Q3 — Dependency ordering (when stories depend on each other):**

> **Story `{id}` depends on `{dependency}`. Should we sequence it later in the sprint or defer?**
> - **A)** Commit now — dependency clears before sprint start
> - **B)** Commit now — dependency is in same sprint
> - **C)** Defer to next sprint
> - **D)** Other — describe briefly

**Q4 — Over-capacity confirmation (mandatory when sum of `final_estimate_hours` > effective capacity):**

> **Committed hours ({committed}) exceed effective capacity ({capacity} − buffer). Which stories should we defer?**
> - **A)** Defer lowest-priority story: `{id}` — `{title}`
> - **B)** Defer two smallest stories
> - **C)** Renegotiate estimates (return to per-story adjustment)
> - **D)** Other — describe briefly

Stop balancing questions once committed total ≤ effective capacity and the facilitator confirms scope.

## Worksheet Row Output

Each committed story produces one row conforming to [`sprint-worksheet-row.json`](../../notion/schema/sprint-worksheet-row.json).

### AI hint vs final estimate columns

| Column | Schema field | Source | Notes |
|--------|--------------|--------|-------|
| AI hint | `ai_estimate_hours` | Midpoint of estimate range from [`3apk-refine-estimate`](../3apk-refine-estimate/SKILL.md) or backlog `estimate_hours` | **Not** sprint commitment |
| Final hours | `final_estimate_hours` | Team after discussion | **Required**; sums to sprint commitment |
| Final points | `final_estimate_points` | Team (optional) | Omit or null if hours-only |
| Adjustment log | `human_adjustment_log` | Team rationale | **Required** in schema for every row |

### Human adjustment log rules

| Scenario | `human_adjustment_log` requirement |
|----------|--------------------------------------|
| `final_estimate_hours` ≠ `ai_estimate_hours` | **Non-empty** rationale explaining delta (mandatory PRD F4) |
| `final_estimate_hours` = `ai_estimate_hours` | Non-empty confirmation, e.g. `"No adjustment — team aligned with AI range midpoint"` |
| Points changed from hint | Include points rationale in same log field |
| Estimate increased | State driver (unknowns, integration risk, AC scope) |
| Estimate decreased | State driver (split scope, reused component, simpler env) |

**Forbidden:** empty string, placeholder `"TBD"`, or omitting log when estimate changed.

### Worksheet Row Output Template

Emit one JSON object per committed story inside the approved **Sprint Draft Block**:

```json
{
  "story_id": "nova-003",
  "sprint_id": "sprint-baseline-01",
  "title": "Sprint worksheet CSV export",
  "user_story": "As a tech lead, I want to export the planning worksheet to a canonical CSV so that I can import sprint commitments into Jira or Trello.",
  "acceptance_criteria": "Given DoR-passed stories in the worksheet\nWhen I export CSV\nThen the file uses the 13-column order from COLUMNS.md",
  "ai_estimate_hours": 4,
  "final_estimate_hours": 5,
  "final_estimate_points": 5,
  "human_adjustment_log": "Increased from 4h — CSV quoting and cross-tool import edge cases",
  "assigned_to": "Alex Chen",
  "dor_passed": true
}
```

**AC formatting:** Join array items with `\n` for worksheet text and CSV export (see [`COLUMNS.md`](../../exports/COLUMNS.md) § Acceptance Criteria Field).

### CSV export columns (13-column canonical)

Worksheet rows plus backlog fields form the export row per [`COLUMNS.md`](../../exports/COLUMNS.md):

| # | CSV column | Source |
|---|------------|--------|
| 1–11 | worksheet fields | `sprint-worksheet-row.json` |
| 12 | `dependencies` | BacklogItem — comma-separated |
| 13 | `status` | BacklogItem — set `Planned` after lock |

Golden reference: [`sample-worksheet-export.csv`](../../fixtures/sample-worksheet-export.csv).

## Asking Questions

When this skill instructs you to ask the user a question:

1. Use your runtime's **interactive question tool** if available — the mechanism that **pauses until the user responds**.
2. If no such tool exists, send **one question** as your complete message and **stop generating**. Do not answer your own question or continue without user input.

### One question per message (strict)

- Your message must contain **exactly one** clarifying question.
- After asking, **STOP**. No follow-up questions, "also" prompts, or "additionally" in the same message.

### Multiple-choice format

- Prefer **labeled options A, B, C, D** so the user can reply with a single letter.
- Always include a fallback: **D) Other — describe briefly** (or **E** when five options are needed).
- Per-story estimate questions use the **Per-Story Estimate Prompt** below.

### Per-Story Estimate Prompt

For each committed story (one turn per story):

> **Story `{story_id}` — `{title}`**
> AI hint: **{ai_estimate_hours}h** (range {low}–{high} from refinement).
> **What is the team's final estimate?**
> - **A)** Accept AI hint — final = {ai_estimate_hours}h
> - **B)** Increase — specify hours and reason
> - **C)** Decrease — specify hours and reason
> - **D)** Defer this story from sprint
> - **E)** Other — describe briefly

On **B** or **C**, follow up (next turn) with:

> **Record human adjustment log for `{story_id}`:** Why did the team change the estimate from {ai}h to {final}h?

On **A**, still record: `"No adjustment — team aligned with AI range midpoint"`.

## Workflow

1. **Acknowledge input** — restate `sprint_id`, `capacity_hours`, and count of DoR-passed candidates.
2. **Validate DoR** — reject any item failing Input Validation; list rejected ids separately.
3. **Capacity preview** — show capacity summary table and hint-hour sum.
4. **Balancing questions** — ask buffer / priority / dependency questions (one per turn) when needed.
5. **Draft AI hints** — set `ai_estimate_hours` per story from backlog hints or AC-driven range (label as hint only).
6. **Per-story estimates** — one **Per-Story Estimate Prompt** per turn; capture `final_estimate_hours`, optional points, and `human_adjustment_log`.
7. **Assignment prompts** — one question per story for `assigned_to` when roster unknown.
8. **Capacity check** — sum `final_estimate_hours`; if over effective capacity, run **Q4 Over-capacity confirmation**.
9. **Present sprint draft** — table of all worksheet rows + commitment total vs capacity; ask:

   > **Approve this sprint draft for lock?**
   > - **A)** Approved — ready for Sprint Lock Block
   > - **B)** Revise estimates (name story)
   > - **C)** Revise scope — add/remove/defer stories
   > - **D)** Reject — restart from capacity preview

10. **On A only** — emit **Sprint Lock Block** (below) with Notion paste + export handoff.
11. **On B/C** — apply edits, re-run capacity check, return to step 9.
12. **On D** — return to step 3.

## Notion Planning Worksheet Integration

Per [`kit/notion/SPEC.md`](../../notion/SPEC.md) §3:

1. Open **Planning Worksheet** → **Sprint Candidates** view (`dor_passed` checked, optional `final_estimate_hours` not empty).
2. For each approved row, create worksheet entry:
   - Link **Backlog item** + **Sprint** relations.
   - Copy denormalised fields: `story_id`, `sprint_id`, `title`, `user_story`, `acceptance_criteria`.
   - Set `ai_estimate_hours`, `final_estimate_hours`, `final_estimate_points`, `human_adjustment_log`, `assigned_to`.
   - Check **`dor_passed`** (rollup from Backlog `passed` or manual sync).
3. **Block rule:** Never add `DoR_Fail` stories — view filter enforces eligibility.
4. After lock, set linked Backlog **`status`** to **`Planned`**.

### Notion Paste Field Mapping

| Sprint Lock Block field | Notion Planning Worksheet property | Schema field |
|-------------------------|-----------------------------------|--------------|
| `story_id` | `story_id` | `story_id` |
| `sprint_id` | `sprint_id` | `sprint_id` |
| `title` | `title` | `title` |
| `user_story` | `user_story` | `user_story` |
| `acceptance_criteria` | `acceptance_criteria` | `acceptance_criteria` |
| `ai_estimate_hours` | `ai_estimate_hours` | `ai_estimate_hours` |
| `final_estimate_hours` | `final_estimate_hours` | `final_estimate_hours` |
| `final_estimate_points` | `final_estimate_points` | `final_estimate_points` |
| `human_adjustment_log` | `human_adjustment_log` | `human_adjustment_log` |
| `assigned_to` | `assigned_to` | `assigned_to` |
| `dor_passed` | `dor_passed` | `dor_passed` |
| Backlog link | `Backlog item` | relation |
| Sprint link | `Sprint` | relation |

## Sprint Lock Ceremony

Complete this checklist **inside the Sprint Lock Block** (emit only after draft approval):

### Sprint Lock Checklist

- [ ] Every committed story has `dor.passed: true` and `status: DoR_Pass` on linked Backlog row
- [ ] Every worksheet row has non-empty `final_estimate_hours`
- [ ] Every row has non-empty `human_adjustment_log` (including "no adjustment" confirmations)
- [ ] Sum of `final_estimate_hours` ≤ effective capacity (capacity − agreed buffer)
- [ ] Each story has `assigned_to` (or explicit team decision to leave blank with note)
- [ ] Linked Backlog rows updated to **`status: Planned`**
- [ ] Sprint row in **Sprints** DB set to **`Committed`** (or team equivalent)
- [ ] **`planning_minutes`** captured for Metrics DB ([`baseline-protocol.md`](../../playbook/baseline-protocol.md) — task_10)
- [ ] Facilitator confirms **Sprint Candidates** view matches committed set

### Sprint Lock Block (emit only after approval)

```markdown
## 3APK Plan Sprint — Locked Commitment (paste-ready)

**sprint_id:** sprint-baseline-01
**capacity_hours:** 24
**committed_hours:** 19
**buffer_hours:** 2.4
**story_count:** 3

### worksheet_rows
```json
[
  { "...": "one SprintWorksheetRow per story" }
]
```

### csv_export_readiness
Header (verbatim from COLUMNS.md):
`story_id,sprint_id,title,user_story,acceptance_criteria,ai_estimate_hours,final_estimate_hours,final_estimate_points,human_adjustment_log,assigned_to,dor_passed,dependencies,status`

### notion_actions
1. Paste each row into Planning Worksheet (Sprint Candidates view).
2. Set Backlog `status` → `Planned` for each committed `story_id`.
3. Update Sprints `status` → `Committed`.

### export_handoff
Sprint is locked. Export canonical CSV from Notion (or compose from rows above), then:
- **Jira:** follow [`kit/exports/jira-recipe.md`](../../exports/jira-recipe.md)
- **Trello:** follow [`kit/exports/trello-recipe.md`](../../exports/trello-recipe.md)
- **Generic:** follow [`kit/exports/generic-fallback.md`](../../exports/generic-fallback.md)

Validate export against [`sample-worksheet-export.csv`](../../fixtures/sample-worksheet-export.csv).

### metrics_capture
Record `planning_minutes` in Metrics DB for this `sprint_id`.
```

## Export Handoff (post-lock only)

**Do not mention export recipes until the sprint is locked.**

After lock:

1. Produce or export CSV matching **13-column order** in [`COLUMNS.md`](../../exports/COLUMNS.md).
2. Run import using **`jira-recipe.md`** (primary) or **`trello-recipe.md`**.
3. Verify required fields populate using fixture CSV as reference.
4. Hand off to execution; capture actual hours at sprint end for **EAR** ([`metric-snapshot.json`](../../notion/schema/metric-snapshot.json)).

## Over-Capacity Protocol

When **sum(`final_estimate_hours`) > effective capacity**:

1. **Stop** — do not proceed to approval prompt.
2. Present over-capacity table:

   | story_id | title | final_estimate_hours |
   |----------|-------|----------------------|
   | … | … | … |
   | **Total** | | **{sum}** |
   | **Effective capacity** | | **{capacity − buffer}** |

3. Ask **Q4 Over-capacity confirmation** (one turn).
4. Remove deferred stories from draft or revise estimates.
5. Re-sum and repeat until feasible.

## Anti-Patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Planning `DoR_Fail` or `Draft` stories | Breaks DoR KPI and worksheet filter |
| Lock/export before approval | HARD-GATE violation |
| Empty `human_adjustment_log` on changed estimate | PRD F4 / schema violation |
| Using `ai_estimate_hours` in capacity sum | Only final estimates commit |
| Skipping over-capacity questions | False feasibility |
| Multiple questions per message | Breaks interactive protocol |
| Export instructions before lock | HARD-GATE violation |

## Planning Smoke Test Procedure

Run manually with fixture data in [`plan-sprint-example.md`](../../fixtures/plan-sprint-example.md):

1. **Input:** Three DoR-passed stories (`nova-003`, `nova-004`, `nova-005`) + `capacity_hours: 24`.
2. **Validate:** Agent rejects `nova-002` (DoR_Fail) if supplied.
3. **Draft:** Agent produces worksheet rows with AI hints and per-story final estimates.
4. **Adjust:** At least one story has increased estimate with non-empty log (matches golden CSV pattern).
5. **Capacity:** Committed total ≤ 24h after buffer.
6. **Over-capacity variant:** Re-run with `capacity_hours: 8` — agent must ask scope reduction questions.
7. **Lock:** Sprint Lock Block appears only after facilitator selects **A** on draft approval.
8. **CSV:** Rows convertible to header in `COLUMNS.md`; compare shape to [`sample-worksheet-export.csv`](../../fixtures/sample-worksheet-export.csv).

## Skill Smoke Test Checklist

- [ ] Attach this `SKILL.md` and inputs from [`plan-sprint-example.md`](../../fixtures/plan-sprint-example.md).
- [ ] Agent rejects backlog item with `dor.passed: false`.
- [ ] Agent asks **at most one** question per turn before draft approval.
- [ ] Agent separates **`ai_estimate_hours`** from **`final_estimate_hours`** in output table.
- [ ] Every changed estimate has non-empty **`human_adjustment_log`**.
- [ ] Agent presents **A/B/C/D approval** before Sprint Lock Block.
- [ ] **Sprint Lock Block** includes checklist + Notion mapping + export handoff.
- [ ] Export recipes referenced **only after** lock approval.
- [ ] Over-capacity scenario triggers **Q4** scope reduction question.

## HARD-GATE Verification Steps

1. **Block test:** After sprint draft table, attempt lock without user reply — agent must **not** emit Sprint Lock Block.
2. **DoR rejection test:** Include `nova-002` — agent must reject with explicit message.
3. **Adjustment log test:** Change estimate without log — agent must block row completion.
4. **Export timing test:** Agent must not mention Jira/Trello export before lock approval.
5. **Capacity test:** Committed hours over capacity — agent must run over-capacity protocol before approval.

## Appendix: Example Run

See [`kit/fixtures/plan-sprint-example.md`](../../fixtures/plan-sprint-example.md) for a redacted transcript with three DoR-passed stories, feasible sprint at 24h capacity, over-capacity variant, and JSON worksheet rows validated against schema.
