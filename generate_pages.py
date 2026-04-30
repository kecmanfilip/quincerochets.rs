#!/usr/bin/env python3
"""Generate all 12 product pages for Quincè crochèts."""
import os

BASE = "/Users/kecman/dev/quincerochets"

MODELS = [
    {
        "slug": "gia",
        "name": "Gia",
        "size": "S",
        "size_label": "Mala torbica",
        "type": "Clutch",
        "price": 4300,
        "badge": "",
        "img": None,
        "desc_short": "Kompaktna, elegantna clutch torbica savršena za večernje izlaske i posebne prilike.",
        "desc_full": "Gia je sofisticirana mala torbica koja ne zauzima mnogo prostora, ali privlači pažnju na svakom koraku. Chunky pletivo od pamučnih traka daje joj bogatu teksturu, dok zlatna pozlaćena pločica potpisuje svaki komad. Idealna za pozorište, svadbu, rodendan ili svaki trenutak kad hoćeš da izgledaš posebno.",
        "dims": "~20 × 14 cm",
        "handle": "Kratka chunky ručka",
        "related": ["evie", "claire", "mini-fiona", "mini-yara"],
    },
    {
        "slug": "evie",
        "name": "Evie",
        "size": "S",
        "size_label": "Mala torbica",
        "type": "Baguette",
        "price": 4500,
        "badge": "",
        "img": None,
        "desc_short": "Baguette stil u chunky pletivu. Dugačka i uska forma koja je savršena za svaki dan.",
        "desc_full": "Evie donosi ikonični baguette oblik u chunky crochet izvedbi. Pamučne trake visokog kvaliteta daju joj mekoću i trajnost istovremeno. Nosi se u ruci ili na podlaktici, a pozlaćena pločica daje konačni elegantan detalj. Dostupna u bordo, nude, crnoj i bojama po izboru.",
        "dims": "~28 × 14 cm",
        "handle": "Kratka chunky ručka",
        "related": ["gia", "claire", "fiona", "zara"],
    },
    {
        "slug": "mini-fiona",
        "name": "Mini Fiona",
        "size": "XS",
        "size_label": "Mini torbica",
        "type": "Mini bucket",
        "price": 4000,
        "badge": "",
        "img": None,
        "desc_short": "Mala verzija bestseler Fione. Sav karakter, kompaktna veličina.",
        "desc_full": "Mini Fiona je manji varijant naše najpopularnije Fione. Zadržava isti prepoznatljivi chunky bucket oblik i zlatnu pločicu, ali u kompaktnijoj formi. Savršena za izlaske kad ne trebaš nositi mnogo. Pametna veličina za telefon, kartice i ključeve.",
        "dims": "~18 × 12 cm",
        "handle": "Kratka chunky ručka",
        "related": ["fiona", "gia", "mini-yara", "evie"],
    },
    {
        "slug": "fiona",
        "name": "Fiona",
        "size": "M",
        "size_label": "Srednja torbica",
        "type": "Bucket bag",
        "price": 4500,
        "badge": "Bestseler",
        "img": "/images/bordo-torbica.jpg",
        "desc_short": "Signature model Quincè crochèts. Prostrana bucket torbica od chunky pamučnih traka, zlatna pločica.",
        "desc_full": "Fiona je naš signature model i apsolutni bestseler. Klasičan bucket bag oblik u chunky crochet izvedbi od visokokvalitetnih pamučnih traka. Prostrana unutrašnjost prima sve što trebaš za ceo dan. Pozlaćena laser gravirana pločica je prepoznatljivi potpis svakog Quincè komada. Dostupna u bordo, nude, crnoj i bojama po izboru.",
        "dims": "~28 × 22 cm",
        "handle": "Chunky ručka + opcija lančića",
        "related": ["mini-fiona", "milla", "dorothy", "maisie"],
    },
    {
        "slug": "yara",
        "name": "Yara",
        "size": "M",
        "size_label": "Srednja torbica",
        "type": "Crossbody",
        "price": 4200,
        "badge": "",
        "img": "/images/dve-torbe.jpg",
        "desc_short": "Elegantni crossbody model sa zlatnim lančićem. Za svaki stil i svaku prigodu.",
        "desc_full": "Yara je naš najomiljeniji crossbody model. Zlatni lančić visoke klase omogućava nošenje na ramenu ili kao crossbody. Chunky pletivo od pamučnih traka daje joj volumen i karakterističan Quincè izgled. Dovoljno prostrana za sve dnevne potrebe, ali i savršena za večernje izlaske.",
        "dims": "~26 × 18 cm",
        "handle": "Zlatni lančić (crossbody + shoulder)",
        "related": ["mini-yara", "zara", "milla", "claire"],
    },
    {
        "slug": "mini-yara",
        "name": "Mini Yara",
        "size": "S",
        "size_label": "Mala torbica",
        "type": "Mini crossbody",
        "price": 3800,
        "badge": "",
        "img": "/images/dve-torbe.jpg",
        "desc_short": "Mini verzija Yare. Zlatni lančić, kompaktna forma, maksimalan stil.",
        "desc_full": "Mini Yara donosi isti elegantni crossbody karakter kao Yara, u manjoj formi savršenoj za izlaske i posebne prilike. Zlatni lančić je ključni detalj koji ovom modelu daje premijum izgled. Primit će telefon, kartice i malo više — sve što trebaš kad ne hoćeš da nosiš veliku torbicu.",
        "dims": "~18 × 14 cm",
        "handle": "Zlatni lančić",
        "related": ["yara", "gia", "zara", "evie"],
    },
    {
        "slug": "emma",
        "name": "Emma",
        "size": "M",
        "size_label": "Srednja torbica",
        "type": "Klasična",
        "price": 3200,
        "badge": "",
        "img": None,
        "desc_short": "Klasična zaobljena torbica od chunky pamučnih traka. Timeless oblik koji odgovara svemu.",
        "desc_full": "Emma je naša klasična zaobljena torbica — timeless oblik koji odgovara svakom stilu, svakodnevnoj garderobi i posebnim prilikama. Chunky pletivo od pamučnih traka daje joj prepoznatljiv Quincè izgled, dok zlatna pozlaćena pločica dodaje premijum detalj. Idealna kao poklon ili za sebe.",
        "dims": "~26 × 20 cm",
        "handle": "Chunky ručka",
        "related": ["fiona", "claire", "maisie", "gia"],
    },
    {
        "slug": "maisie",
        "name": "Maisie",
        "size": "M-L",
        "size_label": "Srednje-velika torbica",
        "type": "Hobo",
        "price": 3200,
        "badge": "",
        "img": None,
        "desc_short": "Relaxed hobo stil u chunky pletivu. Prostrana, udobna, lako se nosi na ramenu.",
        "desc_full": "Maisie donosi relaxed hobo energiju u Quincè chunky crochet izvedbi. Polumesec oblik je idealan za rame, a prostrana unutrašnjost prima sve što trebaš za ceo dan. Mekane pamučne trake čine je udobnom za nošenje, a zlatna pločica daje premijum finish. Savršena za market, kafu, ili ceo radni dan.",
        "dims": "~32 × 22 cm",
        "handle": "Chunky ručka (shoulder bag)",
        "related": ["dorothy", "fiona", "milla", "emma"],
    },
    {
        "slug": "dorothy",
        "name": "Dorothy",
        "size": "L",
        "size_label": "Velika torbica",
        "type": "Tote bag",
        "price": 3500,
        "badge": "Novo",
        "img": None,
        "desc_short": "Veliki, klasičan tote u chunky crochet izvedbi. Za svaki dan kad trebaš nositi sve.",
        "desc_full": "Dorothy je naša najveća i najprostranija torbica. Klasičan tote oblik savršeno odgovara za svaki dan — posao, market, fakultet, putovanje. Chunky pletivo od pamučnih traka daje joj strukturu i volumen, dok zlatna pozlaćena pločica potvrđuje Quincè premijum kvalitet. Nosi se u ruci ili na ramenu.",
        "dims": "~36 × 26 cm",
        "handle": "Dve chunky ručke",
        "related": ["milla", "maisie", "fiona", "emma"],
    },
    {
        "slug": "claire",
        "name": "Claire",
        "size": "M",
        "size_label": "Srednja torbica",
        "type": "Structured",
        "price": 5000,
        "badge": "",
        "img": None,
        "desc_short": "Strukturirana torbica sa čistim linijama. Elegancija u chunky pletivnom pakovanju.",
        "desc_full": "Claire je naš najelegantniji strukturirani model. Za razliku od relaxed hobo stila, Claire ima definisane linije koje daju profesionalan i uredan izgled. Dostupna sa kratkom chunky ručkom ili u kombinaciji sa zlatnim lančićem. Idealna za poslovne prilike, večere i sva mesta gde je bitan detalj.",
        "dims": "~24 × 16 cm",
        "handle": "Chunky ručka + opcija lančića",
        "related": ["gia", "evie", "zara", "emma"],
    },
    {
        "slug": "zara",
        "name": "Zara",
        "size": "M",
        "size_label": "Srednja torbica",
        "type": "Crossbody",
        "price": 4200,
        "badge": "",
        "img": None,
        "desc_short": "Elegantni crossbody sa zlatnim lančićem i chunky ručkom. Dva načina nošenja, bezbroj kombinacija.",
        "desc_full": "Zara kombinuje crossbody funkcionalnost sa premijum chunky estetikom. Dolazi sa zlatnim lančićem i chunky ručkom, što znači da možeš birati kako ćeš je nositi svaki dan. Pamučne trake visokog kvaliteta i pozlaćena pločica čine je jednim od naših najsvestranijih modela.",
        "dims": "~24 × 18 cm",
        "handle": "Zlatni lančić + chunky ručka",
        "related": ["yara", "claire", "mini-yara", "milla"],
    },
    {
        "slug": "milla",
        "name": "Milla",
        "size": "L",
        "size_label": "Velika torbica",
        "type": "Statement bag",
        "price": 4800,
        "badge": "Premium",
        "img": "/images/torbica-i-ruka.jpg",
        "desc_short": "Veliki statement komad sa zlatnim lančićem. Za posebne prilike i svakodnevnu eleganciju.",
        "desc_full": "Milla je naša najupečatljivija torbica. Veliki format i premium chunky pletivo od pamučnih traka čine je pravim statement komadom. Zlatni lančić visoke klase omogućava nošenje na ramenu ili kao crossbody. Pozlaćena pločica je uvek tu da potpiše autentičnost. Milla je investicija u stajl koji traje.",
        "dims": "~34 × 24 cm",
        "handle": "Chunky ručka + zlatni lančić",
        "related": ["dorothy", "fiona", "yara", "zara"],
    },
]

MODEL_MAP = {m["slug"]: m for m in MODELS}

NAV = """<nav class="nav" aria-label="Glavna navigacija">
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
        <a href="/kolekcija/gia/" class="dropdown-item" role="menuitem"><span>Gia</span><span class="dropdown-item-size">S</span></a>
        <a href="/kolekcija/evie/" class="dropdown-item" role="menuitem"><span>Evie</span><span class="dropdown-item-size">S</span></a>
        <a href="/kolekcija/mini-fiona/" class="dropdown-item" role="menuitem"><span>Mini Fiona</span><span class="dropdown-item-size">XS</span></a>
        <a href="/kolekcija/fiona/" class="dropdown-item" role="menuitem"><span>Fiona</span><span class="dropdown-item-size">M</span></a>
        <a href="/kolekcija/yara/" class="dropdown-item" role="menuitem"><span>Yara</span><span class="dropdown-item-size">M</span></a>
        <a href="/kolekcija/mini-yara/" class="dropdown-item" role="menuitem"><span>Mini Yara</span><span class="dropdown-item-size">S</span></a>
        <a href="/kolekcija/emma/" class="dropdown-item" role="menuitem"><span>Emma</span><span class="dropdown-item-size">M</span></a>
        <a href="/kolekcija/maisie/" class="dropdown-item" role="menuitem"><span>Maisie</span><span class="dropdown-item-size">M-L</span></a>
        <a href="/kolekcija/dorothy/" class="dropdown-item" role="menuitem"><span>Dorothy</span><span class="dropdown-item-size">L</span></a>
        <a href="/kolekcija/claire/" class="dropdown-item" role="menuitem"><span>Claire</span><span class="dropdown-item-size">M</span></a>
        <a href="/kolekcija/zara/" class="dropdown-item" role="menuitem"><span>Zara</span><span class="dropdown-item-size">M</span></a>
        <a href="/kolekcija/milla/" class="dropdown-item" role="menuitem"><span>Milla</span><span class="dropdown-item-size">L</span></a>
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
      <a href="/kolekcija/gia/" class="nav-mobile-model">Gia</a>
      <a href="/kolekcija/evie/" class="nav-mobile-model">Evie</a>
      <a href="/kolekcija/mini-fiona/" class="nav-mobile-model">Mini Fiona</a>
      <a href="/kolekcija/fiona/" class="nav-mobile-model">Fiona</a>
      <a href="/kolekcija/yara/" class="nav-mobile-model">Yara</a>
      <a href="/kolekcija/mini-yara/" class="nav-mobile-model">Mini Yara</a>
      <a href="/kolekcija/emma/" class="nav-mobile-model">Emma</a>
      <a href="/kolekcija/maisie/" class="nav-mobile-model">Maisie</a>
      <a href="/kolekcija/dorothy/" class="nav-mobile-model">Dorothy</a>
      <a href="/kolekcija/claire/" class="nav-mobile-model">Claire</a>
      <a href="/kolekcija/zara/" class="nav-mobile-model">Zara</a>
      <a href="/kolekcija/milla/" class="nav-mobile-model">Milla</a>
    </div>
    <a href="/o-nama/" class="nav-mobile-link">O nama</a>
    <a href="/faq/" class="nav-mobile-link">FAQ</a>
    <a href="/kontakt/" class="nav-mobile-cta">Poruči</a>
  </div>
</div>"""

FOOTER = """<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <img src="/images/logo.jpg" alt="Quincè crochèts" class="footer-logo" width="48" height="48" loading="lazy" />
      <p class="footer-brand-name">Quincè crochèts</p>
      <p>Ručno rađene pletene torbice iz Srbije. Svaki komad je jedinstven.</p>
    </div>
    <div class="footer-nav-grid">
      <div class="footer-nav-col"><h4>Sajt</h4><ul><li><a href="/">Početna</a></li><li><a href="/kolekcija/">Kolekcija</a></li><li><a href="/o-nama/">O nama</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/kontakt/">Kontakt</a></li></ul></div>
      <div class="footer-nav-col"><h4>Modeli</h4><ul><li><a href="/kolekcija/gia/">Gia</a></li><li><a href="/kolekcija/evie/">Evie</a></li><li><a href="/kolekcija/fiona/">Fiona</a></li><li><a href="/kolekcija/yara/">Yara</a></li><li><a href="/kolekcija/milla/">Milla</a></li><li><a href="/kolekcija/dorothy/">Dorothy</a></li></ul></div>
      <div class="footer-nav-col"><h4>Još modela</h4><ul><li><a href="/kolekcija/mini-fiona/">Mini Fiona</a></li><li><a href="/kolekcija/mini-yara/">Mini Yara</a></li><li><a href="/kolekcija/emma/">Emma</a></li><li><a href="/kolekcija/maisie/">Maisie</a></li><li><a href="/kolekcija/claire/">Claire</a></li><li><a href="/kolekcija/zara/">Zara</a></li></ul></div>
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
</footer>"""


def product_page(m):
    slug = m["slug"]
    name = m["name"]
    price = m["price"]
    size = m["size"]
    size_label = m["size_label"]
    mtype = m["type"]
    badge = m["badge"]
    img = m["img"]
    desc_short = m["desc_short"]
    desc_full = m["desc_full"]
    dims = m["dims"]
    handle = m["handle"]
    related_slugs = m["related"]
    url = f"https://quincerochets.rs/kolekcija/{slug}/"
    img_url = img if img else f"https://quincerochets.rs/images/logo.jpg"

    # Main image or placeholder
    if img:
        main_img_html = f'<img src="{img}" alt="{name} — Quincè crochèts ručno rađena pletena torbica, {size_label.lower()}" class="product-main-img" width="600" height="750" loading="eager" fetchpriority="high" />'
    else:
        main_img_html = f'''<div class="product-img-placeholder" aria-label="{name} — fotografije uskoro">
          <span class="pi-name">{name}</span>
          <span class="pi-label">Fotografije uskoro</span>
        </div>'''

    badge_html = f'<span class="badge badge-crimson">{badge}</span>' if badge else ""

    # Related cards
    related_html_parts = []
    for rs in related_slugs:
        rm = MODEL_MAP[rs]
        ri = rm["img"]
        if ri:
            ri_html = f'<img src="{ri}" alt="{rm["name"]} — Quincè crochèts pletena torbica" width="280" height="350" loading="lazy" />'
        else:
            ri_html = f'<div class="product-card-placeholder"><span class="placeholder-name">{rm["name"]}</span></div>'
        related_html_parts.append(f'''
      <a href="/kolekcija/{rs}/" class="product-card">
        <div class="product-card-img">{ri_html}</div>
        <div class="product-card-body">
          <h3>{rm["name"]}</h3>
          <p class="card-size">{rm["size"]} · {rm["type"]}</p>
          <div class="card-bottom"><span class="card-price">{rm["price"]:,} RSD</span><span class="card-arrow">→</span></div>
        </div>
      </a>''')
    related_html = "\n".join(related_html_parts)

    schema = f'''{{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Product",
        "@id": "{url}#product",
        "name": "{name}",
        "description": "{desc_short}",
        "image": "{img_url}",
        "brand": {{"@type": "Brand","name": "Quincè crochèts"}},
        "manufacturer": {{"@id": "https://quincerochets.rs/#organization"}},
        "material": "pamučne trake, t-shirt yarn",
        "color": ["bordo", "nude", "crna", "po izboru"],
        "countryOfOrigin": "RS",
        "offers": {{
          "@type": "Offer",
          "price": "{price}",
          "priceCurrency": "RSD",
          "availability": "https://schema.org/MadeToOrder",
          "seller": {{"@id": "https://quincerochets.rs/#organization"}},
          "areaServed": {{"@type": "Country","name": "Srbija"}},
          "itemCondition": "https://schema.org/NewCondition",
          "priceValidUntil": "2026-12-31",
          "url": "{url}"
        }},
        "additionalProperty": [
          {{"@type": "PropertyValue","name": "Veličina","value": "{size}"}},
          {{"@type": "PropertyValue","name": "Tip","value": "{mtype}"}},
          {{"@type": "PropertyValue","name": "Dimenzije","value": "{dims}"}},
          {{"@type": "PropertyValue","name": "Ručka","value": "{handle}"}},
          {{"@type": "PropertyValue","name": "Vreme izrade","value": "5 do 7 radnih dana"}}
        ]
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem","position": 1,"name": "Početna","item": "https://quincerochets.rs/"}},
          {{"@type": "ListItem","position": 2,"name": "Kolekcija","item": "https://quincerochets.rs/kolekcija/"}},
          {{"@type": "ListItem","position": 3,"name": "{name}","item": "{url}"}}
        ]
      }}
    ]
  }}'''

    html = f'''<!DOCTYPE html>
<html lang="sr" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} — Ručno Rađena Pletena Torbica | Quincè crochèts</title>
  <meta name="description" content="{desc_short} Quincè crochèts, Srbija. Cena: {price:,} RSD. Dostava na celoj teritoriji Srbije." />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="sr" href="{url}" />
  <link rel="alternate" hreflang="sr-RS" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="https://quincerochets.rs/" />
  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="Quincè crochèts" />
  <meta property="og:title" content="{name} — Quincè crochèts Pletena Torbica" />
  <meta property="og:description" content="{desc_short}" />
  <meta property="og:image" content="{img_url}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="sr_RS" />
  <meta property="product:price:amount" content="{price}" />
  <meta property="product:price:currency" content="RSD" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{name} — Quincè crochèts" />
  <meta name="twitter:description" content="{desc_short}" />
  <meta name="twitter:image" content="{img_url}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/style.css" />
  <script type="application/ld+json">
  {schema}
  </script>
</head>
<body>
<a href="#main" class="skip-link">Preskoči na sadržaj</a>
{NAV}
<main id="main">
  <div class="breadcrumb-bar container">
    <nav class="breadcrumb" aria-label="Navigacioni put">
      <a href="/">Početna</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="/kolekcija/">Kolekcija</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">{name}</span>
    </nav>
  </div>

  <div class="product-detail">
    <div class="product-detail-grid">

      <!-- Gallery -->
      <div class="product-gallery">
        {main_img_html}
        <img src="/images/closeup-torbica.jpg" alt="Detalj pletiva i zlatne pozlaćene pločice na Quincè crochèts torbici" class="product-detail-img" width="600" height="338" loading="lazy" />
      </div>

      <!-- Info -->
      <div class="product-info">
        <span class="product-info-eyebrow">✦ Quincè crochèts ✦</span>
        <h1>{name}</h1>
        <p class="product-size-tag">{size_label} &middot; {mtype}</p>

        <div class="product-price">{price:,} RSD</div>
        <p class="product-price-note">Cena za jedan komad. Izrađeno na porudžbinu, vreme isporuke 5–7 radnih dana.</p>

        <p class="product-desc">{desc_full}</p>

        <!-- Colors -->
        <p class="colors-label">Dostupne boje</p>
        <div class="color-options">
          <div class="color-option" data-color="bordo" onclick="void(0)"><div class="color-circle" style="background:#7a1522"></div><span>Bordo</span></div>
          <div class="color-option" data-color="nude" onclick="void(0)"><div class="color-circle" style="background:#c5a48a"></div><span>Nude</span></div>
          <div class="color-option" data-color="crna" onclick="void(0)"><div class="color-circle" style="background:#3a2828"></div><span>Crna</span></div>
          <div class="color-option" data-color="custom" onclick="void(0)"><div class="color-circle" style="background:linear-gradient(135deg,#fad4cf,#9b1c2e,#d4941a)"></div><span>Po izboru</span></div>
        </div>

        <!-- Details -->
        <dl class="product-details-grid">
          <div class="detail-item"><dt>Veličina</dt><dd>{size} &mdash; {size_label}</dd></div>
          <div class="detail-item"><dt>Dimenzije</dt><dd>{dims}</dd></div>
          <div class="detail-item"><dt>Ručka</dt><dd>{handle}</dd></div>
          <div class="detail-item"><dt>Materijal</dt><dd>Pamučne trake (t-shirt yarn)</dd></div>
          <div class="detail-item"><dt>Brendirani detalj</dt><dd>Pozlaćena laser gravirana pločica</dd></div>
          <div class="detail-item"><dt>Vreme izrade</dt><dd>5 do 7 radnih dana</dd></div>
        </dl>

        <!-- CTA -->
        <div class="product-cta-box">
          <p>Svaki komad se izrađuje na porudžbinu. Kontaktiraj nas putem Instagrama ili forme za porudžbinu.</p>
          <a href="/kontakt/?model={slug}" class="btn btn-gold btn-full" style="margin-bottom:0.8rem">Poruči {name} →</a>
          <a href="https://www.instagram.com/quincecrochets/" target="_blank" rel="noopener noreferrer" class="btn btn-full" style="background:rgba(255,255,255,0.15);color:#fff;border:1px solid rgba(255,255,255,0.3)">DM na Instagram @quincecrochets</a>
          <p class="product-cta-box-note" style="margin-top:0.8rem">Dostava kurirskom službom na celoj teritoriji Srbije.</p>
        </div>
      </div>

    </div>

    <!-- Related -->
    <div class="related-section" aria-labelledby="related-heading">
      <div class="section-header">
        <span class="eyebrow">✦ Pogledaj i ✦</span>
        <h2 id="related-heading">Slični modeli</h2>
        <div class="divider"></div>
      </div>
      <div class="related-grid">
        {related_html}
      </div>
    </div>

  </div>
</main>
{FOOTER}
<script src="/js/main.js" defer></script>
</body>
</html>'''
    return html


def write_page(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path.replace(BASE, '')}")


if __name__ == "__main__":
    print("Generating product pages...")
    for m in MODELS:
        path = os.path.join(BASE, "kolekcija", m["slug"], "index.html")
        write_page(path, product_page(m))
    print(f"\nDone! Generated {len(MODELS)} product pages.")
