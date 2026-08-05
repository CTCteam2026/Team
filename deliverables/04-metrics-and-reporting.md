# CTC Metrics & Weekly Reporting Framework
**Coast to Coast Conferences & Events** · Reporting cadence off the **Wednesday working sessions**.

> **Two audiences, two artifacts:** the **Google Sheet scorecard** is the working data (numbers, week over week); the **CEO email** is the narrative wrapper (what moved, why it matters, what's next). This doc defines both, plus every metric.

---

## 1. Cadence
- **Wednesday session:** review last week's scorecard, close completed revision items, re-prioritize the roadmap, capture new numbers.
- **Wednesday PM (same day):** update the scorecard tabs; send the CEO email.
- **Baseline = Week 0**, captured before any changes ship, so every later number shows delta vs. start.

---

## 2. The scorecard (Google Sheet)
Seed file: `reporting/weekly-scorecard.xlsx` (import to Google Sheets, or I can create it directly in your Drive). Structure:

**Tab 1 — Progress (execution health)**
| Metric | Baseline | Target | This week | Δ vs. last | Status |
|---|---|---|---|---|---|
| Revision items planned (this phase) | | | | | |
| Revision items completed | | | | | |
| P0 / P1 / P2 burn-down (% done) | | | | | |
| Pages shipped/updated | | | | | |
| Mockups approved | | | | | |
| Open blockers | | | | | |

**Tab 2 — Marketing performance (outcomes)** — grouped below.

**Tab 3 — AI visibility tracker** — the ~15 buyer questions × month, marked ✅ cited / ➖ present / ❌ absent in Gemini/Google AI Overview.

**Tab 4 — Notes/decisions log** — what changed and why (context for the CEO + future you).

Each metric row carries a **RAG status** (🟢 on/ahead of target, 🟡 slipping, 🔴 off track) that drives the email summary.

---

## 3. Progress metrics (are we executing?)
- Revision items planned vs. completed (per phase).
- P0/P1/P2 burn-down %.
- Pages shipped / updated this week.
- Mockups approved.
- Blockers open + age.

## 4. Marketing performance metrics (is it working?)

**a) Page speed**
- Mobile & desktop **PageSpeed** score (Home + key pages).
- **Core Web Vitals:** LCP, INP, CLS (target all "Good": LCP <2.5s, INP <200ms, CLS <0.1).
- Source: PageSpeed Insights / CrUX / Search Console CWV report.

**b) SEO visibility**
- Search Console: **impressions, clicks, avg. position, CTR** (site + top pages).
- **Keywords ranking top 3 / top 10** (tracked set).
- **Indexed pages** count (should stabilize/rise as duplicates are consolidated + 301'd).
- **Referring domains / backlinks** (trend).

**c) AI searchability** *(the priority metric)*
- **# of tracked buyer questions where CTC appears/gets cited** in Gemini/Google AI Overview (out of ~15).
- **Google Business Profile:** views, searches, actions (calls/clicks/directions).
- **Branded search volume** (proxy for entity strength).
- `Google-Extended` crawl access = allowed (binary check).

**d) Conversion**
- **Organic sessions** (GA4).
- **RFP / contact-form submissions** (primary conversion).
- **CTA click-through rate.**
- **Engagement rate / bounce**, avg. engagement time.

> Set a **baseline and target** for every metric in §4. Targets get sharper after the Week-0 measurement pass.

---

## 5. The CEO email
Template: `reporting/ceo-email-template.md`. Sent every Wednesday. Keep it to one screen: **Headline → what moved → why it matters → what's next → one risk/ask.** The scorecard link carries the detail; the email carries the meaning.

---

## 6. Tooling checklist (set up in Week 0)
- [ ] Google Search Console — verified, sitemap submitted.
- [ ] GA4 — organic + conversion events (RFP form) configured.
- [ ] PageSpeed Insights / WebPageTest — baseline pages saved.
- [ ] Rank tracking for the target keyword set.
- [ ] Google Business Profile — claimed + insights access.
- [ ] AI-visibility log — 15 buyer questions defined (from questionnaire §6).
- [ ] Scorecard Google Sheet — shared with the team + CEO (view).
