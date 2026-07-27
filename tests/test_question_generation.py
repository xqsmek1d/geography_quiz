import random
import unittest

from quiz_game.config.enums import PoolType, QuestionCategory, AnswerType, DistractorStrategy

from quiz_game.models.settings import QuizSettings

from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository
from quiz_game.repositories.repository_registry import RepositoryRegistry

from quiz_game.builders.builder_context import BuilderContext
from quiz_game.builders.question_builder_registry import QuestionBuilderRegistry
from quiz_game.builders.country_capital_builder import CountryCapitalBuilder

from quiz_game.pools.pool_factory_registry import PoolFactoryRegistry
from quiz_game.pools.country_pool_factory import CountryPoolFactory

from quiz_game.generators.question_generator import QuestionGenerator
from quiz_game.generators.answer_generator import AnswerGenerator
from quiz_game.generators.distractor_generator import DistractorGenerator

class TestQuestionGeneration(unittest.TestCase):

    def setUp(self):
        """
        Create a fresh question generator before every test.
        """
        
        self.rng = random.Random(42)

        self.settings = QuizSettings(
            question_categories=[QuestionCategory.COUNTRY_CAPITAL,],
            answer_types=[AnswerType.MC,],
            distractor_strategies=[DistractorStrategy.RANDOM,],
        )

        # repositories
        self.repositories = RepositoryRegistry(country_repository=CountryRepository(),city_repository=CityRepository())

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

        builder_registry.register(QuestionCategory.COUNTRY_CAPITAL, CountryCapitalBuilder(builder_context),)

        # pools
        pool_registry = PoolFactoryRegistry()

        pool_registry.register(PoolType.COUNTRY, CountryPoolFactory(),)

        self.question_generator = QuestionGenerator(
            settings=self.settings,
            repositories=self.repositories,
            pool_factory_registry=pool_registry,
            builder_registry=builder_registry,
            answer_generator=answer_generator,
            rng=self.rng,
        )


    def test_generate_country_capital_multiple_choice(self):

        for _ in range(10):

            question, answer_key = self.question_generator.next_question()
            print("")
            print(f"- {question.prompt}")
            for idx, option in enumerate(question.options):
                print(f"{idx+1}. {option}")
            print(f"{answer_key.correct_answer} ({answer_key.correct_option_index+1}) is the answer")


            self.assertEqual(question.category, QuestionCategory.COUNTRY_CAPITAL,)

            self.assertEqual(question.answer_type, AnswerType.MC,)

            self.assertEqual(len(question.options), 4,)

            self.assertIn(answer_key.correct_answer, question.options,)

            self.assertEqual(question.options[answer_key.correct_option_index], answer_key.correct_answer,)


if __name__ == "__main__":
    unittest.main()