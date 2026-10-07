#!/usr/bin/env python3
"""Validate lead_enrichment.json depth after manual/subagent research passes."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "lead_enrichment.json")


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    thin = []
    for slug, e in data.items():
        paras = len(e.get("paragraphs") or [])
        menu = len(e.get("menu_categories") or [])
        svc = len(e.get("services") or [])
        hours = e.get("hours") or []
        has_menu_content = menu > 0 and any(c.get("items") for c in e.get("menu_categories") or [])
        depth_ok = paras >= 2 and (has_menu_content or svc >= 5 or len(hours) >= 1)
        if not depth_ok:
            thin.append(slug)
    print("Slugs:", len(data), "Thin:", len(thin))
    if thin:
        print("\n".join(thin))
    return 0 if len(thin) < 8 else 1


if __name__ == "__main__":
    sys.exit(main())
