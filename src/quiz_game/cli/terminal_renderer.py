from quiz_game.models.game_state import GameState
from quiz_game.models.question import Question
from quiz_game.models.answer_result import AnswerResult

from quiz_game.cli.display import display_question, display_result

from quiz_game.core.timer import GameTimer, QuestionTimer

class TerminalRenderer:

    def __init__(self):
        self.first_render = True
        self.render_height = 0
        self.message = None

    def set_message(self, message: str):
        self.message = message

    def render(
        self,
        game_state: GameState,
        question: Question,
        answer_buffer: str,
        game_time: GameTimer | None = None,
        question_time: QuestionTimer | None = None,
        previous_result: AnswerResult | None = None,
    ):

        question_text = display_question(question)

        lines = []
        if game_state.remaining_lives:
            lines.append(f"Score: {game_state.score} | Lives: {'❤️' * game_state.remaining_lives}")
        else:
            lines.append(f"Score: {game_state.score}")

        if game_time and question_time:
            lines.append(f"Game time: {self._format_time(game_time)} | Question: {question_time}s")
        elif game_time:
            lines.append(f"Game time: {self._format_time(game_time)}")
        elif question_time:
            lines.append(f"Question: {question_time}s")
            
        lines.append("")
        
        if self.message:
            lines.append(self.message)
        elif previous_result:
            lines.extend([display_result(previous_result),])
            
        lines.extend([*question_text.split("\n"),])

        if not self.first_render:
            # Move cursor back to start of screen area
            print(f"\033[{self.render_height}A\033[0G", end="",)

        else:
            self.first_render = False

        for line in lines:
            print(
                "\033[2K"
                + line
            )

        print(
            "\033[2K"
            f"> {answer_buffer}",
            end="",
            flush=True,
        )

        self.render_height = len(lines) + 1

    @staticmethod
    def _format_time(seconds):

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        return f"{minutes:02d}:{seconds:02d}"