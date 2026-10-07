"""Merge curated lead_enrichment.json with palette + assets for rendering."""
import hashlib
import html
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

IMAGES = {
    "barber": "https://images.unsplash.com/photo-1585747860715-2b67a7a7f336?w=1600&q=80",
    "spa": "https://images.unsplash.com/photo-1604654890710-f6390f18ddb0?w=1600&q=80",
    "donut": "https://images.unsplash.com/photo-1551024601-bec78ae704b3?w=1600&q=80",
    "bakery": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1600&q=80",
    "mex": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1600&q=80",
    "food": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1600&q=80",
    "tire": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=1600&q=80",
    "fabric": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600&q=80",
    "check": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1600&q=80",
    "smog": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1600&q=80",
    "auto": "https://images.unsplash.com/photo-1487754180451-c456f581a583?w=1600&q=80",
    "shoe": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=1600&q=80",
    "mower": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=1600&q=80",
    "appliance": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1600&q=80",
    "rad": "https://images.unsplash.com/photo-1625047509248-ec889cbff107?w=1600&q=80",
    "weld": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1600&q=80",
    "martial": "https://images.unsplash.com/photo-1555597673-b21d5c935865?w=1600&q=80",
    "trophy": "https://images.unsplash.com/photo-1517649763962-0c62306601b7?w=1600&q=80",
    "tv": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=1600&q=80",
    "euro": "https://images.unsplash.com/photo-1619642751034-765df279d565?w=1600&q=80",
    "plumb": "https://images.unsplash.com/photo-1585704032915-ebc035e00588?w=1600&q=80",
    "pet": "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=1600&q=80",
    "industrial": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=1600&q=80",
    "rug": "https://images.unsplash.com/photo-1600166896085-959adc3512d1?w=1600&q=80",
    "thai": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=1600&q=80",
    "tow": "https://images.unsplash.com/photo-1544622351-20a7f5172b20?w=1600&q=80",
    "fence": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=1600&q=80",
    "alter": "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=1600&q=80",
}

CATEGORY_SKELETON = {
    "Barbershop": "studio_booking",
    "Nail salon": "studio_booking",
    "Donut shop": "menu_forward",
    "Bakery": "menu_forward",
    "Mexican restaurant": "menu_forward",
    "Thai restaurant": "menu_forward",
    "Tire shop": "service_trust",
    "Auto repair": "service_trust",
    "Auto repair / diagnostics": "service_trust",
    "Auto repair & smog": "service_trust",
    "Smog check": "service_trust",
    "Smog check (STAR)": "service_trust",
    "European auto repair": "service_trust",
    "Import auto repair": "service_trust",
    "Radiator repair": "service_trust",
    "Appliance repair": "service_trust",
    "Towing": "service_emergency",
    "Plumbing": "service_emergency",
    "Martial arts (kung fu)": "studio_booking",
    "Martial arts": "studio_booking",
    "Dog grooming": "studio_booking",
    "Shoe shine": "studio_booking",
    "Auto/marine/furniture upholstery": "craft_workshop",
    "Furniture upholstery": "craft_workshop",
    "Upholstery & embroidery": "craft_workshop",
    "Shoe repair": "craft_workshop",
    "Shoe & leather repair": "craft_workshop",
    "Alterations / tailor": "craft_workshop",
    "Lawn mower / small engine repair": "craft_workshop",
    "Welding / fabrication": "craft_workshop",
    "Mobile welding": "craft_workshop",
    "Industrial contractor / millwright": "craft_workshop",
    "Trophies / engraving": "craft_workshop",
    "TV repair (in-home)": "craft_workshop",
    "Rug cleaning": "craft_workshop",
    "Fence & concrete contractor": "craft_workshop",
}

_cache = None


def _fonts_query(head: str, body: str) -> str:
    return (
        f"family={head.replace(' ', '+')}:wght@400;600;700&"
        f"family={body.replace(' ', '+')}:wght@400;500;600"
    )


def _nav_html(nav) -> str:
    if isinstance(nav, str):
        return nav
    parts = []
    for item in nav:
        href = item.get("href", "#")
        if href == "#location":
            href = "#visit"
        parts.append(f'<a href="{html.escape(href)}">{html.escape(item.get("label", ""))}</a>')
    return "".join(parts)


def _load():
    global _cache
    if _cache is None:
        with open(ENRICH_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def profile_for(slug: str, row: dict) -> dict:
    data = dict(_load()[slug])
    idx = data.get("palette_idx")
    if idx is None:
        idx = int(hashlib.sha256(slug.encode()).hexdigest(), 16) % len(PALETTES)
    pal = PALETTES[idx % len(PALETTES)]

    head = data["font_head"]
    body = data["font_body"]
    image_key = data.get("image_key", "auto")
    hero_image = data.get("hero_image") or IMAGES.get(image_key) or IMAGES["auto"]

    category = row.get("category", "")
    p = {
        **data,
        "colors": pal,
        "font_head": f"'{head}'",
        "font_body": f"'{body}'",
        "fonts_query": data.get("fonts_query") or _fonts_query(head, body),
        "hero_image": hero_image,
        "nav": _nav_html(data.get("nav")),
        "skeleton": data.get("skeleton") or CATEGORY_SKELETON.get(category, "service_trust"),
    }
    p.pop("palette_idx", None)
    p.pop("verification", None)
    p.pop("sources", None)
    p.pop("image_key", None)
    return p
