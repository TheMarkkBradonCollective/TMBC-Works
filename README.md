# TMBC Works — Sacramento preview sites

Static preview websites for local business outreach. Each folder is a self-contained site served as plain HTML/CSS (no build step).

## Structure

| Path | Purpose |
|------|---------|
| `index.html` | Private index linking to all 50 previews (`noindex`) |
| `previews.csv` | Lead number, business name, slug, GitHub Pages URL, email, phone |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll |
| `<slug>/index.html` | One preview site per lead (kebab-case slug from business name) |
| `leads.csv` | Source lead data (reference) |
| `scripts/generate_previews.py` | Generator used to build/regenerate previews |

Live URLs follow:

`https://themarkkbradoncollective.github.io/TMBC-Works/<slug>/`

## GitHub Pages setup

1. Open the repo on GitHub: **Settings → Pages**
2. **Build and deployment → Source:** Deploy from a branch
3. **Branch:** `main` · **Folder:** `/ (root)`
4. Save. The site may take a few minutes to publish.

The root index lists every preview. Each preview includes a small TMBC Works banner and `<meta name="robots" content="noindex">`.

## Local testing

Serve the repo under the same subpath GitHub Pages uses:

```bash
cd /path/to/TMBC-Works
python3 -m http.server 8765
```

Then open `http://localhost:8765/TMBC-Works/` — or symlink/copy the repo into a parent folder named `TMBC-Works` and serve the parent directory.

## Regenerating previews

```bash
python3 scripts/generate_previews.py
```

Edit `scripts/generate_previews.py` (themes, copy templates, slugs) before regenerating. Preview pages use only facts from `leads.csv` and generic category copy elsewhere.

## TMBC Works contact

TMBC contact lives in `scripts/tmbc_constants.py` (mirrored to `_shared/tmbc-config.js`). Regenerate after edits:

```bash
python3 scripts/generate_previews.py
```
