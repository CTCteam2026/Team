# Conference P&L Automation

Turns a P&L from a two-hour typing job into four inputs.

**[`CTC_Conference_PL_Builder.xlsx`](CTC_Conference_PL_Builder.xlsx)** — open it, fill in the
yellow cells, read the P&L. Every number is a live formula; nothing is hardcoded.

## What you tell it

| Input | Where |
|---|---|
| How many **event days** and **set-up days** | INPUTS §2 |
| How many **months of pre-planning** | INPUTS §2 |
| Event size — **attendees, exhibitors, sponsors, speakers, vendors to source** | INPUTS §1 |
| **Scope of work** — 25 line items, Yes/No each | SCOPE tab, column D |
| How many **managers** and **coordinators** work it **onsite** | INPUTS §3 |
| How many **managers** and **coordinators** work it **in pre-planning** | INPUTS §3 |

## What it gives you back

A complete P&L: proposal summary, a pre-planning table, an onsite table with one line per
person, staff overhead, admin fee and grand total — client cost, our cost, net profit and
margin at every level.

## The rules baked in

**Staff rates** — manager **$60/hr** cost, coordinator **$42/hr** cost. Onsite is split
per person (one row each). Pre-planning rolls up by category. Client rates follow the
historical card: PM $90 / EC $65 pre-planning, PM $100 onsite, coordinator overtime at 1.5×.

**Staff overhead** — **$0.61 × every CTC staff hour** (pre-planning + onsite + overtime).
A cost to us, not billed, so it comes out of margin.

**Admin fee** — **2% of the client subtotal**, added on top of what the client pays.
No cost sits against it, so all of it is profit.

**Hour drivers** — each of the 25 scope lines calculates its own hours from the inputs.
Calibrated against the final LCT 2026, AFCI 2027 and WTUI 2027 P&Ls. Where the old note in
the sheet disagreed with what was actually charged, the actuals won — e.g. Exhibit Management
was noted as "exhibitors × 5" but was billed at exactly **exhibitors × 1** on both WTUI (200
hrs / 200 exhibitors) and LCT (35 / 35). Percentage-of-attendee drivers carry a floor and a
cap taken from the observed range, so a 1,500-person event doesn't produce a nonsense number.

Any line you disagree with: type a number into **OVERRIDE HOURS** on the SCOPE tab. Nothing
else changes.

## How well it matches the real P&Ls

Feeding each event's real inputs back through the model:

| Event | Pre-planning hrs | Pre-planning $ | Onsite hrs | Client subtotal |
|---|---|---|---|---|
| LCT / Marine Recreation 2026 | +2% | +2% | **exact** | **+2%** |
| AFCI Studio Summit 2027 | −28% | −24% | **exact** | −19% |
| WTUI 2027 | −2% | −9% | +11% | **−4%** |

AFCI reads low because its final proposal priced Registration at 150 hrs (a full Cvent
build-out plus mobile app) and Programming at 65 hrs (recording & broadcast) — both well
above base scope. That is what the override column is for.

WTUI onsite reads high only because the model defaults managers to 12 hrs/onsite day and
WTUI billed 10. Change that input and it matches exactly.

## Files

| File | What it is |
|---|---|
| `CTC_Conference_PL_Builder.xlsx` | The template. This is the deliverable. |
| `build_pl_template.py` | Generates the template. Edit here to change the scope library or drivers, then re-run. |
| `validate_against_history.py` | Re-runs the three historical events through the model and prints the deltas above. |

Regenerate:

```bash
python3 build_pl_template.py
python3 /root/.claude/skills/synced/xlsx/scripts/recalc.py CTC_Conference_PL_Builder.xlsx 200
python3 validate_against_history.py     # optional back-test
```

## Open item

**Admin fee base.** Implemented as 2% of the *client subtotal* (pre-planning + onsite),
charged on top of the client price. If you meant 2% of our internal cost, or 2% of the
grand total after the multi-year discount, change `C10` on the P&L tab — it is a one-cell
edit, and the fee % itself already lives on INPUTS.
