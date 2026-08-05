from quiz_game.models.settings import QuizSettings
from quiz_game.config.cli_defaults import CLI_CUSTOM_GAMEPLAY_SETTINGS
from quiz_game.config.modes import QUIZ_MODE_SETTINGS
from quiz_game.config.enums import QuizMode, QuestionCategory, DistractorStrategy, AnswerType

# Define invalid combinations of config settings: {IF THIS ONE IS PRESENT: REMOVE THESE ONES}
#QUESTION_CATEGORY_PRECEDENCE_RULES = {
#    QuestionCategory.CITY_COUNTRY: (
#        QuestionCategory.CAPITAL_COUNTRY,
#    ),
#}

ANSWER_TYPE_PRECEDENCE_RULES = {}

DISTRACTOR_STRATEGY_PRECEDENCE_RULES = {}

def resolve_settings(settings: QuizSettings, resolve_custom_settings = True) -> QuizSettings:

    # Resolve custom gameplay settings
    if settings.quiz_mode == QuizMode.CUSTOM and resolve_custom_settings:
        settings.gameplay = CLI_CUSTOM_GAMEPLAY_SETTINGS.model_copy(deep=True)
        return settings

    if settings.quiz_mode == QuizMode.CUSTOM and (not resolve_custom_settings):
        return settings
    
    settings.gameplay = QUIZ_MODE_SETTINGS[settings.quiz_mode].model_copy(deep=True)
    return settings
    
    # Resolve incompatible question category, answer type and distractor strategy combinations:
#    settings.question_categories = apply_precedence_rules(settings.question_categories, QUESTION_CATEGORY_PRECEDENCE_RULES)
#    settings.distractor_strategies = apply_precedence_rules(settings.distractor_strategies, DISTRACTOR_STRATEGY_PRECEDENCE_RULES)
#    settings.answer_types = apply_precedence_rules(settings.answer_types, ANSWER_TYPE_PRECEDENCE_RULES)

def apply_precedence_rules(values,rules):
    values = list(values)

    for dominant_value, redundant_values in rules.items():
        if dominant_value in values:
            values = [
                value 
                for value in values
                if value not in redundant_values
            ]

    return tuple(values)