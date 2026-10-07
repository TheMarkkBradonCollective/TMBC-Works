#!/usr/bin/env python3
"""Generate premium TMBC Works preview sites."""
import csv
import html
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from tmbc_constants import TMBC_FEEDBACK_EMAIL

from lib.catalog import profile_for
from lib.render_site import favicon_svg, render_compare, render_index
from lib.slugs import slugify

CSV_PATH = os.path.join(ROOT, "leads.csv")
BASE_URL = "https://themarkkbradoncollective.github.io/TMBC-Works"


def write_shared_config() -> None:
    shared = os.path.join(ROOT, "_shared")
    os.makedirs(shared, exist_ok=True)
    js = f"""/** Feedback mailto target — not displayed on previews. */
window.TMBC_CONFIG = {{
  feedbackEmail: {json.dumps(TMBC_FEEDBACK_EMAIL)}
}};
"""
    with open(os.path.join(shared, "tmbc-config.js"), "w", encoding="utf-8") as f:
        f.write(js)


def compare_upgrades(row: dict) -> list[str]:
    reasons = (row.get("outdated_reasons") or "").strip()
    pts = []
    if reasons:
        for part in reasons.replace(";", ".").split("."):
            part = part.strip()
            if len(part) > 12:
                pts.append(part[0].upper() + part[1:] if part else part)
    defaults = [
        "Mobile-first layout with readable type and tap-to-call buttons",
        "Secure, modern hosting path with fast static delivery",
        "Clear map, directions, and contact section above the fold on phones",
        "Professional imagery and structured content instead of placeholder blocks",
    ]
    for d in defaults:
        if len(pts) >= 5:
            break
        if d not in pts:
            pts.append(d)
    return pts[:5]


def main():
    # Ensure enrichment exists
    enrich = os.path.join(ROOT, "data", "lead_enrichment.json")
    if not os.path.isfile(enrich):
        import build_enrichment

        build_enrichment.main()

    write_shared_config()
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    previews = []
    for row in rows:
        lead_num = int(row["#"])
        slug = slugify(row["business_name"])
        profile = profile_for(slug, row)
        out_dir = os.path.join(ROOT, slug)
        os.makedirs(out_dir, exist_ok=True)

        page = render_index(row, profile, slug, BASE_URL)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)

        fav = favicon_svg(profile.get("favicon_initial", "B"), profile["colors"]["accent"])
        with open(os.path.join(out_dir, "favicon.svg"), "w", encoding="utf-8") as f:
            f.write(fav)

        compare_url = ""
        if (row.get("website_status") or "") == "outdated":
            upgrades = compare_upgrades(row)
            cmp_html = render_compare(row, profile, slug, BASE_URL, upgrades)
            with open(os.path.join(out_dir, "compare.html"), "w", encoding="utf-8") as f:
                f.write(cmp_html)
            compare_url = f"{BASE_URL}/{slug}/compare.html"

        previews.append(
            {
                "lead_number": lead_num,
                "business_name": row["business_name"],
                "slug": slug,
                "preview_url": f"{BASE_URL}/{slug}/",
                "compare_url": compare_url,
                "email": row.get("email") or "",
                "phone": row["phone"],
            }
        )

    with open(os.path.join(ROOT, "previews.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "lead_number",
                "business_name",
                "slug",
                "preview_url",
                "compare_url",
                "email",
                "phone",
            ],
        )
        w.writeheader()
        w.writerows(previews)

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
    body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 2rem 1rem; }}
    .wrap {{ max-width: 720px; margin: 0 auto; }}
    h1 {{ font-size: 1.5rem; }}
    p.sub {{ color: #94a3b8; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 0 0 0.35rem; }}
    a {{ display: block; padding: 0.65rem 0.85rem; background: #1e293b; border-radius: 8px; color: #f8fafc; text-decoration: none; border: 1px solid #334155; }}
    a:hover {{ border-color: #64748b; }}
    .num {{ color: #38bdf8; font-weight: 600; margin-right: 0.5rem; }}
    .cat {{ float: right; font-size: 0.8rem; color: #94a3b8; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>TMBC Works — Client preview sites</h1>
    <p class="sub">Private index · not indexed by search engines</p>
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
    print(f"Generated {len(previews)} premium previews")


if __name__ == "__main__":
    main()
