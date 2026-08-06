import os

from quiz_game.cli.input_handler import InputHandler
from quiz_game.cli.display import display_question, display_result, display_game_state, display_summary, display_ending
from quiz_game.cli.image_viewer import ImageViewer
from quiz_game.cli.terminal_renderer import TerminalRenderer
from quiz_game.cli.timed_input import TimedInput

from quiz_game.core.quiz_session import QuizSession


class GameLoop:

    def __init__(self, session: QuizSession, viewer: ImageViewer, renderer: TerminalRenderer):
        self.renderer = renderer
        self.session = session
        self.input_handler = InputHandler()
        self.viewer = viewer

    def run(self):

        question_count = 0
        continue_playing = True

        try:
            while continue_playing:

                self.viewer.start()
                self.session.game_timer.start()

                previous_result = None

                while not self.session.is_finished():
                    
                    os.system("clear")
                    self.session.question_timer.start()

                    question_count += 1
                    question = self.session.next_question(question_count=question_count)

                    self.viewer.show(question.image)
                    
                    answer = self.input_handler.get_answer(
                        question=question,
                        game_state=self.session.state,
                        game_timer=self.session.game_timer,
                        question_timer=self.session.question_timer,
                        renderer=self.renderer,
                        previous_result = previous_result,
                        )

                    previous_result = self.session.submit_answer(answer)              

                display_summary(self.session.state)

                continue_playing = display_ending() #PLAY AGAIN IS NOT IMPLEMENTED CURRENTLY


        finally: 
            self.viewer.close()
