#from quiz_game.core.quiz import QuizSession
from quiz_game.config.loader import load_cli_settings
#from quiz_game.generators.question_generator import QuestionGenerator
from quiz_game.cli.display import display_settings#, display_question, display_result

def main():

    settings = load_cli_settings()

    display_settings(settings)
    '''
    quiz = QuizSession(generator, settings)

    while quiz.has_questions():

        question = quiz.next_question()

        display(question)

        answer = input("Answer: ")

        result = quiz.submit_answer(answer)

        display_results(result)

    final_score = quiz.score

    display_final_score(final_score)
    '''
if __name__=="__main__":
    main()