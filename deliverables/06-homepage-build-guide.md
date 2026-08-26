# Homepage Rework — Divi / WordPress Build Guide
*Step-by-step instructions to rebuild the CTC homepage **in the existing Divi builder** to match the approved mockup. No migration. Hand this to whoever has WordPress admin + Divi access.*

**Reference mockup (open side-by-side while building):**
- Full homepage: https://claude.ai/code/artifact/337443c3-7ebe-4a72-82e6-0f881f0c6fbc
- Above-the-fold (desktop + mobile): https://claude.ai/code/artifact/be01f529-9424-4ce5-aa72-f3c327c8b8c7

Brand + copy source of truth: `05-brand-and-voice.md`. Every finding ID (S-1, AI-2…) refers to `02-website-audit.md`.

---

## 0. Before you touch the builder (30 min)
1. **Back up** the site (UpdraftPlus or host snapshot) and **build on a staging copy** if possible.
2. **Global fonts (Divi → Theme Customizer → General → Typography):** set **Heading font = Poppins**, **Body font = Barlow**. *(Divi pulls both from Google Fonts natively. For speed, later self-host via a plugin — see §9.)*
3. **Brand color palette (Divi → any color picker → save to the global palette):**
   `#1F243D` navy · `#417CBC` royal blue · `#EE6197` pink · `#8B5FBF` purple · `#E5E8F8` periwinkle · `#F7F9FD` off-white · `#4C5773` slate.
4. **Primary button gradient (Theme Customizer → Buttons):** background = gradient **`#EE6197 → #8B5FBF → #417CBC`** (100°), text white, fully rounded (border-radius 999px), no border.
5. Create the page: **Pages → Add New → "Home" → Use Divi Builder → Build From Scratch.** (Or edit the existing Home and rebuild section by section so you can revert.)

> **Rule of thumb:** one **Section** per band below; inside it a **Row** with the column layout noted; inside columns the **Modules** listed. Set section/row **max-width to 1160px** and consistent vertical padding (~80px desktop / 48px mobile).

---

## 1. Header / menu (global)
Use **Divi Theme Builder → Global Header** (or the Divi menu):
- Left: logo (the "Coast to Coast" wordmark with the gradient rule + "Conferences & Events" microtype).
- Center/right menu: **What We Do · Why CTC · Industries · Case Studies · About**. *(No format pages — "Services" is a single "What We Do" page.)*
- Right: **"Request a Proposal"** button (primary gradient), sticky on scroll.
- Enable a **sticky, translucent header** (Divi row → Scroll Effects / sticky position).

## 2. Hero section  *(fixes U-1, U-3; the above-the-fold screen)*
**Section:** background `#F7F9FD` (subtle radial pink top-right + blue bottom-left via Divi gradient background if desired).
**Row:** **two columns (≈55% / 45%)**, vertically centered.

**Left column (copy):**
1. **Text module — eyebrow:** `Certified woman-owned · Long Beach, CA · Since 1994` (Poppins 600, 12px, letter-spacing, navy-blue, in a periwinkle pill — style via the module's Background + rounded border).
2. **Text/Heading module — H1:** `In-person events, run *flawlessly* — for 15–40% less.` Poppins 800, ~clamp 40–60px, navy. Wrap **flawlessly** in `<span style="color:#EE6197;font-style:italic;">flawlessly</span>`. **No cursive font** (script is print-only).
3. **Text module — subhead (story, not stats — the tiles carry the numbers):** `Coast to Coast Conferences & Events is your full-service event partner — since 1994, sweating every detail so your team can enjoy the room. Real expertise, real relationships, real energy behind every event.` Barlow, slate, ~19px.
4. **Two Button modules in a row:** `Request a Proposal` (primary gradient) + `See Case Studies` (ghost: transparent, 1px slate border).

**Right column (photo — the above-the-fold visual):**
- **Image module** with the **hero photo** (see §8). Rounded corners (~22px), soft shadow. Add descriptive **alt text** ("CTC-managed conference on the Long Beach waterfront") for accessibility + image SEO (C-5).
- Optional overlay stat ("2,500+ events since 1994") via a small Text module positioned over the image (Divi absolute position) — matches the mockup.

**Below the row — proof strip:** a **4-column row**, each column a Text module styled as a card (white bg, 1px `#E3E7F3` border, 14px radius):
`15–40%` **Saved on event costs** · `25%` **Of your time, back** · `2,500+` **Events produced** · `3M+` **Attendees served**. Numbers Poppins 800 (first two **pink**, last two **navy**); labels slate 13px. Enable **tabular numbers** (custom CSS `font-variant-numeric:tabular-nums`).

**Trust pills row:** a Text module — "Trusted across" + pills: Corporate · Associations · Government · Nonprofit · Sports & Rec.

## 3. AI-answer definition block  *(AI-3 — the sentence built for Gemini)*
Single Text module in a bordered white card, small pink "Written for AI Overviews" chip:
> Coast to Coast Conferences & Events (CTC) is a certified woman-owned, full-service event management company headquartered in Long Beach, California, producing conferences and events for up to 10,000 daily attendees. Founded in 1994, CTC has produced 2,500+ events and is known for cutting event costs 15–40% while giving clients back 25% of their time.

**This exact text is mirrored in the Organization/LocalBusiness JSON-LD (§7 / AI-2).**

## 4. What we do — ONE event-management service  *(fixes T-2, C-1, C-7)*
**Section** white. Kicker "What we do" + H2 `One partner. Every detail.` (pink *italic* on "Every detail").
- **Lede (Text module):** "Full-service event management — we own every moving part from first plan to final teardown, so your team can focus on your people, not the run-of-show. **Whatever your event, wherever it happens**, we make it flawless: board meetings to 10,000-attendee programs, budgets to $8M."
- **No format cards.** "Events, not formats" is structural — a single service, stated as a confident capability. Team energy is NOT here; it lives in §4b (Why CTC).

**Scope-of-work chip cloud:** a Text module with pill-styled links: *Venue & Hotel Negotiation · Registration & Badging · Housing & Room Blocks · Food & Beverage · Event Branding & Signage · **Sponsorship Management** · Speaker Management · Programming & A/V · Stage Production · Exhibit Management · VIP & Press Logistics · Reception Planning · Event Marketing · Financial Management · Onsite Management · Tournaments.*
> **Wording rules:** "**Sponsorship Management**" (never sponsor sales/sourcing) and "**Venue & Hotel Negotiation**" (no room-night stat).

## 4b. Why CTC — the believability beat  *(makes the 15–40% credible)*
**Section** white. Kicker "Why CTC" + H2 `Where the savings actually come from.` (pink *italic* on "actually").
Lede: "Cutting 15–40% isn't corner-cutting — it's what 30 years of relationships, expertise, and a proven process make possible." **Row: 2×2 cards** (Blurb modules):
- **Relationships that pay off** — 30 yrs of vendor/venue/hotel relationships → rates, availability, leverage. *(This is where the 15–40% comes from.)*
- **Expertise you can lean on** — 2,500+ events, 70+ combined years; we've navigated it before.
- **A partner, not a vendor** — one dedicated team, your goals first; 75% of clients return.
- **Energy that shows up** — we love this work and the people; your attendees feel it. *(This is the "team energy" home.)*

## 4c. Who we serve — industries  *(place after Case Study)*
**Section** white. Kicker "Who we serve" + H2 `Trusted across every room.` **Row: 3-col cards** — Corporate · Associations · Government (woman-owned + NAICS) · Nonprofit · Sports & Community · a dark "Your industry, next → Request a Proposal" CTA card.

## 5. How we work — the 4-phase methodology  *(AI-8 — ownable, citable content)*
**Section**; **4-column row**, each a numbered card (Number Counter or styled Text): **Onboarding → Project Management → Onsite Experience → Post-Event Report**, each naming its asset (Welcome Guide · Master Event Showbook · Onsite Event Guide · Post-Event Report). Gradient numerals.

## 6. Proof band + Case study
- **Proof band (dark section, navy bg):** 3–6 stat columns — **2,500+ events · 3M+ attendees · 75% client return · $8M largest budget · 10,000 daily attendees · 70+ yrs combined team**. **Use only these verified numbers** — do NOT add the legacy 30%/50%/60%/5,000/90% claims.
- **Case study teaser:** two-column row (copy + dark image/quote block). Use only clients **cleared for public reference**. Rebuild "Past Events" into structured, metric-led stories (C-3).

## 7. FAQ + schema  *(AI-2, AI-3 — highest-leverage AEO element)*
- Use Divi's **Accordion/Toggle module** for the visible FAQ (the 5 Q&As in the mockup: what is CTC, where located, event size, how it saves money/time, woman-owned/gov).
- **Add `FAQPage` + `Organization` + `LocalBusiness` JSON-LD.** Easiest path: install **Rank Math** (or **Yoast**) and use its schema blocks, OR drop a **Code module** in the footer with hand-written JSON-LD. Include: NAP (Downtown Long Beach), `sameAs` (LinkedIn, Facebook, Crunchbase), founding 1994, **woman-owned** flag, and NAICS/CAGE/CA-Seller-of-Travel identifiers for gov search.
- **Validate every type** in Google's **Rich Results Test** before publishing.

## 8. Hero photo — recommendation *(you approve + license)*
- **Ideal shot:** a real **CTC event** (full room / stage / registration energy) OR the **Long Beach waterfront**, treated as a **duotone in brand navy `#1F243D` → `#417CBC`** so it sits in the palette (matches the mockup placeholder).
- **Format & size:** export **WebP/AVIF**, ~1600px wide, compressed <200KB; provide a 2x for retina. (S-1)
- **Performance:** set the hero image `loading="eager"` + `fetchpriority="high"`; lazy-load everything below the fold. (S-7)
- **Sourcing:** first choice = your own event photography (best authenticity + SEO). If licensing stock for the waterfront: Adobe Stock / Getty / Stocksy — search "Long Beach California waterfront skyline." Apply the duotone in Photoshop or via a Divi image filter (grayscale + brand color overlay). **Send me 2–3 candidates and I'll mock them in.**

## 9. Speed pass (Divi-specific)  *(fixes S-1…S-7)*
- **Images:** convert to WebP + compress site-wide — **Imagify / ShortPixel / Smush**.
- **Caching + critical CSS + defer JS:** **WP Rocket** (or Divi's built-in **Performance** panel: enable Dynamic CSS, Dynamic Module Framework, Critical CSS, defer jQuery/gutenberg, disable unused features).
- **Fonts:** self-host Poppins/Barlow (WP Rocket / OMGF) with `font-display:swap` + preload the hero weight. (S-4)
- **Audit plugins:** deactivate unused plugins/sliders adding render-blocking JS. (S-2)
- **Re-test** in PageSpeed Insights (mobile + desktop) before/after and log the delta in the scorecard.

## 10. Crawlability + technical (do these regardless of the homepage)  *(T-1/AI-1, T-2, T-5)*
- **Cloudflare/robots:** confirm the bot rule that 403s crawlers **allows `Googlebot`, `Google-Extended`, `Bingbot`**. Add `/llms.txt`. (AI-1, AI-5)
- **301 redirects & de-dupe:** merge `/blog/` + `/blogs-2/` + `/content-hub/` → one Resources hub; consolidate the two event-management pages; **merge hybrid-virtual + virtual-event-depot → one page**; 301 legacy brand URLs. (T-2, T-3)
- **Titles/meta:** apply the page-by-page titles/H1s from `03-revision-plan.md §3` via Rank Math/Yoast. (T-4)
- **Submit** the XML sitemap in Google Search Console. (T-5)

---

## Build order (fastest path to value)
1. Global fonts + palette + button gradient (§0).
2. Hero (§2) with a **placeholder** image → this alone lifts above-the-fold conversion + gives Gemini the entity block.
3. AI definition + FAQ + schema (§3, §7) → the AEO win.
4. Services + scope + methodology (§4, §5).
5. Proof + case study (§6).
6. Speed pass (§9) + crawl/redirects (§10).
7. Swap the placeholder for the licensed hero photo (§8).

## Verification
- Preview on **desktop + mobile**; compare to the mockup.
- **Rich Results Test** passes for Organization/LocalBusiness/FAQPage.
- **PageSpeed Insights** mobile score improves; CWV toward "Good."
- Fetch the homepage as Googlebot (Search Console URL Inspection) → renders, not 403.
- Record Week-0 baselines in the scorecard.
