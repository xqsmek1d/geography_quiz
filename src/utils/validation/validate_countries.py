import os

from utils.paths import COUNTRIES_JSON, CITIES_JSON
from utils.paths import COUNTRY_FLAG_IMAGES_DIR, COUNTRY_SHAPE_IMAGES_DIR, COUNTRY_HIGHLIGHT_IMAGES_DIR
from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository
from quiz_game.config.question_pools import NO_CAPITAL, NO_COAT_OF_ARMS, NO_FLAG, NO_HIGHLIGHT_IMAGE, NO_SHAPE_IMAGE

def validate_countries_data():
    countries_report = ["\n===== Country data validation report =====",]
    country_repository = CountryRepository(COUNTRIES_JSON)
    city_repository = CityRepository(CITIES_JSON)

    incorrect_difficulty = []

    missing_capital_id = []
    incorrect_capital_id = []

    missing_flag_images = []
    missing_shape_images = []
    missing_highlight_images = []

    incorrect_corrections = []

    capital_id_dict = city_repository.load_capital_ids()

    for country in country_repository.load_all():

        if not country.difficulty_score or country.difficulty_score < 0 or country.difficulty_score > 1:
            incorrect_difficulty.append(country.id)
        
        if not country.capital_id and country.id not in NO_CAPITAL:
            missing_capital_id.append(country.id)
        
        if country.id not in NO_CAPITAL:
            if country.capital_id not in capital_id_dict:
                incorrect_capital_id.append(country.id)
            elif capital_id_dict[country.capital_id] != country.id:
                incorrect_capital_id.append(country.id)
   
        if country.image not in os.listdir(COUNTRY_FLAG_IMAGES_DIR) and country.id not in NO_FLAG:
            missing_flag_images.append(country.id)
    
        if country.image not in os.listdir(COUNTRY_SHAPE_IMAGES_DIR) and country.id not in NO_SHAPE_IMAGE:
            missing_shape_images.append(country.id)
        
        if country.image not in os.listdir(COUNTRY_HIGHLIGHT_IMAGES_DIR) and country.id not in NO_HIGHLIGHT_IMAGE:
            missing_highlight_images.append(country.id)
        
    difficulty_check = "SUCCESS" if not incorrect_difficulty else "FAILED"
    missing_capital_id_check = "SUCCESS" if not missing_capital_id else "FAILED"
    incorrect_capital_id_check = "SUCCES" if not incorrect_capital_id else "FAILED"
    flag_images_check = "SUCCESS" if not missing_flag_images else "FAILED"
    shape_images_check = "SUCCESS" if not missing_shape_images else "FAILED"
    highlight_images_check = "SUCCESS" if not missing_highlight_images else "FAILED"

    countries_report.append(f"\n- Difficulty value check: {difficulty_check}")
    if difficulty_check == "FAILED":
        countries_report.append(f"INCORRECT difficulty_score: {incorrect_difficulty}")

    countries_report.append(f"\n- Capital ID presence check: {missing_capital_id_check}")
    if missing_capital_id_check == "FAILED":
        countries_report.append(f"MISSING capital_ids: {missing_capital_id}")

    countries_report.append(f"\n- Capital ID reference check: {incorrect_capital_id_check}")
    if incorrect_capital_id_check == "FAILED":
        countries_report.append(f"INCORRECT capital_ids: {incorrect_capital_id}")

    countries_report.append(f"\n- Flag image reference check: {flag_images_check}")
    if flag_images_check == "FAILED":
        countries_report.append(f"Flag images missing in {COUNTRY_FLAG_IMAGES_DIR}: {missing_flag_images}")

    countries_report.append(f"\n- Shape image reference check: {shape_images_check}")
    if shape_images_check == "FAILED":
        countries_report.append(f"Shape images missing in {COUNTRY_SHAPE_IMAGES_DIR}: {missing_shape_images}")

    countries_report.append(f"\n- Highlight image reference check: {highlight_images_check}")
    if highlight_images_check == "FAILED":
        countries_report.append(f"Highlight images missing in {COUNTRY_HIGHLIGHT_IMAGES_DIR}: {missing_highlight_images}")

    return "\n".join(countries_report)

def main():
    print(validate_countries())

if __name__=="__main__":
    main()