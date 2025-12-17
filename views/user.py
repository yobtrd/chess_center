from views.generic import GenericView


class UserView:
    """Inputs and outputs of user's console interface"""

    def __init__(self):
        """Initializes access to generic view methods."""
        self.generic = GenericView()

    # Get methods
    def get_menu_choice(self):
        """Displays the menu and obtain the user's choice."""
        self.generic.display_principal_header("Menu principal")
        options = ["Démarrer un nouveau tournoi",
                   "Enregistrer un nouveau joueur",
                   "Afficher les rapports",
                   "Continuer un tournoi en cours",
                   "Quitter"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_player_datas(self):
        """Displays and obtain input regarding the fields for new player."""
        self.generic.display_level_three_header("Veuillez saisir "
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
        """Displays and obtain input regarding the fields
        for new tournament."""
        self.generic.display_level_three_header("Veuillez saisir les "
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
        """Displays and obtain input regarding tournament menu."""
        self.generic.display_principal_header("Menu du tournoi")
        options = ["Inscrire des joueurs au tournoi",
                   "Démarrer le tournoi",
                   "Annuler et retourner au menu principal"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_tournament_player_menu_choice(self, counter):
        """Displays and obtain input regarding about the menu
        for adding players to the tournament."""
        self.generic.display_principal_header("Inscription des joueurs "
                                              "au tournoi")
        self.display_counter(counter)
        options = ["Inscrire des joueurs déjà enregistrés avec leur "
                   "identifiant national d'échec (INE)",
                   "Inscrire des joueurs déjà enregistrés via une liste",
                   "Enregistrer un nouveau joueur et "
                   "l'inscire au tournoi",
                   "Retourner au menu du tournoi"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_saved_player_choice(self, saved_players_list):
        """Get the saved player's selection choice"""
        options = saved_players_list
        choice = int(self.generic.get_validated_choice(len(options)))
        return saved_players_list[choice - 1]

    def get_match_result(self, match_number, match):
        """Get the results of the current match."""
        message = (f"Enregistrer les résultats pour le match {match_number}:")
        self.generic.display_level_three_header(message)
        options = [f"{match.player1.last_name.upper()} "
                   f"{match.player1.first_name} remporte le match",
                   f"{match.player2.last_name.upper()} "
                   f"{match.player2.first_name} remporte le match",
                   "Match nul"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    # Display methods
    def display_saved_players_list(self, saved_players_list):
        "Displays a list of all the already saved players in the program."
        self.generic.display_level_three_header("Choisissez un joueur "
                                                "dans la liste:")
        for i, player in enumerate(saved_players_list, 1):
            print(f"{i} - {player["last_name"].upper()} "
                  f"{player["first_name"]}")

    def display_tournament_summary(self, tournament):
        """Summarize the tournament's data before start."""
        message = (f"Le {tournament.name} de {tournament.place} "
                   f"à commencé le {tournament.tournament_start_date}")
        self.generic.display_principal_header(message)
        if tournament.description:
            print(tournament.description)
            print("-"*62)
        print("Joueurs inscrits:\n")
        print(", ".join(f"{player.last_name.upper()} {player.first_name}"
                        for player in tournament.players_list))
        print("-"*62)

    def display_add_player_by_id_message(self):
        return input("Veuillez inscrire l'INE du joueur à enregister: ")

    def display_counter(self, counter):
        """Displays the number of players currently registered
        for the tournament."""
        return print(f"Joueur(s) actuellement inscrit(s): "
                     f"{counter}\n" + "-"*62)

    def display_registered_player_succes(self):
        return print("Joueur inscrit !")

    def display_saved_player_success(self):
        return print("Joueur sauvegardé.")

    def display_round_start(self, round):
        self.generic.display_level_two_header(f"Le {round.name} démarre à "
                                              f"{round.round_start_date}")

    def display_round_end(self, round):
        print("\n" + "-" * 62)
        print(" "*8 + f"Le {round.name} fini à {round.round_end_date}")

    def display_matches(self, matches):
        """Displays the paired players for the differents matches."""
        print("Matchs de ce round:\n")
        for i, match in enumerate(matches, 1):
            print(f"- Match {i}: {match.player1.last_name.upper()} "
                  f"{match.player1.first_name} VS "
                  f"{match.player2.last_name.upper()} "
                  f"{match.player2.first_name}")

    def display_results_summary(self, matches_list, round):
        """Displays the end of round summary with matches results."""
        print("\n" + "=" * 62)
        print(f"Résultat du {round.name}:\n")
        for i, match in enumerate(matches_list, 1):
            print(f"Match {i} : {match.match_result[0][0].last_name.upper()} "
                  f"{match.match_result[0][0].first_name}: "
                  f"{match.match_result[0][1]} - "
                  f"{match.match_result[1][0].last_name.upper()} "
                  f"{match.match_result[1][0].first_name}: "
                  f"{match.match_result[1][1]}")

    def display_scores(self, sorted_players):
        """displays the updated scoreboard."""
        self.generic.display_level_three_header("Tableau des scores:")
        for rank, player in enumerate(sorted_players, 1):
            print(f"{rank}. {player.last_name.upper()} {player.first_name}: "
                  f"{player.score}")
        print("=" * 62)

    def display_tournament_end_summary(self, tournament, scoreboard):
        """Displays the end-of-tournament summary and
        the name of the winner(s)."""
        message = (f"Le {tournament.name} a fini le "
                   f"{tournament.tournament_end_date} !\n "
                   "Le gagnant de ce tournoi est "
                   f"{scoreboard[0].first_name.upper()} "
                   f"{scoreboard[0].last_name.upper()} !")
        self.generic.display_principal_header(message)

    # Display Confirmation methods
    def get_tournament_choice(self):
        """Confirmation of the "new tournament" selection."""
        return self.generic.get_confirmation_choice("Démarrer un nouveau "
                                                    "tournoi")

    def get_save_players_choice(self):
        """Confirmation of the "save player" selection."""
        return self.generic.get_confirmation_choice("Enregistrer un "
                                                    "nouveau joueur")

    def get_quit_choice(self):
        """Confirmation of the "quit" selection."""
        return self.generic.get_confirmation_choice("Etes-vous sûr "
                                                    "de vouloir quitter")

    def get_tournament_start_choice(self):
        """Confirmation of the "start tournament" selection."""
        return self.generic.get_confirmation_choice("Prêt à démarrer le "
                                                    "tournoi")

    def get_back_to_menu_choice(self):
        """Confirmation for the return to the menu."""
        return self.generic.get_confirmation_choice("Êtes-vous sûr de vouloir "
                                                    "annuler et revenir au "
                                                    "menu principal")

    def get_add_another_player_choice(self):
        """Confirmation regarding player additions to the tournament."""
        return self.generic.get_confirmation_choice("Inscrire un autre joueur")

    def get_save_another_player_choice(self):
        """Confirmation regarding player save."""
        return self.generic.get_confirmation_choice("Enregistrer un autre "
                                                    "joueur")

    def get_first_round_start_validation(self):
        """Validates the start of the first round."""
        return self.generic.check_press_enter_prompt("démarrer le "
                                                     "premier tour")

    def get_next_round_start_validation(self):
        """Validates the start of the next round."""
        return self.generic.check_press_enter_prompt("démarrer le "
                                                     "prochain tour")

    def get_end_round_validation(self):
        """Validates the start of the end of the round."""
        return self.generic.check_press_enter_prompt("finir le tour "
                                                     "enregistrer les "
                                                     "résultats "
                                                     "des matchs")

    def get_end_tournament_validation(self):
        """Validates the start of the end of the tournament."""
        return self.generic.check_press_enter_prompt("retourner au menu "
                                                     "principal")

    def get_back_to_tournament_menu_validation(self):
        """Validates the return in the tournament menu."""
        return self.generic.check_press_enter_prompt("retourner au menu "
                                                     "du tournoi")

    # Display specific errors methods
    def display_no_saved_players_error(self):
        print("Aucun joueur enregistré, "
              "veuillez d'abord enregistrer un joueur.")

    def display_already_added_player_error(self):
        print("Attention, ce joueur est déjà inscrit au tournoi.")

    def display_players_numbers_error(self):
        print("Attention, un nombre de joueur pair et au moins égal à "
              "deux est nécessaire avant de pouvoir démarrer un tournoi.")

    def display_no_id_match_error(self):
        print('Cet INE ne correspond à aucun joueur enregistré '
              '(Format "AB12345" requis).')
