# Script Analysis 3 - Drive Capital Home HTML

## What this input is
This is a full rendered HTML snapshot of a Next.js page (`Drive Capital - Home`) with:
- semantic section structure,
- class names from CSS modules,
- image/video/content payload,
- `__NEXT_DATA__` JSON containing most copy and media URLs.

Unlike the previous two extension bundles, this is directly useful for page recreation.

## Key layout structure extracted

1. Hero section
- Headline: `GREATNESS IS IN / OUR BACKYARD`
- Dark theme shell
- Scrolling marquee with airport codes and taglines
- 3-image gallery strip

2. Story section
- Heading: `Our Story`
- Body description paragraph
- Two supporting images
- Cities list where each city has airport code and a repeating company marquee

3. Team section
- Two-column image composition
- Heading: `Our Team`
- Long descriptive copy and two support paragraphs

4. Stats marquee block
- Top marquee: `87 companies`, `$2B AUM`
- Bottom marquee: `24 cities`, `16 partners`

5. Portfolio teaser section
- Label: `BUILDING GREATNESS`
- Heading: `OUR PORTFOLIO`
- Description and CTA

6. Prefooter image pair
- Two large images side-by-side

## Design signals to mimic
- Dark base theme
- Condensed, editorial typography feel
- Wide grid with strong horizontal rhythm
- Repeated marquees with long-duration linear animation
- Heavy visual reliance on high-contrast photography
- Large uppercase section labels and compact body copy

## Data source available
The `__NEXT_DATA__` payload includes:
- all major text content
- CTA text/links
- city/company lists
- image/video URLs

This means we can build a close static mimic without needing original React source files.

## Constraints from this HTML dump
- Original CSS module files are not available in this workspace.
- Original Next runtime/chunks are not available locally.
- So exact pixel-perfect parity is not possible from this dump alone.

## What can be recreated accurately
- section order and hierarchy
- textual content
- image assets (using provided Contentful URLs)
- dark visual style
- marquee interactions
- responsive behavior

## Next implementation note
A local static mimic page should be built from this with clean HTML/CSS/JS and no dependency on Next.js chunk files.
