import random
import unittest

from quiz_game.config.enums import PoolType, QuestionCategory, AnswerType, DistractorStrategy

from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.models.answer_key import AnswerKey

from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository
from quiz_game.repositories.repository_registry import RepositoryRegistry

from quiz_game.builders.builder_context import BuilderContext
from quiz_game.builders.question_builder_registry import QuestionBuilderRegistry
from quiz_game.builders.country_capital_builder import CountryCapitalBuilder
from quiz_game.builders.capital_country_builder import CapitalCountryBuilder
from quiz_game.builders.flag_country_builder import FlagCountryBuilder
from quiz_game.builders.map_highlight_country_builder import MapHighlightCountryBuilder

from quiz_game.pools.pool_factory_registry import PoolFactoryRegistry
from quiz_game.pools.country_pool_factory import CountryPoolFactory

from quiz_game.generators.question_generator import QuestionGenerator
from quiz_game.generators.answer_generator import AnswerGenerator
from quiz_game.generators.distractor_generator import DistractorGenerator

PRINT_QUESTIONS = True

class TestQuestionGeneration(unittest.TestCase):

    def setUp(self,):
        """
        Create a fresh question generator before every test.
        """
        
        self.rng = random.Random(42)

        # repositories
        self.repositories = RepositoryRegistry(country_repository=CountryRepository(),city_repository=CityRepository())

    def create_question_generator(self,question_categories: list[QuestionCategory]) -> QuestionGenerator:
        self.settings = QuizSettings(
            question_categories=question_categories,
            answer_types=[AnswerType.MC,],
            distractor_strategies=[DistractorStrategy.RANDOM,],
        )

        # distractors
        distractor_generator = DistractorGenerator(repositories=self.repositories, rng=self.rng)

        # answers
        answer_generator = AnswerGenerator(
            answer_types=self.settings.answer_types,
            distractor_strategies=self.settings.distractor_strategies,
            distractor_generator=distractor_generator,
            rng=self.rng,)

        # builders
        builder_context = BuilderContext(repositories=self.repositories,)

        builder_registry = QuestionBuilderRegistry()
        
        if QuestionCategory.COUNTRY_CAPITAL in question_categories:
            builder_registry.register(QuestionCategory.COUNTRY_CAPITAL, CountryCapitalBuilder(builder_context),)
        if QuestionCategory.CAPITAL_COUNTRY in question_categories:
            builder_registry.register(QuestionCategory.CAPITAL_COUNTRY, CapitalCountryBuilder(builder_context),)
        if QuestionCategory.FLAG_COUNTRY in question_categories:
            builder_registry.register(QuestionCategory.FLAG_COUNTRY, FlagCountryBuilder(builder_context),)
        if QuestionCategory.MAP_HIGHLIGHT_COUNTRY in question_categories:
            builder_registry.register(QuestionCategory.MAP_HIGHLIGHT_COUNTRY, MapHighlightCountryBuilder(builder_context))

        # pools
        pool_registry = PoolFactoryRegistry()

        pool_registry.register(PoolType.COUNTRY, CountryPoolFactory(),)

        return QuestionGenerator(
            settings=self.settings,
            repositories=self.repositories,
            pool_factory_registry=pool_registry,
            builder_registry=builder_registry,
            answer_generator=answer_generator,
            rng=self.rng,
        )

    def assert_valid_mc_question(self, question: Question, answer_key: AnswerKey, expected_category: QuestionCategory,):
        
        self.assertEqual(question.category, expected_category,)

        self.assertEqual(question.answer_type, AnswerType.MC,)

        self.assertEqual(len(question.options), 4,)

        self.assertIn(answer_key.correct_answer, question.options,)

        self.assertEqual(question.options[answer_key.correct_option_index], answer_key.correct_answer,)

    def test_generate_country_capital_multiple_choice(self):
        if PRINT_QUESTIONS:
            print("\n===== TESTING COUNTRY -> CAPITAL MC QUESTION GENERATION =====")
        question_generator = self.create_question_generator([QuestionCategory.COUNTRY_CAPITAL])

        for i in range(1):

            question, answer_key = question_generator.next_question()
            if PRINT_QUESTIONS:
                print(f"Q-{i+1}: {question.prompt}")
                for idx, option in enumerate(question.options):
                    print(f"   {idx+1}. {option}")
                print(f"\nA: {answer_key.correct_answer} ({answer_key.correct_option_index+1})")
                print(f"-----------------------------------------------")
            self.assert_valid_mc_question(question=question, answer_key=answer_key, expected_category=QuestionCategory.COUNTRY_CAPITAL)

    def test_generate_capital_country_multiple_choice(self):
        if PRINT_QUESTIONS:
            print("\n===== TESTING CAPITAL -> COUNTRY MC QUESTION GENERATION =====")
        question_generator = self.create_question_generator([QuestionCategory.CAPITAL_COUNTRY])

        for i in range(1):

            question, answer_key = question_generator.next_question()
            if PRINT_QUESTIONS:
                print(f"Q-{i+1}: {question.prompt}")
                for idx, option in enumerate(question.options):
                    print(f"   {idx+1}. {option}")
                print(f"\nA: {answer_key.correct_answer} ({answer_key.correct_option_index+1})")
                print(f"-----------------------------------------------")
            self.assert_valid_mc_question(question=question, answer_key=answer_key, expected_category=QuestionCategory.CAPITAL_COUNTRY)

    def test_generate_flag_country_multiple_choice(self):
        if PRINT_QUESTIONS:
            print("\n===== TESTING FLAG -> COUNTRY MC QUESTION GENERATION =====")
        question_generator = self.create_question_generator([QuestionCategory.FLAG_COUNTRY])

        for i in range(1):

            question, answer_key = question_generator.next_question()
            if PRINT_QUESTIONS:
                print(f"Q-{i+1}: {question.prompt}, with image: ...{"/".join(question.image.split("/")[-3:])}")
                for idx, option in enumerate(question.options):
                    print(f"   {idx+1}. {option}")
                print(f"\nA: {answer_key.correct_answer} ({answer_key.correct_option_index+1})")
                print(f"-----------------------------------------------")
            self.assert_valid_mc_question(question=question, answer_key=answer_key, expected_category=QuestionCategory.FLAG_COUNTRY) 

    def test_generate_map_highlight_country_multiple_choice(self):
        if PRINT_QUESTIONS:
            print("\n===== TESTING MAP HIGHLIGHT -> COUNTRY MC QUESTION GENERATION =====")
        question_generator = self.create_question_generator([QuestionCategory.MAP_HIGHLIGHT_COUNTRY])

        for i in range(10):

            question, answer_key = question_generator.next_question()
            if PRINT_QUESTIONS:
                print(f"Q-{i+1}: {question.prompt}, with image: ...{"/".join(question.image.split("/")[-3:])}")
                for idx, option in enumerate(question.options):
                    print(f"   {idx+1}. {option}")
                print(f"\nA: {answer_key.correct_answer} ({answer_key.correct_option_index+1})")
                print(f"-----------------------------------------------")
            self.assert_valid_mc_question(question=question, answer_key=answer_key, expected_category=QuestionCategory.MAP_HIGHLIGHT_COUNTRY) 


if __name__ == "__main__":
    unittest.main()