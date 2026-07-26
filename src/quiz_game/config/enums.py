from enum import Enum, StrEnum

class QuizMode(StrEnum):
    PRACTICE = "practice"
    SURVIVAL = "survival"
    TIME_ATTACK = "time_attack"
    HARDCORE = "hardcore"
    RACE = "race"
    MARATHON = "marathon"
    CUSTOM = "custom"

class QuestionCategory(StrEnum):
    COUNTRY_CAPITAL = "country_capital"
    CAPITAL_COUNTRY = "capital_country"
    #FLAG_COUNTRY = "COUNTRY flag -> COUNTRY name"
    #FLAG_CAPITAL = "COUNTRY flag -> COUNTRY capital"
    #MAP_OUTLINE_COUNTRY = "COUNTRY shape -> COUNTRY name"
    #MAP_OUTLINE_CAPITAL = "COUNTRY shape -> CAPITAL name"
    #MAP_HIGHLIGHT_COUNTRY = "COUNTRY worldmap -> COUNTRY name"
    #MAP_HIGHLIGHT_CAPITAL = "COUNTRY worldmap -> CAPITAL name"
    CITY_COUNTRY = "city_country"
    #LANDMARK_CITY = "LANDMARK name -> CITY name"
    #LANDMARK_COUNTRY = "LANDMARK name -> COUNTRY name"
ALL_QUESTION_CATEGORIES = tuple(QuestionCategory)

class AnswerType(StrEnum):
    MC = "multiple_choice"
    OPEN = "open"
    #CLOSED = "closed" # to be implemented
ALL_ANSWER_TYPES = tuple(AnswerType)

class DistractorStrategy(Enum):
    RANDOM = 0
    SAME_REGION = 1
    SAME_SUBREGION = 2
    SAME_COUNTRY = 3
ALL_DISTRACTOR_STRATEGIES = tuple(DistractorStrategy)

class DifficultyLevel(Enum):
    EASY = 0.3
    NORMAL = 0.5
    HARD = 0.7
    WIZARD = 1

class DifficultyProgression(StrEnum):
    FIXED = "fixed"
    PROGRESSIVE = "progressive"
