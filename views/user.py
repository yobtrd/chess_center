from views.generic import GenericView


class UserView:
    """Inputs and outputs of user's console interface"""

    def __init__(self):
        """Initializes access to generic view methods."""
        self.generic = GenericView()

    # === Get methods ===
    def get_main_menu_choice(self):
        """Displays the menu and obtain the user's choice."""
        self.generic.display_principal_header("Menu principal")
        options = [
            "Démarrer un nouveau tournoi",
            "Enregistrer un nouveau joueur",
            "Reprendre un tournoi en cours",
            "Générer des rapports",
            "Quitter",
        ]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_player_datas(self):
        """Displays and obtain input regarding the fields for new player."""
        self.generic.display_level_three_header("Veuillez saisir les informations du joueur")
        fields_config = {
            "last_name": ("Nom de famille du joueur", True, None),
            "first_name": ("Prénom du joueur", True, None),
            "birthdate": ("Date de naissance (DD/MM/YYYY)", True, self.generic.validate_date_format),
            "chess_id": ("ID national (AB12345)", True, self.generic.validate_id_format),
        }
        player_datas = {}
        for field, config in fields_config.items():
            prompt, required, validated = config
            player_datas[field] = self.generic.get_validated_input(prompt, required, validated)
        return player_datas

    def get_tournament_datas(self):
        """Displays and obtain input regarding the fields for new tournament."""
        self.generic.display_level_three_header("Veuillez saisir les informations du tournois")
        fields_config = {
            "name": ("Nom du tournoi", True, None),
            "place": ("Lieu du tournoi", True, None),
            "start_date": ("Date du tournoi (DD/MM/YYYY)", True, self.generic.validate_date_format),
            "total_rounds": (
                "Nombre de tours (appuyer sur Entrée pour laisser sur 4 tours par défaut)",
                False,
                self.generic.validate_round_format,
            ),
            "comment": ("Remarques du directeur (appuyer sur Entrée pour passer)", False, None),
        }
        tournament_datas = {}
        for field, config in fields_config.items():
            prompt, required, validated = config
            tournament_datas[field] = self.generic.get_validated_input(prompt, required, validated)
        return tournament_datas

    def get_tournament_menu_choice(self, tournament):
        """Displays and obtain input regarding tournament menu."""
        self.generic.display_principal_header("Menu du tournoi")
        print(f"{tournament.name} de {tournament.place}")
        self.generic.display_separator_level_two()
        options = ["Accéder au menu d'inscription des joueurs", "Démarrer le tournoi", "Retourner au menu principal"]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_tournament_player_menu_choice(self, counter):
        """Displays and obtain input for adding players to the tournament."""
        self.generic.display_principal_header("Menu d'inscription")
        print(f"Joueur(s) actuellement inscrit(s): {counter}")
        self.generic.display_separator_level_two()
        options = [
            "Inscrire des joueurs déjà enregistrés avec leur identifiant national d'échec",
            "Inscrire des joueurs déjà enregistrés via une liste",
            "Enregistrer un nouveau joueur et l'inscire au tournoi",
            "Voir les joueurs actuellement inscrits au tournoi",
            "Retourner au menu du tournoi",
        ]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_saved_player_choice(self, saved_players_list):
        """Get the saved player's selection."""
        options = saved_players_list
        choice = int(self.generic.get_validated_choice(len(options)))
        return saved_players_list[choice - 1]

    def get_add_player_by_id_id(self):
        """Get the saved players INE input."""
        return input("\nVeuillez inscrire l'INE du joueur à enregister: ")

    def get_match_result(self, match_number, match):
        """Get the results of the current match."""
        message = f"Enregistrer les résultats pour le match {match_number}"
        self.generic.display_level_three_header(message)
        options = [
            f"{match.player1.last_name.upper()} {match.player1.first_name} remporte le match",
            f"{match.player2.last_name.upper()} {match.player2.first_name} remporte le match",
            "Match nul",
        ]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_reports__main_menu_choice(self):
        """Displays the reports menu and obtain the user's choice."""
        self.generic.display_principal_header("Menu des rapports")
        options = [
            "Générer les rapports et les afficher dans le programme",
            "Générer les rapports dans un fichier html",
            "Retourner au menu principal",
        ]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    def get_console_reports_menu_choice(self):
        """Displays the console reports menu and obtain the user's choice."""
        self.generic.display_level_two_header("Menu d'affichage des rapports")
        options = [
            "Afficher la liste des joueurs enregistrés",
            "Afficher la liste des tournois précédents",
            "Retourner au menu des rapports",
        ]
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
        """Displays the console report menu and obtain the user's choice."""
        self.generic.display_level_two_header(f"Rapports du {tournament_name}")
        options = [
            "Afficher la liste des joueurs de ce tournoi",
            "Générer un rapport des rounds et des matchs de ce tournoi",
            "Revenir à la liste des tournois",
        ]
        self.generic.display_options(options)
        return self.generic.get_validated_choice(len(options))

    # === Display methods ===
    def display_saved_players_list(self, saved_players_list):
        "Displays a list of all the already saved players in the program."
        self.generic.display_level_three_header("Choisissez un joueur dans la liste")
        for i, player in enumerate(saved_players_list, 1):
            print(f"{i} - {player["last_name"].upper()} {player["first_name"]}")

    def display_tournament_summary(self, tournament):
        """Summarizes the tournament's data before start or resume."""
        message = f"Le {tournament.name} de {tournament.place} a commencé le {tournament.start_date}"
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
            chunk = players[i: i + 5]
            player_lines.append(", ".join(f"{p.last_name.upper()} {p.first_name}" for p in chunk))
        print("\n" + "\n".join(player_lines))

    def display_round_start(self, round):
        """Displays the start of the round with its name and datetime"""
        message = f"Le {round.name} a démarré le {round.start_date}"
        self.generic.display_level_two_header(message)

    def display_round_end(self, round):
        """Displays the end of the round with its name and datetime"""
        message = f"Le {round.name} s'est terminé le {round.end_date}"
        self.generic.display_level_two_header(message)

    def display_matches(self, matches):
        """Displays the paired players for the differents matches."""
        self.generic.display_level_three_header("Matchs de ce round")
        for i, match in enumerate(matches, 1):
            player1 = f"{match.player1.last_name.upper()} {match.player1.first_name}"
            player2 = f"{match.player2.last_name.upper()} {match.player2.first_name}"
            print(f"- Match {i}: {player1} VS {player2}")

    def display_results_summary(self, matches_list, round):
        """Displays the end of round summary with matches results."""
        self.generic.display_separator_level_one()
        self.generic.display_level_three_header(f"Résultat du {round.name}")
        for i, match in enumerate(matches_list, 1):
            player1 = f"{match.match_result[0][0].first_name} {match.match_result[0][0].last_name}"
            player2 = f"{match.match_result[1][0].first_name} {match.match_result[1][0].last_name}"
            points_p1 = match.match_result[0][1]
            points_p2 = match.match_result[1][1]
            if points_p1 > points_p2:
                result = (
                    f"- Match {i}: {player1} remporte le match !\n  "
                    f"({player1} reçoit {points_p1} point(s), {player2} reçoit {points_p2} point(s))\n"
                )
            elif points_p1 < points_p2:
                result = (
                    f"- Match {i}: {player2} remporte le match !\n  "
                    f"({player2} reçoit {points_p2} point(s), {player1} reçoit {points_p1} point(s))\n"
                )
            elif points_p1 == points_p2:
                result = (
                    f"- Match {i}: Match nul entre {player1} et {player2} !\n  "
                    "(chacun des joueurs reçoit 0.5 points)\n"
                )
            print(result)

    def display_scores(self, sorted_players):
        """displays the updated scoreboard."""
        self.generic.display_level_three_header("Tableau des scores:")
        for rank, player in enumerate(sorted_players, 1):
            print(f"{rank}. {player.last_name.upper()} {player.first_name}: {player.score}")
        self.generic.display_separator_level_one()

    def display_tournament_end_summary(self, tournament):
        """Displays the end-of-tournament summary and winner(s)."""
        message = f"Le {tournament.name} a fini le " f"{tournament.end_date}"
        self.generic.display_principal_header(message)

    def display_tournament_winner(self, winner):
        """Displays the tournament winner."""
        winner = f"{winner.first_name.upper()} {winner.last_name.upper()}"
        message = "Le gagnant de ce tournoi est: "
        self.generic.display_winner_header(message, winner)

    def display_tournament_winners_tied(self, winners_tied):
        """Displays a message in cas of tieds winners."""
        winners_str = ", ".join(f"{w.first_name.upper()} {w.last_name.upper()}" for w in winners_tied)
        message = "Le tournoi se termine sur des égalités ! Les joueurs ex-aequo sont:"
        self.generic.display_winner_header(message, winners_str)

    def display_players_list_console_report(self, saved_players):
        """Displays the list of saved players in the console."""
        print("\nListe des joueurs enregistrés:\n")
        for i, player in enumerate(saved_players, 1):
            print(
                f"{i}. {player["last_name"].upper()} {player["first_name"]} "
                f"({player["birthdate"]}) | INE: {player["chess_id"]}"
            )

    def display_tournaments_list_report(self, saved_tournaments):
        """Displays the list of completed tournaments in the console."""
        self.generic.display_level_two_header("Liste des tournois")
        print(
            "Choisissez un tournoi dans la liste pour afficher des rapports "
            'le concernant,\nou entrer "R" pour retourner '
            "en arrière\n"
        )
        for i, tournament in enumerate(saved_tournaments, 1):
            print(f"{i} - {tournament["tournament_datas"]["name"]} du {tournament["tournament_datas"]["start_date"]}")

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
        self.generic.display_level_three_header("Listes des rounds et matchs du tournoi")
        for round in tournament["tournament_rounds_list"]:
            print(f"\n{round["name"]}:")
            for i, match in enumerate(round["matches"], 1):
                player1 = id_to_name[match["player1"]["chess_id"]]
                player2 = id_to_name[match["player2"]["chess_id"]]
                points_p1 = match["match_result"][match["player1"]["chess_id"]]
                points_p2 = match["match_result"][match["player2"]["chess_id"]]
                if points_p1 > points_p2:
                    result = f"> Remporté par {player1}.\n"
                elif points_p1 < points_p2:
                    result = f"> Remporté par {player2}.\n"
                elif points_p1 == points_p2:
                    result = "> Match nul.\n"
                print(f" - Match {i}: {player1} VS {player2}\n    {result}")

    # === Get confirmation and validation methods ===
    def get_start_new_tournament_choice(self):
        """Confirmation of the "new tournament" selection."""
        return self.generic.get_confirmation_choice("\nDémarrer un nouveau tournoi")

    def get_save_players_choice(self):
        """Confirmation of the "save player" selection."""
        return self.generic.get_confirmation_choice("\nEnregistrer un nouveau joueur")

    def get_resume_last_tournament_choice(self):
        """Confirmation of the resume last tournament selection."""
        return self.generic.get_confirmation_choice("\nReprendre à la dernière sauvegarde du dernier tournoi")

    def get_quit_choice(self):
        """Confirmation of the "quit" selection."""
        return self.generic.get_confirmation_choice("\nÊtes-vous sûr de vouloir quitter")

    def get_tournament_start_choice(self):
        """Confirmation of the "start tournament" selection."""
        return self.generic.get_confirmation_choice("\nPrêt à démarrer le tournoi")

    def get_back_to_main_menu_choice(self):
        """Confirmation for the return to the menu."""
        return self.generic.get_confirmation_choice("\nRetourner au menu principal")

    def get_add_another_player_choice(self):
        """Confirmation regarding player additions to the tournament."""
        return self.generic.get_confirmation_choice("Inscrire un autre joueur via cette méthode")

    def get_save_another_player_choice(self):
        """Confirmation regarding player save."""
        return self.generic.get_confirmation_choice("Enregistrer un autre joueur")

    def get_generate_report_choice(self):
        "Confirmation regarding the generate report selection."
        return self.generic.get_confirmation_choice("\nGénérer des rapports")

    def get_first_round_start_validation(self):
        """Validates the start of the first round."""
        return self.generic.check_press_enter_prompt("démarrer le premier round")

    def get_next_round_start_validation(self):
        """Validates the start of the next round."""
        return self.generic.check_press_enter_prompt("démarrer le prochain round")

    def get_end_round_validation(self):
        """Validates the start of the end of the round."""
        return self.generic.check_press_enter_prompt("finir le round enregistrer les résultats des matchs")

    def get_back_to_main_menu_validation(self):
        """Validates the start of the end of the tournament."""
        return self.generic.check_press_enter_prompt("retourner au menu principal")

    def get_back_to_tournament_menu_validation(self):
        """Validates the return in the tournament menu."""
        return self.generic.check_press_enter_prompt("retourner au menu du tournoi")

    def get_back_to_registration_menu_validation(self):
        """Validates the return in the validation menu"""
        return self.generic.check_press_enter_prompt("retourner au menu d'inscription")

    def go_back_validation(self):
        return self.generic.check_press_enter_prompt("retourner en arrière")

    # === Display information methods ===
    def display_registered_player_succes(self, player):
        print(f"\n{player.first_name} {player.last_name} a été inscrit au tournoi.")

    def display_saved_player_success(self):
        print("\nLe joueur a été enregistré.\n")

    def display_reports_filepath(self):
        print("\nLe fichier a été enregistré dans votre dossier d'installation,\nsous le nom RAPPORTS.html")

    def display_saved_message(self):
        self.generic.rich_print("\n- sauvegarde du tournoi -\n", "save_or_load_info")

    def display_loaded_message(self):
        self.generic.rich_print("\n- Chargement du tournoi -", "save_or_load_info")

    def display_match_resume(self, match_number, round):
        message = (
            f"\n- Le chargement reprend à l'enregistrement des résultats du match {match_number} du {round.name} -\n"
        )
        self.generic.rich_print(message, "loading_state")

    def display_resume_completed_round(self, round):
        message = f"\n- Le chargement reprend à la fin du {round.name} -"
        self.generic.rich_print(message, "loading_state")

    def display_resume_not_ending_round(self, round):
        message = f"\n- Le chargement reprend après le départ du {round.name} -"
        self.generic.rich_print(message, "loading_state")

    def display_resume_ended_round(self, round):
        message = f"\n- Le chargement reprend à la fin du {round.name} -\n"
        self.generic.rich_print(message, "loading_state")

    # === Display specific errors and warnings methods ===
    def display_no_saved_players_error(self):
        message = "\nAttention, aucun joueur enregistré, veuillez d'abord enregistrer un joueur."
        self.generic.rich_print(message, "warning")

    def display_already_added_player_error(self):
        message = "\nAttention, ce joueur est déjà inscrit au tournoi.\n"
        self.generic.rich_print(message, "warning")

    def display_players_numbers_error(self):
        message = ("\nAttention, un nombre de joueur pair et au moins égal à deux est nécessaire\n"
                   "avant de pouvoir démarrer un tournoi.")
        self.generic.rich_print(message, "warning")

    def display_no_id_match_error(self):
        message = '\nAttention, cet INE ne correspond à aucun joueur enregistré (Format "AB12345" requis).\n'
        self.generic.rich_print(message, "warning")

    def display_no_saved_tournament_error(self):
        message = "\nIl n'y a aucun tournoi de sauvegardé pour le moment."
        self.generic.rich_print(message, "warning")

    def display_finished_tournament_error(self):
        message = "\nChargement impossible, le dernier tournoi sauvegardé est terminé !"
        self.generic.rich_print(message, "warning")

    def display_no_registered_players_warning(self):
        message = "\nIl n'y a aucun joueurs inscrits au tournoi pour le moment."
        self.generic.rich_print(message, "warning")

    def display_last_tournament_overwrite_warning(self):
        message = "\nAttention, un tournoi non terminé est déjà sauvegardé, démarrer un nouveau\ntournoi l'écrasera."
        self.generic.rich_print(message, "warning")

    def display_reports_no_saved_players_warning(self):
        message = "\nIl n'y a aucun joueurs enregistrés dans le programme pour le moment."
        self.generic.rich_print(message, "warning")

    def display_reports_no_tournaments_saved_warning(self):
        message = "\nIl n'y a aucun tournois terminés et sauvegardés dans le programme pour le moment."
        self.generic.rich_print(message, "warning")
