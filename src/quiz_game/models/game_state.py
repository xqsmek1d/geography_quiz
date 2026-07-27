from pydantic import BaseModel


class GameState(BaseModel):
    score: int = 0

    questions_asked: int = 0
    questions_correct: int = 0
    questions_incorrect: int = 0

    remaining_lives: int | None = None

    elapsed_time: float = 0.0

    game_over: bool = False