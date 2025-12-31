from views.generic import GenericView


class UserView:
    """Inputs and outputs of user's console interface"""

    def __init__(self):
        """Initializes access to generic view methods."""
        self.generic = GenericView()

    # Get methods
    def get_main_menu_choice(self):
        """Displays the menu and obtain the user's choice."""
        self.generic.display_principal_header("Menu principal")
        options = ["Démarrer un nouveau tournoi",
                   "Enregistrer un nouveau joueur",
                   "Reprendre un tournoi en cours",
                   "Générer des rapports",
                   "Quitter"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_player_datas(self):
        """Displays and obtain input regarding the fields for new player."""
        self.generic.display_level_three_header("Veuillez saisir "
                                                "les informations du joueur")
        fields_config = {
            "last_name": ("Nom de famille du joueur", True, None),
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
                                                "informations du tournois")
        fields_config = {
            "name": ("Nom du tournoi", True, None),
            "place": ("Lieu du tournoi", True, None),
            "start_date": ("Date du tournoi (DD/MM/YYYY)", True,
                           self.generic.validate_date_format),
            "total_rounds": ("Nombre de tours (appuyer sur Entrée pour "
                             "laisser sur 4 tours par défaut)", False,
                             self.generic.validate_round_format),
            "comment": ("Remarques du directeur (appuyer sur Entrée pour "
                        "passer)", False, None)
        }
        tournament_datas = {}
        for field, config in fields_config.items():
            prompt, required, validated = config
            tournament_datas[field] = (
                self.generic.get_validated_input(prompt, required, validated))
        return tournament_datas

    def get_tournament_menu_choice(self, tournament):
        """Displays and obtain input regarding tournament menu."""
        self.generic.display_principal_header("Menu du tournoi")
        print(f"{tournament.name} de {tournament.place}")
        self.generic.display_separator_level_two()
        options = ["Accéder au menu d'inscription des joueurs",
                   "Démarrer le tournoi",
                   "Retourner au menu principal"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_tournament_player_menu_choice(self, counter):
        """Displays and obtain input regarding about the menu
        for adding players to the tournament."""
        self.generic.display_principal_header("Menu d'inscription")
        print(f"Joueur(s) actuellement inscrit(s): {counter}")
        self.generic.display_separator_level_two()
        options = ["Inscrire des joueurs déjà enregistrés avec leur "
                   "identifiant national d'échec",
                   "Inscrire des joueurs déjà enregistrés via une liste",
                   "Enregistrer un nouveau joueur et "
                   "l'inscire au tournoi",
                   "Voir les joueurs actuellement inscrits au tournoi",
                   "Retourner au menu du tournoi"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_saved_player_choice(self, saved_players_list):
        """Get the saved player's selection."""
        options = saved_players_list
        choice = int(self.generic.get_validated_choice(len(options)))
        return saved_players_list[choice - 1]

    def get_add_player_by_id_id(self):
        """Get the saved players INE input."""
        return input("Veuillez inscrire l'INE du joueur à enregister: ")

    def get_match_result(self, match_number, match):
        """Get the results of the current match."""
        message = (f"Enregistrer les résultats pour le match {match_number}")
        self.generic.display_level_three_header(message)
        options = [f"{match.player1.last_name.upper()} "
                   f"{match.player1.first_name} remporte le match",
                   f"{match.player2.last_name.upper()} "
                   f"{match.player2.first_name} remporte le match",
                   "Match nul"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_reports__main_menu_choice(self):
        """Displays the reports menu and obtain the user's choice."""
        self.generic.display_principal_header("Menu des rapports")
        options = ["Générer les rapports et les afficher dans le programme",
                   "Générer les rapports dans un fichier html",
                   "Retourner au menu principal"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_console_reports_menu_choice(self):
        """Displays the console reports menu and obtain the user's choice."""
        self.generic.display_level_two_header("Menu d'affichage des rapports")
        options = ["Afficher la liste des joueurs enregistrés",
                   "Afficher la liste des tournois précédents",
                   "Retourner au menu des rapports"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_report_tournament_choice(self, saved_tournament_list):
        """Get the tournament selection for its report."""
        options = saved_tournament_list
        choice = int(self.generic.get_return_or_validated_choice(len(options)))
        if choice:
            return saved_tournament_list[choice - 1]
        else:
            return False

    def get_tournament_report_choice(self, tournament_name):
        """Displays the console report menu and obtain the user's choice
        for an individual tournament."""
        self.generic.display_level_two_header(f"Rapports du {tournament_name}")
        options = ["Afficher la liste des joueurs de ce tournoi",
                   "Générer un rapport des rounds et des matchs de ce tournoi",
                   "Revenir à la liste des tournois"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    # Display methods
    def display_saved_players_list(self, saved_players_list):
        "Displays a list of all the already saved players in the program."
        self.generic.display_level_three_header("Choisissez un joueur "
                                                "dans la liste")
        for i, player in enumerate(saved_players_list, 1):
            print(f"{i} - {player["last_name"].upper()} "
                  f"{player["first_name"]}")

    def display_tournament_summary(self, tournament):
        """Summarize the tournament's data before start or resume."""
        message = (f"Le {tournament.name} de {tournament.place} "
                   f"a commencé le {tournament.start_date}")
        self.generic.display_principal_header(message)
        print(f"Nombres de tours: {tournament.total_rounds}")
        self.generic.display_separator_level_two()
        if tournament.description:
            print(tournament.description)
            self.generic.display_separator_level_two()
        print(f"Joueurs inscrits: {len(tournament.players_list)}")
        self.display_tournament_players_list(tournament)
        self.generic.display_separator_level_two()

    def display_tournament_players_list(self, tournament):
        """Displays a list of the actual players registered in tournament."""
        players = tournament.players_list
        player_lines = []
        for i in range(0, len(players), 5):
            chunk = players[i:i+5]
            player_lines.append(", ".join(
                f"{p.last_name.upper()} {p.first_name}" for p in chunk))
        print("\n" + "\n".join(player_lines))

    def display_registered_player_succes(self):
        print("Joueur inscrit !")

    def display_saved_player_success(self):
        print("\nJoueur sauvegardé.\n")

    def display_no_regisered_players(self):
        print("\nIl n'y a aucun joueurs inscrits pour le moment.")

    def display_round_start(self, round):
        """Displays the start of the round with its name and datetime"""
        message = (f"Le {round.name} a démarré le {round.start_date}")
        self.generic.display_level_two_header(message)

    def display_round_end(self, round):
        """Displays the end of the round with its name and datetime"""
        message = (f"Le {round.name} s'est terminé le {round.end_date}")
        self.generic.display_level_two_header(message)

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
        self.generic.display_separator_level_one()
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
        self.generic.display_separator_level_one()

    def display_tournament_end_summary(self, tournament):
        """Displays the end-of-tournament summary and
        the name of the winner(s)."""
        message = (f"Le {tournament.name} a fini le "
                   f"{tournament.end_date}")
        self.generic.display_principal_header(message)

    def display_tournament_winner(self, winner):
        """Displays the tournament winner."""
        winner = f"{winner.first_name.upper()} {winner.last_name.upper()}"
        message = "Le gagnant de ce tournoi est:"
        self.generic.display_winner_header(message, winner)

    def display_tournament_winners_tied(self, winners_tied):
        """Displays a message in cas of tieds winners."""
        winners_str = ", ".join(
            f"{w.first_name.upper()} {w.last_name.upper()}"
            for w in winners_tied
        )
        message = ("Le tournoi se termine sur des égalités ! "
                   "Les joueurs ex-aequo sont:")
        self.generic.display_winner_header(message, winners_str)

    def display_saved_message(self):
        print("\n- Tournoi sauvegardé -\n")

    def display_loaded_message(self):
        print("\n- Chargement du tournoi -")

    def display_match_resume(self, match_number, round):
        """Message displayed during loading for empty match results."""
        print(f"\n- Le chargement reprend à l'enregistrement des résultats "
              f"du match {match_number} du {round.name} -\n")

    def display_resume_completed_round(self, round):
        print(f"\n- Le chargement reprend à la fin du {round.name} -")

    def display_resume_not_ending_round(self, round):
        print("\n- Le chargement reprend après le départ du "
              f"{round.name} -")

    def display_resume_ended_round(self, round):
        print(f"\n- Le chargement reprend à la fin du {round.name} -\n")

    def display_players_list_console_report(self, saved_players):
        """Displays the list of saved players in the console."""
        print("\nListe des joueurs sauvegardés:\n")
        for i, player in enumerate(saved_players, 1):
            print(
                f"{i}. {player["last_name"].upper()} {player["first_name"]} "
                f"({player["birthdate"]}) | INE: {player["chess_id"]}"
            )

    def display_tournaments_list_report(self, saved_tournaments):
        """Displays the list of completed tournaments in the console."""
        self.generic.display_level_two_header("Liste des tournois")
        print('Choisissez un tournoi dans la liste pour afficher des rapports '
              'le concernant,\nou entrer "R" pour retourner '
              'en arrière\n')
        for i, tournament in enumerate(saved_tournaments, 1):
            print(
                f"{i} - {tournament["tournament_datas"]["name"]} du "
                f"{tournament["tournament_datas"]["start_date"]}"
            )

    def display_tournament_players_list_report(self, players_list):
        """Displays the list of players in a tournament in the console."""
        self.generic.display_level_three_header("Liste des joueurs du tournoi")
        for i, player in enumerate(players_list, 1):
            print(
                f"{i}. {player["last_name"].upper()} {player["first_name"]} "
                f"({player["birthdate"]}) | INE: {player["chess_id"]}"
            )

    def dispay_round_and_matches_report(self, tournament, id_to_name):
        """Displays the list of rounds and match results in the console."""
        self.generic.display_level_three_header("Listes des rounds et matchs "
                                                "du tournoi")
        for round in tournament["tournament_rounds_list"]:
            print(f"\n{round["name"]}:")
            for i, match in enumerate(round["matches"], 1):
                player1 = id_to_name[match["player1"]["chess_id"]]
                player2 = id_to_name[match["player2"]["chess_id"]]
                p1_points = (
                    match["match_result"][match["player1"]["chess_id"]])
                p2_points = (
                    match["match_result"][match["player2"]["chess_id"]])
                print(f"- Match {i}:\n{player1} ({p1_points}) VS. "
                      f"{player2} ({p2_points})")

    def display_reports_filepath(self):
        """Confirms the recording and displays the path to the report file."""
        print("\nLe fichier a été enregistré dans votre dossier "
              "d'installation,\nsous le nom RAPPORTS.html")

    # Get confirmation and validation methods
    def get_start_new_tournament_choice(self):
        """Confirmation of the "new tournament" selection."""
        return self.generic.get_confirmation_choice("Démarrer un nouveau "
                                                    "tournoi")

    def get_save_players_choice(self):
        """Confirmation of the "save player" selection."""
        return self.generic.get_confirmation_choice("Enregistrer un "
                                                    "nouveau joueur")

    def get_resume_last_tournament_choice(self):
        """Confirmation of the resume last tournament selection."""
        return self.generic.get_confirmation_choice("Reprendre à la dernière "
                                                    "sauvegarde du dernier "
                                                    "tournoi")

    def get_quit_choice(self):
        """Confirmation of the "quit" selection."""
        return self.generic.get_confirmation_choice("Êtes-vous sûr "
                                                    "de vouloir quitter")

    def get_tournament_start_choice(self):
        """Confirmation of the "start tournament" selection."""
        return self.generic.get_confirmation_choice("Prêt à démarrer le "
                                                    "tournoi")

    def get_back_to_main_menu_choice(self):
        """Confirmation for the return to the menu."""
        return self.generic.get_confirmation_choice("Retourner au "
                                                    "menu principal")

    def get_add_another_player_choice(self):
        """Confirmation regarding player additions to the tournament."""
        return self.generic.get_confirmation_choice("Inscrire un autre "
                                                    "joueur via cette "
                                                    "méthode")

    def get_save_another_player_choice(self):
        """Confirmation regarding player save."""
        return self.generic.get_confirmation_choice("Enregistrer un autre "
                                                    "joueur")

    def get_generate_report_choice(self):
        "Confirmation regarding the generate report selection."
        return self.generic.get_confirmation_choice("Générer des rapports")

    def get_first_round_start_validation(self):
        """Validates the start of the first round."""
        return self.generic.check_press_enter_prompt("démarrer le "
                                                     "premier round")

    def get_next_round_start_validation(self):
        """Validates the start of the next round."""
        return self.generic.check_press_enter_prompt("démarrer le "
                                                     "prochain round")

    def get_end_round_validation(self):
        """Validates the start of the end of the round."""
        return self.generic.check_press_enter_prompt("finir le round "
                                                     "enregistrer les "
                                                     "résultats "
                                                     "des matchs")

    def get_back_to_main_menu_validation(self):
        """Validates the start of the end of the tournament."""
        return self.generic.check_press_enter_prompt("retourner au menu "
                                                     "principal")

    def get_back_to_tournament_menu_validation(self):
        """Validates the return in the tournament menu."""
        return self.generic.check_press_enter_prompt("retourner au menu "
                                                     "du tournoi")

    def get_back_to_registration_menu_validation(self):
        """Validates the return in the validation menu"""
        return self.generic.check_press_enter_prompt("retourner au menu "
                                                     "d'inscription")

    def go_back_validation(self):
        return self.generic.check_press_enter_prompt("retourner en arrière")

    # Display specific errors methods
    def display_no_saved_players_error(self):
        print("Attention, aucun joueur enregistré, "
              "veuillez d'abord enregistrer un joueur.")

    def display_already_added_player_error(self):
        print("Attention, ce joueur est déjà inscrit au tournoi.")

    def display_players_numbers_error(self):
        print("Attention, un nombre de joueur pair et au moins égal à "
              "deux est nécessaire avant de pouvoir démarrer un tournoi.")

    def display_no_id_match_error(self):
        print('Attention, cet INE ne correspond à aucun joueur enregistré '
              '(Format "AB12345" requis).')

    def display_no_saved_tournament_error(self):
        print("\nAttention, il n'y a aucun tournoi de sauvegardé "
              "pour le moment.")

    def display_finished_tournament_error(self):
        print("\nAttention, le dernier tournoi sauvegardé est terminé !")
