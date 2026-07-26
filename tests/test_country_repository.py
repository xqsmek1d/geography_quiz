import json
from pathlib import Path

import unittest

from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.models.settings import LocationFilter
from quiz_game.config.enums import DifficultyLevel
from utils.paths import TESTS_DIR, TEST_DATA_DIR, TEST_DATA_COUNTRIES_JSON

country_repository = CountryRepository(TEST_DATA_COUNTRIES_JSON)
print_difficulty_countries = False

class TestLoadWithFilter(unittest.TestCase):

    def test_base(self):
        self.assertEqual(country_repository.load_with_filters(), country_repository.load_all())

    def test_easy_difficulty_filter(self):
        countries = country_repository.load_with_filters(difficulty_level=DifficultyLevel.EASY)
        for country in countries:
            if print_difficulty_countries:
                print(f"Easy country: {country.name}, score: {country.difficulty_score}")
            self.assertEqual(True, country.difficulty_score < DifficultyLevel.EASY.value)

    def test_normal_difficulty_filter(self):
        countries = country_repository.load_with_filters(difficulty_level=DifficultyLevel.NORMAL)
        for country in countries:
            if country.difficulty_score > DifficultyLevel.EASY.value and print_difficulty_countries:
                print(f"Normal country: {country.name}, score: {country.difficulty_score}")
            self.assertEqual(True, country.difficulty_score < DifficultyLevel.NORMAL.value)

    def test_hard_difficulty_filter(self):
        countries = country_repository.load_with_filters(difficulty_level=DifficultyLevel.HARD)
        for country in countries:
            if country.difficulty_score > DifficultyLevel.NORMAL.value and print_difficulty_countries:
                print(f"Hard country: {country.name}, score: {country.difficulty_score}")
            self.assertEqual(True, country.difficulty_score < DifficultyLevel.HARD.value)

    def test_wizard_difficulty_filter(self):
        countries = country_repository.load_with_filters(difficulty_level=DifficultyLevel.WIZARD)
        for country in countries:
            if country.difficulty_score > DifficultyLevel.HARD.value and print_difficulty_countries:
                print(f"Wizard country: {country.name}, score: {country.difficulty_score}")
            self.assertEqual(True, country.difficulty_score < DifficultyLevel.WIZARD.value)

    def test_region_filter(self):
        regions = ["Europe",]
        location_filter = LocationFilter(
            include_regions = regions
        )
        countries = country_repository.load_with_filters(location_filter=location_filter)
        for country in countries:
            self.assertEqual(True, country.region in regions)

    def test_empty_region_filter(self):
        regions = []
        location_filter = LocationFilter(
            include_regions = regions
        )
        self.assertEqual(country_repository.load_with_filters(location_filter=location_filter), country_repository.load_all())

    def test_region_subregion_filter(self):
        regions = ["Asia",]
        subregions = ["North America",]
        location_filter = LocationFilter(
            include_regions = regions,
            include_subregions = subregions,
        )
        countries = country_repository.load_with_filters(location_filter=location_filter)
        for country in countries:
            self.assertEqual(True, (country.region in regions) or (country.subregion in subregions))

    def test_all_filters(self):
        regions = ["Other","OCEANIA","MadeUpContinent"]
        subregions = ["South-East Asia","west europe"]
        location_filter = LocationFilter(
            include_regions = regions,
            include_subregions = subregions,
        )
        countries = country_repository.load_with_filters(difficulty_level=DifficultyLevel.NORMAL,location_filter=location_filter)
        regions = {r.lower() for r in regions}
        subregions = {s.lower() for s in subregions}
        for country in countries:
            self.assertEqual(True, ((country.region.lower() in regions) or (country.subregion.lower() in subregions)) and country.difficulty_score < DifficultyLevel.NORMAL.value)

if __name__=="__main__":
    unittest.main()