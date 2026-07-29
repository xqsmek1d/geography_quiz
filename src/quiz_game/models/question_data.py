from pydantic import BaseModel, Field
from quiz_game.config.enums import QuestionCategory
from quiz_game.config.enums import AnswerType

from quiz_game.config.enums import PoolType

class QuestionData(BaseModel): 
    question_id: str | None = None

    category: QuestionCategory
    answer_pool_type: PoolType
    
    prompt: str

    question_entity_id: str

    correct_answer: str
    correct_answer_id: str | None = None
    optional_prefix: str | None = None
    optional_suffix: str | None = None
    optional_names: list[str] = Field(default_factory=list)

    options: list[str] = Field(default_factory=list)
    correct_option_index: int | None = None

    image: str | None = None

    metadata: dict[str, str | int | float] = Field(default_factory=dict)