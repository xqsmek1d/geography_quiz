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
            correct_answer=country.name,
            correct_answer_id=country.id,
            image=os.path.join(COUNTRY_HIGHLIGHT_IMAGES_DIR,country.image)
        )