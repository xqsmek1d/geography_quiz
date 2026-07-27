from quiz_game.config.enums import DistractorStrategy, PoolType

class DistractorGenerator:

    def __init__(self, repositories, rng):
        self.repositories = repositories
        self.rng = rng

    def generate(self, correct_answer_id: str, distractor_strategy: DistractorStrategy, answer_pool_type: PoolType, num_distractors: int = 3,) -> list[str]:
        
        match distractor_strategy:
            case DistractorStrategy.RANDOM:
                return self.random_distractors(correct_answer_id, answer_pool_type, num_distractors,)
            
            case _:
                raise NotImplementedError

    def random_distractors(self,correct_answer_id: str, answer_pool_type: PoolType, num_distractors: int) -> list[str]:
    
        match answer_pool_type:

            case PoolType.COUNTRY:
                entities = self.repositories.country.load_all()

            case PoolType.CAPITAL:
                entities = self.repositories.city.load_all_capitals()

            case PoolType.CITY:
                entities = self.repositories.city.load_all()

            case PoolType.LANDMARK:
                entities = self.repositories.landmark.load_all()

            case _:
                raise NotImplementedError
        
        candidates = [entity for entity in entities if entity.id != correct_answer_id]
        selected_candidates = self.rng.sample(candidates,num_distractors,)

        return [entity.name for entity in selected_candidates]
