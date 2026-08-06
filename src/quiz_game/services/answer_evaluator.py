import unicodedata

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

from quiz_game.models.answer_key import AnswerKey
from quiz_game.models.answer_result import AnswerResult
from quiz_game.config.enums import MatchType

class AnswerEvaluator():

    def _remove_accents(self, text: str) -> str:
        normalised = unicodedata.normalize("NFD", text)
        return "".join(character for character in normalised if unicodedata.category(character) != "Mn")

    def _normalise(self, text: str) -> str:
        return self._remove_accents(text.casefold().strip())

    @staticmethod
    def _allowed_spelling_distance(answer: str) -> int:
        length = len(answer)
        if length <= 4:
            return 0
        if length <= 7:
            return 2
        if length <= 12:
            return 4
        return max(4, length // 3)

    def _check_spelling(self, submitted: str, accepted_answers: list[str]) -> MatchType:

        normalised_submitted = self._normalise(submitted)

        for answer in accepted_answers:
            normalised_answer = self._normalise(answer)
            
            #print(f"Checking levenshtein distance for {normalised_submitted} against {normalised_answer}")
            distance = Levenshtein.distance(normalised_submitted, normalised_answer,)

            allowed_distance = self._allowed_spelling_distance(normalised_answer)

            #print(f"The levenshtein distance = {distance}, but the allowed was: {allowed_distance}")
            #input("Press enter to continue...")
            if 0 < distance <= allowed_distance:
                return MatchType.SPELLING_MISTAKE

        return MatchType.NO_MATCH

    
    def evaluate(self, answer_key: AnswerKey, submitted_answer: str,) -> AnswerResult:
        
        if submitted_answer:
            submitted = submitted_answer.strip()
        else:
            return AnswerResult(
                submitted_answer=None,
                is_correct=False,
                correct_answer=answer_key.correct_answer,
                match_type=MatchType.TIMEOUT
            )
        
        # Exact Match
        if submitted in (answer.strip() for answer in answer_key.accepted_answers):
            match_type = MatchType.EXACT
        else:
            # Accent-insensitive match
            if self._remove_accents(submitted) in {self._remove_accents(answer) for answer in answer_key.accepted_answers}:
                match_type = MatchType.ACCENT_INSENSITIVE
            else:
                match_type = self._check_spelling(submitted, answer_key.accepted_answers)

        return AnswerResult(
            submitted_answer=submitted_answer,
            is_correct=match_type in {MatchType.EXACT, MatchType.ACCENT_INSENSITIVE, MatchType.SPELLING_MISTAKE},
            correct_answer=answer_key.correct_answer,
            match_type=match_type,
        )