from quiz_game.models.settings import GameplaySettings
from quiz_game.config.enums import QuizMode

QUIZ_MODE_SETTINGS = {
    QuizMode.PRACTICE: GameplaySettings(
        infinite_mode=True,
        question_recycling=True,
    ),
    QuizMode.SURVIVAL: GameplaySettings(
        lives=3,
        infinite_mode=False,
    ),
    QuizMode.TIME_ATTACK: GameplaySettings(
        lives=3,
        question_time=10,
        total_time=180,
        infinite_mode=False,
    ),
    QuizMode.HARDCORE: GameplaySettings(
        lives=1,
        question_time=10,
        infinite_mode=False,
    ),
    QuizMode.MARATHON: GameplaySettings(
        num_questions=100,
        infinite_mode=False,
    ),
    QuizMode.RACE: GameplaySettings(
        num_questions=20,
        lives=1,
        infinite_mode=False,
    ),
}

