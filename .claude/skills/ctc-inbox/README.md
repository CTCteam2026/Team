# CTC Inbox Triage — team install

## What it does

Reads a CTC team member's Gmail, produces one prioritized report grouped by client and event with drafted replies, flagged risks, and proposed ClickUp actions. It **proposes only** — it never sends email or writes to ClickUp.

## Requirements

- **Claude in Chrome extension**, signed into the Google account whose inbox is being read. There is no Gmail connector on this account, so Gmail is read through the browser. The claude.ai web app alone will not work.
- ClickUp connector (already connected on the shared account).

## Install for the team

Zip the `ctc-inbox` folder and upload it under Skills in claude.ai settings. Because the team shares one Claude account, one upload covers everyone. Each person still runs it in their own browser against their own inbox.

## Running it

Type `/ctc-inbox`, or just "run my inbox." Confirm which inbox when asked. Takes a few minutes — it reads the Gmail list view first and only opens the threads that matter.

**It does not run automatically.** See "Automation" below.

## Before the first real run

Three things determine whether this is useful or annoying:

1. **`references/voice-guide.md`** — paste in 8–10 real sent emails. Drafts are generic without this.
2. **`references/guardrails.md`** — set the dollar threshold for escalation, and have someone verify what ClickUp guests can see.
3. **`references/routing-map.md`** — every ClickUp ID is already filled in and verified. Domains fill themselves in: the report surfaces unmapped senders, you confirm, the map grows.

## Automation

There is no per-person automatic run. Gmail is read through each person's own browser session, and the team shares one Claude account, so a scheduled task would fire once against whichever session happened to be open.

The path to real automation, if it's worth it later: per-seat Claude accounts plus a Gmail connector enabled by the Workspace admin. That makes scheduled per-person runs possible and removes the browser dependency entirely.

## Companion skill

`ctc-clickup-push` executes the ClickUp proposals after approval. The interface between them is `references/clickup-handoff.md`.
