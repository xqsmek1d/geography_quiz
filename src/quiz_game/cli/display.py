import os

from quiz_game.models.game_state import GameState

from quiz_game.models.settings import QuizSettings
from quiz_game.models.question import Question
from quiz_game.models.answer_result import AnswerResult

from quiz_game.config.enums import AnswerType, MatchType
from quiz_game.config.constants import MC_LABELS

from quiz_game.cli.image_viewer import ImageViewer


def display_settings(settings: QuizSettings):
    lines = [
        "\n===== QUIZ SETTINGS =====\n",
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
    lines.append(f'\nQuestion difficulty: {settings.difficulty_level.value.upper()}')

    # Make region selection string(s)
    lines.append(f'\nLocation filter:')
    if settings.location_filter.include_regions:
        regions = ", ".join(sorted(settings.location_filter.include_regions))
        lines.append(f"   - regions: {regions}")
    else:
        lines.append("   - regions: all")

    if settings.location_filter.include_subregions:
        subregions = ", ".join(sorted(settings.location_filter.include_subregions))
        lines.append(f"   - subregions: {subregions}")
    else:
        lines.append("   - subregions: all")

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
    if len(settings.distractor_strategies) > 1 and (AnswerType.MC in settings.answer_types):
        lines.append(f'\nDistractor strategies:')
        lines.append("\n".join(f"   - {distractor_strategy.name.lower().replace("_"," ")}" for distractor_strategy in settings.distractor_strategies))

    elif AnswerType.MC in settings.answer_types:
        lines.append(f'\nMultiple choice distraction: {settings.distractor_strategies[0].name.lower().replace("_"," ")}')

    print("\n".join(lines))

def display_gameplay_settings(settings: QuizSettings):
    lines = [
        "\n===== CUSTOM GAMEPLAY SETTINGS =====\n",
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

    print("\n".join(lines))

def display_question(question: Question, print_output=False):

    lines = []

    if question.count is None:
        lines.apppend("\n====== Question ======")
    else:
        lines.append(f"\n====== Question {question.count} ======")

    #viewer.show(question.image)
    
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

    question_text = "\n".join(lines)

    if print_output:
        print(question_text)

    return question_text

def display_result(result: AnswerResult, print_output=False):

    #os.system("clear")

    if result.match_type == MatchType.EXACT:
        text = f"✓ Correct! ({result.correct_answer})" 
    elif result.match_type == MatchType.ACCENT_INSENSITIVE:
        text = f"✓ Correct, but I think the accents were slighlty off. It should have been '{result.correct_answer}'"
    elif result.match_type == MatchType.SPELLING_MISTAKE:
        text = f"✓ Correct, but I think you made a small spelling mistake. It should have been '{result.correct_answer}'"
    elif result.match_type == MatchType.TIMEOUT:
        text = f"✗ Timed out! The correct answer was {result.correct_answer}"
    else:
        text = f"✗ Incorrect. The correct answer was {result.correct_answer}"
    
    if print_output:
        print(text)
    
    return text

def display_score():
    raise NotImplementedError

def display_summary(game_state: GameState):

    os.system("clear")

    print("\nQuiz finished!")
    print(f"Questions: {game_state.questions_asked}")
    print(f"Score: {game_state.score}")

def display_game_state(game_state: GameState):

    print("")
    print(f"Remaining lives: {game_state.remaining_lives}")
    print(f"Score: {game_state.score}")
    print(f"Elapsed time: {game_state.elapsed_time}")

def display_ending() -> bool:

    print("")
    print(f"Thank you for playing!")
    print("")
    print(f"Press Escape to exit...")

    if os.name == "nt":
        return _wait_for_continue_windows()
    
    return _wait_for_continue_unix()
    

def _wait_for_continue_windows() -> bool:
    import msvcrt

    while True:
        key = msvcrt.getwch()
        
        #if key == "\r":
        #    return True

        if key == "\x1b":
            return False

def _wait_for_continue_unix() -> bool:
    import sys
    import termios
    import tty

    file_descriptor = sys.stdin.fileno()

    old_settings = termios.tcgetattr(file_descriptor,)

    try:
        tty.setraw(file_descriptor)

        while True:
            key = sys.stdin.read(1)

            #if key in ("\r", "\n"):
            #    return True

            if key == "\x1b":
                return False

    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)