"""Merge enrichment JSON with palette + layout profile for rendering."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENRICH_PATH = os.path.join(ROOT, "data", "lead_enrichment.json")

PALETTES = [
    {"bg": "#0c0a09", "surface": "#1c1917", "text": "#fafaf9", "muted": "#a8a29e", "accent": "#d97706", "accent2": "#fbbf24", "hero_overlay": "rgba(12,10,9,.72)", "radius": "6px"},
    {"bg": "#fff7ed", "surface": "#ffffff", "text": "#431407", "muted": "#9a3412", "accent": "#ea580c", "accent2": "#fb923c", "hero_overlay": "rgba(67,20,7,.55)", "radius": "18px"},
    {"bg": "#0f172a", "surface": "#1e293b", "text": "#f8fafc", "muted": "#94a3b8", "accent": "#38bdf8", "accent2": "#0ea5e9", "hero_overlay": "rgba(15,23,42,.7)", "radius": "4px"},
    {"bg": "#fdf2f8", "surface": "#fff", "text": "#500724", "muted": "#9d174d", "accent": "#db2777", "accent2": "#f472b6", "hero_overlay": "rgba(80,7,36,.5)", "radius": "20px"},
    {"bg": "#ecfdf5", "surface": "#fff", "text": "#064e3b", "muted": "#047857", "accent": "#059669", "accent2": "#34d399", "hero_overlay": "rgba(6,78,59,.55)", "radius": "14px"},
    {"bg": "#1a1a2e", "surface": "#16213e", "text": "#eaeaea", "muted": "#a0aec0", "accent": "#e94560", "accent2": "#ff6b6b", "hero_overlay": "rgba(26,26,46,.75)", "radius": "0px"},
    {"bg": "#fefce8", "surface": "#fff", "text": "#422006", "muted": "#854d0e", "accent": "#ca8a04", "accent2": "#eab308", "hero_overlay": "rgba(66,32,6,.5)", "radius": "22px"},
    {"bg": "#111827", "surface": "#1f2937", "text": "#f3f4f6", "muted": "#9ca3af", "accent": "#a3e635", "accent2": "#84cc16", "hero_overlay": "rgba(17,24,39,.8)", "radius": "8px"},
    {"bg": "#faf5ff", "surface": "#fff", "text": "#3b0764", "muted": "#7e22ce", "accent": "#9333ea", "accent2": "#c084fc", "hero_overlay": "rgba(59,7,100,.45)", "radius": "16px"},
    {"bg": "#f0f9ff", "surface": "#fff", "text": "#0c4a6e", "muted": "#0369a1", "accent": "#0284c7", "accent2": "#38bdf8", "hero_overlay": "rgba(12,74,110,.5)", "radius": "12px"},
    {"bg": "#292524", "surface": "#44403c", "text": "#fafaf9", "muted": "#d6d3d1", "accent": "#f97316", "accent2": "#fdba74", "hero_overlay": "rgba(41,37,36,.78)", "radius": "10px"},
    {"bg": "#18181b", "surface": "#27272a", "text": "#fafafa", "muted": "#a1a1aa", "accent": "#f43f5e", "accent2": "#fb7185", "hero_overlay": "rgba(24,24,27,.82)", "radius": "2px"},
]

_cache = None


def _load():
    global _cache
    if _cache is None:
        with open(ENRICH_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def profile_for(slug: str, row: dict) -> dict:
    data = _load()[slug]
    pal = PALETTES[data["palette_idx"] % len(PALETTES)]
    p = {
        **data,
        "colors": pal,
        "font_head": f"'{data['font_head']}'",
        "font_body": f"'{data['font_body']}'",
    }
    # Drop non-render keys
    p.pop("palette_idx", None)
    return p
