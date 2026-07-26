from pathlib import Path

# root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PACKAGE_ROOT.parent

# directories
SOURCES_DIR = SRC_ROOT / "sources"
UTILS_DIR = PACKAGE_ROOT / "utils"
DATA_DIR = SRC_ROOT / "data"
ASSETS_DIR = SRC_ROOT / "assets"
CORRECTIONS_DIR = UTILS_DIR / "corrections"

# file paths (sources)
COUNTRIES_CSV = SOURCES_DIR / "countries.csv"
COUNTRIES_CORRECTIONS_JSON = CORRECTIONS_DIR / "countries_csv_corrections.json"
COUNTRIES_GPKG = SOURCES_DIR / "corrected_country_boundaries.gpkg"
COUNTRIES_GPKG_CORRECTIONS_JSON = CORRECTIONS_DIR / "countries_gpkg_corrections.json"
CITIES_GEOJSON = SOURCES_DIR / "corrected_world_cities.geojson"
CITIES_CORRECTIONS_JSON = CORRECTIONS_DIR / "cities.json"

# file paths (data)
COUNTRIES_JSON = DATA_DIR / "countries.json"
CITIES_JSON = DATA_DIR / "cities.json"
LANDMARKS_JSON = DATA_DIR / "landmarks.json"

# file paths (assets)
COUNTRY_FLAG_IMAGES_DIR = ASSETS_DIR / "country_flags"
COUNTRY_SHAPE_IMAGES_DIR = ASSETS_DIR / "country_shapes"
COUNTRY_HIGHLIGHT_IMAGES_DIR = ASSETS_DIR / "country_highlights"

# file paths (testing)
TESTS_DIR = SRC_ROOT / "tests"
TEST_DATA_DIR = TESTS_DIR / "tmp_data"
TEST_DATA_COUNTRIES_JSON = TEST_DATA_DIR / "countries.json"

def main():
    print(f'Package root: {PACKAGE_ROOT}')
    print(f'Src root: {SRC_ROOT}')

    print(f'Sources directory: {SOURCES_DIR}')
    print(f'Utils directory: {UTILS_DIR}')
    print(f'Data directory: {DATA_DIR}')
    print(f'Assets directory: {ASSETS_DIR}')
    print(f'Corrections directory: {CORRECTIONS_DIR}')

    print(f'Country flag images directory: {COUNTRY_FLAG_IMAGES_DIR}')
    print(f'Country shape images directory: {COUNTRY_SHAPE_IMAGES_DIR}')
    print(f'Country highlight images directory: {COUNTRY_HIGHLIGHT_IMAGES_DIR}')

if __name__=="__main__":
    main()