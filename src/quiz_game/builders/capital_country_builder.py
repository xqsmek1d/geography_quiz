from quiz_game.models.question_data import QuestionData
from quiz_game.config.enums import QuestionCategory, PoolType

class CapitalCountryBuilder:

    def __init__(self, context):
        self.repositories = context.repositories

    def build(self, country_id: str) -> QuestionData:

        country = self.repositories.country.get_by_id(country_id)
        capital = self.repositories.city.get_by_id(country.capital_id)

        return QuestionData(
            category=QuestionCategory.CAPITAL_COUNTRY,
            answer_pool_type=PoolType.COUNTRY,
            prompt=f"What country is {capital.name} the capital of?",
            question_entity_id=capital.id,
            correct_answer=country.name,
            correct_answer_id=country.id,
            optional_prefix=country.optional_prefix,
            optional_suffix=country.optional_suffix,
            optional_names=country.optional_names or [],
            metadata={
                "capital_id": capital.id
            }
        )