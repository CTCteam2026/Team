---
name: ctc-inbox
description: Triage a CTC Conferences Gmail inbox and produce a prioritized action report grouped by client and event, with drafted replies, flagged risks, and proposed ClickUp tasks and comments. Use when someone says "run my inbox", "triage my email", "what needs my attention", "catch me up on email", or invokes /inbox. Read-only against Gmail and ClickUp — it proposes, it never sends or creates.
---

# CTC Inbox Triage

Turn a full Gmail inbox into one prioritized report a CTC team member can act on in 10 minutes.

**Hard rule: this skill never writes anywhere.** It does not send email, create ClickUp tasks, post comments, archive, label, or create calendar events. Every action is a *proposal* in the report. Execution is the `ctc-clickup-push` skill's job, after the human approves.

## Before you start

1. Read `references/routing-map.md`, `references/priority-rules.md`, and `references/guardrails.md`. Read `references/voice-guide.md` before drafting any reply.
2. Establish **who is running this**. Ask if unknown: "Which inbox am I reading?" Their name and email determine assignee routing and what counts as "awaiting my reply."
3. Confirm Gmail is reachable. Use the Claude in Chrome browser tools against `mail.google.com`. If the user has multiple Google accounts, confirm the account index (`u/0`, `u/1`, …) before searching — reading the wrong inbox wastes the whole run.

## Step 1 — Pull the inbox (do NOT open threads yet)

The expensive mistake is opening every thread. Gmail's list view already gives you sender, subject, snippet, and timestamp. Triage from the list; open only what you must.

Run two searches by navigating to the Gmail URL directly:

**A. Unread**
`https://mail.google.com/mail/u/0/#search/in%3Ainbox+is%3Aunread+newer_than%3A14d`

**B. Possibly awaiting a reply**
`https://mail.google.com/mail/u/0/#search/in%3Ainbox+is%3Aread+newer_than%3A10d+-from%3Ame+-category%3Apromotions+-category%3Asocial`

For each, use `get_page_text` or `read_page` on the results list and capture every row: sender name, sender address if shown, subject, snippet, date, and the thread's link target.

**Known limitation, be honest about it:** Gmail has no native "he replied last and I never answered" operator. Search B is an approximation and will include threads you already handled. Do not silently drop them — put anything genuinely ambiguous in a short **"Might be waiting on you"** section at the end of the report rather than guessing. Tune this after the first few real runs.

**Cap each run at 50 threads.** If searches return more, take the most recent 50 and say plainly in the report how many were left unexamined.

### Capturing links

Every item in the report needs a working Gmail link. Preferred: the thread permalink `https://mail.google.com/mail/u/<N>/#inbox/<thread-id>`, where the thread id comes from the row's `data-legacy-thread-id` attribute (readable via `read_page` or `javascript_tool`). If that fails, fall back to a search link on the exact subject:
`https://mail.google.com/mail/u/<N>/#search/subject%3A%22<url-encoded subject>%22`

Verify one link works before building the whole report. A report full of dead links is worse than no report.

## Step 2 — Classify every thread

Assign each thread exactly one bucket:

| Bucket | Meaning |
|---|---|
| `client` | Active client on a live event. Maps to a ClickUp folder. |
| `vendor` | Venue, AV, décor, print, catering, staffing — someone CTC is buying from. |
| `partner` | CVB, association, referral source, sponsor. |
| `prospect` | Real inbound interest or an active sales thread. |
| `internal` | Another @ctcconferences.com person. |
| `admin` | Invoices, banking, insurance, contracts, legal, HR, payroll. |
| `noise` | Newsletters, subscriptions, cold outreach, automated notifications. |

Route `client`, `vendor`, and `partner` threads to a client-event using `references/routing-map.md`. Domain alone is not enough for POLB and FerroTec — they each have multiple 2026 events, so disambiguate on subject line, event name, dates, or venue mentioned in the snippet. If you cannot tell, mark the item `⚠️ Event unclear` and ask in the report rather than guessing wrong.

**Unmapped domains:** when a `client`/`vendor`/`partner` sender's domain isn't in the routing map, add it to the report's **"New domains to map"** section with your best-guess client. Once the user confirms, append the row to `references/routing-map.md` so the map improves every run. This is how the map gets built — do not ask the user to fill in 29 rows by hand.

## Step 3 — Score priority

Apply `references/priority-rules.md` in order. The short version:

1. **Money & commitment risk** — contracts, signatures, invoices, deposits, payment problems, cancellations, change orders, anything with a dollar figure or a deadline attached to money.
2. **Who is waiting on you** — explicit asks and direct questions, weighted by how long they have been sitting.
3. **Event date proximity** — nearest event wins. Folder name prefixes are the event date.

Then assign P1 / P2 / P3 / FYI. Never mark more than 8 items P1; if the math produces more, the top 8 are P1 and the rest drop to P2. A report with 20 P1s is a report nobody reads.

## Step 4 — Open only what you need

Open the full thread only for items that are P1 or P2, or where you will draft a reply, or where the snippet is genuinely ambiguous. Expect roughly 10–15 threads per run. Everything else is summarized from its snippet.

## Step 5 — Draft replies

Draft for P1 and P2 items where a reply is the obvious next step. Follow `references/voice-guide.md`.

Do **not** draft for anything on the never-draft list in `references/guardrails.md` — those get flagged for the human with a note on why, and nothing more.

Keep drafts short. A draft that needs heavy editing is worse than a bullet list of the points to make; when you are unsure of a fact, write the bullets and say so rather than inventing a confident answer.

## Step 6 — Propose ClickUp actions

For each actionable item, propose either a **task** or a **comment**, using the folder/list IDs in `references/routing-map.md`.

- **Task** — new work with an owner: a deliverable, a decision to be made, a thing to chase.
- **Comment** — context the team needs on work that already exists. Search for the relevant existing task with `clickup_search` and name it. Do not propose a comment on a task you have not confirmed exists.

**Read the ClickUp visibility rules in `references/guardrails.md` before proposing any comment.** Client guests are members of this ClickUp workspace. An internal FYI posted in a client folder may be readable by that client.

Emit each proposal in this exact block so `ctc-clickup-push` can consume it without re-deriving anything:

```json
{
  "action": "task" | "comment",
  "client": "POLB Small Business Summit",
  "folder_id": "90117832018",
  "list_id": "901113493186",
  "target_task": null,
  "title": "Confirm AV load-in window with venue",
  "body": "…",
  "assignee": "manny@ctcconferences.com",
  "due": "2026-09-15",
  "visibility": "client-safe" | "internal-only",
  "source_email": "https://mail.google.com/mail/u/0/#inbox/…"
}
```

## Step 7 — Build the report

Load the `artifact-design` skill, then publish the report as an Artifact and give the user the link.

Structure, in this order:

1. **Top line** — one sentence. How many threads scanned, how many need action, the single most urgent thing.
2. **Needs you today (P1)** — grouped by client/event. Each item: subject as a Gmail link, sender, one line on what they want, the proposed action, the drafted reply in a collapsible block, and the proposed ClickUp action.
3. **This week (P2)** — same shape, tighter.
4. **Flags & risks** — anything with money, deadline, or relationship risk, plus anything the guardrails told you not to touch. Call out *why* it is a flag.
5. **FYI / no reply needed (P3)** — one line each.
6. **Suppressed** — newsletters and cold outreach as a count and a sender list. No summaries.
7. **Might be waiting on you** — the ambiguous search-B results.
8. **New domains to map** — unmapped senders with your best-guess client, for confirmation.

Design notes: it must be skimmable in 60 seconds. Client/event as the primary grouping, priority as the sort within each group. Gmail and ClickUp links open in new tabs. Drafted replies must be one click to copy. Make the P1 count impossible to miss.

## Close the loop

End with a plain-text list of what you would do next if approved, and tell the user to run `/clickup-push` to execute the ClickUp proposals. Never execute them yourself.
