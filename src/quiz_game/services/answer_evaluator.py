import unicodedata

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

from quiz_game.models.answer_key import AnswerKey
from quiz_game.models.answer_result import AnswerResult
from quiz_game.config.enums import MatchType

class AnswerEvaluator():
    
    def evaluate(self, answer_key: AnswerKey, submitted_answer: str,) -> AnswerResult:

        submitted = submitted_answer.strip()
        
        # Exact Match
        if submitted in (answer.strip() for answer in answer_key.accepted_answers):
            match_type = MatchType.EXACT

            '''
            # Accent-insensitive match
            elif ...
            '''
        else:
            match_type = MatchType.NO_MATCH

        return AnswerResult(
            submitted_answer=submitted_answer,
            is_correct=match_type in {MatchType.EXACT, MatchType.ACCENT_INSENSITIVE, MatchType.SPELLING_MISTAKE},
            correct_answer=answer_key.correct_answer,
            match_type=match_type,
        )