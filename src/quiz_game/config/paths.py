from pathlib import Path

# root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PACKAGE_ROOT.parent

# directories
SOURCES_DIR = SRC_ROOT / "sources"
UTILS_DIR = SRC_ROOT / "utils"
DATA_DIR = PACKAGE_ROOT / "data"
ASSETS_DIR = PACKAGE_ROOT / "assets"
CORRECTIONS_DIR = UTILS_DIR / "corrections"

# file paths (sources)
COUNTRIES_CSV = SOURCES_DIR / "countries.csv"
COUNTRIES_CORRECTIONS_JSON = CORRECTIONS_DIR / "countries.json"
COUNTRIES_GPKG = SOURCES_DIR / "world_bank_official_boundaries_admin0_merged.gpkg"
CITIES_GEOJSON = SOURCES_DIR / "World_Cities.geojson"
CITIES_CORRECTIONS_JSON = CORRECTIONS_DIR / "cities.json"

# file paths (data)
COUNTRIES_JSON = DATA_DIR / "countries.json"
CITIES_JSON = DATA_DIR / "cities.json"
LANDMARKS_JSON = DATA_DIR / "landmarks.json"

# file paths (assets)
FLAG_IMAGES_DIR = ASSETS_DIR / "flags"
MAP_OUTLINES_DIR = ASSETS_DIR / "map_outlines"
MAP_HIGHLIGHTS_DIR = ASSETS_DIR / "map_highlights"