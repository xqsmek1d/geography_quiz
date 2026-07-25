from quiz_game.models.settings import QuizSettings
from quiz_game.config.cli_defaults import CLI_QUIZ_SETTINGS,CLI_CUSTOM_GAMEPLAY_SETTINGS
from quiz_game.config.resolver import resolve_settings

def load_cli_settings() -> QuizSettings:
    settings = CLI_QUIZ_SETTINGS.model_copy(deep=True)
    return resolve_settings(settings)


