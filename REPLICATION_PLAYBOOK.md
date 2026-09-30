"Follow the Web Design & Animation Replication Playbook (attached). Target URL: <URL>. Replicate: <whole page / a section / an animation>. Then re-skin as: brand=<NAME>, color=<#hex>, font=<licensed font>. Build a standalone test page first, then integrate."




# Web Design & Animation Replication Playbook

> **Purpose:** A reusable, self-contained instruction file. Give an AI agent (or yourself)
> **this file + a website URL**, and follow the phases below to faithfully replicate an
> entire webpage — or a single design/animation element from it — then re-skin it with your
> own brand/name/content.
>
> **How to use with an AI agent:**
> 1. Attach this file.
> 2. Paste the target URL.
> 3. Say: *"Follow the Replication Playbook. Target = <URL>. I want to replicate <the whole page / the header logo animation / the hero section / etc.>. Then re-skin it as <MY BRAND>."*
> 4. Answer the agent's clarifying questions (Phase 0).
>
> This document is technique-agnostic: it works for CSS animations, canvas/WebGL, GSAP
> timelines, SVG, sprite masks, scroll effects, etc.

---

## Legal & Ethical Guardrails (read first)

- **Replicate techniques, not stolen brand assets.** Reproducing *how* an effect is built
  (CSS, JS logic, timing, easing) is standard learning. Do **not** ship someone else's
  **logo, copyrighted artwork, proprietary fonts, or brand name** in your live product.
- **Fonts:** Only download/embed fonts with a license that permits it (OFL / Apache /
  purchased). Google Fonts = safe. A site's self-hosted commercial font = **not** safe to reuse.
- **Sprite sheets / baked artwork:** Fine to *study* the original to match feel, but the
  final shipped asset should be **your own regenerated version** (your name, your shapes).
- When in doubt, keep the original assets only in a local `/_reference/` folder used purely
  for study, and never deploy them.

---

## Phase 0 — Scope & Clarify (before touching code)

Decide and confirm:

1. **Scope:** Whole page? A section (hero/header/footer)? Or a single effect (e.g. the logo
   reveal animation)?
2. **Fidelity target:** "Exact 1:1 replica" vs. "same *feel*, my own content."
3. **Re-skin details:** New brand name, exact casing, colors (hex), fonts you're allowed to use,
   frame count / duration if it's an animation.
4. **Ambiguity/creative forks:** For stylized animations, decide the "style" (e.g. sliced-offset
   assemble, blob morph, fragment scatter). If the user says "just match the feel," pick the
   option closest to the reference.
5. **Where it lives:** New standalone test page first (recommended), then integrate into the
   real site once approved.

> **Rule:** Always build a **standalone lab/test page** first (e.g. `xyz-replica.html`).
> Confirm it looks right in isolation before wiring it into the production site.

---

## Phase 1 — Reconnaissance (understand how it's built)

### 1.1 Inspect the live page
- Open the URL. Use browser DevTools:
  - **Elements** → find the target element, read its classes and structure.
  - **Styles/Computed** → note the CSS rules, custom properties (`--vars`), transitions,
    `@keyframes`, `transform`, `clip-path`, `mask`, `filter`.
  - **Network** tab → filter by **CSS / JS / Img / Font / Media**. Note the URLs of:
    stylesheets, JS bundles, sprite PNGs, SVGs, video/lottie, fonts.
  - **Sources** → find the JS that toggles classes / starts timelines (search for the
    element's class name, `is-visible`, `active`, `play`, `IntersectionObserver`, `gsap`,
    `scroll`, `lottie`).

### 1.2 Pull the raw assets for study (terminal)
```bash
# Fetch a stylesheet to read the real rules
curl -L -s "https://SITE/path/to/styles.css" -o /tmp/ref-styles.css

# Fetch a JS bundle (may be minified — grep it for triggers)
curl -L -s "https://SITE/path/to/main.js" -o /tmp/ref-main.js
grep -oE "is-visible|IntersectionObserver|gsap|classList|requestAnimationFrame" /tmp/ref-main.js | sort -u

# Fetch an image/sprite/font asset
curl -L -s "https://SITE/path/to/asset.png" -o /tmp/ref-asset.png
file /tmp/ref-asset.png           # confirms type + dimensions
```

### 1.3 Identify the animation technique
Match what you see to one of these common patterns:

| Signal in DevTools                                   | Technique                          |
|------------------------------------------------------|------------------------------------|
| `mask`/`-webkit-mask` + a tall/wide PNG + `steps(N)` | **Sprite-mask film-strip reveal**  |
| `@keyframes`, `transition`, `transform`              | Pure CSS animation                 |
| `<canvas>` + JS loop                                 | Canvas / WebGL                     |
| `gsap`, `ScrollTrigger`, `timeline`                  | GSAP orchestration                 |
| `<svg>` + `stroke-dasharray`/`<animate>`             | SVG line-draw / SMIL               |
| `.json` + `lottie`/`bodymovin`                       | Lottie (After Effects export)      |
| `IntersectionObserver` / scroll libs (luge, locomotive) | Scroll-triggered reveal         |

> **Document your finding** in one sentence, e.g.:
> *"The logo is a solid color block shaped by a PNG mask; a 50-frame vertical sprite is
> scrubbed via `mask-position: 0 0 → 0 100%` with `transition: mask 1.6s steps(49)`,
> triggered by adding `.is-visible`."*

---

## Phase 2 — Replicate Exactly (prove the mechanism)

Build a standalone HTML file that reproduces the **original** as closely as possible —
including original assets — purely to confirm you understood the mechanism.

- Copy the **verbatim CSS rules** for the element (structure, aspect-ratio hack, transition,
  easing, custom properties).
- Copy the **markup structure** (same nesting/classes).
- Reproduce the **trigger** (class toggle on load / on scroll) and add a **Replay button**
  for testing.
- Scale up if needed (e.g. bump a `--logo-size` var) so you can see it clearly.

**Reference: sprite-mask reveal (the Generous-style effect)**
```css
:root{
  --logo-size: 520px;
  --sprite: url("https://SITE/.../logo-sprite.png"); /* vertical film-strip PNG */
}
.logo{ position:relative; width:var(--logo-size); height:auto; }
.logo:before{ display:block; padding-top:20.6451%; content:""; } /* aspect ratio */
.logo__sprite{
  position:absolute; inset:0;
  background: #0b0f14;                                  /* the ink that gets revealed */
  -webkit-mask: var(--sprite) 0 0 / 100% auto no-repeat;
          mask: var(--sprite) 0 0 / 100% auto no-repeat;
  -webkit-transition: -webkit-mask 1.6s steps(49);
          transition: mask 1.6s steps(49), -webkit-mask 1.6s steps(49);
}
.logo.is-visible .logo__sprite{
  -webkit-mask-position: 0 100%;
          mask-position: 0 100%;
}
```
```html
<div class="logo" id="logo">
  <span class="logo__sprite"></span>
  <span class="sr-only">Brand Name</span>
</div>
<button id="replay">Replay</button>
<script>
  const logo = document.getElementById('logo');
  function play(){
    logo.classList.remove('is-visible');
    void logo.offsetWidth;                 // force reflow → restart transition
    requestAnimationFrame(()=>requestAnimationFrame(()=>logo.classList.add('is-visible')));
  }
  window.addEventListener('load', play);
  replay.addEventListener('click', play);
</script>
```

> **Sprite math:** A strip of `W × H` with `F` frames has frame height `H/F`.
> `steps(F-1)` between `mask-position 0` and `100%` yields `F` discrete frames.
> Displayed with `mask-size: 100% auto` (one frame fills the box at a time).

---

## Phase 3 — Study the Frames (for baked/sprite animations)

If the effect is baked into a sprite/lottie/video, extract and lay out frames to understand
the motion so your regenerated version matches the *feel*.

```python
# Extract a horizontal contact sheet from a vertical sprite strip
from PIL import Image
im = Image.open('/tmp/ref-sprite.png').convert('RGBA')
W, H = im.size
F  = 50                      # frame count
fh = H // F
picks = list(range(0, F, 4)) + [F-1]
sheet = Image.new('RGBA', (W*len(picks), fh), (240,240,235,255))
for i, f in enumerate(picks):
    fr = im.crop((0, f*fh, W, f*fh+fh))
    bg = Image.new('RGBA', fr.size, (240,240,235,255))
    bg.alpha_composite(fr)
    sheet.paste(bg, (i*W, 0))
sheet.convert('RGB').save('/tmp/ref-contact.png')
```
Open the contact sheet and note: *When do shapes read as letters? What's the easing curve
(fast→slow?), the "ambiguous" early style, the overshoot/settle at the end?*

---

## Phase 4 — Re-skin with Your Own Content

### 4.1 If it's CSS/JS/SVG/GSAP driven
- Swap text/colors/fonts, keep the timeline. Replace brand tokens (`--color`, font vars).
- Update `@keyframes`/GSAP targets to your element structure.

### 4.2 If it's a baked sprite (regenerate YOUR strip)
Generate a **new mask film-strip** for your word using a script. Keep the same format
(vertical PNG, same frame box, transparent where empty, solid alpha where ink shows).

```bash
# Download an OFL/Apache font you're allowed to use (example: Anton)
curl -L -s -o /tmp/Anton.ttf \
  "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
```
```python
# Generate a 50-frame "assemble" mask strip for a word (Pillow)
from PIL import Image, ImageDraw, ImageFont
WORD, FRAMES = "Olynta", 50
FW, FH = 314, 70                     # match reference frame box (or your own ratio)
INK = (11,15,20,255)                 # RGBA; alpha is what the CSS mask uses
font = ImageFont.truetype('/tmp/Anton.ttf', 54)

def render_letter_layer():
    # base image of the full word, centered
    base = Image.new('RGBA', (FW, FH), (0,0,0,0))
    d = ImageDraw.Draw(base)
    bbox = d.textbbox((0,0), WORD, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((FW-w)/2 - bbox[0], (FH-h)/2 - bbox[1]), WORD, font=font, fill=INK)
    return base

full = render_letter_layer()
strip = Image.new('RGBA', (FW, FH*FRAMES), (0,0,0,0))
for i in range(FRAMES):
    t = i/(FRAMES-1)
    # EASE: ambiguous->resolved. Example: vertical-band offsets that settle.
    frame = Image.new('RGBA', (FW, FH), (0,0,0,0))
    bands = 12
    import random; random.seed(7)
    for b in range(bands):
        y0 = int(b*FH/bands); y1 = int((b+1)*FH/bands)
        col = full.crop((0,y0,FW,y1))
        # early frames: shift band sideways + fade; later: settle to 0
        maxoff = int(FW*0.9)
        off = int(maxoff*(1-t)*(random.random()*2-1))
        alpha = int(255 * min(1, t*1.6 - b*0.02))
        if alpha <= 0: continue
        shifted = Image.new('RGBA',(FW,y1-y0),(0,0,0,0))
        shifted.alpha_composite(col,(off,0))
        # apply alpha
        a = shifted.split()[3].point(lambda p: p*alpha//255)
        shifted.putalpha(a)
        frame.alpha_composite(shifted,(0,y0))
    strip.paste(frame,(0,i*FH))
strip.save('/PATH/smart-prehospital/assets/anim/olynta-sprite.png')
```
> Tune the `EASE`/offset logic to match what you saw in Phase 3. The **alpha channel is the
> mask** — solid where the letter should show, transparent elsewhere.

### 4.3 Point the replica page at your new strip
Change one line: `--sprite: url("assets/anim/olynta-sprite.png");` — the engine is unchanged.

---

## Phase 5 — Integrate into the Real Site

1. Copy the confirmed CSS/JS/asset into the production files.
2. Replace the old markup (e.g. brand text) with the new element. Search the codebase for
   **every** occurrence of the old name (header, footer, `<title>`, copyright, alt text).
3. Keep design tokens centralized (`:root` custom properties) so colors/fonts stay consistent.
4. Test: load, replay, responsive sizes, reduced-motion (`@media (prefers-reduced-motion)`
   should show the final frame instantly).

---

## Phase 6 — Verify & Polish

- [ ] Matches the reference *feel* (timing, easing, "ambiguous → resolved" arc).
- [ ] Correct on load **and** on replay/scroll re-entry.
- [ ] Responsive (scales with container, no layout shift — aspect-ratio hack in place).
- [ ] Accessible: real text in `.sr-only`, respects `prefers-reduced-motion`.
- [ ] No console errors; assets load (check Network 200s).
- [ ] **No un-licensed original brand assets shipped.**

---

## Quick Reference: Reusable Prompt

> *"Follow the Web Design & Animation Replication Playbook (attached).*
> *Target URL: `<URL>`.*
> *Replicate: `<whole page / header logo animation / hero / footer / …>`.*
> *Then re-skin as: brand=`<NAME>`, casing=`<e.g. Cap + lowercase>`, color=`<#hex>`,*
> *font=`<licensed font>`, frames/duration=`<e.g. 50 / 1.6s>`.*
> *Build a standalone test page first, show me, then integrate.*
> *Follow the legal guardrails — regenerate my own assets, don't ship theirs."*

---

## Toolbox Cheat-Sheet

| Need                        | Tool / command                                             |
|-----------------------------|------------------------------------------------------------|
| Download asset              | `curl -L -s "URL" -o out.ext`                              |
| Check image type/size       | `file img.png` · `sips -g pixelWidth -g pixelHeight img.png` |
| Inspect/resize images       | Python **Pillow** (`from PIL import Image`)                |
| Search minified JS          | `grep -oE "pattern" file.js`                              |
| Animation orchestration     | **GSAP** (`gsap.min.js`) + `ScrollTrigger`                |
| Scroll triggers (native)    | `IntersectionObserver`                                    |
| Vector line-draw            | SVG `stroke-dasharray` / `stroke-dashoffset`             |
| Frame-based reveal          | CSS `mask` + sprite PNG + `steps(N)`                      |
| After-Effects animations    | **Lottie** (`.json` + lottie-web)                         |

---

*Reusable across projects. Keep original brand assets in a local `/_reference/` folder for
study only — ship your own regenerated versions.*
