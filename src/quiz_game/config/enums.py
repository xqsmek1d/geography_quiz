from enum import Enum, StrEnum

from utils.validation.known_data_exceptions import NO_FLAG, NO_HIGHLIGHT_IMAGE

class QuizMode(StrEnum):
    PRACTICE = "practice"
    SURVIVAL = "survival"
    TIME_ATTACK = "time_attack"
    HARDCORE = "hardcore"
    RACE = "race"
    MARATHON = "marathon"
    CUSTOM = "custom"

class PoolType(StrEnum):
    COUNTRY = "country"
    CITY = "city"
    LANDMARK = "landmark"
    CAPITAL = "capital"

class QuestionCategory(StrEnum):
    COUNTRY_CAPITAL = "country_capital"
    CAPITAL_COUNTRY = "capital_country"
    FLAG_COUNTRY = "flag_country"
    #FLAG_CAPITAL = "COUNTRY flag -> COUNTRY capital"
    #MAP_SHAPE_COUNTRY = "COUNTRY shape -> COUNTRY name"
    #MAP_SHAPE_CAPITAL = "COUNTRY shape -> CAPITAL name"
    MAP_HIGHLIGHT_COUNTRY = "highlight-map_country"
    #MAP_HIGHLIGHT_CAPITAL = "COUNTRY worldmap -> CAPITAL name"
    #CITY_COUNTRY = "city_country"
    #LANDMARK_CITY = "LANDMARK name -> CITY name"
    #LANDMARK_COUNTRY = "LANDMARK name -> COUNTRY name"

    @property
    def pool_type(self) -> PoolType:
        match self:
            case QuestionCategory.COUNTRY_CAPITAL:
                return PoolType.COUNTRY
            case QuestionCategory.CAPITAL_COUNTRY:
                return PoolType.COUNTRY
            case QuestionCategory.FLAG_COUNTRY:
                return PoolType.COUNTRY
            case QuestionCategory.MAP_HIGHLIGHT_COUNTRY:
                return PoolType.COUNTRY
            case _:
                raise NotImplementedError

    @property
    def excluded_ids(self) -> list[str]:
        match self:
            case QuestionCategory.COUNTRY_CAPITAL:
                return []
            case QuestionCategory.CAPITAL_COUNTRY:
                return []
            case QuestionCategory.FLAG_COUNTRY:
                return NO_FLAG.copy()
            case QuestionCategory.MAP_HIGHLIGHT_COUNTRY:
                return NO_HIGHLIGHT_IMAGE.copy()
            case _:
                raise NotImplementedError

class AnswerType(StrEnum):
    MC = "multiple_choice"
    OPEN = "open"
    #CLOSED = "closed" # to be implemented

class DistractorStrategy(Enum):
    RANDOM = 0
    SAME_REGION = 1
    SAME_SUBREGION = 2
    SAME_COUNTRY = 3

class DifficultyLevel(Enum):
    EASY = 0.3
    NORMAL = 0.5
    HARD = 0.7
    WIZARD = 1

class DifficultyProgression(StrEnum):
    FIXED = "fixed"
    PROGRESSIVE = "progressive"

ALL_DISTRACTOR_STRATEGIES = tuple(DistractorStrategy)
ALL_ANSWER_TYPES = tuple(AnswerType)
ALL_QUESTION_CATEGORIES = tuple(QuestionCategory)