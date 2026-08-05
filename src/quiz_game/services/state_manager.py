from quiz_game.models.answer_result import AnswerResult
from quiz_game.models.game_state import GameState
from quiz_game.models.settings import QuizSettings

class StateManager():
    """
    Manages changes to the current game state.
    """

    def __init__(self, settings: QuizSettings,):
        
        self.gameplay_settings = settings.gameplay
        self._state = GameState(remaining_lives = settings.gameplay.lives)

    @property
    def state(self) -> GameState:
        return self._state

    def _remove_life(self) -> None:
        """
        Remove one life when the game uses limited lives.
        """
        if self._state.remaining_lives is None:
            return

        self._state.remaining_lives -= 1

        if self._state.remaining_lives <= 0:
            self._state.remaining_lives = 0
            self._state.game_over = True

    def _check_question_limit(self) -> None:
        """
        End the game when the configured question limit is reached.
        """
        if self.gameplay_settings.infinite_mode:
            return

        if (self._state.questions_asked >= self.gameplay_settings.num_questions):
            self._state.game_over = True

    def record_answer(self, answer: AnswerResult) -> None:
        """
        Update the game state using an answer result.
        """
        if answer.is_correct:
            self._state.questions_correct += 1
            self._state.score += 1 # self._state.score += answer.score
        else:  
            self._state.questions_incorrect += 1
            # self._state.score += answer.score
            self._remove_life()

        self._check_question_limit()

    def record_question_asked(self) -> None:
        """
        Record that a new question has been presented.
        """
        self._state.questions_asked += 1