import random

from quiz_game.config.loader import load_cli_settings
from quiz_game.cli.display import display_settings
from quiz_game.core.quiz_session import QuizSession
from quiz_game.cli.game_loop import GameLoop

from quiz_game.generators.distractor_generator import DistractorGenerator

from quiz_game.builders.builder_context import BuilderContext
from quiz_game.builders.country_capital_builder import CountryCapitalBuilder
from quiz_game.builders.capital_country_builder import CapitalCountryBuilder
from quiz_game.builders.flag_country_builder import FlagCountryBuilder
from quiz_game.builders.map_highlight_country_builder import MapHighlightCountryBuilder

from quiz_game.builders.question_builder_registry import QuestionBuilderRegistry

from quiz_game.pools.pool_factory_registry import PoolFactoryRegistry
from quiz_game.pools.country_pool_factory import CountryPoolFactory

from quiz_game.config.enums import QuestionCategory, PoolType

from quiz_game.repositories.repository_registry import RepositoryRegistry
from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository

from quiz_game.generators.answer_generator import AnswerGenerator
from quiz_game.generators.question_generator import QuestionGenerator

from quiz_game.services.answer_evaluator import AnswerEvaluator

def main():

    rng = random.Random()

    settings = load_cli_settings()

    display_settings(settings)

    country_repository = CountryRepository()
    city_repository = CityRepository()
    repositories = RepositoryRegistry(country_repository=country_repository, city_repository=city_repository)

    distractor_generator = DistractorGenerator(repositories=repositories, rng=rng)

    answer_generator = AnswerGenerator(
        answer_types=settings.answer_types,
        distractor_strategies=settings.distractor_strategies,
        distractor_generator=distractor_generator,
        rng=rng,
    )

    builder_context = BuilderContext(repositories=repositories)

    builder_registry = QuestionBuilderRegistry()
    
    builder_registry.register(QuestionCategory.COUNTRY_CAPITAL, CountryCapitalBuilder(builder_context))
    builder_registry.register(QuestionCategory.CAPITAL_COUNTRY, CapitalCountryBuilder(builder_context))
    builder_registry.register(QuestionCategory.FLAG_COUNTRY, FlagCountryBuilder(builder_context))
    builder_registry.register(QuestionCategory.MAP_HIGHLIGHT_COUNTRY, MapHighlightCountryBuilder(builder_context))

    pool_registry = PoolFactoryRegistry()
    pool_registry.register(PoolType.COUNTRY, CountryPoolFactory(),)
   
    question_generator = QuestionGenerator(
        settings=settings,
        repositories=repositories,
        pool_factory_registry=pool_registry,
        builder_registry=builder_registry,
        answer_generator=answer_generator,
        rng=rng)

    answer_evaluator = AnswerEvaluator()

    session = QuizSession(settings, question_generator=question_generator, answer_evaluator=answer_evaluator)

    game_loop = GameLoop(session)

    game_loop.run()

if __name__=="__main__":
    main()