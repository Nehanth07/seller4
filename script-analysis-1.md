# Script Analysis 1 - dti_content_script.js bundle

## What this script is
This is a large, minified Webpack-style JavaScript bundle for a browser extension content script (WalkMe/DTI context collection), not a normal webpage UI script.

## High-level purpose
The script mainly does these things:
- Collects user interaction and engagement metrics from pages.
- Observes web performance metrics (CLS, FCP, FID, LCP, TTFB, TTI, long tasks, resource count).
- Sends collected data to a background extension process.
- Handles domain/application identification rules.
- Applies optional restriction actions like block typing, block pasting, or block site overlays.
- Includes many crypto utilities (CryptoJS algorithms) used for hashing/encryption.

## Important modules spotted
- `8044` ContextBuilder:
  - Core orchestrator for event listeners and context payload creation.
  - Tracks mouse/keyboard/scroll/input/copy/paste/focus/blur.
- `1492` Metrics collector:
  - Aggregates web-vitals style performance metrics.
- `4649` Constants/config:
  - Actions, event types, metrics names, app/domain mappings, limits.
- `6296`, `3601`, `2027`, `7536`:
  - DTID/Discover flow and communication with page/background.
- `590`, `5749`, `3555`, `5399`, `4201`, `870`, `3112`:
  - Activity tracking, rage clicks, input/search tracking, copy/paste, marked text, mouse interactions.
- CryptoJS-related modules (`9021` and many others):
  - SHA family, MD5, AES, DES, Blowfish, RC4, Rabbit, HMAC, PBKDF2, paddings, modes.

## What this means for "mimic the webpage"
This script does **not** define a clear visual page layout/theme/components for a normal site clone.
It is mostly telemetry, tracking, and extension infrastructure.

So from this script alone, we cannot faithfully reconstruct a target webpage design.

## Useful details extracted anyway
- It tracks and hashes interaction text before sending.
- It has app/domain mapping for many products (Google, Microsoft, Salesforce, etc.).
- It can monitor context changes, focus state, and URL changes over time.
- It can enforce restrictions (typing/pasting/site blocking) with DOM listeners and overlays.

## If your goal is to recreate a webpage UI
Please provide at least one of these next:
- The actual HTML/CSS/JS of the target page, or
- A screenshot/video of the target page, or
- A live URL and a list of sections you want copied.

Then I can build a clean page clone in this workspace.

## Quick plain-English summary
This code is best described as a browser extension behavior and analytics engine, not a page template.
