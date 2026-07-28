from enum import Enum, StrEnum

from quiz_game.config.known_data_exceptions import NO_FLAG, NO_HIGHLIGHT_IMAGE, NO_CAPITAL

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
    MAP_HIGHLIGHT_COUNTRY = "highlight-map_country"
    '''
    #FLAG_CAPITAL = "COUNTRY flag -> COUNTRY capital"
    #MAP_SHAPE_COUNTRY = "COUNTRY shape -> COUNTRY name"
    #MAP_SHAPE_CAPITAL = "COUNTRY shape -> CAPITAL name"
    
    #MAP_HIGHLIGHT_CAPITAL = "COUNTRY worldmap -> CAPITAL name"
    #CITY_COUNTRY = "city_country"
    #LANDMARK_CITY = "LANDMARK name -> CITY name"
    #LANDMARK_COUNTRY = "LANDMARK name -> COUNTRY name"
    '''

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
                return NO_CAPITAL.copy()
            case QuestionCategory.CAPITAL_COUNTRY:
                return NO_CAPITAL.copy()
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
    #SAME_COUNTRY = 3

class DifficultyLevel(Enum):
    EASY = 0.3
    NORMAL = 0.5
    HARD = 0.7
    WIZARD = 1

class DifficultyProgression(StrEnum):
    FIXED = "fixed"
    PROGRESSIVE = "progressive"

class MatchType(StrEnum):
    EXACT = "exact"                             # valid name, exact characters used
    ACCENT_INSENSITIVE = "accent_insensitive"   # correct name, only accents differ (Aland instead of Åland)
    SPELLING_MISTAKE = "spelling mistake"       # small typo such as swapped letters or a missing character (Ålnd or Ålnad instead of Åland)
    FUZZY = "fuzzy"                             # broadly similar but less certain (Mehiko instead of Mexico)
    NO_MATCH = "no_match"                       # cannot identify a single broad match

    @property 
    def match_score(self) -> float:
        match self:
            case MatchType.EXACT:
                return 1.0
            case MatchType.ACCENT_INSENSITIVE:
                return 0.9
            case MatchType.SPELLING_MISTAKE:
                return 0.8
            case MatchType.FUZZY:
                return 0.5
            case MatchType.NO_MATCH:
                return 0.0
            case _:
                raise NotImplementedError

ALL_DISTRACTOR_STRATEGIES = tuple(DistractorStrategy)
ALL_ANSWER_TYPES = tuple(AnswerType)
ALL_QUESTION_CATEGORIES = tuple(QuestionCategory)