from datetime import datetime
import re


class View:
    """Inputs and outputs of user's console interface
    Management of user's input errors for this view"""

    REQUIRED_FIELDS = {"last_name", "first_name", "birthdate",
                       "tournament_name", "tournament_place"}

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
            print(f"Choix invalide ;"
                  f"veuillez choisir entre 1 et {max_options}")

    def get_confirmation_choice(self, prompt):
        """Generic method for retrieving the selection of yes/no questions
        and handling errors"""
        while True:
            choice = input(prompt).strip().lower()
            if choice not in ("y", "n"):
                print('Choix invalide; veuillez choisir entre "y" et "n"')
            else:
                return choice

    def validate_field(self, field, value):
        """Generic method for handling required input fields
        and managing errors"""
        if field in self.REQUIRED_FIELDS and value.strip() != "":
            return True
        if field in self.REQUIRED_FIELDS and value.strip() == "":
            print("Erreur, champ obligatoire")
            return False
        if field not in self.REQUIRED_FIELDS:
            return True

    def get_menu_choice(self):
        """Display the menu and obtain the user's choice"""
        print("="*42)
        print(" "*10 + "==== Bienvenue ====" + " "*10)
        print("="*42)
        options = ["Démarrer un nouveau tournoi",
                   "Enregistrer un nouveau joueur",
                   "Afficher les rapports",
                   "Continuer un tournoi en cours",
                   "Quitter"]
        self.display_options(options)
        return self.get_validated_choice(len(options))

    def get_tournament_choice(self):
        """Confirmation of the "new tournament" selection"""
        return self.get_confirmation_choice("Voulez-vous démarrer "
                                            "un nouveau tournoi (y/n) ?\n")

    def get_save_players_choice(self):
        """Confirmation of the "save player" selection"""
        return self.get_confirmation_choice("Enregistrer un "
                                            "nouveau joueur (y/n) ?\n")

    def get_quit_confirmation(self):
        """Confirmation of the "quit" selection"""
        return self.get_confirmation_choice("Etes-vous sûr de "
                                            "vouloir quitter (y/n) ?\n")

    def get_player_datas(self):
        """Display and obtain input regarding the fields for adding players.
        Manages input compliance."""
        player_datas_field = {
                            "last_name": "Nom du joueur",
                            "first_name": "Prénom du joueur",
                            "birthdate": "Date de naissance (DD/MM/YYYY)",
                            "chess_id": "Identifiant national d'échec "
                            "(appuyer sur Entrée pour passer)"
                                }
        player_datas = {}
        for field, prompt in player_datas_field.items():
            while True:
                value = input(f"- {prompt}: ")
                if field == "birthdate":
                    if self.validate_date_format(value):
                        player_datas[field] = value
                        break
                    continue
                if field == "chess_id":
                    if self.validate_id_format(value):
                        player_datas[field] = value
                        break
                    continue
                if self.validate_field(field, value):
                    player_datas[field] = value
                    break
        return player_datas

    def validate_date_format(self, date_str):
        """Generic method for verifying the validity of birth dates"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            print("Erreur, champ obligatoire, format DD/MM/YYYY requis")
            return False

    def validate_id_format(self, id_str):
        """Generic method for verifying the validity of national chess id"""
        if not id_str.strip():
            return True
        if bool(re.match(r"[A-Z]{2}[0-9]{5}", id_str)):
            return True
        else:
            print("Erreur, format AB12345 requis")
            return False

    def get_tournament_datas(self):
        """Display and obtain input regarding the fields for new tournament.
        Manages input compliance."""
        print("="*42)
        tournament_datas_field = {
                                "tournament_name": "Nom du tournoi",
                                "tournament_place": "Lieu du tournoi",
                                "tournament_comment": "Remarques du "
                                "directeur (appuyer sur Entrée pour passer)"
                                 }
        tournament_datas = {}
        for field, prompt in tournament_datas_field.items():
            while True:
                value = input(f"- {prompt}: ")
                if self.validate_field(field, value):
                    tournament_datas[field] = value
                    break
        return tournament_datas

    def get_tournament_menu_choice(self):
        """Display and obtain input regarding tournament menu"""
        print("="*42)
        options = ["Ajouter un joueur",
                   "Démarrer le tournoi"]
        self.display_options(options)
        return self.get_validated_choice(len(options))

    def get_tournament_player_type_choice(self):
        """Display and obtain input regarding about the menu
        for adding players to the tournament"""
        print("="*42)
        print("=== Inscription des joueurs au tournoi ===")
        print("="*42)
        options = ["Enregistrer un nouveau joueur et "
                   "l'inscire au tournoi.",
                   "Inscrire un joueur déjà enregistré."]
        self.display_options(options)
        return self.get_validated_choice(len(options))

    def display_saved_players_list(self, saved_players_list):
        "Display a list of all the already saved players in the program"
        print("="*42)
        print("Choisissez un joueur dans la liste :")
        for index, file in enumerate(saved_players_list, 1):
            print(f"{index} - {file.replace(".json", "").replace("_", " ")}")

    def display_no_saved_players_error(self):
        """Display a specific error indicating
        that no players are saved to the programm."""
        print("Aucun joueur enregistré, "
              "veuillez d'abord enregistrer un joueur.")

    def get_saved_player_choice(self, saved_players_list):
        """Get the saved player's selection choice"""
        options = saved_players_list
        self.display_saved_players_list(options)
        choice = int(self.get_validated_choice(len(options)))
        return saved_players_list[choice - 1]

    def display_added_player_error(self):
        """Display a specific error indicating
        that a players is already registered to a tournament."""
        print("Erreur, ce joueur est déjà inscrit au tournoi")

    def display_no_player_error(self):
        """Display a specific error indicating
        that no players are registered to a tournament"""
        print("Erreur, veuillez d'abord ajouter des joueurs au tournoi.")

    def get_tournament_start_choice(self):
        """Confirmation of the "start tournament" selection"""
        return self.get_confirmation_choice("Prêt à démarrer le "
                                            "tournoi (y/n) ?\n")

    def display_tournament_summary(self, tournament):
        """Summarize the tournament's data before start"""
        print("="*42)
        print(f"Le {tournament.name} de {tournament.place} "
              f"à commencé le {tournament.tournament_start_date} ")
        if tournament.description:
            print(tournament.description)
        print("="*21)
        print("Joueurs :")
        print(", ".join(f"{player.last_name.upper()} {player.first_name}"
                        for player in tournament.players_list))
        print("="*21)

    def get_new_round_start_choice(self):
        """Confirmation of the "start new round" selection"""
        return self.get_confirmation_choice("Prêt à démarrer le "
                                            "premier tour (y/n) ?\n")
