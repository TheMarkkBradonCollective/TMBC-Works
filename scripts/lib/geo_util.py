import json
import os
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEOCODE_PATH = os.path.join(ROOT, "data", "geocodes.json")
UA = "TMBC-Works-Preview-Generator/1.0 (contact: themarkkbrandoncollective@gmail.com)"


def load_geocodes() -> dict:
    if os.path.isfile(GEOCODE_PATH):
        with open(GEOCODE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def geocode_address(address: str):
    q = urllib.parse.quote(address)
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read())
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None


def get_coords(business_name: str, address: str) -> tuple[float, float] | None:
    geo = load_geocodes()
    entry = geo.get(business_name)
    if entry and entry.get("lat") is not None:
        return entry["lat"], entry["lon"]
    try:
        g = geocode_address(address)
        if g:
            geo[business_name] = {"lat": g[0], "lon": g[1]}
            with open(GEOCODE_PATH, "w", encoding="utf-8") as f:
                json.dump(geo, f, indent=2)
            return g
    except Exception:
        pass
    # fallback: city center Sacramento
    return 38.5816, -121.4944


def osm_embed(lat: float, lon: float) -> str:
    pad = 0.012
    bbox = f"{lon - pad},{lat - pad},{lon + pad},{lat + pad}"
    return (
        f"https://www.openstreetmap.org/export/embed.html?"
        f"bbox={urllib.parse.quote(bbox)}&layer=mapnik&marker={lat}%2C{lon}"
    )


def osm_static_map(lat: float, lon: float, w: int = 800, h: int = 360) -> str:
    return (
        "https://staticmap.openstreetmap.de/staticmap.php?"
        f"center={lat},{lon}&zoom=15&size={w}x{h}&markers={lat},{lon},red-pushpin"
    )


def maps_link(address: str) -> str:
    q = urllib.parse.quote(address)
    return f"https://www.google.com/maps/search/?api=1&query={q}"
