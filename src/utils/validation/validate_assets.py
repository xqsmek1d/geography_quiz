import os

from utils.paths import COUNTRIES_JSON, ASSETS_DIR
from utils.paths import COUNTRY_FLAG_IMAGES_DIR, COUNTRY_SHAPE_IMAGES_DIR, COUNTRY_HIGHLIGHT_IMAGES_DIR
from quiz_game.repositories.country_repository import CountryRepository

def validate_assets():
    country_repository = CountryRepository(COUNTRIES_JSON)

    # FLAG IMAGES VALIDATION
    listed_images = country_repository.get_images()
    missing_flag_images = []
    missing_shape_images = []
    missing_highlight_images = []

    for fname in os.listdir(COUNTRY_FLAG_IMAGES_DIR):
        if fname.endswith('.png') and fname not in listed_images:
            missing_flag_images.append(fname)

    for fname in os.listdir(COUNTRY_SHAPE_IMAGES_DIR):
        if fname.endswith('.png') and fname not in listed_images:
            missing_shape_images.append(fname)

    for fname in os.listdir(COUNTRY_HIGHLIGHT_IMAGES_DIR):
        if fname.endswith('.png') and fname not in listed_images:
            missing_highlight_images.append(fname)


    flag_image_check = "SUCCESS" if not missing_flag_images else "FAILED"
    shape_image_check = "SUCCESS" if not missing_shape_images else "FAILED"
    highlight_image_check = "SUCCESS" if not missing_highlight_images else "FAILED"

    # REPORTING    
    assets_report = ["\n===== Assets data validation report =====",]
    #assets_report.append(f"Assets folder: {ASSETS_DIR}")
    #assets_report.append(f"Flag images folder: {COUNTRY_FLAG_IMAGES_DIR}")
    #assets_report.append(f"Shape images folder: {COUNTRY_SHAPE_IMAGES_DIR}")
    #assets_report.append(f"Highlight images folder: {COUNTRY_HIGHLIGHT_IMAGES_DIR}")

    #assets_report.append(f"{len(listed_images)} unique entries found in countries.json")

    assets_report.append(f"\n- Flag images validation: {flag_image_check}")
    if flag_image_check == "FAILED":
        assets_report.append(f"{len(os.listdir(COUNTRY_FLAG_IMAGES_DIR))} files found in {COUNTRY_FLAG_IMAGES_DIR}")
        assets_report.append(f"MISSING in countries.json:\n{missing_flag_images}")

    assets_report.append(f"\n- Country shape images validation: {shape_image_check}")
    if shape_image_check == "FAILED":
        assets_report.append(f"{len(os.listdir(COUNTRY_SHAPE_IMAGES_DIR))} files found in {COUNTRY_SHAPE_IMAGES_DIR}")
        assets_report.append(f"MISSING in countries.json:\n{missing_shape_images}")

    assets_report.append(f"\n- Country highlight images validation: {highlight_image_check}")
    if highlight_image_check == "FAILED":
        assets_report.append(f"{len(os.listdir(COUNTRY_HIGHLIGHT_IMAGES_DIR))} files found in {COUNTRY_HIGHLIGHT_IMAGES_DIR}")
        assets_report.append(f"MISSING in countries.json:\n{missing_highlight_images}")

    return "\n".join(assets_report)

def main():
    print(validate_assets())

if __name__=="__main__":
    main()