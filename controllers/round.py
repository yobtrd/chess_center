import random

from controllers.helper import get_actual_datetime
from models.match import Match
from models.round import Round


class RoundController:
    """Controller for managing the round."""

    def __init__(self, view):
        """Initialization of the player controller with view."""
        self.view = view

    def run_round_flow(self, tournament, save):
        """Manages round flow and loading cases."""
        state = self.get_round_state(tournament)

        if state == "not_all_result_given":
            round = tournament.rounds_list[-1]
            self.process_pending_matches(tournament, round, save)
        elif state == "round_ended":
            round = tournament.rounds_list[-1]
            self.process_resume_ended_round(tournament, round, save)

        else:
            if state == "no_rounds_started":
                round = self.generate_first_round(tournament)
            elif state == "round_completed":
                round = self.generate_next_round(tournament)
            elif state == "round_not_ended":
                round = tournament.rounds_list[-1]
                self.view.display_resume_not_ending_round(round)
                self.view.display_round_start(round)
            self.display_matches(tournament, round, save)
            self.manages_round_end(tournament, round, save)
            self.manages_scores(round.matches_list, tournament, save)
        self.display_round_end_summary(tournament, round)
        save(tournament)

    def get_round_state(self, tournament):
        """Retrieves the progress of a round during loading."""
        matches_status = self.get_matches_status(tournament)
        if tournament.rounds_list:
            round_ended = tournament.rounds_list[-1].end_date
        if tournament.actual_round_index == 0:
            return "no_rounds_started"
        elif all(matches_status) and not round_ended:
            return "round_not_ended"
        elif all(matches_status) and round_ended:
            return "round_ended"
        elif any(matches_status):
            return "not_all_result_given"
        else:
            return "round_completed"

    def get_matches_status(self, tournament):
        """Indicate False if the matches are finished with results, True if not.
        Returns a list of booleans for each match.
        """
        matches_status = []
        if tournament.rounds_list:
            last_round = tournament.rounds_list[-1]
            for match in last_round.matches_list:
                is_unfinished = not match.match_result
                matches_status.append(is_unfinished)
        return matches_status

    def generate_first_round(self, tournament):
        """Manages the creation of the first round."""
        self.view.get_first_round_start_validation()
        round = self.create_new_round(tournament)
        self.generate_first_round_pairs(tournament, round)
        return round

    def generate_next_round(self, tournament):
        """Manages the creation of other rounds."""
        self.view.get_next_round_start_validation()
        round = self.create_new_round(tournament)
        self.generate_intelligent_pairs(tournament, round)
        return round

    def create_new_round(self, tournament):
        """Instance and return a round, add it to the tournament list."""
        new_round = Round(f"Round {len(tournament.rounds_list) + 1}")
        tournament.rounds_list.append(new_round)
        tournament.actual_round_index = len(tournament.rounds_list)
        new_round.start_date = get_actual_datetime()
        self.view.display_round_start(new_round)
        return new_round

    def process_pending_matches(self, tournament, round, save):
        """Manages empty match results during loading."""
        pending_matches = [match for match in round.matches_list if not match.match_result]
        match_number = self.get_actual_match_number(tournament, pending_matches[0])
        self.view.display_match_resume(match_number, round)
        self.manages_scores(pending_matches, tournament, save)

    def process_resume_ended_round(self, tournament, round, save):
        """Manages completed rounds during loading."""
        self.view.display_round_end(round)
        self.view.display_resume_ended_round(round)
        self.manages_scores(round.matches_list, tournament, save)

    def display_matches(self, tournament, round, save):
        """Manages the display of round matches."""
        self.view.display_matches(round.matches_list)
        save(tournament)
        self.view.get_end_round_validation()

    def manages_scores(self, matches_list, tournament, save):
        """Manages points earned based on match resultsand updates player scores."""
        for match in matches_list:
            actual_match_number = self.get_actual_match_number(tournament, match)
            result = self.view.get_match_result(actual_match_number, match)
            if result == "1":
                points_p1 = 1
                points_p2 = 0
            if result == "2":
                points_p1 = 0
                points_p2 = 1
            if result == "3":
                points_p1 = 0.5
                points_p2 = 0.5
            match.add_match_result(points_p1, points_p2)
            match.player1.add_score(points_p1)
            match.player2.add_score(points_p2)
            save(tournament)

    def manages_round_end(self, tournament, round, save):
        """Manages the end of rounds."""
        round.end_date = get_actual_datetime()
        self.view.display_round_end(round)
        save(tournament)

    def display_round_end_summary(self, tournament, round):
        """Displays the end-of-turn summary."""
        self.view.display_results_summary(round.matches_list, round)
        self.view.display_scores(tournament.get_sorted_players())

    def get_actual_match_number(self, tournament, match):
        """Returns the index of the current match."""
        return tournament.rounds_list[-1].matches_list.index(match) + 1

    # === Pairs generation methods ===
    def generate_first_round_pairs(self, tournament, round):
        """Generate pairing with random method for the first round."""
        players_list = tournament.players_list
        random.shuffle(players_list)
        for i in range(0, len(players_list), 2):
            round.matches_list.append(Match(players_list[i], players_list[i + 1]))

    def generate_intelligent_pairs(self, tournament, round):
        """Generate pairing with "smart" method"for the next rounds.
        When all unique matchups have been completed, force rematches.
        """
        sorted_players_list = tournament.get_sorted_players()
        used_players = set()
        previous_matches = self.played_match(tournament)

        for i in range(len(sorted_players_list)):
            player1 = sorted_players_list[i]
            if player1 in used_players:
                continue
            for j in range(i + 1, len(sorted_players_list)):
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
                round.matches_list.append(Match(remaining_players[i], remaining_players[i + 1]))

    def played_match(self, tournament):
        """List all matches already played.
        Returns a sorted tuple to take into account the possibilities.
        """
        previous_matches = set()
        for round in tournament.rounds_list:
            for match in round.matches_list:
                previous_matches.add(tuple(sorted((match.player1.chess_id, match.player2.chess_id))))
        return previous_matches
