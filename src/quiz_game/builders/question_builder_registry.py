class QuestionBuilderRegistry:
    def __init__(self):
        self._builders = {}

    def register(self, category, builder):
        self._builders[category] = builder

    def get_builder(self, category):
        if category not in self._builders:
            raise ValueError(f"ERROR: no builder registered for {category}")
        return self._builders[category]