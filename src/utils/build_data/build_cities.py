import csv
import json
import os
import geopandas as gpd

from utils.paths import COUNTRIES_CSV, CITIES_CORRECTIONS_JSON, CITIES_GEOJSON, CITIES_JSON
from quiz_game.config.known_data_exceptions import NO_CAPITAL_INFO
from quiz_game.repositories.city_repository import CityRepository
from quiz_game.models.city import City
from utils.corrections.country_transformations import normalize_region, normalize_subregion
from utils.corrections.apply_corrections import apply_corrections
from utils.common.json_loader import load_json
from utils.corrections.data_parsers import slugify, sanitise_string, parse_fips

def build_capitals():
    capitals = []

    # Read countries.csv source file and construct countries
    with open(COUNTRIES_CSV, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            country_id = row["iso3"].upper()
            capital = row["capital"]
            
            if capital == "#N/A":
                continue

            capital_id = sanitise_string(f"{country_id}_{capital.upper().replace(" ","_")}")

            capital = City(
                id = capital_id,
                name = capital,
                country_id = country_id,
                is_capital = True,
                is_subcapital = False,
                image = f"{slugify(capital_id).upper()}.png",
            )

            capitals.append(capital)

    # Apply corrections
    corrections = load_json(CITIES_CORRECTIONS_JSON)
    capitals = apply_corrections(capitals,corrections)
    
    # Write countries to a .json file (using a .tmp to catch errors)
    temp_path = CITIES_JSON.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as jsonfile:
        json.dump([capital.model_dump() for capital in capitals], jsonfile, indent=4)

    temp_path.replace(CITIES_JSON)

    print(f"Succesfully wrote {len(capitals)} capitals in {CITIES_JSON}")

def update_capital_info():

    # Load existing cities.json
    if not os.path.exists(CITIES_JSON):
        raise Exception("ERROR: attempting to edit a non-existing cities.json file!")

    city_repository = CityRepository(CITIES_JSON)
    capitals = city_repository.load_all_capitals(as_dict = True)

    cities_df = gpd.read_file(CITIES_GEOJSON, columns=["CITY_NAME", "GMI_ADMIN", "ADMIN_NAME", "FIPS_CNTRY", "CNTRY_NAME", "STATUS", "POP","geometry"])
    count = 0

    for city in cities_df.itertuples():

        if city.STATUS not in {"National and provincial capital", "National capital", "National capital and provincial capital enclave", "Independent and provincial capital",}:
            continue

        country_id = parse_fips(city.FIPS_CNTRY)

        # Find matching city in cities.json
        if country_id not in capitals.keys():
            print(f"Capital not found: {city.CITY_NAME}, country_id: {country_id})")
            continue

        count += 1

        existing_city = capitals[country_id]
        existing_city.population = city.POP
        existing_city.admin_id = city.GMI_ADMIN
        existing_city.admin_name = city.ADMIN_NAME
        if city.geometry is not None:
            existing_city.latitude = city.geometry.y
            existing_city.longitude = city.geometry.x

      
    # Write countries to a .json file (using a .tmp to catch errors)
    temp_path = CITIES_JSON.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as jsonfile:
        json.dump([city.model_dump() for city in capitals.values()], jsonfile, ensure_ascii=False, indent=4,)

    temp_path.replace(CITIES_JSON)

    print(f"Succesfully wrote capital information for {count} in {CITIES_JSON}")

    # Return names of capitals that were not updated
    untouched_capitals = []

    for capital in capitals.values():
        if capital.population == None and capital.country_id not in NO_CAPITAL_INFO:
            untouched_capitals.append((capital.name, capital.country_id))
       
    return untouched_capitals

def append_cities():
    return

def main():
    build_capitals()

    untouched_capitals = update_capital_info()

    if untouched_capitals:
        print("Capitals that were not updated:")
        for entry in untouched_capitals:
            print(entry)

    append_cities()

if __name__ == "__main__":
    main()