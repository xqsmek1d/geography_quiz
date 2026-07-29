import os

from quiz_game.models.question_data import QuestionData
from quiz_game.config.enums import QuestionCategory, PoolType

from utils.paths import COUNTRY_HIGHLIGHT_IMAGES_DIR

class MapHighlightCountryBuilder:

    def __init__(self, context):
        self.repositories = context.repositories

    def build(self, country_id: str) -> QuestionData:

        country = self.repositories.country.get_by_id(country_id)

        return QuestionData(
            category=QuestionCategory.MAP_HIGHLIGHT_COUNTRY,
            answer_pool_type=PoolType.COUNTRY,
            prompt=f"What country is shown here?",
            question_entity_id=country.id,
            correct_answer=country.name,
            correct_answer_id=country.id,
            optional_prefix=country.optional_prefix,
            optional_suffix=country.optional_suffix,
            optional_names=country.optional_names or [],
            image=os.path.join(COUNTRY_HIGHLIGHT_IMAGES_DIR,country.image)
        )