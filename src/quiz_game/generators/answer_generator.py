import random

from quiz_game.config.enums import AnswerType, DistractorStrategy
from quiz_game.generators.distractor_generator import DistractorGenerator

from quiz_game.models.question import Question
from quiz_game.models.question_data import QuestionData
from quiz_game.models.answer_key import AnswerKey
from quiz_game.config.enums import AnswerType


class AnswerGenerator:

    def __init__(self, answer_types: list[AnswerType], distractor_strategies: list[DistractorStrategy], distractor_generator: DistractorGenerator, rng: random.Random,):

        self.answer_types = answer_types
        self.distractor_strategies = distractor_strategies
        self.distractor_generator = distractor_generator
        self.rng = rng


    def create(self, question_data: QuestionData,) -> tuple[Question,AnswerKey]:

        answer_type = self.rng.choice(self.answer_types)

        match answer_type:

            case AnswerType.OPEN:
                return self.create_open(question_data)

            case AnswerType.MC:
                return self.create_multiple_choice(question_data)

            case _:
                raise NotImplementedError

    def create_open(self, question_data: QuestionData):

        question = Question(
            category=question_data.category,
            answer_type=AnswerType.OPEN,
            prompt=question_data.prompt,
            image=question_data.image,
            metadata=question_data.metadata,
        )

        answer_key = AnswerKey(
            answer_pool_type=question_data.answer_pool_type,
            answer_type=AnswerType.OPEN,
            accepted_answers= ...
            correct_answer=question_data.correct_answer,
            correct_answer_id=question_data.correct_answer_id,

        )

        return question, answer_key

    def create_multiple_choice(self, question_data: QuestionData,) -> tuple[Question, AnswerKey]:

        distractor_strategy = self.rng.choice(self.distractor_strategies)

        distractors = self.distractor_generator.generate(correct_answer_id=question_data.correct_answer_id, answer_pool_type=question_data.answer_pool_type, distractor_strategy=distractor_strategy,)

        options = [question_data.correct_answer, *distractors,]

        self.rng.shuffle(options)

        question = Question(
            category=question_data.category,
            answer_type=AnswerType.MC,
            prompt=question_data.prompt,
            options=options,
            image=question_data.image,
        )

        answer_key = AnswerKey(
            answer_pool_type=question_data.answer_pool_type,
            answer_type=AnswerType.MC,
            accepted_answers= ...
            correct_answer=question_data.correct_answer,
            correct_answer_id=question_data.correct_answer_id,
            correct_option_index=options.index(question_data.correct_answer),
        )

        return question, answer_key