import os

from quiz_game.models.question_data import QuestionData
from quiz_game.config.enums import QuestionCategory, PoolType

from utils.paths import COUNTRY_FLAG_IMAGES_DIR

class FlagCountryBuilder:

    def __init__(self, context):
        self.repositories = context.repositories

    def build(self, country_id: str) -> QuestionData:

        country = self.repositories.country.get_by_id(country_id)

        return QuestionData(
            category=QuestionCategory.FLAG_COUNTRY,
            answer_pool_type=PoolType.COUNTRY,
            prompt=f"What country flag is shown here?",
            question_entity_id=country.id,
            correct_answer=country.name,
            correct_answer_id=country.id,
            optional_prefix=country.optional_prefix,
            optional_suffix=country.optional_suffix,
            optional_names=country.optional_names or [],
            image=os.path.join(COUNTRY_FLAG_IMAGES_DIR,country.image)
        )