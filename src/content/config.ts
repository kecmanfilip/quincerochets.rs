import { defineCollection, z } from 'astro:content';

const products = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
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
    // What fits section
    fits_video: z.string().optional(),
    fits_description: z.string().optional(),
    // Product FAQ
    product_faq: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).default([]),
    // Lookbook / Style guide
    lookbook_images: z.array(z.object({
      src: z.string(),
      alt: z.string(),
      caption: z.string().optional(),
    })).default([]),
    has_pdf_guide: z.boolean().default(false),
    pdf_guide_url: z.string().optional(),
    // SEO
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
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
    about_text: z.string().default('Quincè crochèts je mala radionica posvećena izradi ručno pletenih torbica od visokokvalitetnih pamučnih traka. Svaka torbica nastaje ručno, bez mašine.'),
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
