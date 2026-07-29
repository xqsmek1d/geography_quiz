from quiz_game.models.game_state import GameState

from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.models.answer_result import AnswerResult

from quiz_game.config.enums import AnswerType
from quiz_game.config.constants import MC_LABELS

from quiz_game.cli.image_viewer import ImageViewer


def display_settings(settings: QuizSettings):
    lines = [
        "\n===== QUIZ SETTINGS =====",
        f'Quiz mode ({settings.quiz_mode.value.upper()}):'
    ]

    # List quiz mode information
    if settings.gameplay.lives:
        lines.append(f'   - lives = {settings.gameplay.lives}')
    else:
        lines.append(f'   - lives = N/A')

    if settings.gameplay.question_time:
        lines.append(f'   - time per question = {settings.gameplay.question_time} seconds')
    else:
        lines.append(f'   - time per question = N/A')
    
    if settings.gameplay.total_time:
        lines.append(f'   - total time = {settings.gameplay.total_time} seconds')
    else:
        lines.append(f'   - total time = N/A')

    if settings.gameplay.num_questions: 
        lines.append(f'   - number of questions = {settings.gameplay.num_questions}')
    else:
        lines.append(f'   - number of questions = N/A')

    lines.append(f'   - question_recycling: {settings.gameplay.question_recycling}')
    lines.append(f'   - infinite mode: {settings.gameplay.infinite_mode}')
    
    # Make difficulty string(s)
    lines.append(f'\nQuestion difficulty: {settings.difficulty_level}')

    # Make region selection string(s)
    lines.append(' ')
    lines.append(f'Included regions: {settings.location_filter.include_regions}')
    lines.append(f'Included subregions: {settings.location_filter.include_subregions}')

    # Make question category string(s)
    if len(settings.question_categories) > 1:
        lines.append(f'\nQuestion categories:')

        for category in settings.question_categories:
            lines.append(f"   - {category}")
    else:
        lines.append(f'\nQuestion category: {settings.question_categories[0].value}')

    # Make question answer type string(s)
    if len(settings.answer_types) > 1:
        lines.append(f'\nAnswer type categories:')
        lines.append("\n".join(f"   - {answer_type.value.lower()}" for answer_type in settings.answer_types))
    else:
        lines.append(f'\nAnswer type: {settings.answer_types[0].value.lower()}',)
    
    # Make distractor strategy string(s)
    if len(settings.distractor_strategies) > 1 and (AnswerType.MC in settings.answer_types or AnswerType.MIXED in settings.answer_types):
        lines.append(f'\nDistractor strategies:')
        lines.append("\n".join(f"   - {distractor_strategy.name.lower().replace("_"," ")}" for distractor_strategy in settings.distractor_strategies))

    elif AnswerType.MC in settings.answer_types or AnswerType.MIXED in settings.answer_types:
        lines.append(f'\nMultiple choice distraction: {settings.distractor_strategies[0].name.lower().replace("_"," ")}')

    print("\n".join(lines))

def display_question(question: Question, question_count: int | None, viewer: ImageViewer):
    
    lines = []

    if question_count is None:
        lines.apppend("\n====== Question ======")
    else:
        lines.append(f"\n====== Question {question_count} ======")

    viewer.show(question.image)
    
    lines.append("")
    lines.append(question.prompt)
    lines.append("")

    if question.answer_type == AnswerType.MC:
        for label, option in zip(MC_LABELS, question.options):
            lines.append(f"{label}) {option}")
        
        lines.append("")
        lines.append("Type the letter (or the full answer):")
    else:
        lines.append("Type your answer:")

    print("\n".join(lines))

def display_result(result: AnswerResult):

    if result.is_correct:
        print("Correct!")
    else:
        print(f"Incorrect. " f"The answer was {result.correct_answer}")

def display_score():
    raise NotImplementedError

def display_summary(game_state: GameState):

    print("\nQuiz finished!")
    print(f"Questions: {game_state.questions_asked}")
    print(f"Score: {game_state.score}")