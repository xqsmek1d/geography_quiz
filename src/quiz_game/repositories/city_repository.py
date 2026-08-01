import json
from pathlib import Path

from quiz_game.models.city import City
from quiz_game.models.country import Country
from quiz_game.models.settings import LocationFilter

from quiz_game.config.enums import DifficultyLevel
from quiz_game.repositories.country_repository import CountryRepository

from utils.paths import CITIES_JSON

class CityRepository:
    def __init__(self, country_repository: CountryRepository, path: Path = CITIES_JSON):
        
        self.country_repository = country_repository
        self.path = path
        self._cities = None
    
    def _region(self, city: City):
       
        country = self.country_repository.get_by_id(city.country_id)

        if country is None:
            raise ValueError(f"ERROR: country with ID '{city.country_id}' was not found")

        return country.region

    def _subregion(self, city: City):
       
        country = self.country_repository.get_by_id(city.country_id)

        if country is None:
            raise ValueError(f"ERROR: country with ID '{city.country_id}' was not found")

        return country.subregion


    def load_all(self, as_dict: bool=False):

        if self._cities is None:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)

            self._cities = [City(**city) for city in data]

        if as_dict:
            return {city.id: city for city in self._cities}

        return self._cities.copy()

    def load_all_capitals(self,
        difficulty_level: DifficultyLevel | None = None,
        location_filter: LocationFilter | None = None,
        excluded_ids: list[str] | None = None,
        as_dict: bool = False,
        ) -> list[City]:

        cities = self.load_with_filters(difficulty_level=difficulty_level, location_filter=location_filter, excluded_ids=excluded_ids, as_dict=False)

        capitals = [city for city in cities if city.is_capital]

        if as_dict:
            capitals_dict = {}
            for capital in capitals:
                capitals_dict[capital.country_id] = capital
            return capitals_dict

        return capitals

    def load_with_filters(
        self,
        difficulty_level: DifficultyLevel | None = None,
        location_filter: LocationFilter | None = None,
        excluded_ids: list[str] | None = None,
        as_dict: bool = False,
        ) -> list[Country] | None | dict[str, Country]:

        cities = self.load_all()

        # filter exclusions
        if excluded_ids:
            cities = [city for city in cities if city.id not in excluded_ids]

        # filter difficulty
        if difficulty_level:
            cities = [city for city in cities if city.difficulty_score < difficulty_level.max_difficulty_score]

        # filter locations
        if location_filter:
            regions = {r.lower() for r in location_filter.include_regions} if location_filter.include_regions else set()
            subregions = {s.lower() for s in location_filter.include_subregions} if location_filter.include_subregions else set()

            cities = [city for city in cities if (
                (regions and self._region(city).lower() in regions) or              # country is kept if there are region filters and its region is included
                (subregions and self._subregion(city).lower() in subregions) or     # country is kept if there are subregion filters and its region is included
                (not regions and not subregions)                        # country is kept if there was a location_filter with empty region and subregion sets
            )]

        if len(cities) == 0:
            return None

        if as_dict:
            cities_dict = {}
            for city in cities:
                cities_dict[city.id] = city

            return cities_dict
        else:
            return cities

    def load_capital_ids(self) -> dict[list[str]: list[str]]:
        capitals = self.load_all_capitals()
        capital_id_dict = {}

        for capital in capitals:
            capital_id_dict[capital.id] = capital.country_id

        return capital_id_dict

    def get_by_id(self, city_id: str) -> City | None:
        cities = self.load_all(as_dict=True)
        return cities.get(city_id)
        