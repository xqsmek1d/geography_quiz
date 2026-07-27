from quiz_game.repositories.country_repository import CountryRepository
from quiz_game.repositories.city_repository import CityRepository
# from quiz_game.repositories.landmark_repository import LandmarkRepository


class RepositoryRegistry:

    def __init__(
        self,
        country_repository: CountryRepository,
        city_repository: CityRepository | None = None,
        # landmark_repository: LandmarkRepository | None = None,
    ):
        self.country = country_repository
        self.city = city_repository
        # self.landmark = landmark_repository