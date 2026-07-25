import json
from pathlib import Path

from quiz_game.models.city import City

class CityRepository:
    def __init__(self, path: Path):
        self.path = path
    
    def load_all(self) -> list[City]:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)