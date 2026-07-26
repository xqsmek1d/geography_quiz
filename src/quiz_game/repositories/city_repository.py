import json
from pathlib import Path

from quiz_game.models.city import City

class CityRepository:
    def __init__(self, path: Path):
        self.path = path
    
    def load_all(self) -> list[City]:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)

        return [City(**city) for city in data]

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
        