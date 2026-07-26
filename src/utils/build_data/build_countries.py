import csv
import json

from utils.paths import COUNTRIES_CSV, COUNTRIES_JSON, COUNTRIES_CORRECTIONS_JSON
from quiz_game.models.country import Country
from quiz_game.algorithms.country_difficulty import calculate_country_difficulty
from utils.corrections.country_transformations import normalize_region, normalize_subregion
from utils.corrections.apply_corrections import apply_corrections
from utils.common.json_loader import load_json
from utils.corrections.data_parsers import parse_population, parse_area, parse_gdp, sanitise_string

def main():
    build_countries()

def build_countries():    
    countries = []

    max_population = float("-inf")
    max_gdp = float("-inf")
    max_area_sq_km = float("-inf")

    # Read countries.csv source file and construct countries
    with open(COUNTRIES_CSV, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            iso3 = row["iso3"].upper()
            name = row["name"]
            capital = row["capital"]

            country = Country(
                id = iso3,
                name = name,
                optional_prefix = row["optional_prefix"] if row["optional_prefix"] else None,
                optional_suffix = row["optional_suffix"] if row["optional_suffix"] else None,
                optional_names = row["optional_name"].split("or") if row["optional_name"] else None,
                iso2 = row["iso2"].upper(),
                fips = row["fips"].upper() if row["fips"] != "#N/A" else None,
                capital_id = sanitise_string(f"{iso3}_{capital.upper().replace(" ","_")}") if (capital != "#N/A") else None,
                region = normalize_region(row["region"]),
                subregion = normalize_subregion(row["subregion"]),
                population = parse_population(row["population"]),
                area_sq_km = parse_area(row["area_sq_km"]),
                gdp = parse_gdp(row["gdp"]),
                image = f"{iso3}.png",
            )

            countries.append(country)

    # Assign a difficulty score for each country
    for country in countries:
        country.difficulty_score = calculate_country_difficulty(country, countries)

    # Apply corrections
    corrections = load_json(COUNTRIES_CORRECTIONS_JSON)
    countries = apply_corrections(countries,corrections)
    
    # Write countries to a .json file (using a .tmp to catch errors)
    temp_path = COUNTRIES_JSON.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as jsonfile:
        json.dump([country.model_dump() for country in countries], jsonfile, indent=4)

    temp_path.replace(COUNTRIES_JSON)

    print(f"Succesfully wrote {len(countries)} countries in {COUNTRIES_JSON}")

if __name__ == "__main__":
    main()