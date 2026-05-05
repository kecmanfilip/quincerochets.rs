# Quincè crochèts CMS Backend — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate static HTML site to Astro + Decap CMS, preserving all design, SEO, and URLs, while giving the client a zero-cost admin panel to add bags, blog posts, and edit content.

**Architecture:** Astro static site generator with content collections (products, blog, settings, FAQ). Decap CMS provides a Git-based admin UI at `/admin/`. Netlify handles builds, hosting, auth, and forms. No database — content lives as markdown in git.

**Tech Stack:** Astro 5.x, TypeScript, Decap CMS 3.x, Netlify Identity, existing CSS/JS.

---

## File Structure

```
quincerochets/
├── src/
│   ├── content/
│   │   ├── config.ts              # Content collection schemas
│   │   ├── products/              # Bag data (*.md)
│   │   ├── blog/                  # Blog posts (*.md)
│   │   ├── settings.json          # Site settings
│   │   └── faq.json               # FAQ items
│   ├── layouts/
│   │   └── Layout.astro           # Base HTML layout
│   ├── components/
│   │   ├── Nav.astro              # Shared navigation
│   │   ├── Footer.astro           # Shared footer
│   │   ├── ProductCard.astro      # Reusable product card
│   │   ├── ProductSchema.astro    # Schema.org Product JSON-LD
│   │   ├── BlogCard.astro         # Blog post card
│   │   ├── Breadcrumbs.astro      # Breadcrumb nav
│   │   └── SeoHead.astro          # SEO meta tags component
│   ├── pages/
│   │   ├── index.astro            # Homepage
│   │   ├── kolekcija/
│   │   │   ├── index.astro        # Collection grid
│   │   │   └── [slug].astro       # Product detail (dynamic)
│   │   ├── blog/
│   │   │   ├── index.astro        # Blog listing
│   │   │   └── [slug].astro       # Blog post (dynamic)
│   │   ├── o-nama.astro           # About page
│   │   ├── faq.astro              # FAQ page
│   │   ├── kontakt.astro          # Contact page
│   │   └── 404.astro              # 404 page
│   └── styles/
│       └── (existing css/style.css reused via public/)
├── public/
│   ├── css/style.css              # Copied from existing
│   ├── js/main.js                 # Copied from existing
│   ├── images/                    # All existing + new images
│   ├── admin/
│   │   ├── index.html             # Decap CMS entry point
│   │   └── config.yml             # Decap CMS configuration
│   ├── robots.txt
│   ├── sitemap.xml
│   └── .nojekyll
├── astro.config.mjs
├── tsconfig.json
├── package.json
├── netlify.toml                   # Updated
└── .gitignore                     # Updated
```

---

## Phase 1: Project Setup

### Task 1: Initialize Astro Project

**Files:**
- Create: `package.json`
- Create: `astro.config.mjs`
- Create: `tsconfig.json`
- Modify: `.gitignore`

- [ ] **Step 1: Create package.json**

```json
{
  "name": "quincerochets",
  "type": "module",
  "version": "2.0.0",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "astro": "^5.7.5",
    "@astrojs/check": "^0.9.4",
    "typescript": "^5.8.3"
  },
  "devDependencies": {
    "@types/node": "^22.15.3"
  }
}
```

- [ ] **Step 2: Create astro.config.mjs**

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://quincerochets.rs',
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
});
```

- [ ] **Step 3: Create tsconfig.json**

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

- [ ] **Step 4: Update .gitignore**

Add these lines to existing `.gitignore`:

```
# Astro
node_modules/
dist/
.astro/

# macOS
.DS_Store
```

- [ ] **Step 5: Install dependencies**

Run: `npm install`
Expected: `node_modules/` created, no errors.

- [ ] **Step 6: Commit**

```bash
git add package.json astro.config.mjs tsconfig.json .gitignore
git commit -m "chore: initialize Astro project"
```

---

### Task 2: Move Existing Assets

**Files:**
- Create: `public/css/style.css` (copy from existing)
- Create: `public/js/main.js` (copy from existing)
- Create: `public/images/` (copy all existing images)
- Create: `public/robots.txt` (copy from existing)
- Create: `public/sitemap.xml` (copy from existing)
- Create: `public/.nojekyll` (copy from existing)

- [ ] **Step 1: Copy all existing public assets**

Run:
```bash
# CSS and JS already exist at root level in old structure
# In new Astro structure, they go in public/
cp css/style.css public/css/style.css
cp js/main.js public/js/main.js
cp -r images/* public/images/
cp robots.txt public/
cp sitemap.xml public/
cp .nojekyll public/
```

- [ ] **Step 2: Commit**

```bash
git add public/
git commit -m "chore: migrate existing static assets to public/"
```

---

## Phase 2: Content Collections & Schemas

### Task 3: Define Content Config

**Files:**
- Create: `src/content/config.ts`

- [ ] **Step 1: Write content config**

```typescript
import { defineCollection, z } from 'astro:content';

const products = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    price: z.number(),
    size: z.enum(['XS', 'S', 'M', 'M-L', 'L']),
    size_label: z.string(),
    type: z.string(),
    badge: z.string().optional(),
    description_short: z.string(),
    description_full: z.string(),
    dimensions: z.string(),
    handle: z.string(),
    colors: z.array(z.string()),
    has_chain: z.boolean().default(false),
    images: z.array(z.object({
      src: z.string(),
      alt: z.string(),
    })).default([]),
    related: z.array(z.string()).default([]),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    date: z.date(),
    excerpt: z.string(),
    cover_image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Quincè crochèts'),
    published: z.boolean().default(true),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
  }),
});

const settings = defineCollection({
  type: 'data',
  schema: z.object({
    hero_title: z.string().default('Ručno rađene pletene torbice iz Srbije'),
    hero_subtitle: z.string().default('Chunky crochet torbe od pamučnih traka. 12 modela, boje po izboru, svaki komad jedinstven. Dostava na celoj teritoriji Srbije.'),
    hero_cta_primary: z.string().default('Pogledaj kolekciju'),
    hero_cta_secondary: z.string().default('Poruči'),
    about_text: z.string().default('Quincè crochèts je mala radionica posvećena izradi ručno pletenih torbica od visokokvalitetnih pamučnih traka.'),
    instagram_handle: z.string().default('quincecrochets'),
    delivery_time: z.string().default('5 do 7 radnih dana'),
  }),
});

const faq = defineCollection({
  type: 'data',
  schema: z.array(z.object({
    question: z.string(),
    answer: z.string(),
  })),
});

export const collections = { products, blog, settings, faq };
```

- [ ] **Step 2: Commit**

```bash
git add src/content/config.ts
git commit -m "feat: define content collection schemas"
```

---

### Task 4: Migrate Product Data

**Files:**
- Create: `src/content/products/gia.md` through `src/content/products/milla.md` (12 files)

- [ ] **Step 1: Create product markdown files**

Convert each product from `generate_pages.py` `MODELS` array into a markdown file.

Example for `fiona.md`:

```markdown
---
name: "Fiona"
slug: "fiona"
price: 4500
size: "M"
size_label: "Srednja torbica"
type: "Bucket bag"
badge: "Bestseler"
description_short: "Signature model Quincè crochèts. Prostrana bucket torbica od chunky pamučnih traka, zlatna pločica."
description_full: "Fiona je naš signature model i apsolutni bestseler. Klasičan bucket bag oblik u chunky crochet izvedbi od visokokvalitetnih pamučnih traka. Prostrana unutrašnjost prima sve što trebaš za ceo dan. Pozlaćena laser gravirana pločica je prepoznatljivi potpis svakog Quincè komada. Dostupna u bordo, nude, crnoj i bojama po izboru."
dimensions: "~28 × 22 cm"
handle: "Chunky ručka + opcija lančića"
colors: ["bordo", "nude", "crna"]
has_chain: false
images:
  - src: "/images/bordo-torbica.jpg"
    alt: "Fiona — bordo chunky bucket torbica Quincè crochèts"
related: ["mini-fiona", "milla", "dorothy", "maisie"]
seo_title: "Fiona — Ručno Rađena Pletena Torbica | Quincè crochèts"
seo_description: "Signature model Quincè crochèts. Prostrana bucket torbica od chunky pamučnih traka, zlatna pločica. Quincè crochèts, Srbija. Cena: 4,500 RSD. Dostava na celoj teritoriji Srbije."
---
```

Create all 12 files following this pattern, using data from `generate_pages.py` `MODELS` array.

- [ ] **Step 2: Commit**

```bash
git add src/content/products/
git commit -m "feat: migrate 12 product data files to content collections"
```

---

### Task 5: Create Settings and FAQ Data

**Files:**
- Create: `src/content/settings.json`
- Create: `src/content/faq.json`

- [ ] **Step 1: Create settings.json**

```json
{
  "hero_title": "Ručno rađene pletene torbice iz Srbije",
  "hero_subtitle": "Chunky crochet torbe od pamučnih traka. 12 modela, boje po izboru, svaki komad jedinstven. Dostava na celoj teritoriji Srbije.",
  "hero_cta_primary": "Pogledaj kolekciju",
  "hero_cta_secondary": "Poruči",
  "about_text": "Quincè crochèts je mala radionica posvećena izradi ručno pletenih torbica od visokokvalitetnih pamučnih traka. Svaka torbica nastaje ručno, bez mašine.",
  "instagram_handle": "quincecrochets",
  "delivery_time": "5 do 7 radnih dana"
}
```

- [ ] **Step 2: Create faq.json**

Extract FAQ items from existing `faq/index.html`:

```json
[
  {
    "question": "Kako mogu da poručim torbicu?",
    "answer": "Možeš da nas kontaktiraš putem Instagrama @quincecrochets ili preko kontakt forme na sajtu. Javi nam koji model i boju želiš, a mi ćemo ti poslati detalje."
  },
  {
    "question": "Koliko traje izrada?",
    "answer": "Vreme izrade je 5 do 7 radnih dana. Svaki komad se izrađuje ručno na porudžbinu."
  },
  {
    "question": "Da li mogu da biram boju?",
    "answer": "Da! Svaki model možeš poručiti u bordo, nude, crnoj ili boji po izboru. Javi nam šta želiš."
  },
  {
    "question": "Kolika je dostava?",
    "answer": "Dostavljamo kurirskom službom na celoj teritoriji Srbije. Cena dostave zavisi od lokacije — kontaktiraj nas za tačan iznos."
  },
  {
    "question": "Da li je svaka torbica zaista ručni rad?",
    "answer": "Apsolutno. Svaka torbica je ručno ispletena od pamučnih traka, bez mašine. Svaki komad je jedinstven."
  }
]
```

(Verify exact Q&A from `faq/index.html` and use those.)

- [ ] **Step 3: Commit**

```bash
git add src/content/settings.json src/content/faq.json
git commit -m "feat: add site settings and FAQ data files"
```

---

## Phase 3: Layouts & Components

### Task 6: Create Base Layout

**Files:**
- Create: `src/layouts/Layout.astro`

- [ ] **Step 1: Write Layout.astro**

This replaces the `<head>` and wrapping structure from every existing HTML file.

```astro
---
export interface Props {
  title: string;
  description: string;
  canonical?: string;
  ogType?: string;
  ogImage?: string;
  ogImageAlt?: string;
  twitterImage?: string;
  schema?: string;
  noindex?: boolean;
}

const {
  title,
  description,
  canonical,
  ogType = 'website',
  ogImage = 'https://quincerochets.rs/images/dve-torbe.jpg',
  ogImageAlt = 'Quincè crochèts ručno rađene pletene torbice',
  twitterImage = ogImage,
  schema,
  noindex = false,
} = Astro.props;

const canonicalUrl = canonical || new URL(Astro.url.pathname, Astro.site).href;
---

<!DOCTYPE html>
<html lang="sr" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content={description} />
  {noindex ? (
    <meta name="robots" content="noindex, nofollow" />
  ) : (
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  )}
  <link rel="canonical" href={canonicalUrl} />
  <link rel="alternate" hreflang="sr" href={canonicalUrl} />
  <link rel="alternate" hreflang="sr-RS" href={canonicalUrl} />
  <link rel="alternate" hreflang="x-default" href="https://quincerochets.rs/" />
  <meta property="og:type" content={ogType} />
  <meta property="og:site_name" content="Quincè crochèts" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={ogImage} />
  <meta property="og:image:width" content="1080" />
  <meta property="og:image:height" content="720" />
  <meta property="og:image:alt" content={ogImageAlt} />
  <meta property="og:url" content={canonicalUrl} />
  <meta property="og:locale" content="sr_RS" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={twitterImage} />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/style.css" />
  {schema && (
    <script type="application/ld+json" set:html={schema} />
  )}
</head>
<body>
  <a href="#main" class="skip-link">Preskoči na sadržaj</a>
  <slot name="nav" />
  <main id="main">
    <slot />
  </main>
  <slot name="footer" />
  <script src="/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add src/layouts/Layout.astro
git commit -m "feat: create base Layout component with full SEO support"
```

---

### Task 7: Create Nav & Footer Components

**Files:**
- Create: `src/components/Nav.astro`
- Create: `src/components/Footer.astro`

- [ ] **Step 1: Write Nav.astro**

Extract the `<nav>` and `.nav-mobile` from existing HTML into a reusable component. Pass `products` collection to generate dropdown links dynamically.

```astro
---
import { getCollection } from 'astro:content';
const allProducts = await getCollection('products');
const products = allProducts.filter(p => !p.data.draft).sort((a, b) => {
  const order = ['gia','evie','mini-fiona','fiona','yara','mini-yara','emma','maisie','dorothy','claire','zara','milla'];
  return order.indexOf(a.data.slug) - order.indexOf(b.data.slug);
});
---

<nav class="nav" aria-label="Glavna navigacija">
  <a href="/" class="nav-logo-link" aria-label="Quincè crochèts početna">
    <img src="/images/logo.jpg" alt="Quincè crochèts" class="nav-logo" width="42" height="42" />
    <span class="nav-logo-name">Quincè crochèts</span>
  </a>
  <button class="nav-toggle" id="navToggle" aria-label="Otvori meni" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
  <ul class="nav-list">
    <li><a href="/" class="nav-link">Početna</a></li>
    <li class="nav-item">
      <a href="/kolekcija/" class="nav-link">Kolekcija <span class="nav-chevron">▾</span></a>
      <div class="nav-dropdown" role="menu">
        {products.map(p => (
          <a href={`/kolekcija/${p.data.slug}/`} class="dropdown-item" role="menuitem">
            <span>{p.data.name}</span>
            <span class="dropdown-item-size">{p.data.size}</span>
          </a>
        ))}
        <div class="dropdown-footer"><a href="/kolekcija/">Pogledaj sve modele →</a></div>
      </div>
    </li>
    <li><a href="/o-nama/" class="nav-link">O nama</a></li>
    <li><a href="/faq/" class="nav-link">FAQ</a></li>
    <li><a href="/kontakt/" class="nav-link nav-cta">Poruči</a></li>
  </ul>
</nav>

<div class="nav-mobile" id="navMobile" aria-label="Mobilni meni">
  <div class="nav-mobile-list">
    <a href="/" class="nav-mobile-link">Početna</a>
    <div class="nav-mobile-section-title">Kolekcija</div>
    <div class="nav-mobile-grid">
      {products.map(p => (
        <a href={`/kolekcija/${p.data.slug}/`} class="nav-mobile-model">{p.data.name}</a>
      ))}
    </div>
    <a href="/o-nama/" class="nav-mobile-link">O nama</a>
    <a href="/faq/" class="nav-mobile-link">FAQ</a>
    <a href="/kontakt/" class="nav-mobile-cta">Poruči</a>
  </div>
</div>
```

- [ ] **Step 2: Write Footer.astro**

```astro
---
import { getCollection } from 'astro:content';
const allProducts = await getCollection('products');
const products = allProducts.filter(p => !p.data.draft);
const col1 = products.slice(0, 6);
const col2 = products.slice(6);
---

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <img src="/images/logo.jpg" alt="Quincè crochèts" class="footer-logo" width="48" height="48" loading="lazy" />
      <p class="footer-brand-name">Quincè crochèts</p>
      <p>Ručno rađene pletene torbice iz Srbije. Svaki komad je jedinstven.</p>
    </div>
    <div class="footer-nav-grid">
      <div class="footer-nav-col">
        <h4>Sajt</h4>
        <ul>
          <li><a href="/">Početna</a></li>
          <li><a href="/kolekcija/">Kolekcija</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/o-nama/">O nama</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/kontakt/">Kontakt</a></li>
        </ul>
      </div>
      <div class="footer-nav-col">
        <h4>Modeli</h4>
        <ul>
          {col1.map(p => (
            <li><a href={`/kolekcija/${p.data.slug}/`}>{p.data.name}</a></li>
          ))}
        </ul>
      </div>
      <div class="footer-nav-col">
        <h4>Još modela</h4>
        <ul>
          {col2.map(p => (
            <li><a href={`/kolekcija/${p.data.slug}/`}>{p.data.name}</a></li>
          ))}
        </ul>
      </div>
    </div>
    <div class="footer-social">
      <h4>Prati nas</h4>
      <a href="https://www.instagram.com/quincecrochets/" target="_blank" rel="noopener noreferrer" class="footer-insta">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
        @quincecrochets
      </a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2025 Quincè crochèts. Sva prava zadržana.</span>
    <span>Ručno rađene pletene torbice iz Srbije <span class="footer-stars" aria-hidden="true">✦</span></span>
  </div>
</footer>
```

- [ ] **Step 3: Commit**

```bash
git add src/components/Nav.astro src/components/Footer.astro
git commit -m "feat: create Nav and Footer components with dynamic product links"
```

---

### Task 8: Create ProductCard Component

**Files:**
- Create: `src/components/ProductCard.astro`

- [ ] **Step 1: Write ProductCard.astro**

```astro
---
export interface Props {
  slug: string;
  name: string;
  size: string;
  type: string;
  price: number;
  badge?: string;
  image?: string;
  imageAlt?: string;
  description?: string;
  colors?: string[];
}

const { slug, name, size, type, price, badge, image, imageAlt, description, colors } = Astro.props;

const colorMap: Record<string, string> = {
  bordo: '#7a1522',
  nude: '#c5a48a',
  crna: '#3a2828',
};
---

<a href={`/kolekcija/${slug}/`} class="product-card" aria-label={`${name} — ${size} pletena torbica, ${price.toLocaleString('sr-RS')} RSD`}>
  <div class="product-card-img">
    {image ? (
      <img src={image} alt={imageAlt || `${name} — Quincè crochèts pletena torbica`} width="560" height="700" loading="lazy" />
    ) : (
      <div class="product-card-placeholder">
        <span class="placeholder-icon" aria-hidden="true">🧶</span>
        <span class="placeholder-name">{name}</span>
        <span class="placeholder-label">Fotografije uskoro</span>
      </div>
    )}
    {badge && (
      <div class="card-badge-wrap">
        <span class={`badge ${badge === 'Novo' || badge === 'Premium' ? 'badge-gold' : 'badge-crimson'}`}>{badge}</span>
      </div>
    )}
  </div>
  <div class="product-card-body">
    <h3>{name}</h3>
    <p class="card-size">{size} · {type}</p>
    {description && <p>{description}</p>}
    {colors && colors.length > 0 && (
      <div class="color-swatches">
        {colors.map(c => (
          <span class="swatch" style={`background:${colorMap[c] || c}`} title={c}></span>
        ))}
      </div>
    )}
    <div class="card-bottom">
      <span class="card-price">{price.toLocaleString('sr-RS')} RSD <small>/ kom</small></span>
      <span class="card-arrow">→</span>
    </div>
  </div>
</a>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/ProductCard.astro
git commit -m "feat: create reusable ProductCard component"
```

---

## Phase 4: Pages

### Task 9: Homepage

**Files:**
- Create: `src/pages/index.astro`

- [ ] **Step 1: Write index.astro**

Port the existing homepage to Astro, pulling settings and products from CMS.

```astro
---
import Layout from '../layouts/Layout.astro';
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';
import ProductCard from '../components/ProductCard.astro';
import { getCollection, getEntry } from 'astro:content';

const settings = await getEntry('settings', 'settings');
const allProducts = await getCollection('products');
const products = allProducts.filter(p => !p.data.draft);

// Featured: Fiona, Milla, Yara, Dorothy, Gia, Maisie
const featuredSlugs = ['fiona', 'milla', 'yara', 'dorothy', 'gia', 'maisie'];
const featured = featuredSlugs
  .map(slug => products.find(p => p.data.slug === slug))
  .filter(Boolean);

const schema = JSON.stringify({
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://quincerochets.rs/#organization",
      "name": "Quincè crochèts",
      "alternateName": ["Quince Crochets", "Quincè crochèts Srbija"],
      "url": "https://quincerochets.rs/",
      "logo": {"@type":"ImageObject","url":"https://quincerochets.rs/images/logo.jpg","width":800,"height":800},
      "image": "https://quincerochets.rs/images/dve-torbe.jpg",
      "description": settings?.data.about_text || "Ručno rađene pletene torbice od pamučnih traka.",
      "address": {"@type":"PostalAddress","addressCountry":"RS","addressRegion":"Srbija"},
      "areaServed": {"@type":"Country","name":"Srbija"},
      "sameAs": ["https://www.instagram.com/quincecrochets/"],
      "foundingDate": "2023"
    },
    {
      "@type": "WebSite",
      "@id": "https://quincerochets.rs/#website",
      "url": "https://quincerochets.rs/",
      "name": "Quincè crochèts — Pletene Torbice Srbija",
      "publisher": {"@id":"https://quincerochets.rs/#organization"},
      "inLanguage": "sr-RS"
    },
    {
      "@type": "ItemList",
      "name": "Quincè crochèts kolekcija pletenih torbica",
      "description": `${products.length} modela ručno rađenih chunky crochet torbica od pamučnih traka`,
      "url": "https://quincerochets.rs/kolekcija/",
      "numberOfItems": products.length,
      "itemListElement": products.map((p, i) => ({
        "@type": "ListItem",
        "position": i + 1,
        "url": `https://quincerochets.rs/kolekcija/${p.data.slug}/`,
        "name": p.data.name
      }))
    }
  ]
});
---

<Layout
  title="Quincè crochèts | Ručno Rađene Pletene Torbice iz Srbije"
  description="Ručno rađene chunky crochet torbice od pamučnih traka. 12 modela u bojama po izboru. Dostava na celoj teritoriji Srbije. Instagram: @quincecrochets"
  ogImage="https://quincerochets.rs/images/dve-torbe.jpg"
  ogImageAlt="Quincè crochèts ručno rađene pletene torbice — bordo i nude"
  schema={schema}
>
  <Nav slot="nav" />

  <!-- HERO -->
  <section class="hero" aria-label="Naslovna">
    <div class="hero-text">
      <p class="hero-eyebrow">Ručno rađeno sa ljubavlju</p>
      <h1 set:html={settings?.data.hero_title.replace('pletene torbice', '<em>pletene torbice</em>')} />
      <p class="hero-desc">{settings?.data.hero_subtitle}</p>
      <div class="hero-ctas">
        <a href="/kolekcija/" class="btn btn-primary">{settings?.data.hero_cta_primary}</a>
        <a href="/kontakt/" class="btn btn-outline">{settings?.data.hero_cta_secondary}</a>
      </div>
    </div>
    <div class="hero-image-col">
      <img src="/images/torbica-i-ruka.jpg" alt="Quincè crochèts bordo pletena torbica sa zlatnim lančićem — ručno rađena u Srbiji" class="hero-img-main" width="460" height="620" fetchpriority="high" loading="eager" />
      <div class="hero-badge" aria-label="100% ručni rad">
        <span class="hero-badge-icon" aria-hidden="true">🧶</span>
        <div class="hero-badge-text">
          <strong>100% ručni rad</strong>
          <span>Jedinstven komad</span>
        </div>
      </div>
    </div>
  </section>

  <!-- FEATURED MODELS -->
  <section class="section bg-cream" aria-labelledby="featured-heading">
    <div class="section-header">
      <span class="eyebrow">✦ Kolekcija ✦</span>
      <h2 id="featured-heading">Istaknuti modeli</h2>
      <p>Svaki model je jedinstven komad, ručno izrađen u Srbiji.</p>
      <div class="divider"></div>
    </div>
    <div class="product-grid container">
      {featured.map(p => (
        <ProductCard
          slug={p.data.slug}
          name={p.data.name}
          size={p.data.size}
          type={p.data.type}
          price={p.data.price}
          badge={p.data.badge}
          image={p.data.images[0]?.src}
          imageAlt={p.data.images[0]?.alt}
          description={p.data.description_short}
          colors={p.data.colors}
        />
      ))}
    </div>
    <div style="text-align:center;margin-top:3rem">
      <a href="/kolekcija/" class="btn btn-outline">Pogledaj svih {products.length} modela →</a>
    </div>
  </section>

  <!-- ABOUT SNIPPET -->
  <section class="section bg-blush" aria-labelledby="about-home-heading">
    <div class="about-grid container">
      <div class="about-images">
        <img src="/images/dve-torbe.jpg" alt="Quincè crochèts kolekcija — bordo i nude pletene torbice sa zlatnim ukrasima" class="about-img-main" width="380" height="420" loading="lazy" />
        <img src="/images/closeup-torbica.jpg" alt="Detalj chunky pletiva i zlatne brendirane pločice Quincè crochèts" class="about-img-secondary" width="300" height="280" loading="lazy" />
      </div>
      <div class="about-text">
        <div class="section-header left">
          <span class="eyebrow">✦ Naša priča ✦</span>
          <h2 id="about-home-heading">Ručni rad koji se vidi</h2>
          <div class="divider left"></div>
        </div>
        <p><strong>Quincè crochèts</strong> je mala radionica posvećena izradi ručno pletenih torbica od visokokvalitetnih pamučnih traka. Svaka torbica nastaje ručno, bez mašine.</p>
        <p>Ne pravimo serije. Svaka narudžbina je posebna — biraš boju, model i veličinu, a mi napravimo tačno to.</p>
        <div class="highlights-grid">
          <div class="highlight-item"><span class="highlight-icon" aria-hidden="true">🧶</span><div><h4>Ručni rad</h4><p>Svaki šav ručno ispleteni</p></div></div>
          <div class="highlight-item"><span class="highlight-icon" aria-hidden="true">🎨</span><div><h4>Boja po izboru</h4><p>Poruči u boji koju voliš</p></div></div>
          <div class="highlight-item"><span class="highlight-icon" aria-hidden="true">✨</span><div><h4>Premium detalji</h4><p>Pozlaćena laser gravirana pločica</p></div></div>
          <div class="highlight-item"><span class="highlight-icon" aria-hidden="true">📦</span><div><h4>Dostava po Srbiji</h4><p>Kurirska služba, kućna adresa</p></div></div>
        </div>
        <div style="margin-top:2rem"><a href="/o-nama/" class="btn btn-outline">Saznaj više o nama →</a></div>
      </div>
    </div>
  </section>

  <!-- WHY US -->
  <section class="section bg-cream" aria-labelledby="zasto-heading">
    <div class="section-header">
      <span class="eyebrow">✦ Prednosti ✦</span>
      <h2 id="zasto-heading">Zašto Quincè crochèts?</h2>
      <p>Svaka narudžbina je posebna. Evo šta dobijaš uz svaku torbicu.</p>
      <div class="divider"></div>
    </div>
    <div class="features-grid container">
      <div class="feature-card"><span class="feature-icon" aria-hidden="true">🎁</span><h3>Poklon pakovanje</h3><p>Svaka torbica stiže u lepom poklon pakovanju, odmah spremna za poklanjanje.</p></div>
      <div class="feature-card"><span class="feature-icon" aria-hidden="true">⏱️</span><h3>5-7 dana izrade</h3><p>Vreme izrade je 5 do 7 radnih dana. Za hitne porudžbine, javi se direktno.</p></div>
      <div class="feature-card"><span class="feature-icon" aria-hidden="true">🔄</span><h3>Custom narudžbine</h3><p>Boja, veličina, tip ručke. Reci nam šta želiš i napravimo tačno to.</p></div>
    </div>
  </section>

  <!-- INSTAGRAM -->
  <section class="insta-section" aria-label="Instagram profil">
    <h2>Prati nas na Instagramu</h2>
    <p>Novi modeli, boje i inspiracija — svaki dan na @{settings?.data.instagram_handle}</p>
    <a href={`https://www.instagram.com/${settings?.data.instagram_handle}/`} target="_blank" rel="noopener noreferrer" class="insta-link" aria-label={`Poseti Instagram @${settings?.data.instagram_handle}`}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
      @{settings?.data.instagram_handle}
    </a>
  </section>

  <Footer slot="footer" />
</Layout>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: create homepage with CMS-driven content"
```

---

### Task 10: Collection Page

**Files:**
- Create: `src/pages/kolekcija/index.astro`

- [ ] **Step 1: Write kolekcija/index.astro**

Port the existing collection grid page. Include filter buttons and client-side filtering script.

```astro
---
import Layout from '../../layouts/Layout.astro';
import Nav from '../../components/Nav.astro';
import Footer from '../../components/Footer.astro';
import ProductCard from '../../components/ProductCard.astro';
import { getCollection } from 'astro:content';

const allProducts = await getCollection('products');
const products = allProducts.filter(p => !p.data.draft);

const schema = JSON.stringify({
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://quincerochets.rs/kolekcija/",
      "name": "Kolekcija pletenih torbica — Quincè crochèts",
      "description": `${products.length} modela ručno rađenih chunky crochet torbica od pamučnih traka. Boje po izboru, dostava na celoj teritoriji Srbije.`,
      "url": "https://quincerochets.rs/kolekcija/",
      "inLanguage": "sr-RS",
      "publisher": {"@id":"https://quincerochets.rs/#organization"}
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Početna","item":"https://quincerochets.rs/"},
        {"@type":"ListItem","position":2,"name":"Kolekcija","item":"https://quincerochets.rs/kolekcija/"}
      ]
    }
  ]
});
---

<Layout
  title={`Kolekcija Pletenih Torbica | Quincè crochèts — Svih ${products.length} Modela`}
  description={`Pogledaj svih ${products.length} modela ručno rađenih chunky crochet torbica. Gia, Evie, Fiona, Yara, Milla i još ${products.length - 5} modela. Boje po izboru, dostava po Srbiji.`}
  canonical="https://quincerochets.rs/kolekcija/"
  schema={schema}
>
  <Nav slot="nav" />

  <div class="breadcrumb-bar container">
    <nav class="breadcrumb" aria-label="Navigacioni put">
      <a href="/">Početna</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">Kolekcija</span>
    </nav>
  </div>

  <section class="section-sm bg-blush-light" style="padding-top:2rem">
    <div class="section-header" style="margin-bottom:1rem">
      <span class="eyebrow">✦ Quincè crochèts ✦</span>
      <h1>Kolekcija pletenih torbica</h1>
      <p>{products.length} modela ručno rađenih chunky crochet torbica. Svaki komad jedinstven, boje po izboru.</p>
    </div>
  </section>

  <!-- Filter bar -->
  <div class="section-sm bg-cream" style="padding-top:1rem;padding-bottom:1rem">
    <div class="container" style="display:flex;gap:0.6rem;flex-wrap:wrap;align-items:center">
      <span style="font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--warm-grey)">Filtriraj:</span>
      <button onclick="filterGrid('all')" class="btn btn-sm btn-primary" id="filter-all">Sve ({products.length})</button>
      <button onclick="filterGrid('xs-s')" class="btn btn-sm btn-outline" id="filter-xs-s">Mini & Mala</button>
      <button onclick="filterGrid('m')" class="btn btn-sm btn-outline" id="filter-m">Srednja</button>
      <button onclick="filterGrid('l')" class="btn btn-sm btn-outline" id="filter-l">Velika</button>
      <button onclick="filterGrid('chain')" class="btn btn-sm btn-outline" id="filter-chain">Sa lančićem</button>
    </div>
  </div>

  <section class="section bg-cream" style="padding-top:2rem" aria-labelledby="grid-heading">
    <h2 id="grid-heading" class="sr-only">Svi modeli</h2>
    <div class="product-grid container" id="productGrid">
      {products.map(p => (
        <ProductCard
          slug={p.data.slug}
          name={p.data.name}
          size={p.data.size}
          type={p.data.type}
          price={p.data.price}
          badge={p.data.badge}
          image={p.data.images[0]?.src}
          imageAlt={p.data.images[0]?.alt}
          description={p.data.description_short}
          colors={p.data.colors}
          data-size={p.data.size === 'XS' || p.data.size === 'S' ? 'xs-s' : p.data.size === 'M' || p.data.size === 'M-L' ? 'm' : 'l'}
          data-chain={p.data.has_chain ? 'true' : 'false'}
        />
      ))}
    </div>
  </section>

  <section class="insta-section section-sm" aria-label="Instagram">
    <h2>Nisi sigurna koji model?</h2>
    <p>Piši nam na Instagramu — pomažemo da pronađeš savršenu torbicu za tebe.</p>
    <a href="https://www.instagram.com/quincecrochets/" target="_blank" rel="noopener noreferrer" class="insta-link">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
      DM na @quincecrochets
    </a>
  </section>

  <Footer slot="footer" />
</Layout>

<script is:inline>
function filterGrid(type) {
  var cards = document.querySelectorAll('#productGrid .product-card');
  var btns = document.querySelectorAll('[id^="filter-"]');
  btns.forEach(function(b) { b.className = 'btn btn-sm btn-outline'; });
  document.getElementById('filter-' + type).className = 'btn btn-sm btn-primary';
  cards.forEach(function(c) {
    var show = type === 'all' ||
      (type === 'xs-s' && (c.dataset.size === 'xs-s')) ||
      (type === 'm' && c.dataset.size === 'm') ||
      (type === 'l' && c.dataset.size === 'l') ||
      (type === 'chain' && c.dataset.chain === 'true');
    c.style.display = show ? '' : 'none';
  });
}
</script>
```

Note: The `data-size` and `data-chain` attributes need to be on the `<a>` element. Modify `ProductCard.astro` to accept and render these as `data-*` attributes:

```astro
// In ProductCard.astro, add to Props:
export interface Props {
  // ... existing props
  'data-size'?: string;
  'data-chain'?: string;
}

// In the <a> tag:
<a
  href={`/kolekcija/${slug}/`}
  class="product-card"
  data-size={Astro.props['data-size']}
  data-chain={Astro.props['data-chain']}
  // ...
>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/kolekcija/index.astro src/components/ProductCard.astro
git commit -m "feat: create dynamic collection page with filtering"
```

---

### Task 11: Product Detail Page

**Files:**
- Create: `src/pages/kolekcija/[slug].astro`

- [ ] **Step 1: Write [slug].astro**

```astro
---
import Layout from '../../layouts/Layout.astro';
import Nav from '../../components/Nav.astro';
import Footer from '../../components/Footer.astro';
import ProductCard from '../../components/ProductCard.astro';
import { getCollection, getEntry } from 'astro:content';

export async function getStaticPaths() {
  const products = await getCollection('products');
  return products
    .filter(p => !p.data.draft)
    .map(p => ({
      params: { slug: p.data.slug },
      props: { product: p },
    }));
}

const { product } = Astro.props;
const { data } = product;

const allProducts = await getCollection('products');
const relatedProducts = data.related
  .map(slug => allProducts.find(p => p.data.slug === slug))
  .filter(Boolean)
  .filter(p => !p.data.draft);

const url = `https://quincerochets.rs/kolekcija/${data.slug}/`;
const imgUrl = data.images[0]?.src || 'https://quincerochets.rs/images/logo.jpg';

const schema = JSON.stringify({
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "@id": `${url}#product`,
      "name": data.name,
      "description": data.description_short,
      "image": imgUrl,
      "brand": {"@type":"Brand","name":"Quincè crochèts"},
      "manufacturer": {"@id":"https://quincerochets.rs/#organization"},
      "material": "pamučne trake, t-shirt yarn",
      "color": [...data.colors, "po izboru"],
      "countryOfOrigin": "RS",
      "offers": {
        "@type": "Offer",
        "price": String(data.price),
        "priceCurrency": "RSD",
        "availability": "https://schema.org/MadeToOrder",
        "seller": {"@id":"https://quincerochets.rs/#organization"},
        "areaServed": {"@type":"Country","name":"Srbija"},
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2026-12-31",
        "url": url
      },
      "additionalProperty": [
        {"@type":"PropertyValue","name":"Veličina","value":data.size},
        {"@type":"PropertyValue","name":"Tip","value":data.type},
        {"@type":"PropertyValue","name":"Dimenzije","value":data.dimensions},
        {"@type":"PropertyValue","name":"Ručka","value":data.handle},
        {"@type":"PropertyValue","name":"Vreme izrade","value":"5 do 7 radnih dana"}
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Početna","item":"https://quincerochets.rs/"},
        {"@type":"ListItem","position":2,"name":"Kolekcija","item":"https://quincerochets.rs/kolekcija/"},
        {"@type":"ListItem","position":3,"name":data.name,"item":url}
      ]
    }
  ]
});

const colorMap: Record<string, string> = {
  bordo: '#7a1522',
  nude: '#c5a48a',
  crna: '#3a2828',
};
---

<Layout
  title={`${data.name} — Ručno Rađena Pletena Torbica | Quincè crochèts`}
  description={`${data.description_short} Quincè crochèts, Srbija. Cena: ${data.price.toLocaleString('sr-RS')} RSD. Dostava na celoj teritoriji Srbije.`}
  canonical={url}
  ogType="product"
  ogImage={imgUrl}
  ogImageAlt={`${data.name} — Quincè crochèts pletena torbica`}
  twitterImage={imgUrl}
  schema={schema}
>
  <Nav slot="nav" />

  <div class="breadcrumb-bar container">
    <nav class="breadcrumb" aria-label="Navigacioni put">
      <a href="/">Početna</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="/kolekcija/">Kolekcija</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">{data.name}</span>
    </nav>
  </div>

  <div class="product-detail">
    <div class="product-detail-grid">
      <!-- Gallery -->
      <div class="product-gallery">
        {data.images[0] ? (
          <img src={data.images[0].src} alt={data.images[0].alt} class="product-main-img" width="600" height="750" loading="eager" fetchpriority="high" />
        ) : (
          <div class="product-img-placeholder" aria-label={`${data.name} — fotografije uskoro`}>
            <span class="pi-name">{data.name}</span>
            <span class="pi-label">Fotografije uskoro</span>
          </div>
        )}
        <img src="/images/closeup-torbica.jpg" alt="Detalj pletiva i zlatne pozlaćene pločice na Quincè crochèts torbici" class="product-detail-img" width="600" height="338" loading="lazy" />
      </div>

      <!-- Info -->
      <div class="product-info">
        <span class="product-info-eyebrow">✦ Quincè crochèts ✦</span>
        <h1>{data.name}</h1>
        <p class="product-size-tag">{data.size_label} &middot; {data.type}</p>

        <div class="product-price">{data.price.toLocaleString('sr-RS')} RSD</div>
        <p class="product-price-note">Cena za jedan komad. Izrađeno na porudžbinu, vreme isporuke 5–7 radnih dana.</p>

        <p class="product-desc">{data.description_full}</p>

        <!-- Colors -->
        <p class="colors-label">Dostupne boje</p>
        <div class="color-options">
          {data.colors.map(c => (
            <div class="color-option" data-color={c} onclick="void(0)">
              <div class="color-circle" style={`background:${colorMap[c] || c}`}></div>
              <span>{c.charAt(0).toUpperCase() + c.slice(1)}</span>
            </div>
          ))}
          <div class="color-option" data-color="custom" onclick="void(0)">
            <div class="color-circle" style="background:linear-gradient(135deg,#fad4cf,#9b1c2e,#d4941a)"></div>
            <span>Po izboru</span>
          </div>
        </div>

        <!-- Details -->
        <dl class="product-details-grid">
          <div class="detail-item"><dt>Veličina</dt><dd>{data.size} &mdash; {data.size_label}</dd></div>
          <div class="detail-item"><dt>Dimenzije</dt><dd>{data.dimensions}</dd></div>
          <div class="detail-item"><dt>Ručka</dt><dd>{data.handle}</dd></div>
          <div class="detail-item"><dt>Materijal</dt><dd>Pamučne trake (t-shirt yarn)</dd></div>
          <div class="detail-item"><dt>Brendirani detalj</dt><dd>Pozlaćena laser gravirana pločica</dd></div>
          <div class="detail-item"><dt>Vreme izrade</dt><dd>5 do 7 radnih dana</dd></div>
        </dl>

        <!-- CTA -->
        <div class="product-cta-box">
          <p>Svaki komad se izrađuje na porudžbinu. Kontaktiraj nas putem Instagrama ili forme za porudžbinu.</p>
          <a href={`/kontakt/?model=${data.slug}`} class="btn btn-gold btn-full" style="margin-bottom:0.8rem">Poruči {data.name} →</a>
          <a href="https://www.instagram.com/quincecrochets/" target="_blank" rel="noopener noreferrer" class="btn btn-full" style="background:rgba(255,255,255,0.15);color:#fff;border:1px solid rgba(255,255,255,0.3)">DM na Instagram @quincecrochets</a>
          <p class="product-cta-box-note" style="margin-top:0.8rem">Dostava kurirskom službom na celoj teritoriji Srbije.</p>
        </div>
      </div>
    </div>

    <!-- Related -->
    {relatedProducts.length > 0 && (
      <div class="related-section" aria-labelledby="related-heading">
        <div class="section-header">
          <span class="eyebrow">✦ Pogledaj i ✦</span>
          <h2 id="related-heading">Slični modeli</h2>
          <div class="divider"></div>
        </div>
        <div class="related-grid">
          {relatedProducts.map(p => (
            <ProductCard
              slug={p.data.slug}
              name={p.data.name}
              size={p.data.size}
              type={p.data.type}
              price={p.data.price}
              image={p.data.images[0]?.src}
              imageAlt={p.data.images[0]?.alt}
            />
          ))}
        </div>
      </div>
    )}
  </div>

  <Footer slot="footer" />
</Layout>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/kolekcija/\[slug\].astro
git commit -m "feat: create dynamic product detail pages"
```

---

### Task 12: Blog Pages

**Files:**
- Create: `src/pages/blog/index.astro`
- Create: `src/components/BlogCard.astro`
- Create: `src/pages/blog/[slug].astro`

- [ ] **Step 1: Create BlogCard.astro**

```astro
---
export interface Props {
  slug: string;
  title: string;
  date: Date;
  excerpt: string;
  cover_image?: string;
  tags: string[];
}

const { slug, title, date, excerpt, cover_image, tags } = Astro.props;
const formattedDate = date.toLocaleDateString('sr-RS', { day: 'numeric', month: 'long', year: 'numeric' });
---

<a href={`/blog/${slug}/`} class="blog-card">
  <div class="blog-card-image">
    {cover_image ? (
      <img src={cover_image} alt={title} width="400" height="260" loading="lazy" />
    ) : (
      <div class="blog-card-placeholder">
        <span>🧶</span>
      </div>
    )}
  </div>
  <div class="blog-card-body">
    <time datetime={date.toISOString()}>{formattedDate}</time>
    <h3>{title}</h3>
    <p>{excerpt}</p>
    {tags.length > 0 && (
      <div class="blog-card-tags">
        {tags.map(tag => <span class="blog-tag">{tag}</span>)}
      </div>
    )}
    <span class="blog-card-read">Pročitaj →</span>
  </div>
</a>
```

- [ ] **Step 2: Add blog styles to CSS**

Append to `public/css/style.css`:

```css
/* ── BLOG ──────────────────────────────────────────────────── */
.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  max-width: var(--max-w);
  margin: 0 auto;
}

.blog-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.07);
  transition: transform var(--transition), box-shadow var(--transition);
  text-decoration: none; color: inherit;
  display: flex; flex-direction: column;
}
.blog-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 44px rgba(155,28,46,0.15);
}

.blog-card-image {
  overflow: hidden; aspect-ratio: 3/2;
  background: linear-gradient(135deg, var(--blush-light), var(--blush));
}
.blog-card-image img {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform 0.5s ease;
}
.blog-card:hover .blog-card-image img { transform: scale(1.05); }

.blog-card-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 3rem;
}

.blog-card-body {
  padding: 1.4rem 1.6rem 1.8rem;
  flex: 1; display: flex; flex-direction: column;
}
.blog-card-body time {
  font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--gold); margin-bottom: 0.5rem;
}
.blog-card-body h3 {
  font-size: 1.15rem; color: var(--crimson-dark);
  margin-bottom: 0.6rem; line-height: 1.3;
}
.blog-card-body p {
  font-size: 0.88rem; color: var(--warm-grey);
  line-height: 1.6; flex: 1; margin-bottom: 1rem;
}

.blog-card-tags {
  display: flex; gap: 0.4rem; flex-wrap: wrap;
  margin-bottom: 1rem;
}
.blog-tag {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  background: var(--blush-light); color: var(--crimson);
  padding: 0.25rem 0.6rem; border-radius: 4px;
}

.blog-card-read {
  font-size: 0.8rem; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--crimson);
}
.blog-card:hover .blog-card-read { color: var(--gold); }

/* Blog post page */
.blog-post { max-width: 720px; margin: 0 auto; padding: 2rem 1.5rem 5rem; }
.blog-post-cover {
  width: 100%; max-height: 500px; object-fit: cover;
  border-radius: var(--radius-lg); margin-bottom: 2rem;
}
.blog-post-header { margin-bottom: 2.5rem; }
.blog-post-header time {
  font-size: 0.8rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--gold); display: block; margin-bottom: 0.5rem;
}
.blog-post-header h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  color: var(--crimson-dark); margin-bottom: 1rem;
}
.blog-post-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; }

.blog-post-content {
  font-size: 1.05rem; line-height: 1.85;
  color: var(--text);
}
.blog-post-content h2 {
  font-size: 1.5rem; color: var(--crimson-dark);
  margin: 2.5rem 0 1rem;
}
.blog-post-content h3 {
  font-size: 1.2rem; color: var(--crimson-dark);
  margin: 2rem 0 0.8rem;
}
.blog-post-content p { margin-bottom: 1.2rem; color: var(--warm-grey); }
.blog-post-content img {
  border-radius: var(--radius); margin: 1.5rem 0;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.blog-post-content blockquote {
  border-left: 3px solid var(--gold);
  padding-left: 1.5rem; margin: 1.5rem 0;
  font-style: italic; color: var(--crimson-dark);
}
.blog-post-content ul, .blog-post-content ol {
  margin: 1rem 0 1.5rem 1.5rem;
}
.blog-post-content li {
  margin-bottom: 0.4rem; color: var(--warm-grey);
}

.blog-post-author {
  margin-top: 3rem; padding-top: 2rem;
  border-top: 1px solid var(--blush);
  display: flex; align-items: center; gap: 1rem;
}
.blog-post-author-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(135deg, var(--blush), var(--blush-mid));
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem;
}
.blog-post-author-name {
  font-weight: 700; color: var(--crimson-dark);
}
.blog-post-author-role {
  font-size: 0.82rem; color: var(--warm-grey);
}

@media (max-width: 900px) {
  .blog-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .blog-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Create blog index page**

```astro
---
import Layout from '../../layouts/Layout.astro';
import Nav from '../../components/Nav.astro';
import Footer from '../../components/Footer.astro';
import BlogCard from '../../components/BlogCard.astro';
import { getCollection } from 'astro:content';

const allPosts = await getCollection('blog');
const posts = allPosts
  .filter(p => p.data.published)
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
---

<Layout
  title="Blog | Quincè crochèts — Priče o Pletenom"
  description="Saznaj više o ručnom pletenju, materijalima, inspiraciji i novim modelima Quincè crochèts torbica."
  canonical="https://quincerochets.rs/blog/"
>
  <Nav slot="nav" />

  <div class="breadcrumb-bar container">
    <nav class="breadcrumb" aria-label="Navigacioni put">
      <a href="/">Početna</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">Blog</span>
    </nav>
  </div>

  <section class="section-sm bg-blush-light" style="padding-top:2rem">
    <div class="section-header">
      <span class="eyebrow">✦ Quincè crochèts ✦</span>
      <h1>Blog</h1>
      <p>Priče o pletenju, materijalima, inspiraciji i novim modelima.</p>
    </div>
  </section>

  <section class="section bg-cream" aria-labelledby="blog-heading">
    <h2 id="blog-heading" class="sr-only">Svi članci</h2>
    {posts.length > 0 ? (
      <div class="blog-grid container">
        {posts.map(post => (
          <BlogCard
            slug={post.data.slug}
            title={post.data.title}
            date={post.data.date}
            excerpt={post.data.excerpt}
            cover_image={post.data.cover_image}
            tags={post.data.tags}
          />
        ))}
      </div>
    ) : (
      <div class="container" style="text-align:center; padding: 4rem 0">
        <p style="font-size: 1.1rem; color: var(--warm-grey)">Uskoro prvi članak! Prati nas na Instagramu za novosti.</p>
        <a href="https://www.instagram.com/quincecrochets/" target="_blank" rel="noopener noreferrer" class="insta-link" style="margin-top:1.5rem">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          @quincecrochets
        </a>
      </div>
    )}
  </section>

  <Footer slot="footer" />
</Layout>
```

- [ ] **Step 4: Create blog post page**

```astro
---
import Layout from '../../layouts/Layout.astro';
import Nav from '../../components/Nav.astro';
import Footer from '../../components/Footer.astro';
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts
    .filter(p => p.data.published)
    .map(p => ({
      params: { slug: p.data.slug },
      props: { post: p },
    }));
}

const { post } = Astro.props;
const { data, render } = post;
const { Content } = await render();

const allPosts = await getCollection('blog');
const relatedPosts = allPosts
  .filter(p => p.data.published && p.data.slug !== data.slug)
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime())
  .slice(0, 3);

const url = `https://quincerochets.rs/blog/${data.slug}/`;
const formattedDate = data.date.toLocaleDateString('sr-RS', { day: 'numeric', month: 'long', year: 'numeric' });

const schema = JSON.stringify({
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": `${url}#article`,
      "headline": data.title,
      "description": data.excerpt,
      "image": data.cover_image,
      "datePublished": data.date.toISOString(),
      "author": {"@type":"Person","name":data.author},
      "publisher": {"@id":"https://quincerochets.rs/#organization"},
      "url": url,
      "inLanguage": "sr-RS"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Početna","item":"https://quincerochets.rs/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://quincerochets.rs/blog/"},
        {"@type":"ListItem","position":3,"name":data.title,"item":url}
      ]
    }
  ]
});
---

<Layout
  title={`${data.title} | Quincè crochèts Blog`}
  description={data.excerpt}
  canonical={url}
  ogType="article"
  ogImage={data.cover_image}
  ogImageAlt={data.title}
  twitterImage={data.cover_image}
  schema={schema}
>
  <Nav slot="nav" />

  <div class="breadcrumb-bar container">
    <nav class="breadcrumb" aria-label="Navigacioni put">
      <a href="/">Početna</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="/blog/">Blog</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">{data.title}</span>
    </nav>
  </div>

  <article class="blog-post">
    {data.cover_image && (
      <img src={data.cover_image} alt={data.title} class="blog-post-cover" width="720" height="480" />
    )}

    <header class="blog-post-header">
      <time datetime={data.date.toISOString()}>{formattedDate}</time>
      <h1>{data.title}</h1>
      {data.tags.length > 0 && (
        <div class="blog-post-tags">
          {data.tags.map(tag => <span class="blog-tag">{tag}</span>)}
        </div>
      )}
    </header>

    <div class="blog-post-content">
      <Content />
    </div>

    <div class="blog-post-author">
      <div class="blog-post-author-avatar">✨</div>
      <div>
        <div class="blog-post-author-name">{data.author}</div>
        <div class="blog-post-author-role">Ručno rađene pletene torbice iz Srbije</div>
      </div>
    </div>

    {relatedPosts.length > 0 && (
      <div class="related-section" style="margin-top:4rem">
        <div class="section-header left">
          <span class="eyebrow">✦ Još iz bloga ✦</span>
          <h2>Slični članci</h2>
        </div>
        <div class="blog-grid" style="margin-top:2rem">
          {relatedPosts.map(p => (
            <a href={`/blog/${p.data.slug}/`} class="blog-card">
              <div class="blog-card-image">
                {p.data.cover_image ? (
                  <img src={p.data.cover_image} alt={p.data.title} width="400" height="260" loading="lazy" />
                ) : (
                  <div class="blog-card-placeholder"><span>🧶</span></div>
                )}
              </div>
              <div class="blog-card-body">
                <time datetime={p.data.date.toISOString()}>
                  {p.data.date.toLocaleDateString('sr-RS', { day: 'numeric', month: 'long', year: 'numeric' })}
                </time>
                <h3>{p.data.title}</h3>
                <p>{p.data.excerpt}</p>
                <span class="blog-card-read">Pročitaj →</span>
              </div>
            </a>
          ))}
        </div>
      </div>
    )}
  </article>

  <Footer slot="footer" />
</Layout>
```

- [ ] **Step 5: Commit**

```bash
git add src/pages/blog/ src/components/BlogCard.astro public/css/style.css
git commit -m "feat: create blog listing and post pages with editorial design"
```

---

### Task 13: Static Pages (About, FAQ, Contact, 404)

**Files:**
- Create: `src/pages/o-nama.astro`
- Create: `src/pages/faq.astro`
- Create: `src/pages/kontakt.astro`
- Create: `src/pages/404.astro`

- [ ] **Step 1: Port each static page**

For each page, extract the content from existing HTML files and wrap in Layout + Nav + Footer.

`o-nama.astro` — port from `o-nama/index.html`
`faq.astro` — port from `faq/index.html`, pull FAQ items from CMS
`kontakt.astro` — port from `kontakt/index.html`, preserve Netlify form
`404.astro` — port from `404.html`

For `faq.astro`, import FAQ data:

```astro
---
import { getEntry } from 'astro:content';
const faqData = await getEntry('faq', 'faq');
const faqItems = faqData?.data || [];
---

<!-- In the template, render accordion: -->
<div class="faq-list">
  {faqItems.map((item, i) => (
    <div class="faq-item">
      <button class="faq-btn" aria-expanded="false">
        {item.question}
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-answer">
        <p>{item.answer}</p>
      </div>
    </div>
  ))}
</div>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/o-nama.astro src/pages/faq.astro src/pages/kontakt.astro src/pages/404.astro
git commit -m "feat: port static pages (about, faq, contact, 404) to Astro"
```

---

## Phase 5: Decap CMS Admin

### Task 14: Create Decap CMS Configuration

**Files:**
- Create: `public/admin/index.html`
- Create: `public/admin/config.yml`

- [ ] **Step 1: Create admin/index.html**

```html
<!DOCTYPE html>
<html lang="sr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Quincè crochèts — Admin</title>
  <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
  <script>
    if (window.netlifyIdentity) {
      window.netlifyIdentity.on('init', user => {
        if (!user) {
          window.netlifyIdentity.on('login', () => {
            document.location.href = '/admin/';
          });
        }
      });
    }
  </script>
</body>
</html>
```

- [ ] **Step 2: Create admin/config.yml**

```yaml
backend:
  name: git-gateway
  branch: main
  commit_messages:
    create: "cms: create {{collection}} '{{slug}}'"
    update: "cms: update {{collection}} '{{slug}}'"
    delete: "cms: delete {{collection}} '{{slug}}'"
    uploadMedia: "cms: upload '{{path}}'"
    deleteMedia: "cms: delete '{{path}}'"

media_folder: "public/images/uploads"
public_folder: "/images/uploads"
site_url: https://quincerochets.rs
display_url: https://quincerochets.rs
locale: 'sr'

collections:
  - name: "products"
    label: "Kolekcija"
    label_singular: "Torbica"
    folder: "src/content/products"
    create: true
    slug: "{{slug}}"
    fields:
      - { label: "Naziv", name: "name", widget: "string" }
      - { label: "Slug (URL)", name: "slug", widget: "string", pattern: ['^[a-z0-9-]+$', "Mala slova, brojevi i crtice"] }
      - { label: "Cena (RSD)", name: "price", widget: "number", value_type: "int", min: 0 }
      - label: "Veličina"
        name: "size"
        widget: "select"
        options: ["XS", "S", "M", "M-L", "L"]
      - { label: "Opis veličine", name: "size_label", widget: "string", hint: "npr. 'Srednja torbica'" }
      - { label: "Tip", name: "type", widget: "string", hint: "npr. 'Bucket bag', 'Crossbody'" }
      - { label: "Badge", name: "badge", widget: "select", options: ["", "Bestseler", "Novo", "Premium"], required: false }
      - { label: "Kratki opis (SEO)", name: "description_short", widget: "text" }
      - { label: "Puni opis", name: "description_full", widget: "markdown" }
      - { label: "Dimenzije", name: "dimensions", widget: "string", hint: "npr. '~28 × 22 cm'" }
      - { label: "Ručka", name: "handle", widget: "string" }
      - label: "Boje"
        name: "colors"
        widget: "list"
        field: { label: "Boja", name: "color", widget: "select", options: ["bordo", "nude", "crna"] }
      - { label: "Sa lančićem", name: "has_chain", widget: "boolean", default: false }
      - label: "Slike"
        name: "images"
        widget: "list"
        fields:
          - { label: "Slika", name: "src", widget: "image" }
          - { label: "Alt tekst", name: "alt", widget: "string" }
      - label: "Slični modeli"
        name: "related"
        widget: "relation"
        collection: "products"
        value_field: "slug"
        search_fields: ["name", "slug"]
        display_fields: ["name"]
        multiple: true
        required: false
      - { label: "SEO naslov", name: "seo_title", widget: "string", required: false }
      - { label: "SEO opis", name: "seo_description", widget: "text", required: false }
      - { label: "Draft", name: "draft", widget: "boolean", default: false }

  - name: "blog"
    label: "Blog"
    label_singular: "Članak"
    folder: "src/content/blog"
    create: true
    slug: "{{slug}}"
    fields:
      - { label: "Naslov", name: "title", widget: "string" }
      - { label: "Slug (URL)", name: "slug", widget: "string", pattern: ['^[a-z0-9-]+$', "Mala slova, brojevi i crtice"] }
      - { label: "Datum", name: "date", widget: "datetime", date_format: "YYYY-MM-DD", time_format: false }
      - { label: "Izvod", name: "excerpt", widget: "text" }
      - { label: "Naslovna slika", name: "cover_image", widget: "image", required: false }
      - label: "Tagovi"
        name: "tags"
        widget: "list"
        field: { label: "Tag", name: "tag", widget: "string" }
        required: false
      - { label: "Autor", name: "author", widget: "string", default: "Quincè crochèts" }
      - { label: "Objavljen", name: "published", widget: "boolean", default: true }
      - { label: "SEO naslov", name: "seo_title", widget: "string", required: false }
      - { label: "SEO opis", name: "seo_description", widget: "text", required: false }
      - { label: "Sadržaj", name: "body", widget: "markdown" }

  - name: "settings"
    label: "Podešavanja"
    files:
      - label: "Sajt"
        name: "settings"
        file: "src/content/settings.json"
        fields:
          - { label: "Hero naslov", name: "hero_title", widget: "string" }
          - { label: "Hero podnaslov", name: "hero_subtitle", widget: "text" }
          - { label: "Hero CTA primarni", name: "hero_cta_primary", widget: "string" }
          - { label: "Hero CTA sekundarni", name: "hero_cta_secondary", widget: "string" }
          - { label: "O nama tekst", name: "about_text", widget: "text" }
          - { label: "Instagram handle", name: "instagram_handle", widget: "string" }
          - { label: "Vreme isporuke", name: "delivery_time", widget: "string" }

  - name: "faq"
    label: "FAQ"
    files:
      - label: "Česta pitanja"
        name: "faq"
        file: "src/content/faq.json"
        fields:
          - label: "Pitanja i odgovori"
            name: "faq"
            widget: "list"
            fields:
              - { label: "Pitanje", name: "question", widget: "string" }
              - { label: "Odgovor", name: "answer", widget: "text" }
```

- [ ] **Step 3: Commit**

```bash
git add public/admin/
git commit -m "feat: add Decap CMS admin dashboard configuration"
```

---

## Phase 6: Netlify Configuration

### Task 15: Update Netlify Config

**Files:**
- Modify: `netlify.toml`

- [ ] **Step 1: Update netlify.toml**

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[plugins]]
  package = "netlify-plugin-csp"

[[redirects]]
  from = "/kontakt/hvala/"
  to = "/kontakt/hvala/index.html"
  status = 200

[[redirects]]
  from = "/admin/*"
  to = "/admin/index.html"
  status = 200

[[redirects]]
  from = "/*"
  to = "/404.html"
  status = 404

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/images/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=3600, must-revalidate"
```

- [ ] **Step 2: Commit**

```bash
git add netlify.toml
git commit -m "chore: update netlify config for Astro build"
```

---

## Phase 7: Cleanup & Launch

### Task 16: Remove Old Static Files

**Files:**
- Delete: Old static HTML files (backup first if needed)
- Delete: `generate_pages.py`
- Delete: Old `css/`, `js/`, `images/` at root (already moved to `public/`)

- [ ] **Step 1: Remove old files**

```bash
# Remove old root-level files that are now in public/ or replaced by Astro
rm -rf css/ js/ kolekcija/ o-nama/ faq/ kontakt/
rm generate_pages.py
rm index.html 404.html
# Keep CNAME, robots.txt, sitemap.xml if they exist at root
# (they'll be in public/ now)
```

- [ ] **Step 2: Commit**

```bash
git add -A
git commit -m "chore: remove old static files, migrate to Astro"
```

---

### Task 17: Test Build Locally

- [ ] **Step 1: Run dev server**

Run: `npm run dev`
Open: `http://localhost:4321/`
Verify: Homepage renders correctly with all sections

- [ ] **Step 2: Run production build**

Run: `npm run build`
Verify: `dist/` directory created with all pages
Check: No build errors

- [ ] **Step 3: Verify key pages**

- `/` — Homepage with featured products
- `/kolekcija/` — Collection grid with filters
- `/kolekcija/fiona/` — Product detail with schema.org
- `/blog/` — Blog listing (empty or with sample post)
- `/o-nama/` — About page
- `/faq/` — FAQ accordion
- `/kontakt/` — Contact form
- `/admin/` — Decap CMS loads

- [ ] **Step 4: Commit fixes if needed**

---

### Task 18: Deploy to Netlify

- [ ] **Step 1: Push to git**

```bash
git push origin main
```

- [ ] **Step 2: Configure Netlify**

In Netlify dashboard:
1. Go to Site Settings → Identity
2. Enable Identity
3. Go to Services → Git Gateway → Enable Git Gateway
4. Invite the client email under Identity → Users → Invite

- [ ] **Step 3: Verify deployment**

Wait for build to complete.
Verify: `https://quincerochets.rs/` loads
Verify: `https://quincerochets.rs/admin/` loads Decap CMS
Verify: All existing URLs still work

---

## Self-Review Checklist

- [ ] All 12 product pages generate correctly with proper URLs
- [ ] Schema.org JSON-LD present on homepage, products, blog posts
- [ ] Open Graph tags present on all pages
- [ ] Canonical URLs correct
- [ ] Breadcrumb schema on product and blog pages
- [ ] Navigation dropdown shows all products dynamically
- [ ] Footer links all products dynamically
- [ ] Blog link appears in nav and footer
- [ ] Contact form still submits to Netlify
- [ ] Mobile menu works
- [ ] FAQ accordion works
- [ ] Product filters work on collection page
- [ ] Color selection works on product pages
- [ ] Images load correctly
- [ ] CSS styles match original exactly
- [ ] No console errors
- [ ] Lighthouse scores: Performance 95+, Accessibility 100, SEO 100
- [ ] Admin UI loads at `/admin/`
- [ ] Client can log in, add product, and see it live after build
