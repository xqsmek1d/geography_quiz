from utils.validation.validate_countries import validate_countries_data
from utils.validation.validate_assets import validate_assets

"""
This script checks some generated data against each other to ensure consistency and detect outlier for manual maintenance of the dataset
Report includes:

In countries.json;
- whether all countries contain a value in the following fields:
    - difficulty_score
    - image (which should also be present in ALL IMAGE DIRECTORIES)
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

def main():
    print(validate_countries_data())
    #print(validate_cities())
    print(validate_assets())
    print("")

if __name__=="__main__":
    main()