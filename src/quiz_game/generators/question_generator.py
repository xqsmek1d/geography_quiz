import random

from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.repositories.repository_registry import RepositoryRegistry
from quiz_game.builders.question_builder_registry import QuestionBuilderRegistry
from quiz_game.config.enums import QuestionCategory
from quiz_game.pools.pool_factory_registry import PoolFactoryRegistry
from quiz_game.generators.answer_generator import AnswerGenerator
from quiz_game.models.answer_key import AnswerKey

class QuestionGenerator():
    def __init__(self, settings: QuizSettings, repositories: RepositoryRegistry, pool_factory_registry: PoolFactoryRegistry, builder_registry: QuestionBuilderRegistry, answer_generator: AnswerGenerator, rng: random.Random = None):

        self.rng = rng

        self.settings = settings
        self.repositories = repositories
        self.pool_factory_registry = pool_factory_registry
        self.answer_generator = answer_generator
        self.builder_registry = builder_registry

        self.question_pools = self.create_question_pools()
        
    def create_question_pools(self):

        question_pools = {}
        
        for category in self.settings.question_categories:
            
            factory = self.pool_factory_registry.get_factory(category.pool_type)
            question_pools[category] = factory.create(category, self.settings, self.repositories, self.rng)
        
        return question_pools

    def next_question(self) -> Question:

        # Pick a category of question based on available items in the category pools
        available_question_categories = [category for category, pool in self.question_pools.items() if not pool.is_empty()]

        if not available_question_categories:
            raise RuntimeError("ERROR: no questions remaining!")
        
        category = self.rng.choice(available_question_categories)

        selected_id = self.question_pools[category].get_next_id()

        return self.generate_question(category, selected_id)

    def generate_question(self, category: QuestionCategory, entity_id: str,) -> tuple[Question, AnswerKey]:
        builder = self.builder_registry.get_builder(category)

        question_data = builder.build(entity_id)

        return self.answer_generator.create(question_data)