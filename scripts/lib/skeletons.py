"""Category-specific page skeletons (structure, not just palette)."""
from __future__ import annotations

import html


def _sections():
    from lib import render_site as rs

    return rs


def skeleton_css(skeleton: str) -> str:
    if skeleton == "menu_forward":
        return """
    body.skel-menu_forward .hero { min-height: 52vh; align-items: center; text-align: center; }
    body.skel-menu_forward .hero-inner { max-width: 720px; margin: 0 auto; }
    body.skel-menu_forward .hero h1 { max-width: none; }
    body.skel-menu_forward .menu-block { background: var(--surface); padding: 3.5rem 0; margin-top: -2rem; position: relative; z-index: 2; border-radius: calc(var(--radius) * 2) calc(var(--radius) * 2) 0 0; box-shadow: 0 -20px 50px rgba(0,0,0,.08); }
    body.skel-menu_forward .menu-grid { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; }
    body.skel-menu_forward .menu-card { padding: 1.35rem 1.5rem; border-left: 4px solid var(--accent); box-shadow: 0 8px 24px rgba(0,0,0,.06); }
    body.skel-menu_forward .menu-card h3 { font-size: 1.15rem; margin-top: 0; }
    body.skel-menu_forward .hours-block { background: color-mix(in srgb, var(--accent) 12%, var(--bg)); padding: 2rem 0; }
    body.skel-menu_forward .hours-list { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
    body.skel-menu_forward .story-block { padding-top: 2rem; }
    """
    if skeleton == "service_emergency":
        return """
    body.skel-service_emergency .hero { min-height: 58vh; background: var(--surface); align-items: stretch; }
    body.skel-service_emergency .hero-bg { opacity: .35; }
    body.skel-service_emergency .hero-inner { display: grid; gap: 1.5rem; align-items: center; }
    @media(min-width:768px) { body.skel-service_emergency .hero-inner { grid-template-columns: 1fr auto; text-align: left; } }
    body.skel-service_emergency .emergency-cta { background: var(--accent); color: #fff; padding: 1.5rem 2rem; border-radius: var(--radius); text-align: center; box-shadow: 0 12px 40px color-mix(in srgb, var(--accent) 45%, transparent); }
    body.skel-service_emergency .emergency-cta a { color: #fff !important; font-size: 1.75rem; font-weight: 800; text-decoration: none; display: block; }
    body.skel-service_emergency .emergency-cta span { display: block; font-size: .85rem; opacity: .9; margin-top: .35rem; font-weight: 500; }
    body.skel-service_emergency .trust-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: .75rem; margin: 2rem 0 0; }
    body.skel-service_emergency .trust-strip div { background: var(--surface); padding: .75rem; border-radius: 8px; font-size: .82rem; text-align: center; border: 1px solid color-mix(in srgb, var(--muted) 25%, transparent); }
    body.skel-service_emergency .services-block { background: #0f172a; color: #f8fafc; }
    body.skel-service_emergency .services-block h2 { color: #f8fafc; }
    body.skel-service_emergency .svc-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; list-style: none; padding: 0; margin: 0; }
    body.skel-service_emergency .svc-cards li { background: #1e293b; padding: 1rem 1.1rem; border-radius: 10px; border-left: 3px solid var(--accent2); }
    """
    if skeleton == "studio_booking":
        return """
    body.skel-studio_booking .hero { min-height: 48vh; }
    body.skel-studio_booking .gallery-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; max-width: 1100px; margin: -2.5rem auto 0; padding: 0 1.25rem; position: relative; z-index: 3; }
    body.skel-studio_booking .gallery-row div { aspect-ratio: 4/5; border-radius: var(--radius); background: linear-gradient(145deg, color-mix(in srgb, var(--accent) 30%, #111), var(--surface)); border: 1px solid color-mix(in srgb, var(--muted) 30%, transparent); display: flex; align-items: flex-end; padding: .75rem; font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
    @media(max-width:640px) { body.skel-studio_booking .gallery-row { grid-template-columns: 1fr; } body.skel-studio_booking .gallery-row div { aspect-ratio: 16/9; } }
    body.skel-studio_booking .booking-panel { background: var(--surface); margin: 2rem 1.25rem; max-width: 1060px; margin-left: auto; margin-right: auto; padding: 2rem; border-radius: calc(var(--radius) * 1.5); display: grid; gap: 1rem; text-align: center; box-shadow: 0 16px 48px rgba(0,0,0,.1); }
    @media(min-width:768px) { body.skel-studio_booking .booking-panel { grid-template-columns: 1fr auto auto; align-items: center; text-align: left; } }
    body.skel-studio_booking .chip-row { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; }
    body.skel-studio_booking .chip { padding: .45rem .85rem; border-radius: 999px; background: color-mix(in srgb, var(--accent) 15%, transparent); font-size: .82rem; font-weight: 600; }
    body.skel-studio_booking .services-block { padding-top: 1rem; }
    body.skel-studio_booking .svc-list { columns: 1; display: flex; flex-wrap: wrap; gap: .5rem; list-style: none; padding: 0; }
    body.skel-studio_booking .svc-list li { background: var(--surface); padding: .5rem .9rem; border-radius: 999px; border: 1px solid color-mix(in srgb, var(--muted) 25%, transparent); }
    """
    if skeleton == "service_trust":
        return """
    body.skel-service_trust .hero { min-height: 62vh; }
    body.skel-service_trust .trust-bar { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; max-width: 1100px; margin: -2rem auto 0; padding: 0 1.25rem; position: relative; z-index: 2; }
    body.skel-service_trust .trust-bar article { background: var(--surface); padding: 1.1rem; border-radius: var(--radius); box-shadow: 0 10px 30px rgba(0,0,0,.08); border-top: 3px solid var(--accent); font-size: .88rem; }
    body.skel-service_trust .trust-bar strong { display: block; font-size: 1rem; margin-bottom: .25rem; }
    body.skel-service_trust .services-block { background: linear-gradient(180deg, var(--bg), var(--surface)); }
    body.skel-service_trust .svc-list { columns: 1; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: .65rem; list-style: none; padding: 0; }
    body.skel-service_trust .svc-list li { background: var(--surface); padding: .85rem 1rem; border-radius: 8px; border: 1px solid color-mix(in srgb, var(--muted) 20%, transparent); }
    body.skel-service_trust .svc-list li::before { content: "✓ "; color: var(--accent); font-weight: 700; }
    """
    if skeleton == "craft_workshop":
        return """
    body.skel-craft_workshop .hero { min-height: 50vh; }
    body.skel-craft_workshop .process-split { display: grid; gap: 2rem; padding: 3rem 0; }
    @media(min-width:768px) { body.skel-craft_workshop .process-split { grid-template-columns: 1fr 1fr; align-items: start; } }
    body.skel-craft_workshop .process-step { background: var(--surface); padding: 1.25rem; border-radius: var(--radius); margin-bottom: .75rem; border-left: 4px solid var(--accent2); }
    body.skel-craft_workshop .services-block { background: var(--surface); }
    """
    return ""


def section_emergency_cta(phone: str, label: str) -> str:
    ph = _sections().phone_href(phone)
    return f"""
    <div class="emergency-cta reveal">
      <a href="{ph}">{html.escape(phone)}</a>
      <span>{html.escape(label)}</span>
    </div>"""


def section_trust_bar(highlights: list[str]) -> str:
    if not highlights:
        return ""
    cards = "".join(
        f"<article class='reveal'><strong>{html.escape(h)}</strong></article>" for h in highlights[:4]
    )
    return f'<div class="trust-bar reveal">{cards}</div>'


def section_gallery_booking(profile: dict, phone: str, map_url: str) -> str:
    ph = _sections().phone_href(phone)
    labels = profile.get("gallery_labels") or ["Our space", "The work", "Details"]
    gal = "".join(f"<div>{html.escape(lb)}</div>" for lb in labels[:3])
    chips = profile.get("services") or []
    chip_html = "".join(f'<span class="chip">{html.escape(c)}</span>' for c in chips[:8])
    return f"""
    <div class="gallery-row reveal" aria-hidden="true">{gal}</div>
    <div class="booking-panel reveal">
      <div>
        <h2 style="margin:0 0 .5rem;font-size:1.25rem">Book your visit</h2>
        <p style="margin:0;color:var(--muted);font-size:.92rem">{html.escape(profile.get("booking_blurb", "Call ahead or walk in when available."))}</p>
      </div>
      <a class="btn btn-primary" href="{ph}">Call {html.escape(phone)}</a>
      <a class="btn btn-ghost" href="{html.escape(map_url)}">Directions</a>
    </div>
    <section class="services-block reveal" id="services">
      <div class="wrap">
        <h2>{html.escape(profile.get("services_heading", "Services"))}</h2>
        <div class="chip-row">{chip_html}</div>
      </div>
    </section>"""


def section_process_story(profile: dict) -> str:
    paras = profile.get("paragraphs") or []
    steps = profile.get("process_steps") or []
    ps = "".join(f"<p>{html.escape(p)}</p>" for p in paras)
    steps_html = ""
    for s in steps:
        if isinstance(s, str):
            steps_html += f'<div class="process-step reveal"><p style="margin:0">{html.escape(s)}</p></div>'
        else:
            steps_html += (
                f'<div class="process-step reveal"><strong>{html.escape(s.get("title", ""))}</strong>'
                f'<p style="margin:.35rem 0 0">{html.escape(s.get("text", ""))}</p></div>'
            )
    if not paras and not steps:
        return _sections().section_story(profile)
    return f"""
    <section class="story-block reveal" id="story">
      <div class="wrap process-split">
        <div class="story-copy">{ps}{profile.get("aside_html", "")}</div>
        <div>{steps_html}</div>
      </div>
    </section>"""


def section_services_emergency(profile: dict) -> str:
    items = profile.get("services") or []
    lis = "".join(f"<li>{html.escape(s)}</li>" for s in items)
    return f"""
    <section class="services-block reveal" id="services">
      <div class="wrap">
        <h2>{html.escape(profile.get("services_heading", "How we help"))}</h2>
        <ul class="svc-cards">{lis}</ul>
      </div>
    </section>"""


def build_sections(
    skeleton: str,
    profile: dict,
    row: dict,
    name: str,
    address: str,
    lat: float,
    lon: float,
    phone: str,
    map_url: str,
) -> str:
    rs = _sections()
    order = profile.get("sections") or ["story", "services", "menu", "hours", "location", "contact"]
    parts = []

    if skeleton == "studio_booking":
        parts.append(section_gallery_booking(profile, phone, map_url))
        for s in order:
            if s == "story":
                parts.append(rs.section_story(profile))
            elif s == "hours":
                parts.append(rs.section_hours(profile))
            elif s == "location":
                parts.append(rs.section_location(name, address, lat, lon))
            elif s == "contact":
                parts.append(rs.section_contact(row))
        return "".join(parts)

    if skeleton == "service_emergency":
        for s in order:
            if s == "story":
                parts.append(rs.section_story(profile))
            elif s == "services":
                parts.append(section_services_emergency(profile))
            elif s == "hours":
                parts.append(rs.section_hours(profile))
            elif s == "location":
                parts.append(rs.section_location(name, address, lat, lon))
            elif s == "contact":
                parts.append(rs.section_contact(row))
        return "".join(parts)

    if skeleton == "craft_workshop":
        for s in order:
            if s == "story":
                parts.append(section_process_story(profile))
            elif s == "services":
                parts.append(rs.section_services(profile))
            elif s == "menu":
                parts.append(rs.section_menu(profile))
            elif s == "hours":
                parts.append(rs.section_hours(profile))
            elif s == "location":
                parts.append(rs.section_location(name, address, lat, lon))
            elif s == "contact":
                parts.append(rs.section_contact(row))
        return "".join(parts)

    # menu_forward & service_trust & default
    for s in order:
        if s == "story":
            parts.append(rs.section_story(profile))
        elif s == "services":
            parts.append(rs.section_services(profile))
        elif s == "menu":
            parts.append(rs.section_menu(profile))
        elif s == "hours":
            parts.append(rs.section_hours(profile))
        elif s == "location":
            parts.append(rs.section_location(name, address, lat, lon))
        elif s == "contact":
            parts.append(rs.section_contact(row))
    return "".join(parts)


def render_hero_extras(
    skeleton: str, profile: dict, phone: str, highlights: list[str]
) -> str:
    if skeleton == "service_emergency":
        label = profile.get("emergency_label") or "Available for urgent service — call now"
        trust = profile.get("trust_strip") or highlights[:4]
        strip = "".join(f"<div>{html.escape(t)}</div>" for t in trust)
        return section_emergency_cta(phone, label) + f'<div class="trust-strip">{strip}</div>'
    if skeleton == "service_trust":
        return section_trust_bar(highlights)
    return ""
