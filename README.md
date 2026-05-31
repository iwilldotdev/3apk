# 3APK — AI-Augmented Agile Planning Kit

An AI-augmented agile planning kit for **development teams**. It combines **portable skills** (prompt chains with human approval), a **Notion hub** (backlog, DoR, planning, metrics), and **manual export** to Jira or Trello.

Developed as part of a Descomplica Extension Project (PEX), aligned with **SDG 9** (Industry, innovation and infrastructure). The pilot documents applying the kit to a **software development project** run by **RODRIGO HERPICH MULLER LTDA**.

---

## Who this repository is for

| Role | What you do here |
|------|------------------|
| **Team member** | Run skills in your chat/IDE, paste results into Notion, execute the sprint in Jira/Trello |
| **Facilitator** | Set up Notion, run baseline and workshops with the team, collect metrics |
| **Reuse** | Copy only the skills in `kit/skills/` and adapt Notion to your workflow |

---

## What the kit contains

Everything you need to use 3APK lives in [`kit/`](kit/):

| Area | Path | Contents |
|------|------|----------|
| **Skills** | [`kit/skills/`](kit/skills/) | 5 modular skills (4 refinement + 1 planning) |
| **Notion** | [`kit/notion/`](kit/notion/) | Setup guide + JSON Schemas |
| **Export** | [`kit/exports/`](kit/exports/) | Canonical CSV + Jira/Trello recipes |
| **Fixtures** | [`kit/fixtures/`](kit/fixtures/) | Reference JSON/CSV examples |

**Principles:**

- **Human-in-the-loop** — no estimate or acceptance criterion enters the sprint without explicit team approval.
- **LLM-agnostic** — Markdown skills; work in Cursor, Claude, ChatGPT, Copilot Chat, etc.
- **No new SaaS** — Notion + your existing tools; manual export to Jira/Trello.

Detailed index: [`kit/README.md`](kit/README.md).

---

## Prerequisites

- **Notion** account (free tier)
- Any **LLM chat** or IDE with an agent
- **Jira** or **Trello** (optional) — to carry the sprint plan into execution
- ~30 minutes to set up Notion following the guide

**Not required:** server, API, build step, or a specific tool subscription.

---

## Quick start

### 1. Set up the Notion hub

Follow [`kit/notion/SPEC.md`](kit/notion/SPEC.md) and create the four databases:

1. **Backlog** — stories, DoR, status  
2. **Sprints** — capacity, dates  
3. **Planning Worksheet** — sprint commitment (view: DoR-approved only)  
4. **Metrics** — KPIs per sprint  

Fields must follow the schemas in [`kit/notion/schema/`](kit/notion/schema/).

### 2. Install the skills

Copy folders from `kit/skills/` to where your agent reads skills, **or** attach the `SKILL.md` in chat:

| Order | Skill | File |
|-------|-------|------|
| 1 | Raw request → user story | [`3apk-refine-story/SKILL.md`](kit/skills/3apk-refine-story/SKILL.md) |
| 2 | User story → acceptance criteria | [`3apk-refine-ac/SKILL.md`](kit/skills/3apk-refine-ac/SKILL.md) |
| 3 | AC → estimate range (hint) | [`3apk-refine-estimate/SKILL.md`](kit/skills/3apk-refine-estimate/SKILL.md) |
| 4 | Dependencies and risks | [`3apk-refine-risks/SKILL.md`](kit/skills/3apk-refine-risks/SKILL.md) |
| 5 | Sprint planning | [`3apk-plan-sprint/SKILL.md`](kit/skills/3apk-plan-sprint/SKILL.md) |

### 3. Configure export

- CSV columns: [`kit/exports/COLUMNS.md`](kit/exports/COLUMNS.md)  
- **Jira:** [`kit/exports/jira-recipe.md`](kit/exports/jira-recipe.md)  
- **Trello:** [`kit/exports/trello-recipe.md`](kit/exports/trello-recipe.md)  
- **Other tools:** [`kit/exports/generic-fallback.md`](kit/exports/generic-fallback.md)  

Reference: [`kit/fixtures/sample-worksheet-export.csv`](kit/fixtures/sample-worksheet-export.csv).

### 4. Validate the setup

Use the examples in [`kit/fixtures/`](kit/fixtures/) and run:

```bash
python3 kit/fixtures/validate_fixtures.py
python3 kit/exports/test_export_recipes.py
```

---

## Day-to-day usage

### Refine an item (new feature, bug, improvement)

**One skill at a time**, with **human approval** before moving on:

```
Raw request
  → 3apk-refine-story    → approve user story
  → 3apk-refine-ac       → approve acceptance criteria
  → 3apk-refine-estimate → approve estimate range (hint)
  → 3apk-refine-risks    → approve deps/risks + DoR
  → paste into Notion    → DoR_Pass or DoR_Fail
```

- One question per message (multiple choice when possible).  
- The AI does **not** set the final estimate — the team adjusts during planning.  
- Items that fail DoR **do not enter** the sprint.

Examples: [`kit/fixtures/refine-story-example.md`](kit/fixtures/refine-story-example.md) and other `refine-*-example.md` files.

### Plan a sprint

1. Open the **Sprint Candidates** view in Notion (`DoR_Pass` only).  
2. Register the sprint in **Sprints** with `capacity_hours`.  
3. Invoke **`3apk-plan-sprint`** with stories + capacity.  
4. Fill `human_adjustment_log` for every changed estimate.  
5. Approve the sprint draft (Sprint Lock).  
6. Export CSV and import into Jira/Trello.

Example: [`kit/fixtures/plan-sprint-example.md`](kit/fixtures/plan-sprint-example.md).

### Record metrics

After each sprint, add one row in **Metrics**:

| KPI | Short definition |
|-----|------------------|
| **EAR** | Sum(actual hours) / Sum(estimated hours), ≥5 stories |
| **DoR %** | Stories with 4 gates passed / total planned |
| **Planning (min)** | Duration × participants (refinement + planning) |
| **Reopens** | Stories reopened due to AC/scope gaps |

Full schema: [`kit/notion/schema/metric-snapshot.json`](kit/notion/schema/metric-snapshot.json).

---

## Suggested pilot (4–8 weeks)

| Phase | Weeks | Activities |
|-------|-------|------------|
| **Prep** | 0 | Set up Notion; distribute skills |
| **Baseline** | 1 | One cycle **without** the kit; freeze KPIs |
| **Intervention** | 2–5 | Skills + DoR + planning every 1–2 weeks |
| **Evidence** | 6–8 | Compare before/after; consolidate results |

Reference PEX report (academic): [`docs/relatorio-pex/relatorio-pex-ads-iii-william-santos-goncalves.pdf`](docs/relatorio-pex/relatorio-pex-ads-iii-william-santos-goncalves.pdf).

---

## Repository structure

```
3APK/
├── kit/
│   ├── skills/       # 5 modular skills
│   ├── notion/       # SPEC.md + JSON Schemas
│   ├── exports/      # COLUMNS.md + Jira/Trello recipes
│   └── fixtures/     # JSON/CSV examples
├── docs/
│   └── relatorio-pex/   # PEX report (PDF + HTML)
└── README.md
```

---

## References

- [Descomplica PEX Guide](https://pexguiadefinitivo.vercel.app/) (Portuguese)
- SDG 9 — [Industry, innovation and infrastructure (UN)](https://www.un.org/sustainabledevelopment/infrastructure-industrialization/)

---

## License and use

University extension material and an open kit for adaptation by any team. When reusing, keep the human-approval protocol at every refinement step.
