# Handoff Contract: ctc-inbox → ctc-clickup-push

This is the interface between the two skills. `ctc-inbox` **emits** these blocks and does nothing else. `ctc-clickup-push` **consumes** them and is the only thing that writes to ClickUp.

Keeping this contract stable means either skill can be rebuilt without breaking the other.

## The block

```json
{
  "id": "a1",
  "action": "task",
  "client": "POLB Small Business Summit",
  "folder_id": "90117832018",
  "list_id": "901113493186",
  "target_task": null,
  "title": "Confirm AV load-in window with Long Beach Convention Center",
  "body": "Venue came back asking to move load-in from 7am to 10am on 10/7. Need to confirm this still clears setup before doors at 8am on 10/8.",
  "assignee": "manny@ctcconferences.com",
  "due": "2026-09-15",
  "priority": "P1",
  "visibility": "client-safe",
  "source_email": "https://mail.google.com/mail/u/0/#inbox/18f2a…",
  "source_sender": "events@longbeachcc.com"
}
```

## Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Short handle so the human can say "do a1 and a3, skip a2" |
| `action` | yes | `task` or `comment` |
| `client` | yes | Human-readable client/event name |
| `folder_id` | yes | From `routing-map.md`. Verified real IDs. |
| `list_id` | yes | From `routing-map.md`. See the multi-list rules there. |
| `target_task` | comments only | ClickUp task **ID**, found via `clickup_search`. Never propose a comment on a task you have not confirmed exists. |
| `title` | tasks only | Imperative, starts with a verb |
| `body` | yes | Task description or comment text |
| `assignee` | yes | `@ctcconferences.com` address; resolve to ClickUp ID via the team table in `routing-map.md` |
| `due` | tasks only | ISO date, or `null` |
| `priority` | yes | Mirrors the report's P1/P2/P3 |
| `visibility` | yes | `client-safe` or `internal-only` — see `guardrails.md`. **`internal-only` must never route to a client folder.** |
| `source_email` | yes | Gmail permalink, so the task carries its origin |
| `source_sender` | yes | Who it came from |

## Rules for the consuming skill

1. **Nothing executes without explicit human approval**, per block or as an approved batch. "Run the inbox" is not approval to write.
2. **Re-validate `visibility` before writing.** If `internal-only` carries a client `folder_id`, refuse the block and report it. This is a bug-catch, and the bug it catches is the expensive one.
3. **Check for duplicates first.** Run `clickup_search` on the title within the target list before creating. Email threads generate repeat proposals across runs, and duplicate task spam in client folders is the fastest way to lose the team's trust in this system.
4. **Confirm `target_task` still exists** before commenting.
5. **Report back per block** — created, skipped as duplicate, or failed with the reason. Never report a batch as succeeded without per-item confirmation.
6. Nothing here creates lists, folders, or statuses. If a destination doesn't exist, stop and ask.
