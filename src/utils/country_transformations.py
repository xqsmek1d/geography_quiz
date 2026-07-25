SUBREGION_MAP = {
    "Northern Europe": "North Europe",
    "Eastern Europe": "East Europe",
    "Southern Europe": "South Europe",
    "Western Europe": "West Europe",
    "Eastern Asia": "East Asia",
    "South-Eastern Asia": "South-East Asia",
    "Southern Asia": "South Asia",
    "Western Asia": "West Asia",
    "Central Asia": "Central Asia",
    "Northern America": "North America",
    "South America": "South America",
    "Central America": "Central America",
    "Northern Africa": "North Africa",
    "Eastern Africa": "East Africa",
    "Southern Africa": "South Africa",
    "Western Africa": "West Africa",
    "Middle Africa": "Middle Africa",
    "Australia and New Zealand": "Australia and New Zealand",
    "Caribbean": "Caribbean",
    "Melanesia": "Melanesia",
    "Polynesia": "Polynesia",
    "Micronesia": "Micronesia",
}

REGION_MAP = {
    "Europe": "Europe",
    "Asia": "Asia",
    "Americas": "Americas",
    "Africa": "Africa",
    "Oceania": "Oceania",
    "Polar": "Polar",
}

def normalize_region(region: str) -> str:
    return REGION_MAP.get(region, "Other")

def normalize_subregion(subregion: str) -> str:
    return SUBREGION_MAP.get(subregion, "Other")
