import os

from quiz_game.models.settings import QuizSettings, LocationFilter

from quiz_game.cli.display import display_settings, display_gameplay_settings

from quiz_game.config.resolver import resolve_settings
from quiz_game.config.enums import QuizMode, DifficultyLevel, QuestionCategory, AnswerType, DistractorStrategy

from utils.corrections.country_transformations import REGION_MAP, SUBREGION_MAP

class SettingsMenu:

    def __init__(self, settings: QuizSettings):
        self.settings = settings

    def _select_multiple_strings(self, values: list[str], prompt: str,) -> set[str]:

        for index, value in enumerate(values, start=1):
            print(f"{index}. {value}")

        print("\nEnter numbers separated by commas.")
        print("Press Enter to select none.")

        while True:
            choice = input(prompt).strip()

            if not choice:
                return set()

            try:
                indices = [int(value.strip()) - 1 for value in choice.split(",")]

                if any(index < 0 or index >= len(values) for index in indices):
                    raise ValueError

                return {values[index] for index in indices}

            except ValueError:
                print(f"Please enter valid numbers between 1 and {len(values)}.")

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
            if self.settings.quiz_mode == QuizMode.CUSTOM:
                print("7. Change gameplay settings")
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

                case "7":
                    self._clear_screen()
                    self.gameplay_settings_menu()

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
        self.settings = resolve_settings(self.settings, resolve_custom_settings=True)

    # 2
    def change_difficulty(self):
        print("\n--- Change difficulty ---")
        self.settings.difficulty_level = self._select_enum_value(DifficultyLevel, "\nDifficulty level: ")
        self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

    # 3
    def specify_location_filter(self):
        
        regions = list(REGION_MAP.values())
        subregions = list(SUBREGION_MAP.values())

        while True:

            print("\n--- Change regions ---")

            current_filter = self.settings.location_filter
            current_regions = (", ".join(sorted(current_filter.include_regions)) if current_filter.include_regions else "All regions")
            current_subregions = (", ".join(sorted(current_filter.include_subregions)) if current_filter.include_subregions else "All subregions")

            print(f"Included regions: {current_regions}")
            print(f"Included subregions: {current_subregions}")
            print("")
            print("1. Select regions")
            print("2. Select subregions")
            print("3. Include the whole world")
            print("4. Back")

            choice = input("\n> ").strip()

            match choice:

                case "1":
                    self._clear_screen()

                    selected_regions = (self._select_multiple_strings(regions, "\nRegions: ",))

                    print(selected_regions)

                    self.settings.location_filter.include_regions = (selected_regions)                
                    self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

                    self._clear_screen()

                case "2":
                    self._clear_screen()

                    selected_subregions = (self._select_multiple_strings(subregions, "\nSubregions: ",))

                    self.settings.location_filter.include_subregions = (selected_subregions)
                    self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

                    self._clear_screen()

                case "3":
                    self.settings.location_filter = LocationFilter()

                    self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

                    self._clear_screen()

                case "4":
                    self._clear_screen()
                    return

                case _:
                    print("\nInvalid option, try again.")

    # 4
    def select_categories(self):
        print("\n--- Change question categories ---")
        self.settings.question_categories = (self._select_multiple_enum_values(QuestionCategory, "\nQuestion categories: "))
        self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

    # 5
    def select_answer_types(self):
        self.settings.answer_types = (self._select_multiple_enum_values(AnswerType, "\nAnswer types: "))
        self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

    # 6
    def select_distractor_strategies(self):
        if AnswerType.MC not in self.settings.answer_types:
            print("This option is not available. Add multiple choice answer type first!")
            input("\nPress Enter to return...")
            self._clear_screen()

        self.settings.distractor_strategies = (self._select_multiple_enum_values(DistractorStrategy, "\nDistractor strategies: "))
        self.settings = resolve_settings(self.settings, resolve_custom_settings=False)

    # 7
    def gameplay_settings_menu(self):
        if self.settings.quiz_mode != QuizMode.CUSTOM:
            print("This option is not available. Add multiple choice answer type first!")
            input("\nPress Enter to return...")
            self._clear_screen()

        while True:

            display_gameplay_settings(self.settings)

            print("\n--- Modify custom settings ---\n")
            print("1. Set number of lives")
            print("2. Set time per question")
            print("3. Set total time")
            print("4. Set total number of questions")
            print("5. Toggle question recycling")
            print("6. Toggle infinite mode")
            print("7. Back to main menu")

            choice = input("\n> ").strip()

            match choice:
                case "1":
                    self._clear_screen()
                    self.set_lives()

                case "2":
                    self._clear_screen()
                    self.set_time_per_question()

                case "3":
                    self._clear_screen()
                    self.set_total_time()

                case "4":
                    self._clear_screen()
                    self.set_total_question_number()

                case "5":
                    self._clear_screen()
                    self.settings.gameplay.question_recycling = True if self.settings.gameplay.question_recycling == False else False
                    #self.settings = resolve_settings(self.settings, resolve_custom_settings=False)
                    continue

                case "6":
                    self._clear_screen()
                    self.settings.gameplay.infinite_mode = True if self.settings.gameplay.infinite_mode == False else False
                    #self.settings = resolve_settings(self.settings, resolve_custom_settings=False)
                    continue

                case "7":
                    self._clear_screen()
                    return True

                case _:
                    print("\n Invalid option, try again")
                    continue

            self._clear_screen()

    def set_lives(self):
        print("\n--- Set number of lives ---")

        while True:
            print("Enter a number between 1 and 25 (or 0 to disable):")
            choice = input("\n> ").strip()

            try:
                lives = int(choice)

                if lives < 0 or lives > 25:
                    raise ValueError

                break

            except ValueError:
                print(f"Incorrect value entered, please try again...")

        if lives == 0:
            lives = None    
        
        self.settings.gameplay.lives = lives  

    def set_time_per_question(self):
        print("\n--- Set time per question ---")

        while True:
            print("Enter an amount of seconds between 3 and 120:")
            print("(or enter 0 to disable question time)")

            choice = input("\n> ").strip()

            try:
                time = int(choice)

                if time != 0 and (time < 3 or time > 120):
                    raise ValueError

                break

            except ValueError:
                print(f"Incorrect value entered, please try again...")

        if time == 0:
            time = None    
        
        self.settings.gameplay.question_time = time

    def set_total_time(self):
        print("\n--- Set total time ---")

        while True:
            print("Enter an amount of seconds:")
            print("(or enter 0 to disable the time limit)")

            choice = input("\n> ").strip()

            try:
                time = int(choice)

                if time != 0 and time < 60:
                    raise ValueError

                break

            except ValueError:
                print(f"Incorrect value entered, please try again...")

        if time == 0:
            time = None    
        
        self.settings.gameplay.total_time = time

    def set_total_question_number(self):
        print("\n--- Set total number of questions ---")

        while True:
            print("Enter a number greater than 0 (or 0 to disable):")
            choice = input("\n> ").strip()

            try:
                number = int(choice)

                if number < 0:
                    raise ValueError

                break

            except ValueError:
                print(f"Incorrect value entered, please try again...")
                #print(f"Please enter a number greater than 0 (or 0 to disable).")

        if number == 0:
            number = None    
        
        self.settings.gameplay.num_questions = number

        