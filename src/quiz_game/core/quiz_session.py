from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.models.game_state import GameState
from quiz_game.models.answer_result import AnswerResult

from quiz_game.generators.question_generator import QuestionGenerator
from quiz_game.services.services.answer_checker import AnswerChecker
from quiz_game.services.services.state_manager import StateManager

from quiz_game.repositories.country_repository import CountryRepository

class QuizSession: 
    """
    Controls the flow of a quiz.
    """
    def __init__(
        self,
        settings: QuizSettings,
    ):

        self.settings = settings
        self.question_generator = QuestionGenerator(settings, country_repository=CountryRepository())

        self.state = GameState()
        self.__current_question: Question | None = None

        self.answer_checker = AnswerChecker()
        self.state_manager = StateManager()

    def get_current_question(self) -> Question | None:
        return self.__current_question

    def next_question(self):
        """
        Generate and return the next question.
        """
        question = self.generator.next_question()

        self.__current_question = question

        self.state.questions_asked += 1

        return question
    
    def submit_answer(self, answer: str) -> AnswerResult:
        """
        Evaluate the current answer and update the game state.
        """

        if self.__current_question is None:
            raise RuntimeError("ERROR: no active question!")

        result = self.answer_checker.check(self.__current_question,answer,)

        self.state_manager.update(self.state,result)

        self.__current_question = None

        return result

    def has_questions(self):
        return self.generator.has_questions()

    def is_finished(self):
        return self.state.game_over or not self.has_questions()