# Start a LOCAL Claude Code session with browser access (WordPress/Divi cleanup)

This lets a local Claude see your live site + WordPress/Divi back end (screenshots + DOM),
audit it, and assist with cleanup. This cloud session can't drive your browser; a local one can.

---

## Step 1 — Open the session in the project folder
Clone (or open) the repo so the new session has all our deliverables:
```
git clone https://github.com/CTCteam2026/Team.git
cd Team
git checkout claude/ctc-website-audit-redesign-6qfh8n
```
Start Claude Code (desktop app or CLI) **in this folder**.

## Step 2 — Add a browser MCP server
Two good options. **Option A (Browser MCP)** reuses *your already-logged-in Chrome* (so you don't
re-enter the WordPress password) — best for this. **Option B (Playwright MCP)** is a fresh, robust
Chromium you log into once.

**Option A — Browser MCP (attaches to your real Chrome via an extension):**
1. Install the "Browser MCP" Chrome extension (browsermcp.io) and pin it.
2. Add the server (CLI): `claude mcp add browsermcp npx @browsermcp/mcp@latest`
   …or in the desktop app's MCP settings add:
   ```json
   { "mcpServers": { "browsermcp": { "command": "npx", "args": ["@browsermcp/mcp@latest"] } } }
   ```
3. Open Chrome, log into WordPress admin, click the Browser MCP extension → "Connect".

**Option B — Playwright MCP (official, isolated browser):**
```
claude mcp add playwright npx @playwright/mcp@latest
```
or config:
```json
{ "mcpServers": { "playwright": { "command": "npx", "args": ["@playwright/mcp@latest", "--browser", "chrome"] } } }
```
Then, in the session, ask it to open your site and **you** log into `/wp-admin` in that browser window.

## Step 3 — Paste this kickoff prompt into the new session
> You're continuing a website project for **Coast to Coast Conferences & Events (CTC)** — a certified
> woman-owned, full-service event management company in Long Beach, CA. The repo you're in has all the
> context: read `README.md`, then `deliverables/02-website-audit.md`, `deliverables/03-revision-plan.md`,
> and `deliverables/05-brand-and-voice.md`. Goals: **page speed, SEO visibility, and AI searchability
> (Gemini above-the-fold answers)**. The site is **WordPress + Divi**. I've connected a **browser MCP** so
> you can see my screen/browser. Start by opening the live site and my `/wp-admin`, take a look at the
> back end, and help me **audit and clean up** against the plan. Work read-only first: inventory pages,
> plugins, theme/Divi settings, redirects, and confirm the audit findings (duplicate/format pages,
> Cloudflare bot 403, missing schema, speed). Then propose a prioritized cleanup list and only make
> changes I approve, on a staging/draft copy, after we back up.

---

## What to have the local Claude do first (read-only audit)
1. **Page/URL inventory** — list all pages; flag duplicates and the format pages to retire
   (`/in-person/`, `/hybrid-virtual/`, `/virtual-event-depot/`, `/event-management/`, `/event-management-usa/`;
   `/blog/` vs `/blogs-2/` vs `/content-hub/`).
2. **Plugins & theme** — list active plugins; flag bloat / render-blocking / redundant SEO or builder add-ons.
3. **Divi settings** — Theme Options fonts/colors vs. our brand (Poppins/Barlow; blue-forward, purple→blue buttons).
4. **Technical** — robots.txt, XML sitemap, does Cloudflare 403 Googlebot/Google-Extended, HTTPS, canonicals.
5. **Speed** — run PageSpeed Insights on Home + a key page; note LCP/INP/CLS.
6. **Schema** — check for Organization/LocalBusiness/FAQPage; validate in Rich Results Test.
Then produce a **prioritized cleanup list** and pair with you on changes.

## Safety rules (important)
- **Back up first** (UpdraftPlus or host snapshot). Prefer a **staging** site for changes.
- **Don't paste passwords into the chat** — log into WordPress yourself in the browser the MCP controls.
- **Confirm every destructive action** (deleting pages/plugins, changing redirects) before it runs.
- Divi visual-builder automation is fragile — use the browser to **inspect and guide**, make edits in the
  WordPress UI with confirmation, not blind bulk automation.

## Key facts the local Claude should know
- Brand source of truth: `deliverables/05-brand-and-voice.md`. NAP: 1 World Trade Center, Suite 800,
  Long Beach, CA 90831 · 562-980-7566. Certified woman-owned. Founded 1994. Founder/President Michelle Manire.
- Positioning: **"events, not formats"** — one event-management service (retire format pages). Tagline "Your Event Partner."
- Copy rules: **no em dashes**; blue-forward palette; pink used sparingly; script/cursive is print-only.
- Production homepage + paste-ready snippets live in `deliverables/site/` and `deliverables/divi-snippets/`.
