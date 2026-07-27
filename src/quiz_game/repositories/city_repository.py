import json
from pathlib import Path

from quiz_game.models.city import City
from utils.paths import CITIES_JSON

class CityRepository:
    def __init__(self, path: Path = CITIES_JSON):
        self.path = path
        self._cities = None
    
    def load_all(self, as_dict=False):

        if self._cities is None:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)

            self._cities = [City(**city) for city in data]

        if as_dict:
            return {city.id: city for city in self._cities}

        return self._cities.copy()

    def load_all_capitals(self, as_dict: bool = False) -> list[City]:
        cities = self.load_all()
        capitals = [city for city in cities if city.is_capital]

        if as_dict:
            capitals_dict = {}
            for capital in capitals:
                capitals_dict[capital.country_id] = capital
            return capitals_dict

        return capitals

    def load_capital_ids(self) -> dict[list[str]: list[str]]:
        capitals = self.load_all_capitals()
        capital_id_dict = {}

        for capital in capitals:
            capital_id_dict[capital.id] = capital.country_id

        return capital_id_dict

    def load_with_filters():
        raise NotImplementedError

    def get_by_id(self, city_id: str) -> City | None:
        cities = self.load_all(as_dict=True)
        return cities.get(city_id)
        