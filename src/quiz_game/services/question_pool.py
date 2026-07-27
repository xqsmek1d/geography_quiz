import random

from quiz_game.config.constants import RECYCLE_MIN_DISTANCE, RECYCLE_MAX_DISTANCE

class QuestionPool:
    
    def __init__(self, values: list[str], rng_engine: random.Random):
        self.rng = rng_engine
        
        self.remaining = values.copy()
        self.used = []

        self.rng.shuffle(self.remaining)

    def get_next_id(self) -> str | None:
        if not self.remaining:
            return None
        
        value = self.remaining.pop()
        self.used.append(value)

        return value

    def recycle(self, value: str):
        # Insert between the 3rd and the 6th upcoming position
        distance = random.randint(RECYCLE_MIN_DISTANCE, RECYCLE_MAX_DISTANCE)

        index = min(distance - 1, len(self.remaining))

        self.remaining.insert(index, value)

    def reset(self):

        if not self.is_empty():
            return False

        self.remaining = self.used.copy()
        self.used.clear()

        self.rng.shuffle(self.remaining)

        return True

    def is_empty(self) -> bool:
        return len(self.remaining) == 0 