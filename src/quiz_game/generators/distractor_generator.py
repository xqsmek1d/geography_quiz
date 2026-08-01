import random

from quiz_game.config.enums import DistractorStrategy, PoolType
from quiz_game.models.settings import QuizSettings

class DistractorGenerator:

    def __init__(self, settings: QuizSettings, repositories, rng: random.Random):
        
        self.settings = settings
        self.repositories = repositories
        self.rng = rng

    def _load_entities(self, pool_type: PoolType):

        match pool_type:
            case PoolType.COUNTRY:
                return self.repositories.country.load_with_filters(
                    difficulty_level=self.settings.difficulty_level,
                )
                #return self.repositories.country.load_all()

            case PoolType.CAPITAL:
                return self.repositories.city.load_all_capitals(
                    difficulty_level=self.settings.difficulty_level,
                )
                #return self.repositories.city.load_all_capitals()

            case _:
                raise NotImplementedError
    
    def _fill_distractors(self, selected_candidates, num_distractors, excluded_ids, fallback_function,):
        
        if len(selected_candidates) >= num_distractors:
            return selected_candidates

        remaining = num_distractors - len(selected_candidates)
        
        new_excluded_ids = excluded_ids | {entity.id for entity in selected_candidates}
        extra = fallback_function(remaining, new_excluded_ids,)

        return selected_candidates + extra

    def _get_country_attribute(self,entity_id,pool_type,attribute,):
        
        match pool_type:

            case PoolType.COUNTRY:
                country = self.repositories.country.get_by_id(entity_id)
                return getattr(country, attribute)
            
            case PoolType.CAPITAL:
                capital = self.repositories.city.get_by_id(entity_id)
                country = self.repositories.country.get_by_id(capital.country_id)
                return getattr(country, attribute)

            case _:
                raise NotImplementedError

    def _sample(self, candidates, amount):
        return self.rng.sample(candidates, min(amount, len(candidates)))

    def _country_ids_with_attribute(self, attribute: str, value,):
        countries = self.repositories.country.load_all(as_dict=True)
        return {country.id for country in countries.values() if getattr(country, attribute) == value}

    def generate(self, correct_answer_id: str, distractor_strategy: DistractorStrategy, answer_pool_type: PoolType, num_distractors: int = 3,) -> list[str]:

        excluded_ids = {correct_answer_id}

        match distractor_strategy:
            case DistractorStrategy.RANDOM:
                distractor_entities = self.random_distractors(answer_pool_type, num_distractors, excluded_ids)

            case DistractorStrategy.SAME_REGION:
                distractor_entities = self.same_region_distractors(correct_answer_id, answer_pool_type, num_distractors, excluded_ids)

            case DistractorStrategy.SAME_SUBREGION:
                distractor_entities = self.same_subregion_distractors(correct_answer_id, answer_pool_type, num_distractors, excluded_ids)
            
            case _:
                raise NotImplementedError

        return [entity.name for entity in distractor_entities]

    def random_distractors(self, answer_pool_type: PoolType, num_distractors: int, excluded_ids: set[str] | None = None) -> list:

        excluded_ids = excluded_ids or set()

        entities = self._load_entities(answer_pool_type)
        
        candidates = [entity for entity in entities if (entity.id not in excluded_ids)]
        
        selected_candidates = self._sample(candidates, num_distractors)

        if len(selected_candidates) < num_distractors:
            raise RuntimeError(f"Could only generate {len(selected_candidates)} of {num_distractors} required distractors.")
        else:
            return selected_candidates

    def same_region_distractors(self,correct_answer_id: str, answer_pool_type: PoolType, num_distractors: int, excluded_ids: set[str] | None = None) -> list:

        excluded_ids = excluded_ids or set()
        answer_region = self._get_country_attribute(correct_answer_id, answer_pool_type, "region",)

        match answer_pool_type:

            case PoolType.COUNTRY:
                countries = self._load_entities(answer_pool_type)
                candidates = [country for country in countries if (country.region == answer_region and country.id not in excluded_ids)]

            case PoolType.CAPITAL:
                capitals = self.repositories.city.load_all_capitals(as_dict = True, difficulty_level=self.settings.difficulty_level)
                countries = self.repositories.country.load_with_filters(as_dict = True, difficulty_level=self.settings.difficulty_level)
                
                country_id_candidates = self._country_ids_with_attribute("region", answer_region,)
                candidates = [capital for capital in capitals.values() if (capital.country_id in country_id_candidates and capital.id not in excluded_ids)]

            case _:
                raise NotImplementedError

        selected_candidates = self._sample(candidates, num_distractors)

        return self._fill_distractors(
            selected_candidates,
            num_distractors,
            excluded_ids,
            lambda amount, ids:
                self.random_distractors(
                    answer_pool_type,
                    amount,
                    ids,
                ),
        )

    def same_subregion_distractors(self,correct_answer_id: str, answer_pool_type: PoolType, num_distractors: int, excluded_ids: set[str] | None = None) -> list:

        excluded_ids = excluded_ids or set()
        answer_subregion = self._get_country_attribute(correct_answer_id, answer_pool_type, "subregion",)

        match answer_pool_type:

            case PoolType.COUNTRY:
                countries = self._load_entities(answer_pool_type)
                candidates = [country for country in countries if (country.subregion == answer_subregion and country.id not in excluded_ids)]

            case PoolType.CAPITAL:
                capitals = self.repositories.city.load_all_capitals(as_dict = True, difficulty_level=self.settings.difficulty_level)
                countries = self.repositories.country.load_with_filters(as_dict = True, difficulty_level=self.settings.difficulty_level)
                
                country_id_candidates = self._country_ids_with_attribute("subregion", answer_subregion,)
                candidates = [capital for capital in capitals.values() if (capital.country_id in country_id_candidates and capital.id not in excluded_ids)]

            case _:
                raise NotImplementedError

        selected_candidates = self._sample(candidates, num_distractors)

        return self._fill_distractors(
            selected_candidates,
            num_distractors,
            excluded_ids,
            lambda amount, ids:
                self.same_region_distractors(
                    correct_answer_id,
                    answer_pool_type,
                    amount,
                    ids,
                ),
        )