from quiz_game.cli.input_handler import InputHandler
from quiz_game.cli.display import display_question, display_result, display_summary
from quiz_game.cli.display import ImageViewer

from quiz_game.core.quiz_session import QuizSession


class GameLoop:

    def __init__(self, session: QuizSession):
        self.session = session
        self.input_handler = InputHandler()
        self.viewer = ImageViewer()

    def run(self):

        question_count = 0

        try:
            while not self.session.is_finished():
                
                question = self.session.next_question()

                question_count += 1
                display_question(question, question_count, self.viewer)

                answer = self.input_handler.get_answer(question)

                result = self.session.submit_answer(answer)

                display_result(result=result)

            display_summary(self.session.state)

        finally: 
            self.viewer.close()
