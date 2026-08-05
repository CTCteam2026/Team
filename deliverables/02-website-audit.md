# CTC Website Audit — ctcconferences.com
**Coast to Coast Conferences & Events** · Objective: **page speed ↑, SEO visibility ↑, AI searchability ↑ (Gemini above-the-fold answers)**

> **How to read this:** each finding has a **Severity** (🔴 High / 🟠 Medium / 🟡 Low), an **Impact area** (Speed / SEO / AI / UX), and an **Effort** (S/M/L). The revision plan (`03-revision-plan.md`) turns these into a sequenced roadmap.
>
> **Method note:** the live site returns **HTTP 403 to automated crawlers** (Cloudflare bot rule). Findings below combine what's publicly indexed + structural/heuristic review of a WordPress event site. Items marked **⧗ confirm-live** need a hands-on pass with browser DevTools + PageSpeed Insights + Search Console during Week 0 — those tools run as a real browser and aren't blocked. The 403 itself is finding **T-1** and is directly relevant to the AI goal.

---

## Executive summary
CTC has genuinely strong raw material — 32 years, a quantified value prop (15–40% cost / 25% time), a real Long Beach HQ, and multiple service lines. The problem is **not the story; it's how the site packages it for three modern readers: the browser (speed), the search crawler (SEO), and the AI answer engine (AEO).**

> **Added after reviewing the 2026 Master Proposal:** the **website materially lags the current brand.** The proposal shows a stronger identity (Poppins/Barlow, navy-blue-pink gradient, "Your Event Partner"), stronger proof (**2,500+ events, 3M+ attendees, 75% client return, up to 10,000 daily attendees, $8M budgets**), a **certified woman-owned** credential, and a far deeper **scope of work + named methodology** — almost none of which the live site surfaces. Realigning the site to the proposal is itself a major SEO/AEO and conversion upgrade. Details in `05-brand-and-voice.md`.
>
> - **B-2 (new, 🔴 SEO/AI):** "Certified woman-owned" is a high-value trust + government-procurement signal absent from the site's messaging and schema.
> - **C-7 (new, 🟠 SEO/AI):** The site markets only 3 formats; the real 20+ service scope-of-work (a keyword goldmine) is missing.
> - **AI-8 (new, 🟠 AI):** Named methodology (Welcome Guide, Master Event Showbook, Onsite Event Guide, Post-Event Report) is distinctive, ownable, citable content that doesn't exist on the site.

Top themes:
1. **AI answer engines may be partially locked out** (aggressive Cloudflare 403 + likely thin structured data). This is the single biggest lever for the Gemini goal.
2. **Content is fragmented and duplicative** (`/blog/` vs `/blogs-2/`, `/event-management/` vs `/event-management-usa/`, multiple legacy brand pages) — diluting authority and confusing both Google and AI about the canonical page for each topic.
3. **The above-the-fold homepage likely under-sells the quantified value prop** and buries the "what/who/where" that AI answers need in one clean sentence.
4. **Speed is almost certainly image- and plugin-driven** (typical of long-lived WordPress event sites) — high-ROI, low-risk fixes.

---

## A. Page speed & Core Web Vitals

| # | Finding | Sev | Impact | Effort |
|---|---------|-----|--------|--------|
| S-1 | **Image weight** — event sites carry large hero/gallery photos; likely served as JPG/PNG, not WebP/AVIF, and not responsively sized. Biggest LCP driver. **⧗ confirm-live** | 🔴 | Speed | M |
| S-2 | **WordPress plugin/script bloat** — accumulated plugins (sliders, forms, analytics, chat) add render-blocking JS/CSS. **⧗ confirm-live** | 🔴 | Speed | M |
| S-3 | **Render-blocking resources & no critical-CSS** — CSS/JS in `<head>` delays first paint. **⧗ confirm-live** | 🟠 | Speed | M |
| S-4 | **Web-font loading** — custom fonts without `font-display: swap`/preload cause invisible-text/CLS. **⧗ confirm-live** | 🟠 | Speed/UX | S |
| S-5 | **Caching / CDN** — confirm full-page cache + CDN in front of Cloudflare; verify long cache-control on static assets. **⧗ confirm-live** | 🟠 | Speed | S |
| S-6 | **No explicit width/height on media** → layout shift (CLS). **⧗ confirm-live** | 🟡 | Speed/UX | S |
| S-7 | **Above-the-fold not prioritized** — hero image should be `fetchpriority=high`, below-fold images `loading=lazy`. | 🟡 | Speed | S |

**Week-0 measurement:** run **PageSpeed Insights** (mobile + desktop) and **WebPageTest** on Home, a service page, and Past Events. Record LCP / INP / CLS + scores as the baseline in the scorecard.

---

## B. Technical SEO

| # | Finding | Sev | Impact | Effort |
|---|---------|-----|--------|--------|
| T-1 | **Cloudflare returns 403 to non-browser agents.** Blocks some SEO tools and — critically — risks blocking legitimate **AI/answer crawlers** (see D). Must verify the rule allowlists Googlebot, Google-Extended, Bingbot, etc. | 🔴 | SEO/AI | S |
| T-2 | **Duplicate / overlapping pages** — `/blog/` vs `/blogs-2/` vs `/content-hub/`; `/event-management/` vs `/event-management-usa/`; legacy `/ctc-destination-meeting-management/`. Splits ranking signals & confuses canonical topic authority. | 🔴 | SEO/AI | M |
| T-3 | **Legacy brand/redirect hygiene** — old "CTC Destination & Meeting Management" URLs should 301 to their canonical successors; confirm no orphan/duplicate brand pages competing. | 🟠 | SEO | M |
| T-4 | **Title tags & meta descriptions** — several observed titles are generic/repetitive ("Expert Event Management \|Coast to Coast…") and some carry a stray leading space/pipe. Each page needs a unique, keyword- + intent-led title and a written meta description. **⧗ confirm-live** | 🟠 | SEO | M |
| T-5 | **XML sitemap & robots.txt** — confirm a clean sitemap is submitted to Search Console and robots.txt doesn't block assets or AI crawlers. **⧗ confirm-live** | 🟠 | SEO/AI | S |
| T-6 | **Internal linking / IA depth** — service pages appear siloed; weak contextual interlinking limits crawl + topical authority. | 🟠 | SEO | M |
| T-7 | **Canonical tags** — ensure self-referencing canonicals and that duplicates point to the chosen canonical. **⧗ confirm-live** | 🟡 | SEO | S |
| T-8 | **Mobile-friendliness & HTTPS** — confirm responsive rendering + no mixed content. **⧗ confirm-live** | 🟡 | SEO/UX | S |

---

## C. On-page & content SEO

| # | Finding | Sev | Impact | Effort |
|---|---------|-----|--------|--------|
| C-1 | **No clear keyword→page map** — pages don't each own a distinct high-intent query; risk of self-cannibalization (esp. the two event-management pages). | 🔴 | SEO | M |
| C-2 | **Missing high-intent pages** — no dedicated **industry** pages (healthcare, gov, associations, sports/marathons) or **city/region** pages, which are how buyers *and* AI engines match intent. | 🟠 | SEO/AI | L |
| C-3 | **Past Events underused as SEO/proof** — success stories should be structured, named case studies with metrics, schema, and internal links (not a flat list). | 🟠 | SEO/AI/UX | M |
| C-4 | **Heading structure** — ensure one clear H1 per page mapped to the target query; logical H2/H3. **⧗ confirm-live** | 🟠 | SEO | S |
| C-5 | **Image alt text** — event photos likely missing descriptive alt (accessibility + image SEO). **⧗ confirm-live** | 🟡 | SEO/UX | S |
| C-6 | **Content freshness** — dated/updated stamps on case studies + blog boost both SEO and AI trust. | 🟡 | SEO/AI | S |

---

## D. AI searchability / AEO — getting into Gemini's above-the-fold answer *(priority lens)*

Being *cited by* an AI Overview is a different game than ranking a blue link. AI engines favor pages that (a) they can crawl, (b) state facts plainly and consistently, (c) carry structured data, and (d) match the entity across the web.

| # | Finding | Sev | Impact | Effort |
|---|---------|-----|--------|--------|
| AI-1 | **Crawler access** — the Cloudflare 403 (T-1) may be excluding AI crawlers. If Gemini/Google's systems can't fetch the page, CTC can't be cited. **Confirm `Google-Extended` is allowed** in robots.txt and not challenged by Cloudflare. | 🔴 | AI | S |
| AI-2 | **Thin/absent structured data** — likely missing `Organization`, `LocalBusiness`, `Service`, and `FAQPage` schema. This is the strongest machine-readable signal of *who/what/where*. | 🔴 | AI/SEO | M |
| AI-3 | **No extractable answer content** — the site describes CTC in prose, but AI engines lift **self-contained sentences**. There are few "question → crisp answer" blocks a model can quote verbatim. | 🔴 | AI | M |
| AI-4 | **Entity inconsistency** — name/description/NAP vary across the site, LinkedIn, Crunchbase, LeadIQ, directories ("CTC," "Coast to Coast," old brand). Inconsistency weakens the entity the model trusts. | 🟠 | AI | M |
| AI-5 | **No `llms.txt`** — an emerging convention that hands AI models a clean map + boilerplate of who you are. Cheap to add, positions CTC ahead of peers. | 🟡 | AI | S |
| AI-6 | **Under-cited proof** — the 15–40% / 25% stats aren't framed as sourced, citable facts (with context/date), which is exactly what AI answers like to quote. | 🟠 | AI/SEO | S |
| AI-7 | **Weak third-party corroboration** — AI trust rises with consistent off-site mentions (GBP, directories, press). Current footprint is thin/dated. | 🟡 | AI | L |

**How we'll measure AI visibility:** define ~15 buyer questions (from questionnaire §6), run them monthly in Gemini/Google, and log whether CTC appears/gets cited in the AI Overview. Baseline in Week 0.

---

## E. Conversion & UX

| # | Finding | Sev | Impact | Effort |
|---|---------|-----|--------|--------|
| U-1 | **Above-the-fold clarity** — the hero likely doesn't answer *what/who/where + proof + one CTA* within the first screen. This hurts conversion **and** gives AI a weak summary to lift. | 🔴 | UX/AI | M |
| U-2 | **CTA hierarchy** — needs one unmistakable primary action (Request a Proposal/Consult) repeated at natural decision points; avoid competing CTAs. | 🟠 | UX | S |
| U-3 | **Trust signals above the fold** — client logos, a headline stat, and a testimonial should appear early; currently likely buried. | 🟠 | UX/AI | S |
| U-4 | **Mobile nav & form friction** — confirm tap targets, sticky CTA, and a short, low-friction RFP form. **⧗ confirm-live** | 🟡 | UX | S |

---

## Priority shortlist (what moves the needle fastest)
1. **AI-1 / T-1** — unblock crawlers (Cloudflare + robots) so AI/search can even read the site. *(High impact, low effort.)*
2. **AI-2 / AI-3** — add `Organization`/`LocalBusiness`/`Service`/`FAQPage` schema + Q&A answer blocks.
3. **S-1 / S-2** — image compression/next-gen formats + plugin/script trim for CWV.
4. **T-2 / C-1** — de-duplicate pages, set canonicals, build the keyword→page map.
5. **U-1 / U-3** — homepage above-the-fold rewrite with proof (see mockups).

*Full sequencing, owners, and copy in `03-revision-plan.md`.*
