# config/defaults.py

from quiz_game.models.settings import QuizSettings, GameplaySettings, LocationFilter
from quiz_game.config.enums import (
    QuizMode,
    ALL_QUESTION_CATEGORIES,
    ALL_ANSWER_TYPES,
    ALL_DISTRACTOR_STRATEGIES,
    DifficultyLevel,
    DifficultyProgression,
)

CLI_CUSTOM_GAMEPLAY_SETTINGS = GameplaySettings(
    lives = 3,                    
    question_time = 10,   
    total_time = 60,    
    num_questions = 10,   
    question_recycling = True,  
    infinite_mode = False,        
)

CLI_LOCATION_FILTER = LocationFilter(
    include_regions = set(["Europe"]),
    include_subregions = set(["South-East Asia", "North-America"]),
)

CLI_QUIZ_SETTINGS = QuizSettings(
    quiz_mode=QuizMode.PRACTICE,
    question_categories=ALL_QUESTION_CATEGORIES,
    answer_types=ALL_ANSWER_TYPES,
    distractor_strategies=ALL_DISTRACTOR_STRATEGIES,
    gameplay=GameplaySettings(),
    location_filter=CLI_LOCATION_FILTER,
    difficulty_level=DifficultyLevel.NORMAL,
    difficulty_progression=DifficultyProgression.FIXED,
)