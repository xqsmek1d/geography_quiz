import unicodedata

from utils.paths import COUNTRIES_JSON
from quiz_game.repositories.country_repository import CountryRepository

def slugify(text: str) -> str:
    # Convert a text to be suitable for a filename.
    return (text.lower().replace(" ", "_").replace("-", "_").replace("'", ""))

def sanitise_string(text: str) -> str:
    """
    Remove accents/diacritics and return an ASCII-only string.
    """
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    ).replace(".","")

def parse_population(population: str) -> int | None:
    if not population:
        return None

    return int(population)

def parse_area(area_sq_km: str) -> int | None:
    if not area_sq_km:
        return None

    return int(area_sq_km)

def parse_gdp(gdp: str) -> int | None:
    if not gdp:
        return None

    return int(gdp)

def parse_fips(fips: str | None) -> str | None:
    country_repository = CountryRepository(COUNTRIES_JSON)
    fips_to_iso3_dict = country_repository.get_fips_to_iso3()

    if fips == "WE":    # Ariha is located in Syria but had the fips of "WE"
        return "SYR" 
    
    if fips == "NT":    # In Cities source dataset, curacao is set as the netherlands antilles (old)
        return "CUW"

    if fips in fips_to_iso3_dict.keys():
        return fips_to_iso3_dict[fips]

    return None

