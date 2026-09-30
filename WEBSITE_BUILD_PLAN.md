# InterRent — 5‑Page Website Build Plan

> A precise, build‑ready blueprint for a professional, industry‑grade **InterRent** (premium car‑rental) website.
> This document is the single source of truth. A separate model/agent will implement each **Build Prompt** in order.
> Goal: cinematic, editorial, *not* "AI‑generated" looking. Heavy on smooth scroll, parallax, delayed word slide‑ins, and slow gradient image zooms.

---

## 0. How to use this document

- The site is intentionally split into **9 sequential Build Prompts** so an implementing model can complete each one in a single focused pass without losing quality.
- Build in order. Each prompt lists: **Deliverable**, **Depends on**, **Files**, **Detailed spec**, and **Done‑when** acceptance checks.
- Do **not** invent new fonts/colors. Everything must come from the **Design System** (Section 2).
- Reuse the existing repo files as *reference implementations* (Section 1). Copy the technique, re‑skin to the InterRent system.
- Every page must feel hand‑crafted and editorial. Avoid generic centered hero + 3 cards + CTA layouts.

---

## 1. Reference assets already in this repo

Use these as proven, working technique references. Lift the mechanics, re‑theme to InterRent.

| Reference file | What to harvest from it |
|---|---|
| `page4.html` | Anton display font, dark `#0f1923` palette, neon‑burst micro‑animations, 3D flip cards, staggered "deal‑in" entrance. Use for the **Fleet card** interactions. |
| `index.html` | **Lenis** smooth heavy scroll setup, full‑screen **slide‑over page transitions** (`translateX(100%)` with `cubic-bezier(0.77,0,0.175,1)`), colossal stroked headline, Outfit font. Core scroll + transition engine. |
| `how-interrent-works.html` / `services.html` | **Massive layered stroked text** that assembles/slides on scroll (`service-layer` with `-webkit-text-stroke`, `clip-path`), interactive numbered list with `#D1FF00` hover sweep. Use for **How It Works** + section headers. |
| `navbar.html` / `navbaropen.html` | Fixed corner **neon LED nav bar**, expand/collapse on scroll, Gellix/Inter. Base for the **global navigation**. |
| `footer_final.html` / `footer.html` | **GSAP wave text** footer, `ScrollTrigger` reveal, Bricolage Grotesque. Base for the **global footer**. |
| `opening-animation.html` | GSAP cinematic **preloader/intro** on `#060606` with radial glow + grid. Base for the **site preloader**. |
| `drive-capital-mimic.html` | Clean dark panel system, CSS variables, `clamp()` fluid spacing. Base for **content/spec panels**. |
| Local media: `IMG_8751.MP4`, `clip.mp4`, `IMG_8753.MOV` | Background/hero video loops (muted, autoplay, playsinline). |

**Known gaps to handle:** the custom font files `telegraf/*` and `gellix/*` are missing locally. Do **not** rely on them — use the Google Fonts stack in Section 2 and treat Telegraf/Gellix only as optional `@font-face` with graceful fallback.

---

## 2. Design System (single source of truth)

### 2.1 Brand
- **Name:** InterRent (wordmark: `INTER` in white, `RENT` in accent, tight `letter-spacing:-0.03em`).
- **Positioning:** Premium / performance car rental. Editorial, confident, cinematic — think a luxury automotive magazine crossed with a game "night market."
- **Voice:** short, punchy, kinetic. Big verbs. No filler.

### 2.2 Color tokens
```css
:root{
  /* Base */
  --ink:        #0b0e13;   /* page background (near‑black, cool) */
  --ink-2:      #0f1923;   /* panel background (from page4) */
  --ink-3:      #141d28;   /* raised panel */
  --line:       #2a3646;   /* hairline borders */
  --paper:      #f0efe9;   /* light "editorial" section bg */
  --paper-ink:  #12151b;   /* text on paper sections */

  /* Text */
  --fg:         #ece8e1;   /* primary text on dark */
  --fg-dim:     #9aa4b2;   /* secondary text */

  /* Accents (use sparingly, one dominant per section) */
  --accent:     #ff4655;   /* signature red (page4) — primary CTA/brand */
  --gold:       #e5c56d;   /* premium tier */
  --cyan:       #00e5ff;   /* electric highlight */
  --lime:       #d1ff00;   /* interactive hover sweep (from services) */

  /* Effects */
  --glow-accent: 0 0 25px rgba(255,70,85,.55);
}
```
Rule: **one dominant accent per page.** Home = red, Fleet = gold, How It Works = lime, Experience = cyan, Contact = red. Keeps it cohesive, not rainbow.

### 2.3 Typography (Google Fonts only — no missing files)
```html
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Outfit:wght@200;300;400;500;700;800&family=Plus+Jakarta+Sans:wght@400;600;800&family=Barlow+Condensed:wght@600;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap" rel="stylesheet">
```
| Role | Font | Notes |
|---|---|---|
| Display / hero (the "Night Market" font) | **Anton** | uppercase, tight tracking, huge sizes (`clamp(3rem, 12vw, 12rem)`). |
| Colossal stroked scroll text | **Outfit 800** or Anton | for parallax layered headlines. |
| Body / UI | **Outfit** (300–500) | clean, modern, readable. |
| Editorial labels / numbers | **Barlow Condensed** | eyebrows, indices `01 / 02`. |
| Soft accent headings (footer) | **Bricolage Grotesque** | for the wave footer only. |

Type scale (fluid): `--fs-hero: clamp(3rem,12vw,12rem)`, `--fs-h2: clamp(2rem,6vw,5rem)`, `--fs-h3: clamp(1.4rem,3vw,2.4rem)`, `--fs-body: clamp(1rem,1.15vw,1.25rem)`, `--fs-eyebrow: .8rem` (uppercase, `letter-spacing:.25em`).

### 2.4 Spacing / layout
- Max content width `--max: 1440px`; gutters `clamp(20px, 5vw, 96px)`.
- Section vertical rhythm `clamp(80px, 14vh, 200px)`.
- 12‑column mental grid; asymmetric, editorial placement (avoid dead‑center everything).

### 2.5 Motion principles (the soul of the site)
- **Global easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (smooth "settle"). Transitions `0.6s–1.2s`.
- **Smooth scroll:** Lenis, heavy feel (`lerp ~0.08`, `duration ~1.2`).
- **Never** animate everything at once — stagger by `0.08s–0.12s`.
- Respect `prefers-reduced-motion` → disable parallax/large motion, keep opacity fades.
- Keep 60fps: animate only `transform`, `opacity`, `filter`; add `will-change` on animated nodes only.

### 2.6 Signature motion patterns (reused site‑wide)
Define each once, reuse everywhere:

1. **Delayed word slide‑in ("line‑by‑line reveal").**
   Split headline into words/lines; each word wrapped in an overflow‑hidden mask; words start `translateY(120%) rotate(4deg)` and rise to `0` with a per‑word stagger of `0.06–0.1s`. Triggered by ScrollTrigger when the block enters the viewport (or on the incoming page during a page transition).

2. **Parallax on scroll.**
   Foreground text and background media move at different speeds. Background media `yPercent: -15 → 15`; foreground headline `yPercent: 10 → -10`, tied to scroll via ScrollTrigger `scrub: true`.

3. **Slow gradient image zoom (the hero image treatment).**
   Image sits in a fixed‑ratio frame with `overflow:hidden`. On enter, image scales `1.0 → 1.18` slowly (`scrub` across the section) and never fully "arrives" while in view. A gradient veil (`linear-gradient(to top, var(--ink) 0%, transparent 60%)`) overlays the bottom for text legibility. Optional subtle blur‑to‑sharp (`filter: blur(8px) → blur(0)`) on first entrance.

4. **Page‑to‑page slide‑over transition.**
   Incoming full‑screen panel slides `translateX(100%) → 0`; outgoing panel stays put and dims (`filter: brightness(.5)`). During the incoming slide, its headline runs pattern #1 (delayed word slide‑in). This is the "words move up when pages shift" effect the brief asks for.

5. **Interactive list hover sweep.**
   Numbered rows: dark fill scales in from center (`scaleY(0)→1`), text/number flips to `--lime`, row indents `padding-left`. (Straight from `services.html`.)

### 2.7 Tech stack
- Plain HTML/CSS/JS per page (no build step) so files open directly, matching the repo.
- **GSAP 3 + ScrollTrigger** (CDN) for scroll animation.
- **Lenis** (CDN) for smooth scroll.
- Optional **SplitType** (CDN) for word/line splitting, or a tiny hand‑rolled splitter.
- No frameworks required. Tailwind is optional and only if a page already leans on it — prefer hand CSS for consistency.

---

## 3. Global architecture

### 3.1 File / folder structure
```
/site/
  index.html          → Page 1: Home
  fleet.html          → Page 2: The Fleet
  how-it-works.html   → Page 3: How It Works
  experience.html     → Page 4: Experience / Story
  contact.html        → Page 5: Contact / Book
  /assets/
    css/base.css      → design tokens + resets + shared components
    js/lenis-init.js  → smooth scroll bootstrap
    js/motion.js      → reusable GSAP helpers (word reveal, parallax, image zoom)
    js/nav.js         → shared nav behavior
    img/              → place images here (hero, fleet, story)
    video/            → symlink/copy IMG_8751.MP4, clip.mp4, IMG_8753.MOV
```
> Keep it self‑contained under `/site/` so nothing collides with the many existing prototype files in the repo root.

### 3.2 Shared components (built once, included on every page)
- **Preloader / intro** (only first load): re‑skin `opening-animation.html`. Reveals wordmark, then lifts to expose Home.
- **Navigation:** fixed neon corner bar (from `navbar.html`) + full‑screen overlay menu (from `navbaropen.html`). Links to all 5 pages, active state, animated open/close.
- **Footer:** GSAP wave‑text footer (from `footer_final.html`), re‑skinned. Contains nav, contact, socials, big InterRent wordmark.
- **Smooth‑scroll + motion boot:** shared `lenis-init.js` + `motion.js` on every page.
- **Page transition layer:** an empty full‑screen `.transition-panel` used to animate route changes; on link click, panel slides in, navigates, slides out revealing the new page with headline word‑reveal.

### 3.3 Navigation map
```
Home ──► Fleet ──► How It Works ──► Experience ──► Contact
   ╰───────────────── global nav (any → any) ──────────────╯
```

---

## 4. The 5 pages — detailed section specs

> Each page: dark cinematic base, **one dominant accent**, at least one *light "paper" editorial break* for contrast, ends with the global footer.

### PAGE 1 — Home (`index.html`) · accent: **red**
1. **Preloader → hero handoff.** Cinematic intro resolves into hero.
2. **Hero:** full‑viewport muted looping video (`IMG_8751.MP4`) behind a colossal Anton headline "DRIVE THE / EXTRAORDINARY" using **word slide‑in** (#1). Gradient veil bottom. Small eyebrow "PREMIUM CAR RENTAL". Subtle scroll cue.
3. **Statement / manifesto:** parallax stroked text (from `services.html` technique) — a single bold sentence assembling on scroll.
4. **Featured fleet strip:** horizontal, 3–4 Anton cards re‑skinned from `page4.html` (hover = neon burst, click‑to‑flip reveals spec). Accent gold hints for premium tier.
5. **"By the numbers" band** on **paper** background: animated counters (fleet size, cities, years) with Barlow Condensed indices; slow gradient image zoom (#3) beside them.
6. **Split CTA:** big Anton "READY?" → link to Contact, with lime hover sweep.
7. **Footer.**

### PAGE 2 — The Fleet (`fleet.html`) · accent: **gold**
1. **Page‑transition entrance** (slide‑over + word reveal) with title "THE FLEET".
2. **Filter rail** (optional, static ok): tiers — *Sport / Luxury / Electric / Off‑road* as a `services.html`‑style interactive list.
3. **Fleet grid:** each vehicle = large image in a **gradient‑zoom frame** (#3) + Anton name + Barlow spec row (HP / 0‑100 / price/day). On hover, image zoom accelerates slightly and a `--gold` hairline draws around the frame.
4. **Detail spotlight:** one hero vehicle, split layout — sticky image (parallax) on one side, scrolling spec copy on the other (drive‑capital panel style).
5. **CTA band** → Contact.
6. **Footer.**

### PAGE 3 — How It Works (`how-it-works.html`) · accent: **lime**
1. **Transition entrance**, title "HOW IT WORKS" (reuse `how-interrent-works.html` layered stroked title).
2. **Numbered steps** (01 Choose → 02 Reserve → 03 Unlock → 04 Drive): the interactive numbered list with hover sweep (#5), each row expands to show detail + a small zoom image.
3. **Parallax explainer:** alternating left/right blocks — text with word slide‑in, images with gradient zoom, moving at parallax speeds.
4. **FAQ accordion** (from `services.html`/`how-interrent-works.html` FAQ styling), smooth height transitions.
5. **CTA** → Contact.
6. **Footer.**

### PAGE 4 — Experience / Story (`experience.html`) · accent: **cyan**
1. **Transition entrance**, title "THE EXPERIENCE".
2. **Full‑bleed video moment** (`clip.mp4` / `IMG_8753.MOV`) with parallax overlay quote, word slide‑in.
3. **Editorial timeline / story:** pinned scroll section (ScrollTrigger pin) where copy advances while a background image slowly gradient‑zooms.
4. **Gallery mosaic:** asymmetric image grid, each tile gradient‑zoom on enter, staggered.
5. **Pull‑quote** on **paper** background for contrast.
6. **CTA** → Contact.
7. **Footer.**

### PAGE 5 — Contact / Book (`contact.html`) · accent: **red**
1. **Transition entrance**, title "LET'S DRIVE".
2. **Split layout:** left = large Anton statement + contact details (email, phone, locations) with word reveal; right = booking/contact form (name, email, vehicle interest, dates, message) styled on the drive‑capital dark panel system, with focus‑glow states.
3. **Map / locations band** (static styled block ok) with parallax label text.
4. **Reassurance strip:** 3 short promises (insurance, 24/7, delivery) as animated items.
5. **Footer** (the wave footer shines here as the closer).

---

## 5. Build Prompts (implement in this exact order)

> Each prompt is self‑contained. Give the implementing model this document + the target prompt. Keep the Design System (Section 2) pinned in context for every prompt.

### Prompt 1 — Foundation & Design System
- **Deliverable:** `/site/assets/css/base.css` (tokens, reset, typography, buttons, panels, paper/dark section utilities, hairlines, focus states) + font `<link>` snippet + a `_stub` HTML that visually proves every token, type size, button, and section style.
- **Depends on:** nothing.
- **Done‑when:** all color/type/spacing tokens render; light + dark section utilities exist; reduced‑motion media query present.

### Prompt 2 — Motion & Scroll Engine
- **Deliverable:** `lenis-init.js` + `motion.js` exposing reusable helpers:
  `revealWords(el)` (pattern #1), `parallax(el, opts)` (#2), `imageZoom(frameEl)` (#3), `initListHover()` (#5). GSAP + ScrollTrigger + Lenis wired together (Lenis drives ScrollTrigger via `raf`).
- **Depends on:** Prompt 1.
- **Done‑when:** a demo section shows word reveal, scroll parallax, and slow image zoom working at 60fps; reduced‑motion disables them.

### Prompt 3 — Global Nav + Page‑Transition Layer
- **Deliverable:** shared nav (neon corner bar + full‑screen overlay menu) and the `.transition-panel` slide‑over that runs headline word‑reveal on the incoming page. `nav.js`.
- **Depends on:** Prompts 1–2. Reference `navbar.html`, `navbaropen.html`, `index.html` slide logic.
- **Done‑when:** nav opens/closes smoothly, active state works, clicking a link plays slide‑over → navigates → incoming title reveals.

### Prompt 4 — Global Footer + Preloader
- **Deliverable:** wave‑text footer component (re‑skin `footer_final.html`) and first‑load preloader (re‑skin `opening-animation.html`) that hands off to the hero.
- **Depends on:** Prompts 1–2.
- **Done‑when:** footer wave triggers on scroll into view; preloader plays once then reveals page; both use design tokens.

### Prompt 5 — Page 1: Home
- **Deliverable:** `/site/index.html` fully assembled with all Section‑4 Page‑1 sections, using shared CSS/JS + nav + footer + preloader.
- **Depends on:** Prompts 1–4.
- **Done‑when:** hero video + word reveal, parallax statement, fleet cards (page4 flip/burst re‑skinned), counters on paper band, CTA, footer — all smooth.

### Prompt 6 — Page 2: The Fleet
- **Deliverable:** `/site/fleet.html`.
- **Depends on:** Prompts 1–4.
- **Done‑when:** fleet grid images use gradient zoom + gold hairline hover; detail spotlight uses sticky/parallax; transition entrance works.

### Prompt 7 — Page 3: How It Works
- **Deliverable:** `/site/how-it-works.html`.
- **Depends on:** Prompts 1–4. Reference `how-interrent-works.html`, `services.html`.
- **Done‑when:** layered stroked title, numbered interactive steps with lime sweep, parallax explainer blocks, FAQ accordion.

### Prompt 8 — Page 4: Experience
- **Deliverable:** `/site/experience.html`.
- **Depends on:** Prompts 1–4.
- **Done‑when:** full‑bleed video moment, pinned story scroll, staggered gradient‑zoom gallery, paper pull‑quote.

### Prompt 9 — Page 5: Contact + Final QA pass
- **Deliverable:** `/site/contact.html` + a cross‑page QA sweep (consistent nav/footer, link map, reduced‑motion, mobile responsiveness, no console errors).
- **Depends on:** Prompts 1–8.
- **Done‑when:** form styled with focus‑glow, all 5 pages inter‑link, transitions consistent, passes acceptance checklist (Section 6).

---

## 6. Global acceptance checklist (applies to every page)

- [ ] One dominant accent per page; palette stays within tokens.
- [ ] Anton used for display; Outfit for body; Barlow for indices — no stray fonts.
- [ ] Every major headline uses **delayed word slide‑in** on entrance/transition.
- [ ] At least one **parallax** relationship (fg vs bg) per page.
- [ ] Every hero/feature image uses the **slow gradient zoom** frame.
- [ ] Page transitions use the **slide‑over + incoming word‑reveal**.
- [ ] Smooth scroll (Lenis) active; 60fps; only transform/opacity/filter animated.
- [ ] `prefers-reduced-motion` respected (motion reduced to fades).
- [ ] Fully responsive: mobile hero readable, grids collapse, nav overlay works on touch.
- [ ] No missing‑font fallback breakage (Telegraf/Gellix optional only).
- [ ] Consistent nav + footer on all 5 pages; correct active states and link map.
- [ ] No horizontal scroll leak from oversized text (`overflow-x:hidden` guard).
- [ ] No console errors; videos are muted+playsinline+loop and lazy where possible.

---

## 7. Content placeholders (so copy isn't "AI filler")

Use tight, brand‑voice copy. Suggested seeds (editable):
- Home hero: **"DRIVE THE EXTRAORDINARY"** / eyebrow "PREMIUM CAR RENTAL — SINCE 2014".
- Manifesto: "We don't rent cars. We hand you the keys to a feeling."
- Fleet tiers: *Sport · Luxury · Electric · Off‑road*.
- Steps: *Choose · Reserve · Unlock · Drive*.
- Contact: **"LET'S DRIVE"** / "Tell us where you're headed."

Leave clearly marked `<!-- IMAGE: … -->` and `<!-- VIDEO: … -->` slots so real assets drop in later.

---

## 8. Notes & guardrails for the implementing model

- Prefer **editorial, asymmetric** layouts. Avoid the generic "centered hero + three equal cards + centered CTA" template — that reads as AI‑generated.
- Reuse the *mechanics* from reference files but **re‑theme** to the InterRent tokens; don't paste their brand colors (pink `#FF55F8`, etc.).
- Keep JS modular and shared; do not re‑implement the same animation per page.
- Test each page served over `http://` (matches the repo's `run-pages.command` / `python3 -m http.server`) so video/autoplay behaves.
- Ship each prompt as working, self‑contained output before moving to the next.
```
