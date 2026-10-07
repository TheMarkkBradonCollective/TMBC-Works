#!/usr/bin/env python3
import csv
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765/TMBC-Works"
fail = 0

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

if fail:
    sys.exit(1)
print("All checks passed for", len(rows), "previews")
