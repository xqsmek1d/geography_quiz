from quiz_game.models.answer_result import AnswerResult
from quiz_game.models.game_state import GameState

class StateManager():
    def __init__(self):
        print("\nSTATE MANAGER INITIATED")

    def update(self, game_state: GameState, result: AnswerResult):
        print("\nSTATE MANAGER SHOULD UPDATE THE GAME STATE")