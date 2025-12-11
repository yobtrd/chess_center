from datetime import datetime
import re


class GenericView:
    """Manage all the generic methods for the user input errors"""

    def get_confirmation_choice(self, prompt, yes="y", no="n"):
        """Generic method for retrieving the selection of yes/no questions
        and handling errors"""
        while True:
            choice = input(f"{prompt} ({yes}/{no}) ?\n").strip().lower()
            if choice == yes:
                return True
            if choice == no:
                return False
            print(f'Veuillez entrer "{yes}" pour confirmer ou '
                  f'"{no}" pour annuler')

    def display_options(self, options):
        """Generic method for enumerating multiple choices menu"""
        for i, option, in enumerate(options, 1):
            print(f"{i} - {option}")

    def get_validated_choice(self, max_options):
        """Generic method for retrieving multiple-choice selections
        and handling errors"""
        while True:
            choice = input("Choix: ")
            if choice.isdigit() and 1 <= int(choice) <= max_options:
                return choice
            print(f"Choix invalide; "
                  f"veuillez choisir entre 1 et {max_options}")

    def get_validated_input(self, prompt, required, validated):
        """Generic method to verify the user's input validation.
        required True is a requided field,
        validated True valid a specific format needed"""
        while True:
            value = input(f"- {prompt}: ").strip()
            if required and not value:
                print("Ce champ est obligatoire")
                continue
            if validated and not validated(value):
                continue
            return value

    def validate_date_format(self, date_str):
        """Generic method for verifying the validity of birth dates"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            print("Un format DD/MM/YYYY est requis")
            return False

    def validate_id_format(self, id_str):
        """Generic method for verifying the validity of national chess id"""
        if bool(re.match(r"[A-Z]{2}[0-9]{5}", id_str)):
            return True
        else:
            print('Un format "AB12345" est requis')
            return False

    def display_menu_header(self, title, width=42, char="="):
        """Display the menus headers with a center title"""
        separator = char * width
        title_line = f"=== {title} ==="
        padding = (width - len(title_line)) // 2
        print(f"{separator}\n{' ' * padding}{title_line}\n{separator}")

    def display_selection_header(self, description, width=42, char="-"):
        """Display a header when a selection is done"""
        separator = char * width
        print(f"{separator}\n{description}\n{separator}")
