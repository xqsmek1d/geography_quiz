from quiz_game.models.city import City
from quiz_game.repositories.country_repository import CountryRepository

def get_capital_difficulty(capital: City):
    country_repository = CountryRepository()
    countries = country_repository.load_all(as_dict=True)
    return countries[capital.country_id].difficulty_score


