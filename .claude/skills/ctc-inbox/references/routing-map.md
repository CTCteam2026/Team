# CTC Routing Map

Maps an email sender to a client, an event, and a ClickUp destination.

**All ClickUp IDs below are real and verified** (pulled from the workspace on 2026-09-09). The `Domains` and `Owner` columns are the parts that need filling in — and they fill themselves in over time via the "New domains to map" step in the skill. Do not sit down and complete this by hand.

Workspace ID: `36249759`
Spaces: `2026 Clients` = `90110201054` · `2027 Clients` = `90114251500` · `CTC Internal` = `48571640`

## Confidence key

- ✅ **Confirmed** — domain verified from a ClickUp guest account on that client's work.
- 🟡 **Inferred** — reasonable guess, needs one human confirmation before trusted.
- ⬜ **Unmapped** — no domain known yet. Route by subject/event name until someone confirms one.

## 2026 client events

Sorted by event date. The `MM-DD` prefix in the folder name **is** the event date — that is the event-proximity signal the priority rules use.

| Event date | Client / Event | Folder ID | List | List ID | Domains | Conf. | Owner |
|---|---|---|---|---|---|---|---|
| 02-06 | ASDA Annual | `90116160669` | Project Management | `901110584093` | `asdanet.org` | ✅ | TODO |
| 03-07 | IgNS Virtual | `90117619684` | Project Management | `901113152694` | — | ⬜ | TODO |
| 03-11 | FerroTec Executive Retreat | `90117497361` | Half Moon Bay | `901112916399` | — | ⬜ | TODO |
| 03-11 | ↳ *(also)* | `90117497361` | Client Experience | `901112916457` | — | | |
| 03-23 | AFCI | `90117420811` | Hollywood, CA | `901112740337` | — | ⬜ | TODO |
| 04-07 | WTUI | `90116251279` | Long Beach, CA | `901112263199` | `wtui.com`, `mrenergy.com`🟡 | ✅ | TODO |
| 04-22 | IIT2026 | `90115149994` | Long Beach, CA | `901108642353` | — | ⬜ | TODO |
| 05-01 | Switch4Good *(sponsor only)* | `90117661405` | Los Angeles, CA | `901113228770` | — | ⬜ | TODO |
| 05-03 | Flying Tigers | `90117346707` | Honolulu, HI | `901112552145` | — | ⬜ | TODO |
| 05-03 | OC Marathon | `90116370425` | Project Management | `901111073351` | — | ⬜ | TODO |
| 05-11 | POLB Green Truck Signing | `90117836956` | LB | `901113504519` | `polb.com` | ✅ | TODO |
| 06-13 | FerroTec Summer Picnics | `90117583581` | NH `901113086309` / CA `901113219192` | — | — | ⬜ | TODO |
| 06-23 | CEOSC Booth | `90117635761` | List | `901113181825` | — | ⬜ | TODO |
| 07-09 | NICA | `90117172425` | Las Vegas, NV | `901112201311` | `infusioncenter.org` | ✅ | TODO |
| 07-12 | FerroTec Talent Planning | `90118057636` | Project Management | `901113961009` | — | ⬜ | TODO |
| 07-12 | ↳ *(also)* | `90118057636` | Client Experience | `901113961010` | — | | |
| 07-26 | CIRM Trainee 2026 | `90117571267` | Project Management | `901113063224` | `cirm.ca.gov` | ✅ | TODO |
| 08-26 | California CASA | `90117554453` | Costa Mesa, CA | `901113029141` | `californiacasa.org` | ✅ | TODO |
| 08-28 | POLB Cargo Security Summit | `90118200771` | Project Management | `901114227184` | `polb.com` | ✅ | TODO |
| 09-12 | WWCCA | `90111525140` | LB City, CA | `901112477912` | — | ⬜ | TODO |
| 09-13 | #Imparables | `90117307547` | Ontario, CA | `901112476428` | — | ⬜ | TODO |
| 09-15 | FerroTec Sales Conference | `90118161938` | Project Management | `901114155615` | — | ⬜ | TODO |
| 10-08 | POLB Small Business Summit | `90117832018` | Long Beach | `901113493186` | `polb.com` | ✅ | TODO |
| 10-15 | IgNS National Conference | `90117843336` | LV, Nevada | `901113517439` | — | ⬜ | TODO |
| 10-24 | West Basin | `90118055189` | El Segundo | `901113956727` | — | ⬜ | TODO |
| 11-02 | LCT | `90118120782` | Newport Beach | `901114085073` | — | ⬜ | TODO |
| 11-07 | LACDA | `90118283193` | LA County | `901114380645` | — | ⬜ | TODO |
| 11-09 | CCBA | `90118204662` | Irvine | `901114234386` | — | ⬜ | TODO |
| 12-05 | FerroTec Holiday Party | `90118135923` | NH `901114115532` / CA `901114119188` | — | — | ⬜ | TODO |
| TBD | MLM Guru | `90117307550` | Peru `901112963238` / Mexico `901112476437` / NY `901112963265` | — | — | ⬜ | TODO |

## 2027

| Event date | Client / Event | Folder ID | List | List ID | Domains | Conf. |
|---|---|---|---|---|---|---|
| 03-21-2027 | WTUI | `90118220418` | Palm Springs, CA | `901114262058` | `wtui.com` | ✅ |

## CTC Internal

Use these for anything that is **not** client-visible — internal FYIs, vendor problems you don't want a client reading, sales, and ops.

| Purpose | Folder | Folder ID | Lists |
|---|---|---|---|
| Sales & marketing | Sales & Marketing | `90090172667` | Q1 `901105518972` · Q2 `901108742438` · Q3 `901108743212` · Q4 `901108743215` · Steps for Onboarding `901114261943` |
| Internal event ops | Events | `90110197033` | Q1 `901100441552` · Q2 `901100441553` · Q3 `901100441554` · Q4 `901100441556` |

## Multi-event clients — domain is NOT enough

These clients have several 2026 events. A `@polb.com` or FerroTec email **must** be disambiguated on subject line, event name, dates, or venue before routing.

- **POLB** — Green Truck Signing (05-11) · Cargo Security Summit (08-28) · Small Business Summit (10-08)
- **FerroTec** — Executive Retreat (03-11) · Summer Picnics (06-13) · Talent Planning (07-12) · Sales Conference (09-15) · Holiday Party (12-05)
- **WTUI** — 2026 Long Beach (04-07) · 2027 Palm Springs (03-21-2027)
- **IgNS** — Virtual (03-07) · National Conference (10-15)

If the email doesn't say which, mark it `⚠️ Event unclear` and ask in the report. Do not guess.

## Known structural problem: list names are inconsistent

Most folders have one list, but the naming has drifted three ways — the template's `Project Management` / `Client Experience`, a city name (`Long Beach, CA`, `Half Moon Bay`), and in one case literally `List`. Rule for the skill:

1. If the folder has exactly one list, use it.
2. If it has `Project Management` and `Client Experience`, put delivery work in Project Management and anything guest-facing in Client Experience.
3. If it has multiple location lists (FerroTec picnics NH/CA, MLM Guru Peru/Mexico/NY), the location must come from the email. Ask if unclear.

*Worth fixing at the source: standardizing every client folder to the template's two lists would make routing deterministic.*

## CTC team

| Name | Email | ClickUp ID |
|---|---|---|
| Madeleine Monroe | madeleine@ctcconferences.com | 54266291 |
| Susannah d'Arcy | susannah@ctcconferences.com | 54194337 |
| Michelle Manire | michelle@ctcconferences.com | 54194340 |
| Krystal Bordner | krystal@ctcconferences.com | 54194342 |
| Calli France | calli@ctcconferences.com | 54148812 |
| Manny Estrada | manny@ctcconferences.com | 75315648 |
| Zia Bella Blair | ziabella@ctcconferences.com | 75353093 |
| Talisha Brantley | talisha@ctcconferences.com | 75393930 |
| Nate Peters | nate@ctcconferences.com | 75541071 |
| Maia Nantais | maia@ctcconferences.com | 81577122 |
| Brooke Abel | brooke@ctcconferences.com | 81577123 |
| Sara Kiper | sara@ctcconferences.com | 87361001 |
| Jennifer Garcia | jennifer@ctcconferences.com | 87405650 |

Anyone whose address is **not** `@ctcconferences.com` is external — treat as client, vendor, partner, or prospect, never as internal.

## Enrichment: HubSpot

HubSpot holds ~7,900 companies, overwhelmingly prospects and cold outreach rather than active clients. **Do not use it as a routing source.** It is useful for exactly one thing: deciding whether an unrecognized sender is a real known contact or cold outreach. Use `search_crm_objects` on COMPANY by domain when a sender is unfamiliar and the answer changes how you'd classify it. Otherwise skip it — it costs a round trip.
