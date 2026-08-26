# CTC custom-HTML pages (hybrid approach)

Hand-coded, SEO-optimized landing pages for the **hybrid** setup: these pages are custom HTML;
the **blog and forms stay in WordPress**.

## Files
- `homepage.html` — complete, standalone homepage (own `<head>` with title/meta/canonical +
  Organization/LocalBusiness + FAQPage JSON-LD, Google Fonts, all sections, footer). Light theme.

## How to publish in WordPress (Divi installed)
Pick one method:

**A. Blank canvas page template (cleanest).**
1. In a **child theme**, add a template `page-blank.php` that outputs `the_content()` with no header/footer builder wrapper (or use a "blank/canvas page template" plugin such as *Blank Slate* / *Fullscreen Templates*).
2. Create the Home page → assign that template → paste the **`<body>` contents** of `homepage.html` into a full-width **Custom HTML** block/module.
3. Put the `<head>` bits (title, meta description, canonical, the two JSON-LD `<script>` blocks) into your SEO plugin (Rank Math/Yoast → "Edit snippet" + "Schema/Code") **or** the theme's per-page `<head>` injector. Don't duplicate the `<title>`/meta if the SEO plugin already sets them.

**B. Simplest (whole document).**
Serve `homepage.html` as-is via a blank template that echoes the raw file. Keep the global header/footer consistent with the blog.

## Before publishing
- **Swap the hero photo:** upload a licensed image to the Media Library; replace the `src` on `<img id="ctc-hero-photo">`. Keep the alt text.
- **Confirm the schema NAP** (street address + add a phone) in the JSON-LD — flagged in an HTML comment.
- **Wire links:** nav + CTAs currently point to `/contact/`, `/case-studies/`, etc. — match to your real slugs; "Request a Proposal" can instead embed a **HubSpot form**.
- **Forms:** pure HTML can't run a WP form plugin inline — link to a WP contact page or drop in a HubSpot embed.
- **301 redirects** from the old format URLs → the new pages (see `../03-revision-plan.md`).
- Test on a **draft/staging** page, run **PageSpeed Insights** + Google **Rich Results Test**, then publish.

## Why this is good for SEO/AI
Server-delivered semantic HTML (not a JS app), fast (no builder bloat → better Core Web Vitals),
with exact JSON-LD schema and quotable FAQ content — ideal input for Google and for Gemini's
AI Overviews. Keep the XML sitemap submitted in Search Console.
