# Website Migration Plan: Squarespace to Static HTML + Tailwind CSS

## What I Found

### Current Squarespace Structure (emjoydesign.com)
The site has a **two-page pattern** for most projects:
- **Page 1 (Results)**: Title, brief summary, key metric, "My process" / "Try it" links
- **Page 2 (Process)**: Full case study — context, research, approach, findings, metrics, team

**Pages discovered:**
| Page | URL |
|------|-----|
| Home | `/` |
| About Emily | `/biocontact` |
| Drive GenAI Organize (results) | `/drive-genai-organize` |
| Drive GenAI Organize (process) | `/pdf-1` |
| Workspace Video Player (results) | `/google-workspace-video-player` |
| Workspace Video Player (process) | `/gooogleworkspacevideoplayer` |
| Gemini + Video (results) | `/gemini-in-workspace-video` |
| Workspace PDF (results) | `/workspace-pdf-consumption` |
| Workspace PDF (process) | `/pdf` |
| Lemonaid | `/lemonaid-health` |
| Lemonaid PIMS (results) | `/pims` |
| Lemonaid PIMS (process) | `/lemonaid-pims-process` |
| Planned Parenthood (results) | `/planned-parenthood` |
| Planned Parenthood (process) | `/pp-mail-order-process` |
| BrightScope Beacon | `/brightscope` |

### Existing workspace-video-player.html
Already combines results + process into a single page. Uses custom inline CSS with:
- Sticky header nav (Emily Thomas | Work, About Emily)
- Centered hero (title, subtitle, "See my process" | "Use it")
- Two-column grid sections (label | content) for Overview, UX Lead, Impact, etc.
- Full-width image visuals and side-by-side comparisons
- Divider lines between major sections
- Quotes with purple left border
- Footer with tagline + project navigation links
- Responsive breakpoints at 768px

---

## The Plan

### Step 1: Set up Tailwind CSS
- Add Tailwind via CDN (`<script src="https://cdn.tailwindcss.com">`) for rapid development
- Configure a custom `tailwind.config` in the `<script>` tag to define:
  - **Colors**: purple accent (`#c799d1`), body text (`#333`), muted text (`#8b8989`)
  - **Fonts**: `proxima-nova` (body), `Open Sans` (headings/nav), `EB Garamond` (footer tagline), `Lato` (footer nav)
  - **Spacing/sizing** matching the existing design

### Step 2: Convert workspace-video-player.html to Tailwind
- Replace all inline `<style>` CSS with Tailwind utility classes
- Preserve the exact same visual design — this is a 1:1 conversion, not a redesign
- Keep all existing content, images, and structure intact
- Verify in browser that it matches the current version

### Step 3: Extract a reusable page template
From the converted Workspace Video Player, identify the **shared components** that every project page will use:
- **Header** — sticky nav with logo + Work/About links
- **Hero** — project title, subtitle, action links
- **Section** — two-column label/content grid (the core content block)
- **Visual** — full-width image with optional caption
- **Visual Pair** — side-by-side comparison images
- **Quote** — styled blockquote with purple accent
- **Divider** — horizontal rule between major sections
- **Footer** — tagline + project navigation links

### Step 4: Create remaining project pages
Build each project as a **single combined page** (merging results + process):

1. **drive-genai-organize.html** — Combine results summary + full process case study
2. **gemini-video.html** — Results + process content
3. **workspace-pdf.html** — Results + full process case study
4. **lemonaid.html** — Results page (no separate process page exists on Squarespace)
5. **lemonaid-pims.html** — Results + process
6. **planned-parenthood.html** — Results + process
7. **brightscope.html** — Results page (no separate process page exists on Squarespace)

Each page follows the same structure:
```
Header
Hero (title + subtitle + links)
Overview / Role / Impact sections
[Divider]
Full process content (Context, Research, Problems, Approach, Findings, Metrics, Team)
Footer
```

### Step 5: Create index.html (Home) and about.html
- **index.html**: Hero tagline ("I'm a product designer living and working in Boulder") + project navigation links — matching the Squarespace home layout
- **about.html**: Bio, Aristotle quote, professional experience, contact info

### Step 6: Wire up navigation
- Header links: "Work" -> `index.html`, "About Emily" -> `about.html`
- Footer project links: each points to the correct project HTML file
- "Emily Thomas" logo -> `index.html`

---

## File Structure
```
emjoy/
  index.html                    # Home page
  about.html                    # About Emily page
  workspace-video-player.html   # (converted to Tailwind)
  drive-genai-organize.html
  gemini-video.html
  workspace-pdf.html
  lemonaid.html
  lemonaid-pims.html
  planned-parenthood.html
  brightscope.html
```

## Key Decisions
- **Tailwind via CDN** for now (can switch to build step later for production)
- **All images stay hosted on Squarespace CDN** — no need to download/re-host during migration
- **No JavaScript frameworks** — pure HTML + Tailwind, keeping it simple
- **Combined pages** — results and process merged into one scrollable page per project
- **Start with Workspace Video Player** conversion as the template, then replicate for all others

## Build Order
1. Convert `workspace-video-player.html` to Tailwind (template/reference)
2. Create `index.html` (home)
3. Create `about.html`
4. Build project pages in order: Drive GenAI Organize, Gemini + Video, Workspace PDF, Lemonaid, Lemonaid PIMS, Planned Parenthood, BrightScope
5. Final pass: verify all navigation links, responsive behavior, visual consistency
