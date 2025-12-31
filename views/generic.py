from datetime import datetime
import re


class GenericView:
    """Manages all the generic methods for the user input errors."""

    DEFAULT_WIDTH = 82

    def get_confirmation_choice(self, prompt, yes="y", no="n"):
        """Manages yes/no questions and related inputs errors."""
        while True:
            choice = input(f"{prompt} ({yes}/{no}) ?\n").strip().lower()
            if choice == yes:
                return True
            if choice == no:
                return False
            print(f'Veuillez entrer "{yes}" pour confirmer ou '
                  f'"{no}" pour annuler\n')

    def display_options(self, options):
        """Enumerates multiple choices menu."""
        for i, option, in enumerate(options, 1):
            print(f"{i} - {option}")

    def get_validated_choice(self, max_options):
        """Manages multiple-choice selections and related errors."""
        while True:
            choice = input("Choix: ")
            if choice.isdigit() and 1 <= int(choice) <= max_options:
                return choice
            print("Choix invalide, "
                  f"veuillez choisir entre 1 et {max_options}")

    def get_return_or_validated_choice(self, max_options):
        while True:
            choice = input("Choix: ").upper()
            if choice.isdigit() and 1 <= int(choice) <= max_options:
                return choice
            if choice == "R":
                return False
            print("Choix invalide, "
                  f'veuillez choisir entre 1 et {max_options} '
                  'ou "R" pour revenir en arrière')

    def get_validated_input(self, prompt, required, validated):
        """checks the validation of data entered by the user in the field.
        required True is a requided field.
        validated True valid a specific format needed."""
        while True:
            value = input(f"- {prompt}: ").strip()
            if required and not value:
                print("Ce champ est obligatoire")
                continue
            if validated and not validated(value):
                continue
            return value

    def check_press_enter_prompt(self, prompt):
        """Blocking method waiting for Enter key press."""
        while True:
            if not input(f"\nAppuyer sur Entrée pour {prompt}...").strip():
                return
            print("Veuillez appuyer uniquement sur Entrée pour continuer.")

    def validate_date_format(self, date_str):
        """Checks the validity of birth dates."""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            print("Un format DD/MM/YYYY est requis")
            return False

    def validate_id_format(self, id_str):
        """Checks the validity of national chess id."""
        if bool(re.match(r"[A-Z]{2}[0-9]{5}$", id_str)):
            return True
        else:
            print('Un format "AB12345" est requis')
            return False

    def validate_round_format(self, round_str):
        """Checks the validity of total rounds numbers."""
        if not round_str.strip():
            return True
        try:
            if int(round_str) <= 0:
                raise ValueError
        except ValueError:
            print("Appuyer uniquement sur Entrée pour laisser le nombre "
                  "de tours par défaut (4) ou saisissez un nombre "
                  "supérieur à 0")
            return False
        return True

    def display_principal_header(self, title, width=DEFAULT_WIDTH, char="="):
        """Displays a level 1 header with a center title."""
        separator = char * width
        title_line = f"-== {title} ==-"
        padding = (width - len(title_line)) // 2
        print(f"\n{separator}\n{' ' * padding}{title_line}\n{separator}")

    def display_level_two_header(self, message, width=DEFAULT_WIDTH, char="-"):
        """Displays a level 2 header."""
        separator = char * width
        padding = (width - len(message)) // 2
        print(f"\n{separator}\n{' ' * padding}{message}\n{separator}")

    def display_level_three_header(self, message,
                                   width=DEFAULT_WIDTH, char="-"):
        """Displays a level 3 header with underline."""
        separator = char * width
        underline = char * len(message)
        print(f"{separator}\n{message}\n{underline} ")

    def display_winner_header(self, message, winner,
                              width=DEFAULT_WIDTH, char="*"):
        """Displays header for winner message."""
        separator = f"{char * width}\n{char * width}"
        winner_line = f"*** {winner} ***"
        padding_one = (width - len(winner_line)) // 2
        padding_two = (width - len(message)) // 2
        print(f"\n{separator}\n{' ' * padding_two}{message}\n\n"
              f"{' ' * padding_one}{winner_line}\n\n{separator}")

    def display_separator_level_one(self, width=DEFAULT_WIDTH):
        """Separator for the wiew."""
        print("=" * width)

    def display_separator_level_two(self, width=DEFAULT_WIDTH):
        """Separator for the wiew."""
        print("-" * width)
