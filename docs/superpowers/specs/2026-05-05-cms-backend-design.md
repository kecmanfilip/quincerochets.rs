# Quincè crochèts — CMS Backend Design Spec

> **Date:** 2026-05-05
> **Scope:** Migrate static HTML site to Astro + Decap CMS, enabling non-technical client to add bags, blog posts, and edit page content.
> **Cost Target:** $0/month hosting

---

## 1. Goals

1. **Client can add new bags** without touching code — via web UI at `/admin/`
2. **Client can write blog posts** with images, tags, and publishing dates
3. **Client can edit page content** — homepage text, about section, FAQ items
4. **Preserve all existing SEO** — schema.org, Open Graph, canonical URLs, hreflang
5. **Preserve all existing design** — colors, typography, layout, animations
6. **Zero hosting cost** — use Netlify free tier

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENT BROWSER                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Public Site  │  │ /admin/      │  │ Netlify Identity │  │
│  │ (Astro SSG)  │  │ (Decap CMS)  │  │ (Auth)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  NETLIFY                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Git Repo     │  │ Build Hook   │  │ CDN / Hosting    │  │
│  │ (Content)    │  │ (Auto-build) │  │ (Static HTML)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Content flow:**
1. Client logs into `/admin/` via Netlify Identity
2. Decap CMS reads/writes content as markdown files in the git repo
3. On save, Decap commits to git
4. Netlify detects the commit, triggers build
5. Astro reads content collections, generates static HTML
6. Netlify deploys new site to CDN

---

## 3. Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Framework | Astro | ^5.x | Static site generation, content collections |
| Language | TypeScript | ^5.x | Type safety for content schemas |
| CMS | Decap CMS | ^3.x | Git-based content management UI |
| Auth | Netlify Identity | — | User authentication for /admin/ |
| Styling | Existing CSS | — | `public/css/style.css` preserved |
| Hosting | Netlify | — | Build, deploy, CDN, forms |
| Images | Local repo | — | `public/images/` — no external service |

---

## 4. Content Schema

### 4.1 Products (bags)

```typescript
// src/content/config.ts
const products = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),                    // "Fiona"
    slug: z.string(),                    // "fiona"
    price: z.number(),                   // 4500
    size: z.enum(['XS','S','M','M-L','L']),
    size_label: z.string(),              // "Srednja torbica"
    type: z.string(),                    // "Bucket bag"
    badge: z.string().optional(),        // "Bestseler" | "Novo" | "Premium"
    description_short: z.string(),       // Meta description + OG
    description_full: z.string(),        // Long product description
    dimensions: z.string(),              // "~28 × 22 cm"
    handle: z.string(),                  // "Chunky ručka + opcija lančića"
    colors: z.array(z.string()),         // ["bordo", "nude", "crna"]
    has_chain: z.boolean().default(false),
    images: z.array(z.object({
      src: z.string(),
      alt: z.string(),
    })),
    related: z.array(z.string()),        // ["mini-fiona", "milla", ...]
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});
```

### 4.2 Blog Posts

```typescript
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
```

### 4.3 Site Settings (singleton)

```typescript
const settings = defineCollection({
  type: 'data',
  schema: z.object({
    hero_title: z.string(),
    hero_subtitle: z.string(),
    hero_cta_primary: z.string(),
    hero_cta_secondary: z.string(),
    about_text: z.string(),
    instagram_handle: z.string().default('quincecrochets'),
    contact_email: z.string().optional(),
    delivery_time: z.string().default('5 do 7 radnih dana'),
  }),
});
```

### 4.4 FAQ Items

```typescript
const faq = defineCollection({
  type: 'data',
  schema: z.array(z.object({
    question: z.string(),
    answer: z.string(),
  })),
});
```

---

## 5. URL Structure (Preserved)

| URL | Page | Source |
|-----|------|--------|
| `/` | Homepage | `src/pages/index.astro` |
| `/kolekcija/` | Collection grid | `src/pages/kolekcija/index.astro` |
| `/kolekcija/fiona/` | Product detail | `src/pages/kolekcija/[slug].astro` |
| `/blog/` | Blog listing | `src/pages/blog/index.astro` *(NEW)* |
| `/blog/prvi-post/` | Blog post | `src/pages/blog/[slug].astro` *(NEW)* |
| `/o-nama/` | About | `src/pages/o-nama.astro` |
| `/faq/` | FAQ | `src/pages/faq.astro` |
| `/kontakt/` | Contact | `src/pages/kontakt.astro` |
| `/admin/` | CMS Dashboard | `public/admin/index.html` |

**All existing URLs preserved.** No 301 redirects needed.

---

## 6. Page Design

### 6.1 Homepage (`/`)

**Layout:** Same as current — hero, featured products, about snippet, why-us, Instagram CTA.

**Changes:**
- Featured products section pulls from CMS — shows first 6 non-draft products
- Hero text editable via CMS settings
- About snippet text editable via CMS settings

### 6.2 Collection Page (`/kolekcija/`)

**Layout:** Same grid, same filters.

**Changes:**
- Grid populated from `getCollection('products')`
- Filter buttons still work client-side
- Badges, prices, descriptions all from CMS

### 6.3 Product Detail (`/kolekcija/:slug/`)

**Layout:** Same two-column layout (gallery left, info right).

**Changes:**
- Dynamic route `[slug].astro`
- All product data from CMS
- Related products resolved via `related` slugs
- Schema.org Product JSON-LD generated dynamically
- OG tags generated dynamically

### 6.4 Blog Listing (`/blog/`)

**Layout:** Editorial grid of post cards.

**Design:**
- Page header with eyebrow "✦ Blog ✦", title "Priče o pletenom", subtitle
- Grid of cards: cover image, title, excerpt, date, tags
- Each card links to post
- Responsive: 3 cols → 2 cols → 1 col

### 6.5 Blog Post (`/blog/:slug/`)

**Layout:** Editorial article layout.

**Design:**
- Cover image (full width, max-height 500px)
- Title, date, tags
- Rich text content (prose styling matching brand)
- Author block
- Related posts (3 latest)
- Schema.org Article JSON-LD
- OG tags for social sharing

### 6.6 About, FAQ, Contact

**Layout:** Preserved exactly.

**Changes:**
- FAQ accordion items from CMS
- About text from CMS settings
- Contact form unchanged (still Netlify Forms)

---

## 7. Admin UI (Decap CMS)

### 7.1 Collections

**Kolekcija (Products)**
- List view with name, price, size, badge
- Editor fields: all product fields
- Image widget for uploading product photos
- Relation widget for "related products"
- Draft toggle

**Blog**  
- List view with title, date, published status
- Editor fields: title, slug, date, excerpt, cover image, tags, content
- Markdown body with rich text editor
- Published toggle

**Podešavanja (Settings)**
- Singleton — only one document
- Hero text fields
- About text (textarea)
- Contact info

**FAQ**
- List of Q&A pairs
- Reorderable

### 7.2 Authentication

- Netlify Identity with invite-only registration
- Client receives email invite, sets password
- Login at `/admin/`
- No public registration

---

## 8. SEO Preservation Checklist

Every page must output:
- [ ] `<title>` — from CMS or fallback
- [ ] `<meta name="description">` — from CMS
- [ ] `<link rel="canonical">` — current URL
- [ ] `<link rel="alternate" hreflang>` — sr, sr-RS, x-default
- [ ] `<meta property="og:*">` — Open Graph tags
- [ ] `<meta name="twitter:*">` — Twitter Card tags
- [ ] `application/ld+json` — Schema.org structured data
- [ ] `<meta name="robots" content="index, follow">`

Product pages additionally:
- [ ] Schema.org Product with Offer, Brand, additionalProperty
- [ ] Schema.org BreadcrumbList
- [ ] `product:price:amount` and `product:price:currency` OG tags

Homepage additionally:
- [ ] Schema.org Organization
- [ ] Schema.org WebSite
- [ ] Schema.org ItemList (collection)

Blog posts additionally:
- [ ] Schema.org Article
- [ ] Schema.org BreadcrumbList

---

## 9. Image Strategy

**Product images:**
- Stored in `public/images/products/{slug}/`
- Client uploads via Decap CMS image widget
- CMS commits image to git
- Astro references via `/images/products/{slug}/filename.jpg`
- Recommended: 1200×1500px, JPEG, ~200KB each

**Blog cover images:**
- Stored in `public/images/blog/`
- Same upload workflow

**Existing images:**
- All current images in `public/images/` preserved
- New product images go to subdirectories for organization

**Image optimization:**
- Astro `astro:assets` for responsive images (optional Phase 2)
- For Phase 1, use standard `<img>` with lazy loading

---

## 10. Build & Deploy

**Build command:** `npm run build`
**Output directory:** `dist/`
**Node version:** 20.x

**Netlify configuration:**
- Identity enabled
- Git Gateway enabled (for Decap CMS)
- Build hooks: automatic on push
- Form handling: preserve existing contact form
- Redirects: SPA fallback for admin, 404 page

---

## 11. Performance Targets

- Lighthouse Performance: 95+
- Lighthouse Accessibility: 100
- Lighthouse SEO: 100
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s

Astro's static output + minimal JS + existing optimized CSS should easily hit these.

---

## 12. Security

- No server-side code exposed (static output only)
- CMS behind auth (Netlify Identity)
- No database = no SQL injection
- No user input on public pages = no XSS surface
- Security headers preserved from existing `netlify.toml`

---

## 13. Rollback Strategy

Since everything is in git:
- Bad content change? Revert the commit in GitHub/Netlify.
- Bad deployment? Netlify maintains deploy history — one-click rollback.
- No database migrations to worry about.

---

## 14. Out of Scope (Phase 2)

- E-commerce checkout (still order-via-Instagram/DM)
- User accounts for customers
- Inventory management
- Multi-language (i18n)
- Newsletter subscription
- Image optimization pipeline (Astro assets)
- Search functionality

These can be added later without architectural changes.
