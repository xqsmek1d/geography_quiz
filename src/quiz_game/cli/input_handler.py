from quiz_game.models.question import Question
from quiz_game.config.enums import AnswerType

from quiz_game.config.constants import MC_LABELS

class InputHandler:

        def get_answer(self, question: Question):

            match question.answer_type:

                case AnswerType.MC:
                    return self._multiple_choice(question)
                
                case AnswerType.OPEN:
                    return self._open_answer()

                case _:
                    raise NotImplementedError

        def _multiple_choice(self, question: Question):

            valid_letters = MC_LABELS[:len(question.options)]

            lookup = {label.lower(): option for label, option in zip(valid_letters, question.options)}
            lookup.update({option.strip().lower(): option for option in question.options})

            while True:
                answer = input("> ").strip().lower()

                if answer in lookup:
                    return lookup[answer]
                
                print(f"Please enter one of: {', '.join(valid_letters)} (or type the answer)")

        def _open_answer(self):

            return input("> ").strip()
