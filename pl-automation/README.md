# Conference P&L Automation

Turns a P&L from a two-hour typing job into a handful of inputs.

**[`CTC_Conference_PL_Builder.xlsx`](CTC_Conference_PL_Builder.xlsx)** — open it, fill in the
yellow cells, tick the scope, read the P&L. Every number is a live formula.

## Tabs

| Tab | What it does |
|---|---|
| **INPUTS** | The only place you type numbers. Event size, schedule, staffing, rates, fees. |
| **SCOPE** | All 56 sub-items from the 2026 Master Proposal Template. Yes/No each, plus a per-line hour override. |
| **P&L** | Reads out at the proposal's **top-level headings** — VENUE SOURCING, VENUE MANAGEMENT, EVENT BRANDING… |
| **HOW TO USE** | One page explaining the scale index and the money. |

## Scope of work

The SCOPE tab mirrors the proposal exactly, sub-item by sub-item:

```
VENUE SOURCING: Request for Proposal
VENUE SOURCING: Venue/Hotel Analysis
VENUE SOURCING: Site Visits
VENUE SOURCING: Contract Negotiations
TOURNAMENTS: Venue Booking & Coordination
TOURNAMENTS: Registration & Communications
TOURNAMENTS: Check-In & Onsite Management
...
```

The P&L rolls these into the 20 top-level headings, so the P&L reads the same way the
proposal does. Turn on one sub-item or all four — the heading appears once either way, and
disappears entirely if nothing under it is selected.

**One item is not in the proposal:** `EVENT BRANDING: Graphic Design (add-on)`, defaulted to
**No**. Two of the three reference P&Ls billed 55–65 hours for graphic design as a separate
line, so leaving it out made those events impossible to reproduce. It sits inside the branding
block and stays invisible unless you sell it.

## The Event Scale Index — the new hour model

The old drivers were flat percentages of attendance ("10% of attendees = hours"). Those were
fitted on small events and break at scale: 10% of 1,500 attendees is 150 hours of branding
work, and no event has ever been billed that way.

What the numbers actually show is that hours grow **sub-linearly** with size. Total
pre-planning hours across the reference events were 263 at ~200 attendees, 617 at 500, and
1,182 at 1,500 — attendance rose 7.5×, hours rose 4.5×.

So most lines are now priced as **a base weight × an Event Scale Index**:

```
ESI = (attendees / 250)^(1/3)  ×  (planning months / 6)^(1/2)  ×  (event days / 3)^(1/4)
```

ESI = 1.00 is a 250-person, 3-day event with 6 months of planning. Doubling attendance raises
it ~26%, not 100%. Each scope line carries a base weight — its hours at ESI 1.00 — so the
whole library scales together and stays in proportion.

Divide each event's real hours by its ESI and the implied base weights come out nearly
identical across all three events, which is the evidence the index is doing real work:

| Line | LCT ÷ 0.76 | AFCI ÷ 1.54 | WTUI ÷ 2.23 |
|---|---|---|---|
| Venue Management | 26 | 23 | 31 |
| Event Branding | 24 | 16 | 22 |
| Post-Event | 11 | 10 | 9 |
| Planning / Timeline | 11 | 10 | 7 |

**Lines with a real count behind them skip the index** and bill directly, because that matched
history exactly:

| Line | Driver |
|---|---|
| Exhibit Management | exhibitors × 1 hr — *WTUI billed 200 for 200 exhibitors, LCT 35 for 35* |
| Sponsor Management | sponsors × 1 hr |
| Speaker Management | speakers × 1 hr, split 0.7 prep / 0.3 onsite |
| Third Party Vendors | vendors × 5 hrs |
| Site Visits | site visits × 10 hrs |
| Meetings, PM system, approvals | 1 hr per planning week each |

Disagree with any line? Type a number into **OVERRIDE HOURS**. Nothing else changes.

## How well it reproduces the reference P&Ls

Each event's real inputs and real scope selection fed back through the model:

| Event | Pre-planning hrs | Pre-planning $ | Onsite hrs | Onsite $ | Client subtotal |
|---|---|---|---|---|---|
| LCT / Marine Recreation 2026 | **+3%** | **+2%** | exact | +4% | **+3%** |
| AFCI Studio Summit 2027 | −6% | −5% | exact | −10% | −7% |
| WTUI 2027 | +5% | −5% | exact | exact | −4% |

Every line is within 10%, most within 5%. Onsite hours land **exactly** on all three once the
manager hours-per-day input is set to what each event actually billed (14 for LCT, 12 for
AFCI, 10 for WTUI). AFCI's onsite dollars read low because it carried three production
assistants at $45/hr, which this model prices as coordinators.

Run `python3 validate_against_history.py` to reproduce, or `-v` for the per-heading breakdown.

## Rates and money

- Manager **$60/hr** cost, coordinator **$42/hr** cost.
- Onsite is split **per person** — one row each, driven by headcount. Pre-planning rolls up
  **by category**, with headcount setting the weekly-meeting rate and the workload check.
- Client rates: manager $90 / coordinator $65 pre-planning, manager $100 onsite, coordinator
  overtime at 1.5×.
- **Staff overhead $0.61 × every staff hour** — a cost, not billed, so it reduces margin.
- **Admin fee 2% of the client subtotal** — added on top, nothing costs against it.
- Multi-year discount 5%, off unless switched on.

## Look

Matches the house style from the reference P&Ls: magenta title bar with yellow type, blue
section bands, pink totals rows, Poppins headings over Barlow body, `$#,##0.00` rates. No
other conference is named anywhere in the workbook.

## Files

| File | What it is |
|---|---|
| `CTC_Conference_PL_Builder.xlsx` | The template. This is the deliverable. |
| `build_pl_template.py` | Generates it. Edit the `SCOPE` list to change items or base weights, then re-run. |
| `validate_against_history.py` | Back-test against the three reference events. |

```bash
python3 build_pl_template.py
python3 /root/.claude/skills/synced/xlsx/scripts/recalc.py CTC_Conference_PL_Builder.xlsx 240
python3 validate_against_history.py -v
```

## Open item

**Admin fee base.** Implemented as 2% of the client subtotal (pre-planning + onsite +
overhead), charged on top and before any multi-year discount. If you meant 2% of our internal
cost or of the post-discount total, it is a one-cell edit at `C10` on the P&L tab.
