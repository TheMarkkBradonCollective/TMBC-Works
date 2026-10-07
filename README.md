# TMBC Works — Sacramento preview sites

Static, premium-style preview websites for local business outreach. **No build step** — plain HTML/CSS/JS served from GitHub Pages.

## Structure

| Path | Purpose |
|------|---------|
| `index.html` | Private index of all 50 previews (`noindex`) |
| `previews.csv` | lead_number, business_name, slug, preview_url, **compare_url**, email, phone |
| `_shared/tmbc.css`, `_shared/tmbc.js` | TMBC overlay (banner, feedback, sticky call/directions bar) |
| `_shared/tmbc-config.js` | Feedback mailto target only (not shown on pages) |
| `scripts/tmbc_constants.py` | Same feedback email for the generator |
| `<slug>/index.html` | Redesigned preview |
| `<slug>/compare.html` | Before/after (outdated-site leads only) |
| `<slug>/assets/legacy-site.png` | Screenshot of previous site (when capture succeeds) |
| `data/lead_enrichment.json` | Verified copy + visual assignments |
| `scripts/generate_previews.py` | Build/regenerate all sites |

Live URL pattern: `https://themarkkbradoncollective.github.io/TMBC-Works/<slug>/`

## GitHub Pages

**Settings → Pages → Deploy from branch `main` / (root)**. Ensure `.nojekyll` is present.

## Regenerate everything

```bash
cd scripts
# Edit data/lead_enrichment.json (curated copy) then:
python3 capture_legacy.py      # optional: refresh compare screenshots
python3 generate_previews.py
python3 verify_previews.py     # with local server under /TMBC-Works/
```

Local test:

```bash
ln -sfn "$(pwd)" /tmp/ghpages/TMBC-Works
cd /tmp/ghpages && python3 -m http.server 8765
```

## TMBC on-page policy

Preview pages show **only** the banner text “Website preview designed by TMBC Works” — no TMBC email or phone on the page. Owners submit feedback via the **Send feedback** button (mailto to the address in `tmbc_constants.py`).
