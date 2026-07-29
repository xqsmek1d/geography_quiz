from pydantic import BaseModel, Field
from quiz_game.config.enums import QuestionCategory, AnswerType, PoolType

class Question(BaseModel): 
    category: QuestionCategory
    answer_type: AnswerType

    prompt: str

    question_entity_id: str

    question_id: str | None = None

    options: list[str] = Field(default_factory=list)

    image: str | None = None

    metadata: dict[str, str | int | float] = Field(default_factory=dict)