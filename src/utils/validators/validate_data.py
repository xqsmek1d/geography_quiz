import csv
import json
import os
import shutil
from pathlib import Path

from quiz_game.config.paths import COUNTRIES_CSV, COUNTRIES_JSON, COUNTRIES_CORRECTIONS_JSON, FLAG_IMAGES_DIR, ASSETS_DIR
from quiz_game.models.country import Country
from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.difficulty.country_difficulty import calculate_country_difficulty
from utils.country_transformations import normalize_region, normalize_subregion
from utils.corrections.corrections import apply_corrections
from utils.json_loader import load_json_as_dict

"""
This script checks some generated data against each other to ensure consistency and detect outlier for manual maintenance of the dataset
Report includes:

In countries.json;
- whether all countries contain a value in the following fields:
    - name
    - id
    - difficulty_level
    - flag image (which should also be present in FLAG_IMAGES_DIR)
    - capital_id (which should also be present in cities.json)
- whether all corrections were applied properly

In cities.json;
- whether all cities contain a value in the following fields:
    - id (which should also be present in countries.json if is_capital == true)
    - name 
    - country_id (which should also be present in countries.json)
    - is_capital (which should be true if the id is found in countries.json)

In quiz_game/assets/flags; 
- Whether all images in the folder are also present in countries.json
"""

def validate_countries():
    countries_report = ["===== Country data validation report =====",]



    return countries_report

def validate_assets():
    country_repository = CountryRepository(COUNTRIES_JSON)

    # FLAGS VALIDATION
    listed_flag_images = country_repository.get_flag_images()
    missing_images = []

    for fname in os.listdir(FLAG_IMAGES_DIR):
        if fname.endswith('.png') and fname not in listed_flag_images:
            missing_images.append(fname)

    flag_image_check = "SUCCESS" if not missing_images else "FAILED"
    
    # REPORTING    
    assets_report = ["\n===== Assets data validation report =====",]
    assets_report.append(f"Assets folder: {ASSETS_DIR}")
    assets_report.append(f"Flags folder: {FLAG_IMAGES_DIR}")

    assets_report.append(f"\n== Flags validation: {flag_image_check} ==")
    assets_report.append(f"{len(os.listdir(FLAG_IMAGES_DIR))} files found in {FLAG_IMAGES_DIR}")
    assets_report.append(f"{len(listed_flag_images)} unique flag_image entries found in countries.json")
    assets_report.append("Images in the folder not present in countries.json:")
    assets_report.append(f"   {missing_images}")

    return "\n".join(assets_report)

def main():
    #print(validate_countries())
    #print(validate_cities())
    print(validate_assets())

if __name__=="__main__":
    main()