import os

from quiz_game.models.settings import QuizSettings
from quiz_game.cli.display import display_settings

from quiz_game.config.resolver import resolve_settings

from quiz_game.config.enums import QuizMode, DifficultyLevel, QuestionCategory, AnswerType, DistractorStrategy

class SettingsMenu:

    def __init__(self, settings: QuizSettings):
        self.settings = settings

    def _select_enum_value(self, enum_class, prompt: str):

        values = list(enum_class)

        for index, value in enumerate(values, start=1):
            print(f"{index}. {value.value}")

        while True:
            choice = input(prompt)

            try:
                index = int(choice) - 1

                if index < 0 or index >= len(values):
                    raise ValueError

                return values[index]

            except ValueError:
                print(f"Please enter a number between 1 and {len(values)}.")

    def _select_multiple_enum_values(self, enum_class, prompt: str):

        values = list(enum_class)

        for index, value in enumerate(values, start=1):
            print(f"{index}. {value.value}")

        print("\nEnter numbers separated by commas (e.g. 1,3,5): ")

        while True:
            choice = input(prompt)

            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]

                if any(index < 0 or index >= len(values) for index in indices):
                    raise ValueError

                return [values[index] for index in indices]

            except ValueError:
                print(f"Please enter valid numbers between 1 and {len(values)}.")

    def _clear_screen(self):
        os.system("clear")

    def run(self) -> QuizSettings:

        while True:

            display_settings(self.settings)

            choice = input("\nStart quiz with these settings? (Y/n): ").strip().lower()

            if choice in {"", "y", "yes"}:
                self._clear_screen()
                return self.settings

            if choice in {"n", "no"}:
                self._clear_screen()

                if self.modify_settings():
                    return self.settings

                self._clear_screen()
                display_settings(self.settings)

            else:
                print("Please enter Y or N.")

    # Main menu
    def modify_settings(self):
                
        while True:

            display_settings(self.settings)

            print("\n--- Modify settings ---\n")
            print("1. Change quiz mode")
            print("2. Change difficulty")
            print("3. Change regions")
            print("4. Change question categories")
            print("5. Change answer types")
            if AnswerType.MC in self.settings.answer_types:
                print("6. Change distractor strategies")
            print("99. START QUIZ")

            choice = input("\n> ").strip()

            match choice:
                case "1":
                    self._clear_screen()
                    self.change_quiz_mode()

                case "2":
                    self._clear_screen()
                    self.change_difficulty()
  
                case "3":
                    self._clear_screen()
                    self.specify_location_filter()
  
                case "4":
                    self._clear_screen()
                    self.select_categories()

                case "5":
                    self._clear_screen()
                    self.select_answer_types()

                case "6":
                    self._clear_screen()
                    self.select_distractor_strategies()

                case "99":
                    self._clear_screen()
                    return True

                case _:
                    print("\n Invalid option, try again")
                    continue

            self._clear_screen()

    # 1
    def change_quiz_mode(self):
        print("\n--- Change quiz mode ---")
        self.settings.quiz_mode = self._select_enum_value(QuizMode, "\nQuiz mode: ")
        self.settings = resolve_settings(self.settings)

    # 2
    def change_difficulty(self):
        print("\n--- Change difficulty ---")
        self.settings.difficulty_level = self._select_enum_value(DifficultyLevel, "\nDifficulty level: ")
        self.settings = resolve_settings(self.settings)

    # 3
    def specify_location_filter(self):
        raise NotImplementedError

    # 4
    def select_categories(self):
        print("\n--- Change question categories ---")
        self.settings.question_categories = (self._select_multiple_enum_values(QuestionCategory, "\nQuestion categories: "))
        self.settings = resolve_settings(self.settings)

    # 5
    def select_answer_types(self):
        self.settings.answer_types = (self._select_multiple_enum_values(AnswerType, "\nAnswer types: "))
        self.settings = resolve_settings(self.settings)

    # 6
    def select_distractor_strategies(self):
        if AnswerType.MC not in self.settings.answer_types:
            print("This option is not available. Add multiple choice answer type first!")
            input("\nPress Enter to return...")
        else:
            self.settings.distractor_strategies = (self._select_multiple_enum_values(DistractorStrategy, "\nDistractor strategies: "))
            self.settings = resolve_settings(self.settings)