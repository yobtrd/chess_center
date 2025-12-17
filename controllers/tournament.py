import random
from models.tournament import Tournament
from models.match import Match


class TournamentController():
    """controller for managing the tournament."""

    def __init__(self, view, player_controller):
        """Initialization of the main menu.
        Initialize the view and the needed controllers."""
        self.view = view
        self.player_controller = player_controller

    def run_new_tournament(self):
        """Start a tournament with the retrieved data.
        Display the tournament menu."""
        tournament_datas = self.view.get_tournament_datas()
        tournament = Tournament(tournament_datas["tournament_name"],
                                tournament_datas["tournament_place"],
                                tournament_datas["tournament_start_date"],
                                tournament_datas["tournament_comment"]
                                )
        while True:
            choice = self.view.get_tournament_menu_choice()
            if choice == "1":
                if self.tournament_player_add_menu(tournament):
                    continue
            elif choice == "2":
                if self.tournament_start(tournament):
                    break
            elif choice == "3":
                if self.view.get_back_to_menu_choice():
                    return False
                continue
        self.view.display_tournament_summary(tournament)
        while len(tournament.rounds_list) < tournament.total_round:
            self.run_round(tournament)
        self.end_tournament(tournament)

    def tournament_player_add_menu(self, tournament):
        """Manages the player addition menu.
        Return True to return to the tournament menu."""
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
                return True

    def add_tournament_players_by_id(self, tournament):
        """Manages the addition of players by chess ID method."""
        should_continue = True
        while should_continue:
            checked_player = self.player_controller.add_player_by_id()
            if checked_player is None:
                self.view.display_no_saved_players_error()
            elif checked_player is False:
                self.view.display_no_id_match_error()
            elif checked_player:
                add_success = tournament.add_tournament_player(checked_player)
                if add_success:
                    self.view.display_registered_player_succes()
                else:
                    self.view.display_already_added_player_error()
            should_continue = self.view.get_add_another_player_choice()

    def add_tournament_players_by_list(self, tournament):
        """Manages the addition of players by list method."""
        while True:
            checked_player = self.player_controller.add_players_by_list()
            if checked_player is None:
                self.view.display_no_saved_players_error()
                break
            add_success = tournament.add_tournament_player(checked_player)
            if add_success:
                self.view.display_registered_player_succes()
            else:
                self.view.display_already_added_player_error()
            if not self.view.get_add_another_player_choice():
                break

    def add_tournament_new_players(self, tournament):
        """Manages the addition of players using the player save method."""
        while True:
            player = self.player_controller.save_new_player()
            tournament.add_tournament_player(player)
            self.view.display_registered_player_succes()
            if not self.view.get_add_another_player_choice():
                break

    def tournament_start(self, tournament):
        """Manages choices and errors related to the start of the tournament.
        Return False to return to the tournament menu.
        Return True to start the tournament."""
        if tournament.check_players_numbers():
            self.view.display_players_numbers_error()
            self.view.get_back_to_tournament_menu_validation()
            return False
        if self.view.get_tournament_start_choice():
            return True
        return False

    def run_round(self, tournament):
        """Manages the start and end of rounds."""
        if tournament.actual_round_index == 0:
            self.view.get_first_round_start_validation()
            round = tournament.generate_round()
            self.view.display_round_start(round)
            self.generate_first_round_pairs(tournament, round)
        else:
            self.view.get_next_round_start_validation()
            round = tournament.generate_round()
            self.view.display_round_start(round)
            self.generate_intelligent_pairs(tournament, round)
        matches_list = round.matches_list
        self.view.display_matches(matches_list)
        self.view.get_end_round_validation()
        self.view.display_round_end(round)
        self.manages_scores(matches_list)
        self.view.display_results_summary(matches_list, round)
        self.view.display_scores(tournament.get_sorted_players())

    def generate_first_round_pairs(self, tournament, round):
        """Generate pairing with random method for the first round."""
        players_list = tournament.players_list
        random.shuffle(players_list)
        for i in range(0, len(players_list), 2):
            round.matches_list.append(Match(players_list[i],
                                            players_list[i+1]))

    def generate_intelligent_pairs(self, tournament, round):
        """Generate pairing with "smart" method"for the next rounds.
        When all unique matchups have been completed, force rematches."""
        sorted_players_list = tournament.get_sorted_players()
        used_players = set()
        previous_matches = self.played_match(tournament)
        for i in range(len(sorted_players_list)):
            player1 = sorted_players_list[i]
            if player1 in used_players:
                continue
            for j in range(i+1, len(sorted_players_list)):
                player2 = sorted_players_list[j]
                if player2 in used_players:
                    continue
                players_ids = sorted((player1.chess_id, player2.chess_id))
                if tuple(players_ids) not in previous_matches:
                    round.matches_list.append(Match(player1, player2))
                    used_players.update({player1, player2})
                    break
        self.check_and_add_remaining_players(tournament, round, used_players)

    def check_and_add_remaining_players(self, tournament, round, used_players):
        """Generate pairing with scores to force rematches"""
        remaining_players = []
        for player in tournament.get_sorted_players():
            if player not in used_players:
                remaining_players.append(player)
        if len(remaining_players) >= 2:
            for i in range(0, len(remaining_players), 2):
                round.matches_list.append(Match(remaining_players[i],
                                                remaining_players[i+1]))

    def played_match(self, tournament):
        """List all matches already played.
        Returns a sorted tuple to take into account the possibilities."""
        previous_matches = set()
        for round in tournament.rounds_list:
            for match in round.matches_list:
                previous_matches.add(tuple(sorted((match.player1.chess_id,
                                                   match.player2.chess_id))))
        return previous_matches

    def manages_scores(self, matches_list):
        """Manages points earned based on match results.
        Updates player scores."""
        for match_number, match in enumerate(matches_list, 1):
            result = self.view.get_match_result(match_number, match)
            if result == "1":
                pointp1 = 1
                pointp2 = 0
            if result == "2":
                pointp1 = 0
                pointp2 = 1
            if result == "3":
                pointp1 = 0.5
                pointp2 = 0.5
            match.add_match_result(pointp1, pointp2)
            match.player1.add_score(pointp1)
            match.player2.add_score(pointp2)

    def end_tournament(self, tournament):
        """Manages the end of tournaments."""
        scoreboard = tournament.get_sorted_players()
        self.view.display_tournament_end_summary(tournament, scoreboard)
        self.view.display_scores(scoreboard)
        self.view.get_end_tournament_validation()
