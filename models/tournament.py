import datetime

DATETIME = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")


class Tournament:
    """Data and business logic of the tournament"""

    def __init__(self, name, place, tournament_start_date, description=None,
                 tournament_end_date=None, total_round=4):
        """Initiate all the data needed for the tournament"""
        self.name = name
        self.place = place
        self.description = description
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.total_round = total_round
        self.players_list = []
        self.rounds_list = []
        self.actual_round_index = 0

    def add_tournament_player(self, player):
        """Add player to tournament if not already registered
        Return False if a player is already added"""
        if self.check_already_added_player(player):
            return False
        self.players_list.append(player)
        return True

    def check_already_added_player(self, player):
        """Method for checking if a player
        is already registered for the tournament
        Return True if already added"""
        for p in self.players_list:
            if (p.chess_id == player.chess_id):
                return True

    def check_players_numbers(self):
        """Method for checking if the registered player
        is enough to start a tournament
        Return True if good."""
        if len(self.players_list) >= 2 and len(self.players_list) % 2 == 0:
            return False
        return True
