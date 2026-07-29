from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.models.game_state import GameState
from quiz_game.models.answer_key import AnswerKey
from quiz_game.models.answer_result import AnswerResult

from quiz_game.generators.question_generator import QuestionGenerator
from quiz_game.services.answer_evaluator import AnswerEvaluator
from quiz_game.services.state_manager import StateManager

class QuizSession: 
    """
    Controls the flow of a quiz.
    """
    def __init__(
        self,
        settings: QuizSettings,
        question_generator: QuestionGenerator,
        answer_evaluator: AnswerEvaluator,
    ):

        self.settings = settings
        self.question_generator = question_generator

        self.state = GameState()
        self._current_question: Question | None = None
        self._current_answer_key: AnswerKey | None = None

        self.answer_evaluator = answer_evaluator
        self.state_manager = StateManager()

    def get_current_question(self) -> Question | None:
        return self._current_question

    def next_question(self) -> Question:
        """
        Generate and return the next question.
        """
        if not self.has_questions():
            raise RuntimeError("ERROR: no questions remaining!")

        question, answer_key = self.question_generator.next_question()

        self._current_question = question
        self._current_answer_key = answer_key

        self.state.questions_asked += 1

        return question
    
    def submit_answer(self, answer: str) -> AnswerResult:
        """
        Evaluate the current answer and update the game state.
        """

        if self._current_question is None or self._current_answer_key is None:
            raise RuntimeError("ERROR: no active question or answer key!")

        result = self.answer_evaluator.evaluate(self._current_answer_key, answer,)

        if not result.is_correct and self.settings.gameplay.question_recycling:
            self.question_generator.recycle_question(self._current_question.category, self._current_question.question_entity_id)

        self.state_manager.update(self.state,result)

        self._current_question = None
        self._current_answer_key = None

        return result

    def has_questions(self) -> bool:
        return self.question_generator.has_questions()

    def is_finished(self) -> bool:
        return self.state.game_over or not self.has_questions()