# CTC Website Revision Plan
**Coast to Coast Conferences & Events** · Turns the audit findings into sequenced, build-ready work.

> Copy below is **draft, pending questionnaire confirmation** of the value-prop numbers and voice. Titles/meta are written to be pasted straight into WordPress (Yoast/RankMath). Every item traces to an audit finding ID.

---

## 0. Brand alignment (do this first)
Realign the site to the **2026 proposal brand** (full spec in `05-brand-and-voice.md`): Poppins + Barlow + Amsterdam Three script; navy `#1F243D` / royal blue `#417CBC` / pink `#EE6197` with the pink→purple→blue logo gradient; "Your Event Partner" positioning; and the current proof numbers (2,500+ events, 3M+ attendees, 75% return, 10,000 daily attendees, $8M). Surface **certified woman-owned** and the **named methodology** (Onboarding → Project Management → Onsite Experience → Post-Event Report) prominently. The mockups already implement this.

## 1. Information architecture (proposed)

**Problem:** duplicate/fragmented pages (T-2) dilute authority and confuse crawlers + AI.

**Proposed sitemap:**
```
Home
├── Services
│   ├── In-Person Events & Conferences   ← PRIMARY service (lead here)
│   └── Hybrid & Virtual  (ONE merged page — secondary; incl. Virtual Event Depot)
├── Industries              ← NEW hub (Associations, Corporate, Government, Nonprofit, Sports/Endurance)
├── Case Studies            ← rebuild of "Past Events" as structured, metric-led stories
├── About
│   ├── Our Story (1994→today, the rebrand)
│   └── Our Team
├── Resources  (single content hub — merge /blog/, /blogs-2/, /content-hub/)
├── FAQ                     ← NEW, schema-marked, feeds AI answers
└── Contact / Request a Proposal
```

**Consolidation actions:**
- Merge `/blog/`, `/blogs-2/`, `/content-hub/` → one **Resources** hub; 301 the losers. *(T-2)*
- Pick ONE canonical event-management page; 301 `/event-management-usa/` into it (or repurpose as a national landing page with distinct intent). *(T-2, C-1)*
- 301 all legacy `CTC Destination & Meeting Management` URLs → successors. *(T-3)*
- Add contextual internal links between Services ⇄ Industries ⇄ Case Studies. *(T-6)*

---

## 2. Homepage above-the-fold rewrite *(U-1, U-3, AI-3)*

The first screen must answer **what / who / where + proof + one action** — for humans *and* for the AI engine that will summarize the page.

**Draft copy** (visualized in `/mockups/homepage-hero.html`, built in the **current brand**: Poppins/Barlow, navy-blue-pink gradient, Sacramento script accent):

- **Eyebrow:** `Certified woman-owned · Long Beach, CA · Since 1994`
- **H1:** `In-person events, run flawlessly — for 15–40% less.` *(with "flawlessly" as a pink **italic** accent — no cursive on the web)*
- **Subhead:** `Coast to Coast Conferences & Events (CTC) is your full-service partner for in-person events and conferences. Since 1994 we've produced 2,500+ events for up to 10,000 daily attendees — cutting event costs 15–40% and giving back 25% of your time. Real expertise, real relationships, real energy — it's why 75% of clients come back, year after year.`
- **Proof strip (4 stat tiles):** `15–40% cost saved` · `25% time back` · `2,500+ events` · `3M+ attendees`
- **Primary CTA:** `Request a Proposal` (logo gradient) · **Secondary:** `See Case Studies`
- **Trust row:** market-segment pills (Corporate / Associations / Government / Nonprofit / Sports & Rec); swap for cleared client logos when available.

> **Why this wording:** it packs the exact entity facts (name, service, location, founding year, scale, quantified benefit) into two sentences an AI Overview can lift verbatim — while reading as confident human copy.

---

## 3. Page-by-page title tags, meta descriptions & H1 *(T-4, C-1, C-4)*

*Draft — confirm numbers/voice first. Format: **Title** (≤60 char target) / **Meta** (≤155 char) / **H1**.*

**Home**
- Title: `In-Person Event Management Company in Long Beach, CA | CTC`
- Meta: `Certified woman-owned, full-service in-person event & conference management since 1994. We run events up to 10,000 attendees and cut event costs 15–40%. Get a proposal.`
- H1: `In-person events, flawlessly run — for 15–40% less.`

**In-Person Events & Conferences** *(primary service page)*
- Title: `In-Person Event & Conference Management | CTC`
- Meta: `From board meetings to 10,000-attendee conferences — venue & hotel negotiation, logistics, registration, onsite management and exhibitor coordination, handled end to end.`
- H1: `In-person events, managed down to the last detail.`

**Hybrid & Virtual** *(ONE merged, secondary page)*
- Title: `Hybrid & Virtual Event Management | CTC`
- Meta: `When your event goes beyond the room, CTC extends it online — the right technology and genuine engagement, measured from registration to report. Incl. Virtual Event Depot.`
- H1: `Hybrid & virtual, when the moment calls for it.`

**Industries (hub)**
- Title: `Event Management for Associations, Corporate & Government | CTC`
- Meta: `Specialized event management for associations, corporations, nonprofits and government — matched to your audience, goals and budget.`
- H1: `Event expertise for your industry.`

**Case Studies**
- Title: `Event Management Case Studies & Results | CTC`
- Meta: `Real CTC events with real numbers: cost savings, attendee satisfaction and sponsor lead growth. See how we deliver.`
- H1: `Proof, by the numbers.`

**About / Our Story**
- Title: `About CTC — Event Experts Since 1994 | Long Beach, CA`
- Meta: `Coast to Coast Conferences & Events has produced flawless events for 32 years. Meet the team and the story behind the Long Beach-based firm.`
- H1: `32 years of getting events right.`

**Contact**
- Title: `Request a Proposal | Coast to Coast Conferences & Events`
- Meta: `Tell us about your event and get a tailored proposal from CTC's Long Beach team. In-person, hybrid or virtual — 100 to 10,000+ attendees.`
- H1: `Let's plan your event.`

*(Remaining pages follow the same pattern; full sheet delivered with the copy pass.)*

---

## 4. AI-searchability build (AEO) *(AI-1…AI-6)*

1. **Unblock crawlers** — adjust Cloudflare bot rule + robots.txt to explicitly allow `Googlebot`, `Google-Extended`, `Bingbot`, `DuckDuckBot`; verify with live fetch tests. *(AI-1, T-1)*
2. **Structured data** (JSON-LD in `<head>`):
   - `Organization` + `LocalBusiness` — name, logo, NAP, geo, hours, sameAs (LinkedIn, Facebook, Crunchbase); include the **woman-owned** signal and NAICS/registration identifiers (561920, CAGE 5SN86, CA Seller of Travel) for trust + government-procurement search.
   - `Service` — in-person event planning (primary) + one merged hybrid/virtual; plus the deeper scope where relevant.
   - `FAQPage` on the FAQ + service pages.
   - `BreadcrumbList` site-wide; `Review`/`AggregateRating` where legitimately sourced.
   - Validate every type in **Google Rich Results Test**.
3. **Answer blocks** — add a concise **FAQ** answering the ~15 buyer questions (questionnaire §6), each a self-contained, quotable answer. Example:
   > **Q: Where is Coast to Coast Conferences & Events located?**
   > A: CTC is headquartered in Downtown Long Beach, California, and produces events nationwide.
4. **Consistent boilerplate + NAP** everywhere (site footer, schema, GBP, directories) using the approved questionnaire §3 boilerplate. *(AI-4)*
5. **Citable proof** — present the 15–40% / 25% stats with brief context + "as of 2026" framing. *(AI-6)*
6. **Add `/llms.txt`** — name, one-line description, key URLs, boilerplate. *(AI-5)*

---

## 5. Speed build *(S-1…S-7)*
- Convert images to WebP/AVIF, compress, and serve responsive sizes; add `fetchpriority=high` to the hero, `loading=lazy` below the fold. *(S-1, S-7)*
- Audit + remove/replace heavy plugins; defer non-critical JS; inline critical CSS. *(S-2, S-3)*
- `font-display: swap` + preload primary font. *(S-4)*
- Confirm full-page caching + CDN + long cache-control on static assets. *(S-5)*
- Add explicit width/height to media to kill CLS. *(S-6)*
- **Target:** mobile PageSpeed 50→85+, all three CWV in "Good."

---

## 6. Prioritized roadmap (mapped to Wednesday sessions)

| Phase | Timeframe | Focus | Key items |
|-------|-----------|-------|-----------|
| **P0 — Quick wins** | Weeks 1–2 | Unblock + baseline + fast fixes | Fix crawler 403 (AI-1/T-1), submit sitemap, image compression (S-1), homepage hero copy + trust row (U-1/U-3), add `Organization`/`LocalBusiness` schema, GBP cleanup, set baselines in scorecard |
| **P1 — Structural** | Weeks 3–6 | Consolidate + optimize + AEO depth | De-dupe pages + 301s (T-2/T-3), keyword→page map + title/meta rollout (T-4/C-1), `Service`/`FAQPage` schema + FAQ answer blocks (AI-2/AI-3), plugin/JS trim (S-2/S-3), Case Studies rebuild (C-3) |
| **P2 — Growth engine** | Weeks 7+ | New surface area + content | Industries + city landing pages (C-2), Resources hub merge (T-2), content calendar for the hub, `llms.txt` (AI-5), backlink/GBP campaign for entity corroboration (AI-7), ongoing CWV monitoring |

Each Wednesday session reviews the scorecard, closes P-items, and re-prioritizes.

---

## 7. Open dependencies
- Questionnaire answers (locks value-prop numbers + voice before final copy).
- Access decision: implement on the live WordPress site (needs staging + credentials) **or** rebuild in this repo — deferred per your choice; specs above are build-agnostic.
- Cloudflare/WordPress admin access to apply crawler + schema + speed fixes.
- Confirmed client logos/testimonials we're cleared to publish.
