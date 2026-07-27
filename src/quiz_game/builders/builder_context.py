from quiz_game.repositories.repository_registry import RepositoryRegistry
from quiz_game.generators.answer_generator import AnswerGenerator


class BuilderContext:

    def __init__(self, repositories: RepositoryRegistry):

        self.repositories = repositories