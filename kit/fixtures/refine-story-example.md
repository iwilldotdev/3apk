# Refine Story — Example Run (Redacted)

Fictional fixture: **`nova-001`** from [`sample-backlog-items.json`](sample-backlog-items.json) (status: `Draft`).

| Field | Fixture value |
|-------|----------------|
| `id` | `nova-001` |
| `title` | Add OAuth provider to customer portal |
| `raw_request` | Clients keep asking to log in with Google — can we add that? |
| `status` | Draft |

---

## Turn 1 — Facilitator

> Run `3apk-refine-story`. Backlog id: `nova-001`.
>
> Raw request: "Clients keep asking to log in with Google — can we add that?"

## Turn 2 — Agent

Restated: customers want Google sign-in on the customer portal.

**Who is the primary actor for this story?**

- **A)** End customer (portal user signing in)
- **B)** Internal admin configuring auth providers
- **C)** Support agent helping customers with login issues
- **D)** Other — describe briefly

## Turn 3 — Facilitator

> A

## Turn 4 — Agent

**What is the primary outcome you want from Google login in this story?**

- **A)** Customers can sign in with Google as an alternative to email/password
- **B)** Customers can only sign in with Google (replace email/password)
- **C)** Google login plus automatic account linking for existing email users
- **D)** Other — describe briefly

## Turn 5 — Facilitator

> A

## Turn 6 — Agent (draft)

**Proposed title:** Enable Google sign-in for customer portal

**Proposed user story:**

As a **customer**, I want to **sign in to the portal with my Google account** so that **I can access my account without creating and remembering a separate password**.

**Approve this user story?**

- **A)** Approved — output is final; ready for AC refinement
- **B)** Revise title only
- **C)** Revise user story only
- **D)** Reject — restart clarification

## Turn 7 — Facilitator

> A

## Turn 8 — Agent (approved Paste Block)

```markdown
## 3APK Refine Story — Approved Output

**id:** nova-001
**status:** Refining

### title
Enable Google sign-in for customer portal

### raw_request
Clients keep asking to log in with Google — can we add that?

### user_story
As a customer, I want to sign in to the portal with my Google account so that I can access my account without creating and remembering a separate password.
```

**Handoff:** Run **`3apk-refine-ac`** with the approved `user_story` above. Path: `kit/skills/3apk-refine-ac/SKILL.md`.

---

## Notion paste check

| Notion Backlog field | Paste from block | Rename required? |
|----------------------|------------------|------------------|
| Title | `### title` line | No |
| Raw Request | `### raw_request` section | No |
| User Story | `### user_story` paragraph | No |
| Status | Set to `Refining` manually | No |

## Schema conformance

- `title` and `user_story` satisfy [`backlog-item.json`](../notion/schema/backlog-item.json) string types.
- `user_story` uses canonical "As a … I want … so that …" format per schema description.
- No `acceptance_criteria` populated at this step (correct chain boundary).
