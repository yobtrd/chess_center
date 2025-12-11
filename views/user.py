from views.generic import GenericView


class UserView:
    """Inputs and outputs of user's console interface"""

    def __init__(self):
        self.generic = GenericView()

    # Get methods
    def get_menu_choice(self):
        """Display the menu and obtain the user's choice"""
        self.generic.display_menu_header("Bienvenue")
        options = ["Démarrer un nouveau tournoi",
                   "Enregistrer un nouveau joueur",
                   "Afficher les rapports",
                   "Continuer un tournoi en cours",
                   "Quitter"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_player_datas(self):
        """Display and obtain input regarding the fields for new player."""
        self.generic.display_selection_header("Veuillez saisir "
                                              "les informations du joueur:")
        fields_config = {
            "last_name": ("Nom du joueur", True, None),
            "first_name": ("Prénom du joueur", True, None),
            "birthdate": ("Date (DD/MM/YYYY)",
                          True, self.generic.validate_date_format),
            "chess_id": ("ID national (AB12345)",
                         True, self.generic.validate_id_format)
        }
        player_datas = {}
        for field, config in fields_config.items():
            prompt, required, validated = config
            player_datas[field] = (
                self.generic.get_validated_input(prompt, required, validated))
        return player_datas

    def get_tournament_datas(self):
        """Display and obtain input regarding the fields for new tournament."""
        self.generic.display_selection_header("Veuillez saisir les "
                                              "informations du tournois:")
        fields_config = {
            "tournament_name": ("Nom du tournoi", True, None),
            "tournament_place": ("Lieu du tournoi", True, None),
            "tournament_start_date": ("Date du tournoi",
                                      True, self.generic.validate_date_format),
            "tournament_comment": ("Remarques du directeur "
                                   "(appuyer sur Entrée pour passer)",
                                   False, None)
        }
        tournament_datas = {}
        for field, config in fields_config.items():
            prompt, required, validated = config
            tournament_datas[field] = (
                self.generic.get_validated_input(prompt, required, validated))
        return tournament_datas

    def get_tournament_menu_choice(self):
        """Display and obtain input regarding tournament menu"""
        self.generic.display_menu_header("Menu du tournoi")
        options = ["Inscrire des joueurs au tournoi",
                   "Démarrer le tournoi",
                   "Annuler et retourner au menu principal"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_tournament_player_menu_choice(self, counter):
        """Display and obtain input regarding about the menu
        for adding players to the tournament"""
        self.generic.display_menu_header("Inscription des joueurs au tournoi")
        self.display_counter(counter)
        options = ["Inscrire des joueurs déjà enregistrés avec leur "
                   "identifiant national d'échec (INE).",
                   "Inscrire des joueurs déjà enregistrés via une liste.",
                   "Enregistrer un nouveau joueur et "
                   "l'inscire au tournoi.",
                   "Retourner au menu du tournoi."]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_saved_player_choice(self, saved_players_list):
        """Get the saved player's selection choice"""
        options = saved_players_list
        choice = int(self.generic.get_validated_choice(len(options)))
        return saved_players_list[choice - 1]

    # Display methods
    def display_saved_players_list(self, saved_players_list):
        "Display a list of all the already saved players in the program"
        self.generic.display_selection_header("Choisissez un joueur "
                                              "dans la liste:")
        for i, player in enumerate(saved_players_list, 1):
            print(f"{i} - {player["last_name"].upper()} "
                  f"{player["first_name"]}")

    def display_tournament_summary(self, tournament):
        """Summarize the tournament's data before start"""
        self.generic.display_menu_header(f"Le {tournament.name} "
                                         f"de {tournament.place} "
                                         f"à commencé le "
                                         f"{tournament.tournament_start_date}")
        if tournament.description:
            print(tournament.description)
            print("-"*42)
        print("Joueurs inscrits:")
        print(", ".join(f"{player.last_name.upper()} {player.first_name}"
                        for player in tournament.players_list))
        print("-"*42)

    def display_add_player_by_id_message(self):
        return input("Veuillez inscrire l'INE du joueur à enregister: ")

    def display_counter(self, counter):
        """displays a counter showing the number of players currently
        registered for the tournament"""
        return print(f"Joueur(s) actuellement inscrit(s): "
                     f"{counter}\n" + "-"*42)

    def display_registered_player_succes(self):
        return print("Joueur inscrit !")

    def display_saved_player_success(self):
        return print("Joueur sauvegardé.")

    # Display Confirmation methods
    def get_tournament_choice(self):
        """Confirmation of the "new tournament" selection"""
        return self.generic.get_confirmation_choice("Démarrer un nouveau "
                                                    "tournoi")

    def get_save_players_choice(self):
        """Confirmation of the "save player" selection"""
        return self.generic.get_confirmation_choice("Enregistrer un "
                                                    "nouveau joueur")

    def get_quit_choice(self):
        """Confirmation of the "quit" selection"""
        return self.generic.get_confirmation_choice("Etes-vous sûr "
                                                    "de vouloir quitter")

    def get_tournament_start_choice(self):
        """Confirmation of the "start tournament" selection"""
        return self.generic.get_confirmation_choice("Prêt à démarrer le "
                                                    "tournoi")

    def get_back_to_menu_choice(self):
        """Confirmation for the return to the menu"""
        return self.generic.get_confirmation_choice("Êtes-vous sûr de vouloir "
                                                    "annuler et revenir au "
                                                    "menu principal ?")

    def get_new_round_start_choice(self):
        """Confirmation of the "start new round" selection"""
        return self.generic.get_confirmation_choice("Prêt à démarrer "
                                                    "le premier tour")

    def get_add_another_player_choice(self):
        """Confirmation regarding player additions to the tournament"""
        return self.generic.get_confirmation_choice("Inscrire un autre joueur")

    def get_save_another_player_choice(self):
        """Confirmation regarding player save"""
        return self.generic.get_confirmation_choice("Enregistré "
                                                    "un autre joueur")

    # Display specific errors methods
    def display_no_saved_players_error(self):
        """Display a specific error indicating
        that no players are saved to the programm."""
        print("Aucun joueur enregistré, "
              "veuillez d'abord enregistrer un joueur.")

    def display_already_added_player_error(self):
        """Display a specific error indicating
        that a players is already registered to a tournament."""
        print("Attention, ce joueur est déjà inscrit au tournoi")

    def display_players_numbers_error(self):
        """Display a specific error indicating
        that that the number of players is not correct to start a tournament"""
        print("Attention, un nombre de joueur pair et au moins égal à "
              "deux est nécessaire avant de pouvoir démarrer un tournoi.")

    def display_no_id_match_error(self):
        print('Cet INE ne correspond à aucun joueur enregistré '
              '(Format "AB12345" requis)')
