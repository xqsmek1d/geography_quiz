from pydantic import BaseModel, Field

from quiz_game.config.enums import (
    QuizMode,
    QuestionCategory,
    AnswerType,
    DistractorStrategy,
    DifficultyLevel,
    DifficultyProgression,
    ALL_ANSWER_TYPES,
    ALL_QUESTION_CATEGORIES,
    ALL_DISTRACTOR_STRATEGIES
)

class GameplaySettings(BaseModel): 
    lives: int | None = None           # Quiz stops when the player has no lives left, which are lost every incorrect answer
    question_time: int | None = None   # Answer is assumed incorrect if time for the question expires
    total_time: int | None = None      # Quiz stops at the indicated time
    num_questions: int | None = None   # Quiz stops at the maximum number of question (incorrect answers do not count)
    question_recycling: bool = False    # Question with incorrect answer is added back to the pool
    infinite_mode: bool = False         # Question pools are refilled when empty

class LocationFilter(BaseModel): 
    include_regions: set[str] = Field(default_factory=set)
    include_subregions: set[str] = Field(default_factory=set)

class QuizSettings(BaseModel):
    quiz_mode: QuizMode = QuizMode.PRACTICE     
    question_categories: tuple[QuestionCategory, ...] = ALL_QUESTION_CATEGORIES
    answer_types: tuple[AnswerType, ...] = ALL_ANSWER_TYPES
    distractor_strategies: tuple[DistractorStrategy, ...] = ALL_DISTRACTOR_STRATEGIES
    gameplay: GameplaySettings = Field(default_factory=GameplaySettings)
    location_filter: LocationFilter = Field(default_factory=LocationFilter)
    #country_filter: CountryFilter (here for possible future purpose)
    difficulty_level: DifficultyLevel = DifficultyLevel.NORMAL
    difficulty_progression: DifficultyProgression = DifficultyProgression.FIXED