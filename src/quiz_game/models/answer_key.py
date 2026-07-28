from pydantic import BaseModel
from quiz_game.config.enums import PoolType

class AnswerKey(BaseModel):
    correct_answer: str
    accepted_answers: list[str]

    correct_answer_id: str | None = None
    correct_option_index: int | None = None

    answer_pool_type: PoolType
    
