from quiz_game.config.enums import PoolType

class PoolFactoryRegistry:

    def __init__(self):
        self.factories = {}

    def register(self, pool_type: PoolType, factory):
        self.factories[pool_type] = factory

    def get_factory(self, pool_type: PoolType):
        if pool_type not in self.factories:
            raise ValueError(f"ERROR: no factory registered for pool type '{pool_type}'")

        return self.factories[pool_type]