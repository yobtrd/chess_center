import re
from pathlib import Path


class ReportController:
    """Controller for managing the reports."""

    def __init__(self, view, player_controller, tournament_controller):
        """Initialization of the report controller.
        Initialize the view and the needed controllers.
        Initialize the path for the privates files.
        """
        self.view = view
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.filepath = Path("data/reports/")
        self.filepath.mkdir(parents=True, exist_ok=True)

    def reports_main_menu(self):
        """Manages reports menu selection.
        Return True to return to the main menu.
        """
        while True:
            choice = self.view.get_reports__main_menu_choice()
            if choice == "1":
                if not self.console_reports_menu():
                    continue
            elif choice == "2":
                self.run_html_reports_generation()
                self.view.go_back_validation()
            elif choice == "3":
                if self.view.get_back_to_main_menu_choice():
                    return True

    def console_reports_menu(self):
        """Manages the console's report menu.
        Return False to return to the reports main menu.
        """
        while True:
            choice = self.view.get_console_reports_menu_choice()
            if choice == "1":
                self.generate_saved_players_list_console_report()
                self.view.go_back_validation()
            elif choice == "2":
                self.generate_tournaments_list_console_reports()
            elif choice == "3":
                return False

    def generate_saved_players_list_console_report(self):
        """Manages the report concerning the list of registered players."""
        if self.are_no_players_saved():
            self.view.display_reports_no_saved_players_warning()
        else:
            list_to_use = self.player_controller.saved_players_list
            players_list = self.get_alphabetical_player_list(list_to_use)
            self.view.display_players_list_console_report(players_list)

    def generate_tournaments_list_console_reports(self):
        """Manages the reports of finished tournaments.
        Check if there are any saved tournaments and display them if so.
        Return False by entering "R" to return to the console report menu.
        """
        ended_tournaments = self.checks_for_ended_tournaments()
        if self.are_no_tournament_saved(ended_tournaments):
            self.view.display_reports_no_tournaments_saved_warning()
            self.view.go_back_validation()
        else:
            while True:
                ended_tournaments = self.checks_for_ended_tournaments()
                self.view.display_tournaments_list_report(ended_tournaments)
                tournament_choice = self.view.get_report_tournament_choice(ended_tournaments)
                if tournament_choice:
                    self.tournament_report_console(tournament_choice)
                else:
                    return False

    def tournament_report_console(self, tournament):
        """Manages the menu for reports on a single tournament."""
        tournament_name = tournament["tournament_datas"]["name"]
        while True:
            choice = self.view.get_tournament_report_choice(tournament_name)
            if choice == "1":
                self.tournament_players_list_console(tournament)
                if self.view.go_back_validation():
                    return True
            elif choice == "2":
                self.tournament_rounds_and_matches_console(tournament)
                if self.view.go_back_validation():
                    return True
            elif choice == "3":
                return True

    def tournament_players_list_console(self, tournament):
        """Manages the display of players for a selected tournament."""
        list_to_use = self.get_tournament_players_details(tournament)
        players_list = self.get_alphabetical_player_list(list_to_use)
        self.view.display_tournament_players_list_report(players_list)

    def tournament_rounds_and_matches_console(self, tournament):
        """Manages the display of rounds and matches for
        a selected tournament.
        """
        id_to_name = self.get_chess_id_to_name()
        self.view.dispay_round_and_matches_report(tournament, id_to_name)

    def run_html_reports_generation(self):
        """Manages the generation and save of all HTML files for reports."""
        self.generate_main_html_file()
        self.generate_saved_players_list_html()
        self.generate_tournaments_list_html()

    def generate_main_html_file(self):
        """Create the user'smain html file"""
        html_file = self.main_html_file()
        with open("RAPPORTS.html", "w") as file:
            file.write(html_file)
        self.view.display_reports_filepath()

    def generate_saved_players_list_html(self):
        """Create and save the saved players list html file."""
        html_content = self.generate_players_list_content()
        file_name = "liste_joueurs_enregistres.html"
        self.save_generated_html_file(html_content, file_name)

    def generate_tournaments_list_html(self):
        """Create and save the finished tournament list html file."""
        html_content = self.generate_tournaments_content()
        file_name = "liste_tournois_precedent.html"
        self.save_generated_html_file(html_content, file_name)

    def save_generated_html_file(self, content, file_name):
        """Save a specific file in the correct filepath and name."""
        with open(self.filepath / file_name, "w") as file:
            file.write(content)

    def html_wrapper(title):
        """Decorator factory wrapping returned content in full HTML skeleton.
        Decorator injecting content into <html><body> structure with title.
        """

        def decorator(function):
            def wrapper(self):
                content = function(self)
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{title}</title>
                </head>
                <body>
                    <h1>{title}</h1>
                    {content}
                </body>
                </html>"""

            return wrapper

        return decorator

    @html_wrapper(title="Menu des rapports")
    def main_html_file(self):
        """Create the main report menu html file."""
        links = [
            ("liste_joueurs_enregistres.html", "Liste des joueurs enregistrés"),
            ("liste_tournois_precedent.html", "Liste des tournois précédents"),
        ]
        items = [f'<li><a href="data/reports/{file}">{text}</a></li>' for file, text in links]
        return f"<ul>{''.join(items)}</ul>"

    @html_wrapper(title="Liste des joueurs enregistrés")
    def generate_players_list_content(self):
        """Create the saved players list html file."""
        if self.are_no_players_saved():
            return "<li>Il n'y a aucun joueurs sauvegardés dans le programme pour le moment.</li>"
        else:
            list_to_use = self.player_controller.saved_players_list
            players_list = self.get_alphabetical_player_list(list_to_use)
            return "\n".join(
                f"<li>{p['last_name'].upper()} {p['first_name']}" f"({p['birthdate']}) | INE: {p['chess_id']}</li>"
                for p in players_list
            )

    @html_wrapper(title="Liste des tournois précédents")
    def generate_tournaments_content(self):
        """Create the finished tournaments list html file.
        calls the method to create each HTML file for each tournament.
        """
        ended_tournament = self.checks_for_ended_tournaments()
        if self.are_no_tournament_saved(ended_tournament):
            return "<li>Il n'y a aucun tournois terminés et sauvegardés dans le programme pour le moment.</li>"
        else:
            items = []
            for tournament in ended_tournament:
                tournament_name = tournament["tournament_datas"]["name"]
                tournament_date = tournament["tournament_datas"]["start_date"]
                base_name = self.clean_filename(tournament_name)
                file_path = f"{base_name}.html"
                title = f"{tournament_name} du {tournament_date}"
                items.append(f'<li><a href="{file_path}">{title}</li>')
                html_file = self.generate_individual_tournaments_content(tournament, title)
                self.save_generated_html_file(html_file, file_path)
            return "<ul>" + "\n".join(items) + "</ul>"

    def generate_individual_tournaments_content(self, tournament, title):
        """Create the individual tournament html file."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <h2>Liste des joueurs ayant participé au tournoi:</h2>
            {self.generate_tournament_players_html(tournament)}
            <h2>Liste des rounds et résultats des matchs:</h2>
            {self.generate_rounds_and_matches_html(tournament)}
        </body>
        </html>
        """

    def generate_tournament_players_html(self, tournament):
        """Create the tournament players list for the tournament html page."""
        list_to_use = self.get_tournament_players_details(tournament)
        players_list = self.get_alphabetical_player_list(list_to_use)
        return "\n".join(
            f"""<li>{p['last_name'].upper()} {p['first_name']}
                ({p['birthdate']}) | INE: {p['chess_id']}</li>"""
            for p in players_list
        )

    def generate_rounds_and_matches_html(self, tournament):
        """Create the tournament rounds and matches for
        the tournament html page.
        """
        id_to_name = self.get_chess_id_to_name()
        html = []
        for round in tournament["tournament_rounds_list"]:
            html.append(f"<h3>{round['name']}</h3><ul>")
            for i, match in enumerate(round["matches"], 1):
                player1 = id_to_name[match["player1"]["chess_id"]]
                player2 = id_to_name[match["player2"]["chess_id"]]
                p1_points = match["match_result"][match["player1"]["chess_id"]]
                p2_points = match["match_result"][match["player2"]["chess_id"]]
                html.append(f"<li>" f"Match {i}: {player1} ({p1_points}) VS. {player2} ({p2_points})</li>")
            html.append("</ul>")
        return "\n".join(html)

    def clean_filename(self, name):
        """Cleans tournament names so the file can be saved reliably."""
        name = name.strip().lower()
        name = re.sub(r"[^\w\-]", "", name)
        return re.sub(r"_+", "_", name)

    def get_alphabetical_player_list(self, list):
        """Sort a list of players alphabetically."""
        return sorted(list, key=lambda p: (p["last_name"], p["first_name"]))

    def get_tournament_players_details(self, tournament):
        """Retrieves all information about a player via their chess ID."""
        player_ids = {p["chess_id"] for p in tournament["tournament_players_list"]}
        return [p for p in self.player_controller.saved_players_list if p["chess_id"] in player_ids]

    def get_chess_id_to_name(self):
        """Converts a player's chess ID into their first and last name."""
        return {
            p["chess_id"]: f"{p["last_name"].upper()} {p["first_name"]}"
            for p in self.player_controller.saved_players_list
        }

    def checks_for_ended_tournaments(self):
        """Only retrieve completed tournaments."""
        saved_tournaments = self.tournament_controller.saved_tournaments_list
        return [t for t in saved_tournaments if t["tournament_datas"]["end_date"]]

    def are_no_players_saved(self):
        """Returns True if there are no players saved in the program."""
        if len(self.player_controller.saved_players_list) == 0:
            return True

    def are_no_tournament_saved(self, ended_tournament):
        """Returns True if there are no finished tournament saved in the program."""
        if len(ended_tournament) == 0:
            return True
