#!/usr/bin/env python3
"""Generate 50 static preview sites for TMBC Works leads."""
import csv
import html
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "leads.csv")
BASE_URL = "https://themarkkbradoncollective.github.io/TMBC-Works"

# Manual slug overrides where auto-slug is awkward
SLUG_OVERRIDES = {
    "5 STAR SMOG (Star Station)": "5-star-smog",
    "Fix Car's - Automotive Diagnostic & Repair Shop": "fix-cars-auto-repair",
    "J & T Auto Repair": "j-t-auto-repair",
    "K.S Complete Shoe Repair": "ks-complete-shoe-repair",
    "I love my shoe shine": "i-love-my-shoe-shine",
    "Chita's Taquería": "chitas-taqueria",
    "Larson Industrial Services, Inc.": "larson-industrial-services",
    "59th Street Barbershop": "59th-street-barbershop",
    "16th Street Donuts": "16th-street-donuts",
    "Nor Cali Fences And Concrete": "nor-cali-fences-and-concrete",
    "Aluminum and Stainless Weldmasters": "weldmasters",
    "Sacramento Radiator Sales and Service": "sacramento-radiator",
    "Trophy Center & Port Engraving": "trophy-center-port-engraving",
    "Prime Service Co. Appliance Repair": "prime-service-appliance-repair",
    "E Z Tires": "e-z-tires",
    "Pass and Go Smog": "pass-and-go-smog",
    "Aarin's Barbershop": "aarins-barbershop",
    "Aarin\u2019s Barbershop": "aarins-barbershop",
    "Jack's Donuts Wheel": "jacks-donuts-wheel",
    "CK's Donuts": "cks-donuts",
    "Marie's Donuts": "maries-donuts",
    "Mike's Mower Shop": "mikes-mower-shop",
    "Schroeder's Shoe Repair": "schroeders-shoe-repair",
    "Norm's Barber Shop": "norms-barber-shop",
    "Antonio's Barber Shop": "antonios-barber-shop",
    "Jay's Mobile Welding & Fabricating": "jays-mobile-welding",
    "Moore's Martial Arts of Sacramento": "moores-martial-arts",
    "John's Towing": "johns-towing",
    "Pino's Auto Repair": "pinos-auto-repair",
    "El Novillero Restaurant": "el-novillero",
}

THEMES = [
    {"id": "midnight-gold", "bg": "#0f1419", "surface": "#1a2332", "accent": "#c9a227", "text": "#f4f1ea", "muted": "#a8b0bc", "hero_grad": "linear-gradient(135deg,#0f1419 0%,#2a3544 50%,#1a2332 100%)", "radius": "4px", "font_h": "Georgia,serif", "font_b": "system-ui,sans-serif", "layout": "classic"},
    {"id": "coral-cream", "bg": "#fff8f3", "surface": "#ffffff", "accent": "#e85d4c", "text": "#2d2a26", "muted": "#6b6560", "hero_grad": "linear-gradient(120deg,#ffe8dc,#fff8f3 60%,#ffd4c4)", "radius": "16px", "font_h": "'Trebuchet MS',sans-serif", "font_b": "Verdana,sans-serif", "layout": "split"},
    {"id": "forest-sage", "bg": "#f2f5f0", "surface": "#ffffff", "accent": "#3d6b4f", "text": "#1e2b22", "muted": "#5a6b5e", "hero_grad": "linear-gradient(160deg,#dce8df,#f2f5f0)", "radius": "8px", "font_h": "Palatino,serif", "font_b": "Helvetica,Arial,sans-serif", "layout": "cards"},
    {"id": "electric-blue", "bg": "#0a1628", "surface": "#122038", "accent": "#3b9eff", "text": "#e8f0fa", "muted": "#8ba3c0", "hero_grad": "linear-gradient(180deg,#0a1628,#163054)", "radius": "0", "font_h": "Impact,'Arial Black',sans-serif", "font_b": "Tahoma,sans-serif", "layout": "bold"},
    {"id": "lavender-soft", "bg": "#faf7fc", "surface": "#ffffff", "accent": "#7c5cbf", "text": "#2a2438", "muted": "#6d6478", "hero_grad": "linear-gradient(145deg,#ede5f7,#faf7fc)", "radius": "24px", "font_h": "Optima,sans-serif", "font_b": "Calibri,sans-serif", "layout": "minimal"},
    {"id": "rust-brick", "bg": "#1c1210", "surface": "#2a1e1a", "accent": "#d4654a", "text": "#f5ebe6", "muted": "#b09a90", "hero_grad": "linear-gradient(135deg,#1c1210,#3d2820)", "radius": "6px", "font_h": "'Book Antiqua',serif", "font_b": "Arial,sans-serif", "layout": "classic"},
    {"id": "mint-charcoal", "bg": "#f0faf7", "surface": "#ffffff", "accent": "#0d9488", "text": "#134e4a", "muted": "#5f7a76", "hero_grad": "linear-gradient(90deg,#ccfbf1,#f0faf7)", "radius": "12px", "font_h": "Futura,'Century Gothic',sans-serif", "font_b": "system-ui,sans-serif", "layout": "split"},
    {"id": "sunset-warm", "bg": "#fff5eb", "surface": "#fffcf7", "accent": "#ea580c", "text": "#431407", "muted": "#9a3412", "hero_grad": "linear-gradient(180deg,#fed7aa,#fff5eb)", "radius": "20px", "font_h": "Georgia,serif", "font_b": "Segoe UI,sans-serif", "layout": "cards"},
    {"id": "slate-cyan", "bg": "#1e293b", "surface": "#334155", "accent": "#22d3ee", "text": "#f1f5f9", "muted": "#94a3b8", "hero_grad": "linear-gradient(135deg,#0f172a,#1e293b 70%,#334155)", "radius": "8px", "font_h": "Arial,sans-serif", "font_b": "Verdana,sans-serif", "layout": "bold"},
    {"id": "rose-blush", "bg": "#fdf2f4", "surface": "#ffffff", "accent": "#be185d", "text": "#4a1027", "muted": "#9d174d", "hero_grad": "linear-gradient(120deg,#fce7f3,#fdf2f4)", "radius": "14px", "font_h": "'Times New Roman',serif", "font_b": "Tahoma,sans-serif", "layout": "minimal"},
]

CATEGORY_COPY = {
    "Barbershop": {
        "tagline": "Neighborhood cuts in Sacramento",
        "services": ["Haircuts & trims", "Beard shaping", "Walk-ins welcome when available"],
        "hero_icon": "barber",
    },
    "Nail salon": {
        "tagline": "Nail care in Citrus Heights",
        "services": ["Manicures & pedicures", "Nail shaping & polish", "Relaxing salon visits"],
        "hero_icon": "spa",
    },
    "Donut shop": {
        "tagline": "Fresh donuts & morning treats",
        "services": ["Fresh-baked donuts", "Coffee & morning favorites", "Counter service"],
        "hero_icon": "donut",
    },
    "Bakery": {
        "tagline": "Baked goods made with care",
        "services": ["Fresh pastries", "Specialty baked goods", "Counter orders"],
        "hero_icon": "bakery",
    },
    "Mexican restaurant": {
        "tagline": "Mexican flavors in Sacramento",
        "services": ["Lunch & dinner service", "Classic Mexican dishes", "Dine-in & takeout"],
        "hero_icon": "food",
    },
    "Tire shop": {
        "tagline": "Tires & wheel service",
        "services": ["Tire sales & installation", "Balancing & rotation", "Local auto service"],
        "hero_icon": "auto",
    },
    "Auto/marine/furniture upholstery": {
        "tagline": "Upholstery for vehicles & furniture",
        "services": ["Auto upholstery", "Marine upholstery", "Furniture reupholstery"],
        "hero_icon": "fabric",
    },
    "Furniture upholstery": {
        "tagline": "Furniture upholstery & repair",
        "services": ["Reupholstery", "Fabric replacement", "Custom cushions"],
        "hero_icon": "fabric",
    },
    "Smog check": {
        "tagline": "Smog inspections in Sacramento",
        "services": ["Smog checks", "DMV-required testing", "Quick turnaround"],
        "hero_icon": "check",
    },
    "Smog check (STAR)": {
        "tagline": "STAR-certified smog station",
        "services": ["STAR smog tests", "DMV-required inspections", "Licensed testing"],
        "hero_icon": "check",
    },
    "Auto repair": {
        "tagline": "Local auto repair you can trust",
        "services": ["Diagnostics & repair", "Routine maintenance", "Honest service"],
        "hero_icon": "auto",
    },
    "Auto repair / diagnostics": {
        "tagline": "Diagnostics & automotive repair",
        "services": ["Computer diagnostics", "Engine & drivetrain repair", "Maintenance services"],
        "hero_icon": "auto",
    },
    "Auto repair & smog": {
        "tagline": "Repair & smog in one stop",
        "services": ["Auto repair", "Smog inspections", "Maintenance"],
        "hero_icon": "auto",
    },
    "Shoe repair": {
        "tagline": "Quality shoe repair",
        "services": ["Sole & heel repair", "Stitching & patching", "Leather care"],
        "hero_icon": "shoe",
    },
    "Shoe & leather repair": {
        "tagline": "Shoe & leather repair downtown",
        "services": ["Shoe repair", "Leather goods repair", "Quick turnaround"],
        "hero_icon": "shoe",
    },
    "Shoe shine": {
        "tagline": "Professional shoe shine",
        "services": ["Shoe shines", "Leather conditioning", "Walk-in service"],
        "hero_icon": "shoe",
    },
    "Alterations / tailor": {
        "tagline": "Alterations & tailoring",
        "services": ["Hemming & adjustments", "Repairs & resizing", "Custom fittings"],
        "hero_icon": "fabric",
    },
    "Lawn mower / small engine repair": {
        "tagline": "Small engine repair specialists",
        "services": ["Lawn mower repair", "Small engine service", "Seasonal tune-ups"],
        "hero_icon": "tool",
    },
    "Appliance repair": {
        "tagline": "Appliance repair service",
        "services": ["In-home appliance repair", "Diagnostics", "Major brand service"],
        "hero_icon": "tool",
    },
    "Radiator repair": {
        "tagline": "Radiator sales & service",
        "services": ["Radiator repair", "Cooling system service", "Parts & installation"],
        "hero_icon": "auto",
    },
    "Welding / fabrication": {
        "tagline": "Welding & metal fabrication",
        "services": ["Aluminum welding", "Stainless fabrication", "Custom metal work"],
        "hero_icon": "tool",
    },
    "Martial arts (kung fu)": {
        "tagline": "Kung fu training in Sacramento",
        "services": ["Group classes", "Traditional kung fu", "All ages welcome"],
        "hero_icon": "martial",
    },
    "Martial arts": {
        "tagline": "Martial arts for the whole family",
        "services": ["Kids & adult classes", "Self-discipline & fitness", "Structured programs"],
        "hero_icon": "martial",
    },
    "Trophies / engraving": {
        "tagline": "Awards, trophies & engraving",
        "services": ["Custom trophies", "Engraving services", "Corporate & team awards"],
        "hero_icon": "trophy",
    },
    "TV repair (in-home)": {
        "tagline": "In-home TV repair",
        "services": ["Television repair", "Mobile service calls", "Sacramento-area coverage"],
        "hero_icon": "tool",
    },
    "European auto repair": {
        "tagline": "European automotive specialists",
        "services": ["European make service", "Diagnostics & repair", "Maintenance programs"],
        "hero_icon": "auto",
    },
    "Import auto repair": {
        "tagline": "Import auto repair & service",
        "services": ["Import vehicle repair", "Scheduled maintenance", "Diagnostics"],
        "hero_icon": "auto",
    },
    "Mobile welding": {
        "tagline": "Mobile welding & fabrication",
        "services": ["On-site welding", "Fabrication projects", "Repair work"],
        "hero_icon": "tool",
    },
    "Plumbing": {
        "tagline": "Plumbing service in Sacramento",
        "services": ["Repairs & installations", "Leak diagnostics", "Residential plumbing"],
        "hero_icon": "tool",
    },
    "Upholstery & embroidery": {
        "tagline": "Upholstery & embroidery",
        "services": ["Custom upholstery", "Embroidery services", "Commercial & residential"],
        "hero_icon": "fabric",
    },
    "Dog grooming": {
        "tagline": "Dog grooming with care",
        "services": ["Baths & haircuts", "Nail trimming", "Breed-friendly styling"],
        "hero_icon": "pet",
    },
    "Industrial contractor / millwright": {
        "tagline": "Industrial contracting & millwright work",
        "services": ["Industrial installation", "Millwright services", "Commercial projects"],
        "hero_icon": "tool",
    },
    "Rug cleaning": {
        "tagline": "Professional rug cleaning",
        "services": ["Area rug cleaning", "Drop-off service", "Fiber-safe methods"],
        "hero_icon": "fabric",
    },
    "Thai restaurant": {
        "tagline": "Thai cuisine in Sacramento",
        "services": ["Curries & noodles", "Lunch & dinner", "Dine-in & takeout"],
        "hero_icon": "food",
    },
    "Towing": {
        "tagline": "Local towing service",
        "services": ["Emergency towing", "Roadside assistance", "Sacramento-area service"],
        "hero_icon": "auto",
    },
    "Fence & concrete contractor": {
        "tagline": "Fences & concrete work",
        "services": ["Fence installation", "Concrete flatwork", "Free estimates"],
        "hero_icon": "tool",
    },
}

# Verified one-liners from lead notes (only where explicitly documented)
VERIFIED_FACTS = {
    27: "Family-run Mexican restaurant serving Sacramento since 1970.",
    7: "Reopened in December 2025 under new ownership with a longtime baker at the helm.",
    36: "Serving Sacramento since 2006.",
    33: "More than 65 years serving the Sacramento area with awards and engraving.",
    18: "Veteran-owned smog check station.",
    6: "Known for late-night hours — a local favorite on Freeport Boulevard.",
    4: "Classic neighborhood barbershop on Folsom Boulevard.",
    22: "Convenient downtown location near Cesar Chavez Park.",
    34: "Mobile in-home TV repair serving the greater Sacramento area.",
}

UNSPLASH = {
    "barber": ("https://images.unsplash.com/photo-1585747860715-2b67a7a7f336?w=1200&q=80", "Photo: Unsplash"),
    "spa": ("https://images.unsplash.com/photo-1604654890710-f6390f18ddb0?w=1200&q=80", "Photo: Unsplash"),
    "donut": ("https://images.unsplash.com/photo-1551024601-bec78ae704b3?w=1200&q=80", "Photo: Unsplash"),
    "bakery": ("https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1200&q=80", "Photo: Unsplash"),
    "food": ("https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1200&q=80", "Photo: Unsplash"),
    "auto": ("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=1200&q=80", "Photo: Unsplash"),
    "fabric": ("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80", "Photo: Unsplash"),
    "check": ("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1200&q=80", "Photo: Unsplash"),
    "shoe": ("https://images.unsplash.com/photo-1549298916-b41d501d3772?w=1200&q=80", "Photo: Unsplash"),
    "tool": ("https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1200&q=80", "Photo: Unsplash"),
    "martial": ("https://images.unsplash.com/photo-1555597673-b21d5c935865?w=1200&q=80", "Photo: Unsplash"),
    "trophy": ("https://images.unsplash.com/photo-1517649763962-0c62306601b7?w=1200&q=80", "Photo: Unsplash"),
    "pet": ("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=1200&q=80", "Photo: Unsplash"),
}


def slugify(name: str) -> str:
    if name in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[name]
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-")


def phone_href(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"tel:+1{digits}"
    return f"tel:{digits}"


def map_embed_url(address: str) -> str:
    q = urllib.parse.quote(address)
    return f"https://maps.google.com/maps?q={q}&t=&z=15&ie=UTF8&iwloc=&output=embed"


def map_link_url(address: str) -> str:
    q = urllib.parse.quote(address)
    return f"https://www.google.com/maps/search/?api=1&query={q}"


def hero_svg(icon: str, accent: str) -> str:
    """Inline decorative SVG for hero when image is decorative overlay."""
    return f'<div class="hero-pattern" aria-hidden="true"></div>'


def build_page(row: dict, lead_num: int, theme: dict) -> str:
    name = row["business_name"]
    category = row["category"]
    address = row["address"]
    phone = row["phone"]
    email = (row.get("email") or "").strip()
    copy = CATEGORY_COPY.get(category, {
        "tagline": f"{category} in the Sacramento area",
        "services": ["Professional service", "Local business", "Contact us for details"],
        "hero_icon": "tool",
    })
    img_url, img_credit = UNSPLASH.get(copy["hero_icon"], UNSPLASH["tool"])
    verified = VERIFIED_FACTS.get(lead_num, "")
    tagline = verified if verified else copy["tagline"]
    services_html = "".join(f"<li>{html.escape(s)}</li>" for s in copy["services"])
    email_block = ""
    if email:
        email_block = f'<p><a href="mailto:{html.escape(email)}">{html.escape(email)}</a></p>'
    else:
        email_block = "<p>Call us for inquiries.</p>"

    layout = theme["layout"]
    hero_class = f"hero hero-{layout}"

    nav_links = """
      <a href="#services">Services</a>
      <a href="#visit">Visit</a>
      <a href="#contact">Contact</a>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{html.escape(name)} | {html.escape(category)}</title>
  <style>
    *,*::before,*::after{{box-sizing:border-box}}
    :root{{
      --bg:{theme["bg"]};
      --surface:{theme["surface"]};
      --accent:{theme["accent"]};
      --text:{theme["text"]};
      --muted:{theme["muted"]};
      --radius:{theme["radius"]};
      --font-h:{theme["font_h"]};
      --font-b:{theme["font_b"]};
    }}
    body{{
      margin:0;
      font-family:var(--font-b);
      background:var(--bg);
      color:var(--text);
      line-height:1.6;
    }}
    .tmbc-banner{{
      background:#111827;
      color:#e5e7eb;
      font-size:0.75rem;
      text-align:center;
      padding:0.45rem 1rem;
      border-bottom:1px solid #374151;
    }}
    .tmbc-banner a{{color:#93c5fd}}
    header.site-header{{
      display:flex;
      flex-wrap:wrap;
      align-items:center;
      justify-content:space-between;
      gap:1rem;
      padding:1rem 1.25rem;
      max-width:1100px;
      margin:0 auto;
    }}
    .logo{{
      font-family:var(--font-h);
      font-size:1.35rem;
      font-weight:700;
      letter-spacing:0.02em;
    }}
    nav a{{
      color:var(--muted);
      text-decoration:none;
      margin-left:1rem;
      font-size:0.95rem;
    }}
    nav a:hover{{color:var(--accent)}}
    .hero{{
      position:relative;
      overflow:hidden;
      max-width:1100px;
      margin:0 auto 2rem;
      border-radius:var(--radius);
    }}
    .hero-classic,.hero-minimal{{
      min-height:320px;
      background:{theme["hero_grad"]};
      padding:3rem 1.5rem;
      display:flex;
      flex-direction:column;
      justify-content:center;
    }}
    .hero-split{{
      display:grid;
      grid-template-columns:1fr;
      gap:0;
      background:var(--surface);
    }}
    @media(min-width:768px){{
      .hero-split{{grid-template-columns:1.1fr 0.9fr}}
    }}
    .hero-split .hero-copy{{padding:2.5rem 1.5rem}}
    .hero-split .hero-visual{{
      min-height:260px;
      background:url('{img_url}') center/cover no-repeat;
    }}
    .hero-cards,.hero-bold{{
      min-height:280px;
      padding:2.5rem 1.5rem;
      background:{theme["hero_grad"]};
    }}
    .hero-bold h1{{font-size:clamp(2rem,6vw,3.5rem);text-transform:uppercase}}
    .hero h1{{
      font-family:var(--font-h);
      font-size:clamp(1.75rem,5vw,2.75rem);
      margin:0 0 0.75rem;
      line-height:1.15;
    }}
    .hero p.lead{{
      font-size:1.1rem;
      color:var(--muted);
      max-width:36rem;
      margin:0 0 1.25rem;
    }}
    .btn-row{{display:flex;flex-wrap:wrap;gap:0.75rem}}
    .btn{{
      display:inline-block;
      padding:0.65rem 1.25rem;
      border-radius:var(--radius);
      text-decoration:none;
      font-weight:600;
      font-size:0.95rem;
    }}
    .btn-primary{{
      background:var(--accent);
      color:#fff;
    }}
    .btn-outline{{
      border:2px solid var(--accent);
      color:var(--accent);
    }}
    main{{max-width:1100px;margin:0 auto;padding:0 1.25rem 3rem}}
    section{{margin-bottom:2.5rem}}
    h2{{
      font-family:var(--font-h);
      font-size:1.5rem;
      margin:0 0 1rem;
      color:var(--text);
    }}
    .services-grid{{
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
      gap:1rem;
    }}
    .card{{
      background:var(--surface);
      padding:1.25rem;
      border-radius:var(--radius);
      border:1px solid color-mix(in srgb,var(--muted) 25%,transparent);
    }}
    .card ul{{margin:0;padding-left:1.1rem}}
    .visit-grid{{
      display:grid;
      grid-template-columns:1fr;
      gap:1.5rem;
    }}
    @media(min-width:768px){{
      .visit-grid{{grid-template-columns:1fr 1fr}}
    }}
    .map-wrap{{
      border-radius:var(--radius);
      overflow:hidden;
      min-height:220px;
      border:1px solid color-mix(in srgb,var(--muted) 30%,transparent);
    }}
    .map-wrap iframe{{width:100%;height:260px;border:0;display:block}}
    .contact-box{{
      background:var(--surface);
      padding:1.5rem;
      border-radius:var(--radius);
    }}
    .contact-box a{{color:var(--accent)}}
    footer{{
      text-align:center;
      padding:2rem 1rem;
      font-size:0.85rem;
      color:var(--muted);
      border-top:1px solid color-mix(in srgb,var(--muted) 25%,transparent);
    }}
    .category-pill{{
      display:inline-block;
      font-size:0.8rem;
      text-transform:uppercase;
      letter-spacing:0.08em;
      color:var(--accent);
      margin-bottom:0.5rem;
    }}
    .hero-visual-only{{
      min-height:200px;
      margin-top:1rem;
      border-radius:var(--radius);
      background:url('{img_url}') center/cover no-repeat;
      opacity:0.92;
    }}
    .img-credit{{
      font-size:0.65rem;
      color:var(--muted);
      margin-top:0.35rem;
    }}
  </style>
</head>
<body>
  <div class="tmbc-banner">
    Website preview designed by TMBC Works ·
    <a href="mailto:hello@tmbcworks.com">hello@tmbcworks.com</a> · Sacramento, CA
  </div>
  <header class="site-header">
    <div class="logo">{html.escape(name)}</div>
    <nav aria-label="Primary">{nav_links}</nav>
  </header>

  <section class="{hero_class}" aria-label="Introduction">
    {"<div class='hero-copy'>" if layout == "split" else ""}
    <span class="category-pill">{html.escape(category)}</span>
    <h1>{html.escape(name)}</h1>
    <p class="lead">{html.escape(tagline)}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{phone_href(phone)}">Call {html.escape(phone)}</a>
      <a class="btn btn-outline" href="{html.escape(map_link_url(address))}">Get directions</a>
    </div>
    {"</div><div class='hero-visual' role='img' aria-label='Decorative stock photo'></div>" if layout == "split" else f"<div class='hero-visual-only' role='img' aria-label='Decorative stock photo'></div><p class='img-credit'>{html.escape(img_credit)}</p>"}
  </section>

  <main>
    <section id="services">
      <h2>What we offer</h2>
      <div class="services-grid">
        <div class="card">
          <ul>{services_html}</ul>
        </div>
        <div class="card">
          <p style="margin:0;color:var(--muted)">We focus on friendly, reliable service for our neighbors. Reach out by phone{"" if not email else " or email"} to learn more about availability.</p>
        </div>
      </div>
    </section>

    <section id="visit">
      <h2>Location</h2>
      <div class="visit-grid">
        <div>
          <p><strong>Address</strong><br>{html.escape(address)}</p>
          <p><a href="{html.escape(map_link_url(address))}">Open in Google Maps</a></p>
        </div>
        <div class="map-wrap">
          <iframe title="Map to {html.escape(name)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="{html.escape(map_embed_url(address))}"></iframe>
        </div>
      </div>
    </section>

    <section id="contact">
      <h2>Contact</h2>
      <div class="contact-box">
        <p><strong>Phone:</strong> <a href="{phone_href(phone)}">{html.escape(phone)}</a></p>
        {email_block}
      </div>
    </section>
  </main>

  <footer>
    <p>{html.escape(name)} · {html.escape(category)} · Sacramento area</p>
    <p>Preview site — hours &amp; details may vary; confirm with the business directly.</p>
  </footer>
</body>
</html>
"""


def main():
    # Copy CSV to repo root if using uploads path
    upload_csv = "/home/ubuntu/.cursor/projects/workspace/uploads/leads_c721.csv"
    if not os.path.exists(CSV_PATH) and os.path.exists(upload_csv):
        import shutil
        shutil.copy(upload_csv, CSV_PATH)

    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    previews = []
    for i, row in enumerate(rows):
        lead_num = int(row["#"])
        slug = slugify(row["business_name"])
        theme = THEMES[i % len(THEMES)]
        theme = {**theme, "layout": THEMES[(i + lead_num) % len(THEMES)]["layout"]}
        out_dir = os.path.join(ROOT, slug)
        os.makedirs(out_dir, exist_ok=True)
        page = build_page(row, lead_num, theme)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        previews.append({
            "lead_number": lead_num,
            "business_name": row["business_name"],
            "slug": slug,
            "preview_url": f"{BASE_URL}/{slug}/",
            "email": row.get("email") or "",
            "phone": row["phone"],
        })

    # previews.csv
    with open(os.path.join(ROOT, "previews.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["lead_number", "business_name", "slug", "preview_url", "email", "phone"])
        w.writeheader()
        for p in previews:
            w.writerow(p)

    # Root index.html
    links = "\n".join(
        f'        <li><a href="{html.escape(p["slug"])}/"><span class="num">{p["lead_number"]:02d}</span> '
        f'{html.escape(p["business_name"])} <span class="cat">{html.escape(rows[i]["category"])}</span></a></li>'
        for i, p in enumerate(previews)
    )
    root_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>TMBC Works — Preview Index (Private)</title>
  <style>
    body {{
      font-family: system-ui, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      margin: 0;
      padding: 2rem 1rem;
      line-height: 1.5;
    }}
    .wrap {{ max-width: 720px; margin: 0 auto; }}
    h1 {{ font-size: 1.5rem; margin: 0 0 0.5rem; }}
    p.sub {{ color: #94a3b8; margin: 0 0 1.5rem; font-size: 0.95rem; }}
    ul {{ list-style: none; padding: 0; margin: 0; }}
    li {{ margin: 0 0 0.35rem; }}
    a {{
      display: block;
      padding: 0.65rem 0.85rem;
      background: #1e293b;
      border-radius: 8px;
      color: #f8fafc;
      text-decoration: none;
      border: 1px solid #334155;
    }}
    a:hover {{ border-color: #64748b; background: #273449; }}
    .num {{ color: #38bdf8; font-weight: 600; margin-right: 0.5rem; }}
    .cat {{ float: right; font-size: 0.8rem; color: #94a3b8; }}
    @media(max-width:540px){{ .cat {{ float: none; display: block; margin-top: 0.25rem; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>TMBC Works — Client preview sites</h1>
    <p class="sub">Private index for pitch previews. Not indexed by search engines.</p>
    <ul>
{links}
    </ul>
  </div>
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_html)

    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print(f"Generated {len(previews)} previews")
    print(json.dumps(previews[:3], indent=2))


if __name__ == "__main__":
    main()
