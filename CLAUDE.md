# Quince Crochèts — Website Project

## Project Overview

Building a frontend-only website for **Quince Crochèts**, a handmade bag brand. The owner crochets and knits bags by hand using recycled cotton yarn. Every bag is a one-of-a-kind, handcrafted piece. The brand has a warm, artisan character with a strong feminine identity and a touch of luxury.

This is NOT a generic e-commerce template. It should feel like a high-end artisan brand website, think the visual warmth of a handmade object combined with refined editorial aesthetics.

## Brand Identity

- **Name**: Quince Crochèts (note the accent on the è)
- **Logo**: Bold retro serif typography in deep red on a salmon/blush pink background, with gold four-pointed star accents
- **Logo file**: `logo.jpg`
- **Brand colors extracted from logo and products**:
  - Salmon/blush pink: `#F4A8A0` (logo background)
  - Deep crimson red: `#B41E2D` (logo typography)
  - Gold/amber: `#E8A020` (logo stars, bag tags)
  - Burgundy/wine: `#6B1C2A` (signature bag color)
  - Nude/blush beige: `#C9A88A` (second bag color)
  - Deep aubergine: `#3D1A2E` (darker bag variant)
  - Warm off-white: `#FAF6F1` (backgrounds)

## Product

Handmade crocheted bags made from **recycled cotton** T-shirt yarn. Current product line visible in provided images:

- **Burgundy hobo bag** — chunky crochet stitch, rounded silhouette, short top handles, gold oval brand tag (`bordo_torbica.jpg`)
- **Nude/beige hobo bag** — same silhouette as burgundy, lighter colorway (`dve_torbe.jpg`)
- **Deep purple/aubergine bag with chain** — chunky crochet, gold chain strap + top handle, gold oval tag, more structured shape (`torbica_i_ruka.jpg`)
- Both colorways shown together with gold string lights in product still life (`dve_torbe.jpg`)
- Close-up of the gold oval brand tag on the nude bag (`closeup_torbica.jpg`)

## Available Image Assets

All images are in the project root or `images/` folder:

| File | Content |
|------|---------|
| `logo.jpg` | Brand logo, use in header/hero |
| `bordo_torbica.jpg` | Burgundy bag worn with boho floral dress, lifestyle shot |
| `closeup_torbica.jpg` | Close-up of gold brand tag on nude bag, texture detail |
| `dve_torbe.jpg` | Both bags (burgundy + nude) styled with gold string lights |
| `torbica_i_ruka.jpg` | Aubergine bag with gold chain, held against white wall |

## Site Structure

Single-page layout (or minimal multi-section):

1. **Hero** — full-screen or near-full-screen, logo prominent, one hero image, tagline
2. **About / Brand Story** — short, warm copy about handmade craft, recycled cotton, the maker
3. **Products / Collection** — gallery of the bags with brief descriptions
4. **Craftsmanship section** — close-up texture shot, short copy about the material and process
5. **Contact / Order** — how to reach the owner (placeholder: Instagram link, email)
6. **Footer** — logo, minimal links

## Copy Direction (placeholder text to use)

**Tagline options** (choose the best fitting one):
- "Crafted by hand. Made to last."
- "Every stitch, intentional."
- "Handmade with recycled cotton."

**Brand story (short)**:
"Each Quince Crochèts bag starts as recycled cotton yarn and ends as something you'll carry for years. Made entirely by hand, one stitch at a time."

**Product descriptions**:
- Burgundy hobo: "The Classic — deep burgundy, chunky hobo silhouette, recycled cotton. Available to order."
- Nude hobo: "The Soft — warm nude, same chunky silhouette. A quieter statement."  
- Aubergine chain bag: "The Evening — deep aubergine with a gold chain. For when you want both craft and elegance."

**Contact section**: "Want a bag? Send a message on Instagram or via email. Custom colors available on request."

## Aesthetic Direction for the Developer

Read `/mnt/skills/public/frontend-design/SKILL.md` before writing any code.

The aesthetic should be:
- **Warm artisan luxury** — not boho-cheap, not cold minimalist. Think editorial meets handmade.
- **Typography**: Pair a refined serif display font (something with personality, like Playfair Display, Cormorant Garamond, or similar from Google Fonts) with a clean, warm body font. The logo's retro serif character should inform the display font choice.
- **Color**: Use the warm off-white as the base. Burgundy and gold as the dominant accent system. Nude beige as a secondary neutral. Avoid using all colors at once; let the palette breathe.
- **Layout**: Editorial, with full-bleed image sections, generous whitespace, and intentional asymmetry. The product images are strong; let them breathe on the page.
- **Motion**: Subtle. Slow fade-ins on scroll, gentle image reveals. Nothing jarring. The craft is slow and deliberate; the site should feel the same.
- **NO generic elements**: No hero carousel with dots, no grid of identical product cards with "Add to Cart" buttons, no stock-looking sections.

## Technical Constraints

- **Frontend only** — no backend, no database, no CMS
- **Static HTML/CSS/JS** OR **React/Vite** — choose what produces the cleanest result
- All images are local assets; reference them by filename
- Mobile-responsive is required
- No external dependencies for functionality; Google Fonts is fine
- Performance matters: optimize image usage, no bloated libraries

## What Success Looks Like

Someone visits this site and immediately understands: this is a premium handmade product with a distinctive identity. They want to own one of these bags. The site does not look like a template, a Wix site, or a generic small business page. It looks like something a thoughtful designer built specifically for this brand.
