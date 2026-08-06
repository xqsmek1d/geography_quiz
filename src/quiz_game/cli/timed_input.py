import os
import sys
import time

from quiz_game.core.timer import GameTimer, QuestionTimer
from quiz_game.models.question import Question
from quiz_game.models.game_state import GameState
from quiz_game.models.answer_result import AnswerResult
from quiz_game.cli.terminal_renderer import TerminalRenderer


class TimedInput:

    @staticmethod
    def get(
        game_state: GameState,
        question: Question,
        game_timer: GameTimer,
        question_timer: QuestionTimer,
        renderer: TerminalRenderer,
        previous_result: AnswerResult | None = None,
    ) -> str | None:

        if question_timer:
            question_timer.start()

        '''
        if os.name == "nt":
            return TimedInput._windows_input(
                prompt,
                game_timer,
                question_timer,
                renderer,
            )
        '''

        return TimedInput._unix_input(
            game_state = game_state,
            question = question,
            game_timer = game_timer,
            question_timer = question_timer,
            renderer = renderer,
            previous_result = previous_result,
        )

    '''
    @staticmethod
    def _windows_input(
        prompt,
        game_timer,
        question_timer,
        renderer,
        ):

        import msvcrt

        answer = []

        while True:

            question_time = (question_timer.remaining if question_timer else None)

            if question_timer and question_timer.expired:
                return None

            if renderer:

                renderer.render(
                    game_time=(game_timer.elapsed if game_timer else 0),
                    question_time=question_time,
                    prompt=prompt,
                    answer="".join(answer),
                )

            if msvcrt.kbhit():

                key = msvcrt.getwch()

                if key in ("\r", "\n"):
                    return "".join(answer)

                if key == "\x08":

                    if answer:
                        answer.pop()

                elif key == "\x03":
                    raise KeyboardInterrupt

                elif key.isprintable():
                    answer.append(key)

            time.sleep(0.01)
    '''

    @staticmethod
    def _unix_input(
        game_state: GameState,
        question: Question,
        game_timer: GameTimer,
        question_timer: QuestionTimer,
        renderer: TerminalRenderer,
        previous_result: AnswerResult | None = None,
        ):

        import select
        import termios
        import tty

        answer = []

        fd = sys.stdin.fileno()

        old_settings = termios.tcgetattr(fd)

        try:

            tty.setcbreak(fd)

            while True:

                question_time = (question_timer.remaining if question_timer else None)

                if question_timer.duration and question_timer.expired:
                    return None

                readable, _, _ = select.select([sys.stdin], [], [], 0.01,)

                if readable:

                    key = sys.stdin.read(1)

                    if key in ("\r", "\n"):
                        return "".join(answer)

                    if key in ("\x7f", "\x08"):

                        if answer:
                            answer.pop()

                    elif key == "\x03":
                        raise KeyboardInterrupt

                    elif key.isprintable():
                        answer.append(key)

                renderer.render(
                    game_state=game_state,
                    question=question,
                    answer_buffer="".join(answer),
                    game_time=(game_timer.remaining if game_timer.duration else game_timer.elapsed),
                    question_time=question_time,
                    previous_result=previous_result
                    )

        finally:

            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings,)