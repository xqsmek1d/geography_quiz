from quiz_game.models.question_data import QuestionData
from quiz_game.config.enums import QuestionCategory, PoolType

class CountryCapitalBuilder:

    def __init__(self, context):
        self.repositories = context.repositories

    def build(self, country_id: str) -> QuestionData:

        country = self.repositories.country.get_by_id(country_id)
        capital = self.repositories.city.get_by_id(country.capital_id)

        return QuestionData(
            category=QuestionCategory.COUNTRY_CAPITAL,
            answer_pool_type=PoolType.CAPITAL,
            prompt=f"What is the capital of {country.name}?",
            correct_answer=capital.name,
            correct_answer_id=capital.id,
            metadata={
                "country_id": country.id
            }
        )