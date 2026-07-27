from pydantic import BaseModel

class AnswerKey(BaseModel):
    correct_answer: str
    correct_answer_id: str | None = None
    correct_option_index: int | None = None
