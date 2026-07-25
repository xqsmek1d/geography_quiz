import json
from pathlib import Path

from quiz_game.models.country import Country

class CountryRepository:
    def __init__(self, path: Path):
        self.path = path
    
    def load_all(self) -> list[Country]:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)

        return [Country(**country) for country in data]

    def load_all(self) -> list[Country]:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)

        return [Country(**country) for country in data]

    def get_flag_images(self) -> list[str]:
        countries = self.load_all()
        return set([country.flag_image for country in countries])
