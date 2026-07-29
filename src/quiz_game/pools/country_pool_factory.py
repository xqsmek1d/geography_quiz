from quiz_game.services.question_pool import QuestionPool

class CountryPoolFactory:

    def create(self, category, settings, repositories, rng):

        countries = repositories.country.load_with_filters(
            difficulty_level=settings.difficulty_level,
            location_filter=settings.location_filter,
            excluded_ids=category.excluded_ids,
            as_dict=True,
        )

        if not countries:
            raise RuntimeError(f"ERROR: no countries available for category {category}")

        return QuestionPool(list(countries.keys()), rng_engine=rng, infinite_mode=settings.gameplay.infinite_mode)