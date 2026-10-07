"""Render bespoke preview HTML for one lead."""
from __future__ import annotations

import html
import json
import os
import urllib.parse

from tmbc_constants import TMBC_FEEDBACK_EMAIL

from lib.geo_util import get_coords, maps_link, osm_embed, osm_static_map


def phone_href(phone: str) -> str:
    import re

    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"tel:+1{digits}"
    return f"tel:{digits}"


def feedback_mailto(business_name: str, has_website: bool) -> str:
    q1 = (
        "What would you change about your current website?"
        if has_website
        else "What would you want a website to do for your business?"
    )
    q2 = "What would you change about this redesigned version?"
    body = (
        f"Business: {business_name}\n\n"
        f"{q1}\n\n[Your answer here]\n\n"
        f"{q2}\n\n[Your answer here]\n\n"
        f"— Sent via TMBC Works preview feedback"
    )
    subject = f"Website feedback: {business_name}"
    return (
        f"mailto:{TMBC_FEEDBACK_EMAIL}?"
        f"subject={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )


def favicon_svg(initial: str, accent: str) -> str:
    ch = html.escape(initial[:1].upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="8" fill="{html.escape(accent)}"/>
  <text x="16" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" font-weight="700" fill="#fff">{ch}</text>
</svg>'''


def section_hours(profile: dict) -> str:
    hours = profile.get("hours") or []
    hours_note = (profile.get("hours_note") or "").strip()
    if not hours and not hours_note:
        return ""
    items = "".join(f"<li>{html.escape(h)}</li>" for h in hours)
    note = hours_note
    if note and not note.startswith("<"):
        note = f"<p>{html.escape(note)}</p>"
    return f"""
    <section class="hours-block reveal" id="hours">
      <div class="wrap">
        <h2>Hours</h2>
        {f'<ul class="hours-list">{items}</ul>' if items else ''}
        {note}
      </div>
    </section>"""


def section_menu(profile: dict) -> str:
    cats = profile.get("menu_categories") or []
    if not cats:
        return ""
    cards = ""
    for c in cats:
        title = html.escape(c["title"])
        items = "".join(f"<li>{html.escape(i)}</li>" for i in c.get("items", []))
        cards += f'<article class="menu-card reveal"><h3>{title}</h3><ul>{items}</ul></article>'
    return f"""
    <section class="menu-block reveal" id="menu">
      <div class="wrap">
        <h2>{html.escape(profile.get("menu_heading", "Highlights"))}</h2>
        <p class="menu-note">{html.escape(profile.get("menu_note", ""))}</p>
        <div class="menu-grid">{cards}</div>
      </div>
    </section>"""


def section_services(profile: dict) -> str:
    items = profile.get("services") or []
    if not items:
        return ""
    lis = "".join(f"<li>{html.escape(s)}</li>" for s in items)
    return f"""
    <section class="services-block reveal" id="services">
      <div class="wrap">
        <h2>{html.escape(profile.get("services_heading", "Services"))}</h2>
        <ul class="svc-list">{lis}</ul>
      </div>
    </section>"""


def section_story(profile: dict) -> str:
    paras = profile.get("paragraphs") or []
    if not paras:
        return ""
    ps = "".join(f"<p>{html.escape(p)}</p>" for p in paras)
    return f"""
    <section class="story-block reveal" id="story">
      <div class="wrap story-grid">
        <div class="story-copy">{ps}</div>
        <div class="story-aside">{profile.get("aside_html", "")}</div>
      </div>
    </section>"""


def section_location(name: str, address: str, lat: float, lon: float) -> str:
    mlink = html.escape(maps_link(address))
    embed = html.escape(osm_embed(lat, lon))
    static = html.escape(osm_static_map(lat, lon))
    return f"""
    <section class="location-block reveal" id="visit">
      <div class="wrap loc-grid">
        <div>
          <h2>Find us</h2>
          <p class="addr">{html.escape(address)}</p>
          <p><a class="text-link" href="{mlink}">Open in Google Maps</a></p>
        </div>
        <div class="map-frame">
          <iframe title="Map to {html.escape(name)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{embed}"></iframe>
          <noscript><img src="{static}" alt="Map location" width="800" height="360" loading="lazy"></noscript>
        </div>
      </div>
    </section>"""


def section_contact(row: dict) -> str:
    phone = row["phone"]
    email = (row.get("email") or "").strip()
    email_line = (
        f'<p>Email: <a href="mailto:{html.escape(email)}">{html.escape(email)}</a></p>'
        if email
        else "<p>Email: call for the best contact address.</p>"
    )
    return f"""
    <section class="contact-block reveal" id="contact">
      <div class="wrap contact-inner">
        <h2>Contact</h2>
        <p class="phone-big"><a href="{phone_href(phone)}">{html.escape(phone)}</a></p>
        {email_line}
      </div>
    </section>"""


def layout_css(profile: dict) -> str:
    c = profile["colors"]
    lid = profile["layout"]
    extra = profile.get("layout_css", "")
    hero_grad = profile.get("hero_grad", "to top, var(--hero-overlay), transparent 55%")
    return f"""
    :root {{
      --bg: {c['bg']};
      --surface: {c['surface']};
      --text: {c['text']};
      --muted: {c['muted']};
      --accent: {c['accent']};
      --accent2: {c.get('accent2', c['accent'])};
      --hero-overlay: {c.get('hero_overlay', 'rgba(0,0,0,.45)')};
      --radius: {c.get('radius', '12px')};
    }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:{profile['font_body']}, system-ui, sans-serif; line-height:1.65; }}
    h1,h2,h3 {{ font-family:{profile['font_head']}, Georgia, serif; line-height:1.15; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 1.25rem; }}
    a {{ color: var(--accent); }}
    .site-header {{
      display:flex; align-items:center; justify-content:space-between; gap:1rem;
      padding:1rem 1.25rem; max-width:1100px; margin:0 auto;
    }}
    .logo {{ font-family:{profile['font_head']}, serif; font-weight:700; font-size:1.15rem; letter-spacing:.02em; }}
    .site-nav a {{ color:var(--muted); text-decoration:none; margin-left:1rem; font-size:.9rem; }}
    .site-nav a:hover {{ color:var(--accent); }}
    .hero {{ position:relative; min-height:{profile.get('hero_min', '72vh')}; display:flex; align-items:flex-end; overflow:hidden; }}
    .hero-bg {{ position:absolute; inset:0; background:url('{profile['hero_image']}') center/cover no-repeat; transform:scale(1.02); }}
    .hero-bg::after {{ content:''; position:absolute; inset:0; background:linear-gradient({hero_grad}); }}
    .hero-inner {{ position:relative; z-index:1; padding:3rem 1.25rem 2.5rem; max-width:1100px; margin:0 auto; width:100%; }}
    .hero-kicker {{ text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; color:var(--accent2); font-weight:700; }}
    .hero h1 {{ font-size:clamp(2rem,6vw,3.4rem); margin:.35rem 0 .75rem; max-width:14ch; }}
    .hero-lead {{ font-size:1.12rem; max-width:40rem; color:var(--muted); margin:0 0 1.25rem; }}
    .btn-row {{ display:flex; flex-wrap:wrap; gap:.75rem; }}
    .btn {{ display:inline-block; padding:.7rem 1.2rem; border-radius:var(--radius); font-weight:700; text-decoration:none; font-size:.92rem; transition: transform .2s ease, box-shadow .2s ease; }}
    .btn:hover {{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,.15); }}
    .btn-primary {{ background:var(--accent); color:#fff !important; }}
    .btn-ghost {{ border:2px solid var(--accent); color:var(--accent) !important; background:transparent; }}
    .highlights {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:1rem; margin-top:1.5rem; }}
    .hl {{ background:rgba(255,255,255,.08); backdrop-filter:blur(6px); border:1px solid rgba(255,255,255,.12); padding:.85rem; border-radius:var(--radius); font-size:.85rem; }}
    .layout-split .hero {{ display:grid; grid-template-columns:1fr; min-height:auto; }}
    @media(min-width:900px) {{
      .layout-split .hero {{ grid-template-columns:1.05fr .95fr; align-items:stretch; min-height:70vh; }}
      .layout-split .hero-bg {{ position:relative; min-height:360px; }}
      .layout-split .hero-inner {{ display:flex; flex-direction:column; justify-content:center; background:var(--surface); color:var(--text); }}
      .layout-split .hero-bg::after {{ background:linear-gradient(90deg, var(--surface) 0%, transparent 40%), var(--hero-overlay); }}
    }}
    .layout-editorial .hero h1 {{ max-width:none; font-size:clamp(2.4rem,7vw,4rem); }}
    .layout-editorial .hero-inner {{ padding-top:4rem; }}
    .layout-cardhero .hero {{ min-height:auto; padding:2rem 0 0; align-items:stretch; }}
    .layout-cardhero .hero-card {{ margin:0 1.25rem; border-radius:calc(var(--radius) * 1.5); overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,.18); }}
    .story-grid {{ display:grid; gap:2rem; padding:3rem 0; }}
    @media(min-width:768px) {{ .story-grid {{ grid-template-columns:1.2fr .8fr; }} }}
    .story-aside {{ background:var(--surface); padding:1.25rem; border-radius:var(--radius); border:1px solid color-mix(in srgb, var(--muted) 25%, transparent); font-size:.92rem; }}
    .services-block, .menu-block, .hours-block, .location-block, .contact-block {{ padding:2.75rem 0; }}
    .services-block {{ background:var(--surface); }}
    .svc-list {{ columns:2; gap:2rem; padding-left:1.1rem; margin:0; }}
    @media(max-width:640px) {{ .svc-list {{ columns:1; }} }}
    .menu-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; }}
    .menu-card {{ background:var(--surface); padding:1.1rem 1.25rem; border-radius:var(--radius); border:1px solid color-mix(in srgb, var(--muted) 22%, transparent); }}
    .menu-note {{ color:var(--muted); font-size:.9rem; max-width:40rem; }}
    .hours-list {{ list-style:none; padding:0; margin:0; display:grid; gap:.35rem; }}
    .hours-list li {{ padding:.55rem .75rem; background:var(--surface); border-radius:8px; border:1px solid color-mix(in srgb, var(--muted) 20%, transparent); }}
    .loc-grid {{ display:grid; gap:1.25rem; }}
    @media(min-width:768px) {{ .loc-grid {{ grid-template-columns: .9fr 1.1fr; align-items:start; }} }}
    .map-frame {{ border-radius:var(--radius); overflow:hidden; border:1px solid color-mix(in srgb, var(--muted) 25%, transparent); min-height:260px; background:#e2e8f0; }}
    .map-frame iframe {{ width:100%; height:280px; border:0; display:block; }}
    .contact-inner {{ text-align:center; background:var(--surface); padding:2rem; border-radius:var(--radius); }}
    .phone-big {{ font-size:1.6rem; font-weight:800; margin:.5rem 0; }}
    .phone-big a {{ text-decoration:none; color:var(--text); }}
    .biz-footer {{ text-align:center; padding:2rem 1rem 3rem; color:var(--muted); font-size:.85rem; border-top:1px solid color-mix(in srgb, var(--muted) 20%, transparent); }}
    .img-credit {{ font-size:.65rem; color:var(--muted); margin-top:.5rem; }}
    {extra}
    /* layout: {lid} */
    """


def render_index(row: dict, profile: dict, slug: str, base_url: str) -> str:
    name = row["business_name"]
    address = row["address"]
    phone = row["phone"]
    has_web = (row.get("website_status") or "") == "outdated"
    lat, lon = get_coords(name, address)
    map_url = maps_link(address)
    ph = phone_href(phone)
    nav = profile.get(
        "nav",
        '<a href="#story">About</a><a href="#services">Services</a><a href="#visit">Visit</a><a href="#contact">Contact</a>',
    )
    highlights = profile.get("highlights") or []
    hl_html = "".join(f'<div class="hl">{html.escape(h)}</div>' for h in highlights)
    hero_class = f"hero layout-{profile['layout']}"
    compare_link = ""
    if has_web:
        compare_link = f'<p class="compare-link"><a href="compare.html">See before &amp; after →</a></p>'

    sections_order = profile.get(
        "sections",
        ["story", "services", "menu", "hours", "location", "contact"],
    )
    sec_html = ""
    for s in sections_order:
        if s == "story":
            sec_html += section_story(profile)
        elif s == "services":
            sec_html += section_services(profile)
        elif s == "menu":
            sec_html += section_menu(profile)
        elif s == "hours":
            sec_html += section_hours(profile)
        elif s == "location":
            sec_html += section_location(name, address, lat, lon)
        elif s == "contact":
            sec_html += section_contact(row)

    og_img = profile["hero_image"]
    page_url = f"{base_url}/{slug}/"
    desc = html.escape(profile.get("meta_description") or profile.get("subhead") or row["category"])
    fav = favicon_svg(profile.get("favicon_initial", name[:1]), profile["colors"]["accent"])
    feedback_q = (
        "What would you change about your current website?"
        if has_web
        else "What would you want a website to do for your business?"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{html.escape(name)} — {html.escape(row['category'])}</title>
  <meta name="description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(name)}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{html.escape(page_url)}">
  <meta property="og:image" content="{html.escape(og_img)}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?{profile['fonts_query']}&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../_shared/tmbc.css">
  <style>{layout_css(profile)}</style>
  <!-- Hero image: {html.escape(profile.get('hero_credit', 'Unsplash'))} -->
</head>
<body data-biz-phone="{ph}" data-biz-map="{html.escape(map_url)}">
  <div class="tmbc-banner">Website preview designed by TMBC Works</div>
  <header class="site-header">
    <div class="logo">{html.escape(name)}</div>
    <nav class="site-nav" aria-label="Primary">{nav}</nav>
  </header>
  <section class="{hero_class}" aria-label="Welcome">
    <div class="hero-bg" role="img" aria-label="Decorative photograph"></div>
    <div class="hero-inner">
      <p class="hero-kicker">{html.escape(row['category'])}</p>
      <h1>{html.escape(profile.get('headline', name))}</h1>
      <p class="hero-lead">{html.escape(profile.get('subhead', ''))}</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="{ph}">Call {html.escape(phone)}</a>
        <a class="btn btn-ghost" href="{html.escape(map_url)}">Directions</a>
      </div>
      {f'<div class="highlights">{hl_html}</div>' if hl_html else ''}
      {compare_link}
    </div>
  </section>
  {sec_html}
  <div class="wrap">
    <aside class="tmbc-feedback reveal" aria-label="Preview feedback for TMBC Works">
      <h2>Help TMBC Works refine this preview</h2>
      <p>This section is for the business owner — not part of the live site design.</p>
      <span class="tmbc-q">{html.escape(feedback_q)}</span>
      <span class="tmbc-q">What would you change about this redesigned version?</span>
      <a class="tmbc-mail" href="{html.escape(feedback_mailto(name, has_web), quote=True)}">Send feedback</a>
    </aside>
  </div>
  <footer class="biz-footer">
    <p>{html.escape(name)} · {html.escape(address)}</p>
    <p class="img-credit">Stock photography via Unsplash (see HTML comment). Hours and offerings may change — please confirm with the business.</p>
  </footer>
  <div class="tmbc-sticky-bar" aria-label="Quick actions">
    <a class="tmbc-sticky-call" href="{ph}">Call</a>
    <a class="tmbc-sticky-map" href="{html.escape(map_url)}">Directions</a>
  </div>
  <script src="../_shared/tmbc-config.js" defer></script>
  <script src="../_shared/tmbc.js" defer></script>
</body>
</html>
"""


def render_compare(row: dict, profile: dict, slug: str, base_url: str, upgrades: list[str]) -> str:
    name = row["business_name"]
    has_img = os.path.isfile(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), slug, "assets", "legacy-site.png")
    )
    old_block = (
        '<img src="assets/legacy-site.png" alt="Previous website screenshot" width="900" loading="lazy">'
        if has_img
        else '<p class="missing">Previous site could not be captured (down, blocked, or unrelated URL). See lead notes.</p>'
    )
    ups = "".join(f"<li>{html.escape(u)}</li>" for u in upgrades)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{html.escape(name)} — Before &amp; After | TMBC Preview</title>
  <link rel="stylesheet" href="../_shared/tmbc.css">
  <style>
    body {{ font-family: system-ui, sans-serif; margin:0; background:#0f172a; color:#e2e8f0; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:2rem 1.25rem 3rem; }}
    h1 {{ font-size:1.6rem; }}
    .grid {{ display:grid; gap:1.5rem; }}
    @media(min-width:900px) {{ .grid {{ grid-template-columns:1fr 1fr; }} }}
    .panel {{ background:#1e293b; border-radius:12px; padding:1rem; border:1px solid #334155; }}
    .panel h2 {{ font-size:1rem; margin-top:0; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; }}
    .panel img {{ width:100%; border-radius:8px; border:1px solid #475569; }}
    .upgrades {{ background:#111827; padding:1.25rem; border-radius:12px; margin-top:1.5rem; }}
    .upgrades ul {{ margin:0; padding-left:1.2rem; }}
    a {{ color:#93c5fd; }}
  </style>
</head>
<body>
  <div class="tmbc-banner">Website preview designed by TMBC Works</div>
  <div class="wrap">
    <h1>{html.escape(name)}</h1>
    <p><a href="index.html">← Back to redesigned preview</a></p>
    <div class="grid">
      <div class="panel">
        <h2>Current / previous web presence</h2>
        {old_block}
      </div>
      <div class="panel">
        <h2>Proposed redesign</h2>
        <p>Mobile-first layout, clear calls to action, modern typography, and trustworthy contact paths.</p>
        <p><a href="index.html">Open full preview →</a></p>
        <iframe src="index.html" title="Preview" style="width:100%;height:420px;border:1px solid #475569;border-radius:8px;background:#fff"></iframe>
      </div>
    </div>
    <div class="upgrades">
      <h2>Concrete upgrades in this concept</h2>
      <ul>{ups}</ul>
    </div>
  </div>
</body>
</html>
"""
