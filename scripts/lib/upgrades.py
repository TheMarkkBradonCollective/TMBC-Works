"""Optional 'upgrade' feature sections (new TMBC standard).

Only rendered when a profile has an "upgrade" dict, so older previews are untouched.
Anything that needs setup by the business is labelled DEMO on the page.
"""
import html
from urllib.parse import quote_plus

E = html.escape
DEMO = '<span class="demo-tag">DEMO</span>'

UPGRADE_CSS = """
.up-block { padding: 3.5rem 0; }
.up-block:nth-of-type(even) { background: var(--surface); }
.up-block h2 { margin-top: 0; }
.demo-tag { display:inline-block; font: 700 .7rem/1 system-ui,sans-serif; letter-spacing:.08em; background:#f59e0b; color:#111; padding:.3rem .5rem; border-radius:4px; vertical-align:middle; margin-left:.5rem; }
.demo-note { font-size:.85rem; color:var(--muted); border-left:3px solid #f59e0b; padding-left:.75rem; }
.up-grid { display:grid; gap:1rem; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); }
.up-card { background:var(--bg); border:1px solid color-mix(in srgb,var(--muted) 25%,transparent); border-radius:var(--radius); padding:1.25rem; }
.up-block:nth-of-type(even) .up-card { background: var(--bg); }
.rating-big { font-size:3rem; font-weight:700; line-height:1; }
.stars { color:#f5b301; font-size:1.4rem; letter-spacing:.1em; }
.price-row { display:flex; justify-content:space-between; gap:1rem; border-bottom:1px dashed color-mix(in srgb,var(--muted) 35%,transparent); padding:.55rem 0; }
.price-row b { white-space:nowrap; }
.up-form { display:grid; gap:.75rem; max-width:560px; }
.up-form label { display:grid; gap:.25rem; font-size:.9rem; }
.up-form input, .up-form select, .up-form textarea { font:inherit; padding:.65rem .75rem; border-radius:8px; border:1px solid color-mix(in srgb,var(--muted) 40%,transparent); background:var(--bg); color:var(--text); }
.up-form button, .up-btn { font:inherit; font-weight:600; background:var(--accent); color:#fff; border:0; border-radius:8px; padding:.8rem 1.2rem; cursor:pointer; text-decoration:none; display:inline-block; }
.up-form .chk { display:flex; gap:.5rem; align-items:flex-start; grid-template-columns:none; }
.gal-ph { aspect-ratio:4/3; border-radius:var(--radius); display:flex; align-items:center; justify-content:center; text-align:center; padding:1rem; color:var(--muted); background:repeating-linear-gradient(45deg,color-mix(in srgb,var(--muted) 10%,transparent) 0 12px,transparent 12px 24px); border:2px dashed color-mix(in srgb,var(--muted) 40%,transparent); }
.up-feats { display:flex; flex-wrap:wrap; gap:.5rem; padding:0; list-style:none; }
.up-feats li { background:color-mix(in srgb,var(--accent) 12%,transparent); border-radius:999px; padding:.35rem .8rem; font-size:.85rem; }
.up-toast { margin-top:.5rem; font-weight:600; color:var(--accent); }
"""

DEMO_JS = """<script>
document.querySelectorAll('form[data-demo]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var t=f.querySelector('.up-toast');if(t){t.textContent='DEMO only: nothing was sent. Please call the shop for now.';}});});
</script>"""


def _stars(r: float) -> str:
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)


def section_reviews(u: dict, name: str, address: str) -> str:
    r = u.get("rating")
    if not r:
        return ""
    q = quote_plus(f"{name} {address}")
    links = f'<a class="up-btn" href="https://www.google.com/maps/search/?api=1&query={q}">Read reviews on Google</a>'
    fb = u.get("facebook")
    if fb:
        links += f' <a class="up-btn" href="{E(fb, quote=True)}">Facebook page</a>'
    return f"""
    <section class="up-block reveal" id="reviews"><div class="wrap">
      <h2>What customers say</h2>
      <div class="up-grid">
        <div class="up-card"><div class="rating-big">{r:.1f}</div><div class="stars" aria-label="{r:.1f} out of 5">{_stars(r)}</div>
          <p>{E(str(u.get('review_count','')))} reviews{(' on ' + E(u['rating_source'])) if u.get('rating_source') else ''}</p></div>
        <div class="up-card"><p>Rating and review count from public listings. Read the full reviews in the customers' own words:</p><p>{links}</p>
          <p class="demo-note">{DEMO} A live, auto-updating Google reviews feed can be embedded here once connected to the business's Google profile. No review text is shown on this preview.</p></div>
      </div>
    </div></section>"""


def section_pricing(u: dict, phone_href: str) -> str:
    items = u.get("sample_prices") or []
    if not items:
        return ""
    rows = "".join(f'<div class="price-row"><span>{E(a)}</span><b>{E(b)}</b></div>' for a, b in items)
    return f"""
    <section class="up-block reveal" id="pricing"><div class="wrap">
      <h2>Upfront pricing {DEMO}</h2>
      <p class="demo-note">Sample prices for illustration only. These are NOT the business's real prices; the owner would fill these in. Call <a href="{phone_href}">the shop</a> for actual pricing.</p>
      <div class="up-card">{rows}</div>
    </div></section>"""


def section_booking(u: dict) -> str:
    b = u.get("booking")
    if not b:
        return ""
    opts = "".join(f"<option>{E(o)}</option>" for o in b.get("options", []))
    extra = ""
    if b.get("date"):
        extra += '<label>Preferred day and time<input type="datetime-local" name="when"></label>'
    if b.get("photo"):
        extra += '<label>Photo of the item (optional)<input type="file" accept="image/*" name="photo"></label>'
    sms = ""
    if u.get("sms"):
        sms = f'<label class="chk"><input type="checkbox" checked> <span>{E(u["sms"])} {DEMO}</span></label>'
    return f"""
    <section class="up-block reveal" id="book"><div class="wrap">
      <h2>{E(b.get('title','Request an appointment'))} {DEMO}</h2>
      <p class="demo-note">This form is a demonstration and does not send anything yet. It would need to be connected to the shop's phone or email before going live.</p>
      <form class="up-form" data-demo>
        <label>Name<input name="name" autocomplete="name"></label>
        <label>Mobile number<input name="tel" type="tel" autocomplete="tel"></label>
        <label>{E(b.get('select_label','Service'))}<select name="svc">{opts}</select></label>
        {extra}
        <label>Notes<textarea name="notes" rows="3"></textarea></label>
        {sms}
        <button type="submit">{E(b.get('button','Send request'))}</button>
        <div class="up-toast" role="status"></div>
      </form>
    </div></section>"""


def section_gallery(u: dict) -> str:
    g = u.get("gallery") or []
    if not g:
        return ""
    cells = "".join(f'<div class="gal-ph">Photo placeholder:<br>{E(x)}</div>' for x in g)
    return f"""
    <section class="up-block reveal" id="gallery"><div class="wrap">
      <h2>{E(u.get('gallery_title','Our work'))} {DEMO}</h2>
      <p class="demo-note">Placeholders only. The business's own photos would go here.</p>
      <div class="up-grid">{cells}</div>
    </div></section>"""


def section_features(u: dict) -> str:
    f = u.get("features") or []
    if not f:
        return ""
    lis = "".join(f"<li>{E(x)}</li>" for x in f)
    return f"""
    <section class="up-block reveal" id="whats-new"><div class="wrap">
      <h2>What this website adds</h2>
      <ul class="up-feats">{lis}</ul>
      <p class="demo-note">Items marked {DEMO} are previews of features that need setup before launch.</p>
    </div></section>"""


def render_upgrades(profile: dict, name: str, address: str, phone_href: str) -> str:
    u = profile.get("upgrade")
    if not u:
        return ""
    return (section_features(u) + section_booking(u) + section_pricing(u, phone_href)
            + section_reviews(u, name, address) + section_gallery(u))
