from pydantic import BaseModel, Field
from quiz_game.config.enums import MatchType

class AnswerResult:
    submitted_answer = str
    correct: bool
    match_type: MatchType