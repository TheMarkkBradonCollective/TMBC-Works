#!/usr/bin/env python3
"""Capture screenshots of outdated lead websites for compare.html."""
import csv
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(ROOT, "leads.csv")

from lib.slugs import slugify


def capture(url: str, dest: str) -> bool:
    if os.path.isfile(dest) and os.path.getsize(dest) > 8000:
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    ud = f"/tmp/chrome-cap-{abs(hash(dest)) % 10**6}"
    os.makedirs(ud, exist_ok=True)
    urls = [url]
    if url.startswith("https://"):
        urls.append("http://" + url[len("https://") :])
    for attempt in urls:
        cmd = [
            "timeout",
            "28",
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--user-data-dir={ud}",
            "--window-size=1280,900",
            f"--screenshot={dest}",
            "--virtual-time-budget=5000",
            attempt,
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=35)
            if r.returncode == 0 and os.path.isfile(dest) and os.path.getsize(dest) > 8000:
                return True
        except Exception:
            pass
    return False


def main():
    ok = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("website_status") or "") != "outdated":
                continue
            url = (row.get("current_website") or "").strip()
            if not url:
                continue
            slug = slugify(row["business_name"])
            dest = os.path.join(ROOT, slug, "assets", "legacy-site.png")
            if capture(url, dest):
                ok += 1
                print("OK", slug)
            else:
                print("FAIL", slug, url)
    print("Captured", ok, "legacy screenshots")


if __name__ == "__main__":
    main()
