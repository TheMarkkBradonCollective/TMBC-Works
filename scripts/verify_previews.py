#!/usr/bin/env python3
import csv
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765/TMBC-Works"
fail = 0
_HERO_BG_RE = re.compile(r"background:url\('([^']+)'\)")
_OG_IMAGE_RE = re.compile(r'property="og:image" content="([^"]+)"')


def hero_image_url(html: str) -> str | None:
    m = _HERO_BG_RE.search(html)
    if m:
        return m.group(1).replace("&amp;", "&")
    m = _OG_IMAGE_RE.search(html)
    if m:
        return m.group(1).replace("&amp;", "&")
    return None


def hero_image_ok(url: str, timeout: float = 20) -> bool:
    if not url or not url.startswith("https://"):
        return False
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "TMBC-Works-Verify/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code in (405, 403):
            req = urllib.request.Request(
                url,
                method="GET",
                headers={"User-Agent": "TMBC-Works-Verify/1.0", "Range": "bytes=0-0"},
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                    return resp.status in (200, 206)
            except Exception:
                return False
        return False
    except Exception:
        return False

with open(ROOT / "previews.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    slug = row["slug"]
    path = ROOT / slug / "index.html"
    if not path.is_file():
        print("MISSING:", slug)
        fail += 1
        continue
    html = path.read_text(encoding="utf-8")
    checks = [
        ('name="robots" content="noindex"', "NO NOINDEX"),
        ("Website preview designed by TMBC Works", "NO BANNER"),
        ("../_shared/tmbc.css", "NO SHARED CSS"),
        ("tmbc-sticky-bar", "NO STICKY BAR"),
        ("tmbc-feedback", "NO FEEDBACK"),
        ("openstreetmap.org/export/embed.html", "NO OSM MAP"),
        ('property="og:title"', "NO OG"),
        ("favicon.svg", "NO FAVICON"),
    ]
    for needle, label in checks:
        if needle not in html:
            print(label, slug)
            fail += 1
    if "themarkkbrandoncollective@gmail.com" in html and "mailto:" in html:
        # email may appear only inside encoded mailto — allow mailto but not visible text
        if re.search(r">[^<]*themarkkbrandoncollective@gmail.com", html):
            print("TMBC EMAIL VISIBLE", slug)
            fail += 1
    if "(530) 978-9886" in html or "+15309789886" in html:
        print("TMBC PHONE VISIBLE", slug)
        fail += 1
    if row.get("compare_url"):
        if not (ROOT / slug / "compare.html").is_file():
            print("MISSING COMPARE", slug)
            fail += 1
    try:
        with urllib.request.urlopen(f"{BASE}/{slug}/", timeout=8) as resp:
            if resp.status != 200:
                print("HTTP", resp.status, slug)
                fail += 1
    except Exception as e:
        print("FETCH", slug, e)
        fail += 1
    hero_url = hero_image_url(html)
    if not hero_url:
        print("NO HERO IMAGE URL", slug)
        fail += 1
    elif not hero_image_ok(hero_url):
        print("HERO IMAGE NOT OK (expected HTTP 200)", slug, hero_url)
        fail += 1

if fail:
    sys.exit(1)
print("All checks passed for", len(rows), "previews")
