#!/usr/bin/env python3
import csv
import re
import sys
import urllib.request

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765/TMBC-Works"
fail = 0

with open(ROOT / "previews.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        slug = row["slug"]
        path = ROOT / slug / "index.html"
        if not path.is_file():
            print(f"MISSING: {slug}")
            fail += 1
            continue
        html = path.read_text(encoding="utf-8")
        if 'name="robots" content="noindex"' not in html:
            print(f"NO NOINDEX: {slug}")
            fail += 1
        if "TMBC Works" not in html:
            print(f"NO BANNER: {slug}")
            fail += 1
        if re.search(r'href="/(?!/)', html):
            print(f"ABSOLUTE PATH LINK: {slug}")
            fail += 1
        try:
            with urllib.request.urlopen(f"{BASE}/{slug}/", timeout=5) as resp:
                if resp.status != 200:
                    print(f"HTTP {resp.status}: {slug}")
                    fail += 1
        except Exception as e:
            print(f"FETCH FAIL {slug}: {e}")
            fail += 1

if fail:
    sys.exit(1)
print("All checks passed for", sum(1 for _ in open(ROOT / "previews.csv")) - 1, "previews")
