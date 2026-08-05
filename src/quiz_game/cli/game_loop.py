from quiz_game.cli.input_handler import InputHandler
from quiz_game.cli.display import display_question, display_result, display_game_state, display_summary, display_ending
from quiz_game.cli.image_viewer import ImageViewer

from quiz_game.core.quiz_session import QuizSession


class GameLoop:

    def __init__(self, session: QuizSession, viewer: ImageViewer):
        self.session = session
        self.input_handler = InputHandler()
        self.viewer = viewer

    def run(self):

        question_count = 0
        continue_playing = True

        try:
            while continue_playing:

                while not self.session.is_finished():

                    self.viewer.start()
                    
                    display_game_state(self.session.state)

                    question = self.session.next_question()

                    question_count += 1
                    display_question(question, question_count, self.viewer)

                    answer = self.input_handler.get_answer(question)

                    result = self.session.submit_answer(answer)

                    display_result(result=result)

                display_summary(self.session.state)

                continue_playing = display_ending()



        finally: 
            self.viewer.close()
