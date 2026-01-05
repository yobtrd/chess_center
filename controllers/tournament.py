import json
from pathlib import Path

from controllers.helper import get_actual_datetime
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class TournamentController:
    """controller for managing the tournament."""

    def __init__(self, view, player_controller, round_controller):
        """Initialization of the main menu.
        Initializes the view and the needed controllers.
        """
        self.view = view
        self.player_controller = player_controller
        self.round_controller = round_controller
        self.filepath = Path("data/tournaments/tournaments.json")
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.saved_tournaments_list = []
        self.load_saved_tournaments_list()

    def create_new_tournament(self):
        """Retieves and creates a new tournament."""
        tournament_datas = self.view.get_tournament_datas()
        parameters = {
            "name": tournament_datas["name"],
            "place": tournament_datas["place"],
            "start_date": tournament_datas["start_date"],
            "end_date": None,
            "total_rounds": tournament_datas.get("total_rounds") or "4",
            "description": tournament_datas["comment"],
        }
        tournament = Tournament(**parameters)
        self.save_tournament(tournament)
        return tournament

    def tournament_menu(self, tournament):
        """Manages tournament menu selection.
        Returns True to start the tournament.
        Returns False to return to main menu.
        """
        while True:
            choice = self.view.get_tournament_menu_choice(tournament)
            if choice == "1":
                if self.tournament_player_add_menu(tournament):
                    continue
            elif choice == "2":
                if not tournament.check_players_numbers():
                    if self.view.get_tournament_start_choice():
                        while self.run_tournament_flow(tournament):
                            continue
                        return False
                else:
                    self.view.display_players_numbers_error()
                    self.view.get_back_to_tournament_menu_validation()
            elif choice == "3":
                if self.view.get_back_to_main_menu_choice():
                    return False

    def tournament_player_add_menu(self, tournament):
        """Manages the player addition menu.
        Returns True to return to the tournament menu.
        """
        while True:
            counter = len(tournament.players_list)
            choice = self.view.get_tournament_player_menu_choice(counter)
            if choice == "1":
                self.add_tournament_players_by_id(tournament)
            elif choice == "2":
                self.add_tournament_players_by_list(tournament)
            elif choice == "3":
                self.add_tournament_new_players(tournament)
            elif choice == "4":
                if len(tournament.players_list) == 0:
                    self.view.display_no_registered_players_warning()
                self.view.display_tournament_players_list(tournament)
                self.view.get_back_to_registration_menu_validation()
            elif choice == "5":
                return True

    def add_tournament_players_by_id(self, tournament):
        """Manages the addition of players by chess ID method."""
        while True:
            checked_player = self.player_controller.add_player_by_id()
            if checked_player is None:
                self.view.display_no_saved_players_error()
                self.view.get_back_to_registration_menu_validation()
                break
            elif checked_player is False:
                self.view.display_no_id_match_error()
            elif checked_player:
                add_success = tournament.add_tournament_player(checked_player)
                if add_success:
                    self.view.display_registered_player_succes(checked_player)
                    self.save_tournament(tournament)
                else:
                    self.view.display_already_added_player_error()
            if not self.view.get_add_another_player_choice():
                break

    def add_tournament_players_by_list(self, tournament):
        """Manages the addition of players by list method."""
        while True:
            checked_player = self.player_controller.add_players_by_list()
            if checked_player is None:
                self.view.display_no_saved_players_error()
                self.view.get_back_to_registration_menu_validation()
                break
            add_success = tournament.add_tournament_player(checked_player)
            if add_success:
                self.view.display_registered_player_succes(checked_player)
                self.save_tournament(tournament)
            else:
                self.view.display_already_added_player_error()
            if not self.view.get_add_another_player_choice():
                break

    def add_tournament_new_players(self, tournament):
        """Manages the addition of players using the player save method."""
        while True:
            player = self.player_controller.save_new_player()
            tournament.add_tournament_player(player)
            self.view.display_registered_player_succes(player)
            self.save_tournament(tournament)
            if not self.view.get_add_another_player_choice():
                break

    def run_tournament_flow(self, tournament):
        """Manages tournament flow."""
        self.view.display_tournament_summary(tournament)
        self.manages_tournament_loading(tournament)
        while not self.tournament_is_finished(tournament):
            self.round_controller.run_round_flow(tournament, self.save_tournament)
        self.end_tournament(tournament)

    def end_tournament(self, tournament):
        """Manages the end of tournaments."""
        scoreboard = tournament.get_sorted_players()
        tournament.end_date = get_actual_datetime()
        self.view.display_tournament_end_summary(tournament)
        self.manage_tournament_winner(scoreboard)
        self.view.display_scores(scoreboard)
        self.save_tournament(tournament)
        self.view.get_back_to_main_menu_validation()

    def manage_tournament_winner(self, scoreboard):
        """Get and manage the tournament winner, handle cas of tied winners."""
        max_score = scoreboard[0].score
        max_score_list = [p for p in scoreboard if p.score == max_score]
        if len(max_score_list) == 1:
            winner = max_score_list[0]
            self.view.display_tournament_winner(winner)
        else:
            winners_tied = max_score_list
            self.view.display_tournament_winners_tied(winners_tied)

    # === Save and load methods ===
    def load_saved_tournaments_list(self):
        """Load the saved_tournament_list.
        Reset the list in case of corrupt file or no players saved.
        """
        try:
            with open(self.filepath, "r") as file:
                self.saved_tournaments_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_tournaments_list = []

    def save_tournament(self, tournament):
        """Saves the datas of a tournament state in a JSON file."""
        self.load_saved_tournaments_list()
        players_list = [p.to_dict() for p in tournament.players_list]
        rounds_list = [r.to_dict() for r in tournament.rounds_list]
        tournament_datas = {
            "tournament_datas": tournament.to_dict(),
            "tournament_players_list": players_list,
            "tournament_rounds_list": rounds_list,
        }

        existing_index = self.find_existing_tournament(tournament)
        if existing_index is not None:
            self.saved_tournaments_list[existing_index] = tournament_datas
        else:
            self.saved_tournaments_list.append(tournament_datas)

        with open(self.filepath, "w") as file:
            json.dump(self.saved_tournaments_list, file)
        self.view.display_saved_message()

    def find_existing_tournament(self, tournament_to_check):
        """Search saved tournaments if the tournament already exists.
        Returns the index of the existing tournament.
        Returns None if no tournament is found.
        """
        for (
            index,
            tournament,
        ) in enumerate(self.saved_tournaments_list):
            if tournament["tournament_datas"]["name"] == tournament_to_check.name:
                return index
        return None

    def load_last_tournament(self):
        """Rebuilds the datas of the last tournament state with a JSON file.
        Returns the reserialized tournament.
        Returns None in case of exception.
        """
        if not self.saved_tournaments_list:
            return None
        with open(self.filepath, "r") as file:
            self.saved_tournaments_list = json.load(file)
            datas = self.saved_tournaments_list[-1]
            tournament = Tournament(**datas["tournament_datas"])
            rounds_list = datas.get("tournament_rounds_list", [])
            players_dict = self.load_full_players(datas)
            tournament.players_list = list(players_dict.values())
            tournament.rounds_list = [Round.from_dict(r, players_dict) for r in rounds_list]
            tournament.actual_round_index = len(tournament.rounds_list)
            self.rebuild_scores(tournament)
            self.view.display_loaded_message()
            return tournament

    def load_full_players(self, datas):
        """Rebuilds a Player model with just its chess ID."""
        players_dict = {}
        saved_chess_ids = [p["chess_id"] for p in datas.get("tournament_players_list", [])]
        for player_data in self.player_controller.saved_players_list:
            if player_data["chess_id"] in saved_chess_ids:
                player = Player.from_dict(player_data)
                players_dict[player.chess_id] = player
        return players_dict

    def rebuild_scores(self, tournament):
        """Reconstructs player scores with match results after reset."""
        for player in tournament.players_list:
            player.score = 0.0
        for round in tournament.rounds_list:
            for match in round.matches_list:
                if match.match_result:
                    match.player1.score += float(match.match_result[0][1])
                    match.player2.score += float(match.match_result[1][1])

    def manages_tournament_loading(self, tournament):
        """Handles cases of a completed round during loading."""
        matches_status = self.round_controller.get_matches_status(tournament)
        if len(tournament.rounds_list) > 0:
            last_round = tournament.rounds_list[-1]
            if last_round.end_date and not any(matches_status):
                self.view.display_resume_completed_round(last_round)

    def tournament_is_finished(self, tournament):
        """Checks if the tournament is completely finished."""
        rounds_completed = len(tournament.rounds_list) == tournament.total_rounds
        all_matches_processed = all(m.match_result for r in tournament.rounds_list for m in r.matches_list)
        return rounds_completed and all_matches_processed
