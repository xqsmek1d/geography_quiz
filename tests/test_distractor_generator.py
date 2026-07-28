import unittest
import random

from quiz_game.config.enums import DistractorStrategy, PoolType
from quiz_game.generators.distractor_generator import DistractorGenerator
from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository
from quiz_game.repositories.repository_registry import RepositoryRegistry

PRINT_OPTIONS = True

class TestDistractorGenerator(unittest.TestCase):

    def setUp(self):

        self.rng = random.Random(42)
        self.repositories = RepositoryRegistry(country_repository=CountryRepository(), city_repository=CityRepository(),)
        self.generator = DistractorGenerator(repositories=self.repositories, rng=self.rng,)


    def test_random_country_distractors(self):

        if PRINT_OPTIONS:
            print(f"===== TEST RANDOM COUNTRY DISTRACTORS =====")

        correct_answer = "NLD"

        country = self.repositories.country.get_by_id(correct_answer)

        distractors = self.generator.generate(
            correct_answer_id=correct_answer,
            distractor_strategy=DistractorStrategy.RANDOM,
            answer_pool_type=PoolType.COUNTRY,
            num_distractors=3,
        )

        if PRINT_OPTIONS:
            print(f"Input country answer id: {correct_answer}")
            print(f"Correct option: {country.name}")
            for idx, distractor in enumerate(distractors):
                print(f"Distractor {idx + 1}: {distractor}")

        self.assertEqual(len(distractors), 3)
        self.assertNotIn(self.repositories.country.get_by_id(correct_answer).name, distractors,)


    def test_same_region_country_distractors(self):
        
        if PRINT_OPTIONS:
            print(f"\n===== TEST SAME REGION COUNTRY DISTRACTORS =====")

        correct_answer = "NLD"

        country = self.repositories.country.get_by_id(correct_answer)

        distractors = self.generator.generate(
            correct_answer_id=correct_answer,
            distractor_strategy=DistractorStrategy.SAME_REGION,
            answer_pool_type=PoolType.COUNTRY,
            num_distractors=3,
        )

        if PRINT_OPTIONS:
            print(f"Input country answer id: {correct_answer}")
            print(f"Correct option: {country.name}")
            for idx, distractor in enumerate(distractors):
                print(f"Distractor {idx + 1}: {distractor}")
        

        self.assertEqual(len(distractors), 3)

        for distractor in distractors:

            country_match = next(
                c for c in self.repositories.country.load_all()
                if c.name == distractor
            )

            self.assertEqual(country_match.region, country.region,)
            self.assertNotEqual(country_match.id, correct_answer,)

    def test_same_subregion_country_distractors(self):

        if PRINT_OPTIONS:
            print(f"\n===== TEST SAME SUBREGION COUNTRY DISTRACTORS =====")

        correct_answer = "NLD"

        country = self.repositories.country.get_by_id(correct_answer)

        distractors = self.generator.generate(
            correct_answer_id=correct_answer,
            distractor_strategy=DistractorStrategy.SAME_SUBREGION,
            answer_pool_type=PoolType.COUNTRY,
            num_distractors=3,
        )

        if PRINT_OPTIONS:
            print(f"Input country answer id: {correct_answer}")
            print(f"Correct option: {country.name}")
            for idx, distractor in enumerate(distractors):
                print(f"Distractor {idx + 1}: {distractor}")

        self.assertEqual(len(distractors), 3)

        for distractor in distractors:

            country_match = next(
                c for c in self.repositories.country.load_all()
                if c.name == distractor
            )

            self.assertEqual(country_match.subregion, country.subregion,)
            self.assertNotEqual(country_match.id, correct_answer,)


    def test_same_region_capital_distractors(self):

        if PRINT_OPTIONS:
            print(f"\n===== TEST SAME REGION CAPITAL DISTRACTORS =====")

        correct_answer = "NLD_AMSTERDAM"

        capital = self.repositories.city.get_by_id(correct_answer)

        distractors = self.generator.generate(
            correct_answer_id=correct_answer,
            distractor_strategy=DistractorStrategy.SAME_REGION,
            answer_pool_type=PoolType.CAPITAL,
            num_distractors=3,
        )

        if PRINT_OPTIONS:
            print(f"Input capital answer id: {correct_answer}")
            print(f"Correct option: {capital.name}")
            for idx, distractor in enumerate(distractors):
                print(f"Distractor {idx + 1}: {distractor}")

        self.assertEqual(len(distractors), 3)

        for distractor in distractors:

            capital_match = next(
                c for c in self.repositories.city.load_all_capitals()
                if c.name == distractor
            )

            country = self.repositories.country.get_by_id(capital_match.country_id)
            original_country = self.repositories.country.get_by_id(capital.country_id)

            self.assertEqual(country.region, original_country.region,)


    def test_same_subregion_capital_distractors(self):

        if PRINT_OPTIONS:
            print(f"\n===== TEST SAME SUBREGION CAPITAL DISTRACTORS =====")

        correct_answer = "NLD_AMSTERDAM"

        capital = self.repositories.city.get_by_id(correct_answer)

        original_country = self.repositories.country.get_by_id(capital.country_id)

        distractors = self.generator.generate(
            correct_answer_id=correct_answer,
            distractor_strategy=DistractorStrategy.SAME_SUBREGION,
            answer_pool_type=PoolType.CAPITAL,
            num_distractors=3,
        )

        if PRINT_OPTIONS:
            print(f"Input capital answer id: {correct_answer}")
            print(f"Correct option: {capital.name}")
            for idx, distractor in enumerate(distractors):
                print(f"Distractor {idx + 1}: {distractor}")

        self.assertEqual(len(distractors), 3)

        for distractor in distractors:

            capital_match = next(
                c for c in self.repositories.city.load_all_capitals()
                if c.name == distractor
            )

            country = self.repositories.country.get_by_id(capital_match.country_id)
            self.assertEqual(country.subregion, original_country.subregion,)


if __name__ == "__main__":
    unittest.main()