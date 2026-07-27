import json
from pathlib import Path
from typing import Any

from quiz_game.models.country import Country
from quiz_game.models.settings import LocationFilter
from quiz_game.config.enums import DifficultyLevel
from utils.paths import COUNTRIES_JSON

class CountryRepository:
    def __init__(self, path: Path = COUNTRIES_JSON):
        self.path = path
        self._countries = None
    
    def load_all(self, as_dict=False):

        if self._countries is None:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)

            self._countries = [Country(**country) for country in data]

        if as_dict:
            return {country.id: country for country in self._countries}

        return self._countries.copy()


    def get_images(self) -> set[str]:
        return set([country.image for country in self._countries])

    def load_with_filters(
        self,
        difficulty_level: DifficultyLevel | None = None,
        location_filter: LocationFilter | None = None,
        excluded_ids: list[str] | None = None,
        as_dict: bool = False,
        ) -> list[Country] | None | dict[str, Country]:

        countries = self.load_all()

        # filter exclusions
        if excluded_ids:
            countries = [country for country in countries if country.id not in excluded_ids]

        # filter difficulty
        if difficulty_level:
            countries = [country for country in countries if country.difficulty_score < difficulty_level.value]

        # filter locations
        if location_filter:
            regions = {r.lower() for r in location_filter.include_regions} if location_filter.include_regions else set()
            subregions = {s.lower() for s in location_filter.include_subregions} if location_filter.include_subregions else set()

            countries = [country for country in countries if (
                (regions and country.region.lower() in regions) or              # country is kept if there are region filters and its region is included
                (subregions and country.subregion.lower() in subregions) or     # country is kept if there are subregion filters and its region is included
                (not regions and not subregions)                        # country is kept if there was a location_filter with empty region and subregion sets
            )]
        
        if len(countries) == 0:
            return None

        if as_dict:
            countries_dict = {}
            for country in countries:
                countries_dict[country.id] = country

            return countries_dict
        else:
            return countries
    
    def get_fips_to_iso3(self) -> dict[str, str]:
        countries = self.load_all()
        fips_to_iso3_dict = {}
        for country in countries:
            if country.fips and country.fips != "#N/A":
                fips_to_iso3_dict[country.fips] = country.id

        return fips_to_iso3_dict

    def get_by_id(self, country_id: str) -> Country | None:
        countries = self.load_all(as_dict=True)
        return countries.get(country_id)