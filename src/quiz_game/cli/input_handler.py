import threading
import time

from quiz_game.models.question import Question
from quiz_game.config.enums import AnswerType

from quiz_game.config.constants import MC_LABELS

from quiz_game.cli.timed_input import TimedInput

from quiz_game.cli.terminal_renderer import TerminalRenderer

class InputHandler:

    def get_answer(self, question: Question, renderer: TerminalRenderer, **kwargs,):

        while True:
            raw_answer = TimedInput.get(question=question, renderer=renderer, **kwargs)

            if raw_answer is None:
                return None

            match question.answer_type:

                case AnswerType.MC:
                    answer = self._resolve_multiple_choice(question, raw_answer,)

                    if answer is not None:
                        renderer.set_message(None)
                        return answer

                    renderer.set_message(f"Please enter one of: {', '.join(self.valid_letters)} (or type the answer)")
                
                case AnswerType.OPEN:
                    return raw_answer.strip()

                case _:
                    raise NotImplementedError

    def _resolve_multiple_choice(self, question: Question, answer: str,):

        self.valid_letters = MC_LABELS[:len(question.options)]

        lookup = {label.lower(): option for label, option in zip(self.valid_letters, question.options)}

        lookup.update({option.lower(): option for option in question.options})

        return lookup.get(answer.strip().lower())
