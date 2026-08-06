from pydantic import BaseModel, Field
from quiz_game.config.enums import MatchType

class AnswerResult(BaseModel):
    submitted_answer: str | None
    is_correct: bool
    correct_answer: str
    match_type: MatchType
    score: float | None = None