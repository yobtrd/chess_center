import random


class Tournament:
    """Data and business logic of the tournament."""

    def __init__(self, name, place, start_date, end_date=None, total_rounds=4, description=None, actual_round_index=0):
        """Initiate all the data needed for the tournament.
        players_list lists all registered players in the tournament.
        rounds_list list all the Round instance of the tournament.
        """
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.total_rounds = int(total_rounds)
        self.description = description
        self.actual_round_index = actual_round_index
        self.players_list = []
        self.rounds_list = []

    def to_dict(self):
        """Transform a Tournament model to a tournament's dictionnary datas."""
        return {
            "name": self.name,
            "place": self.place,
            "start_date": str(self.start_date),
            "end_date": self.end_date,
            "total_rounds": self.total_rounds,
            "description": self.description,
        }

    def add_tournament_player(self, player):
        """Add player to tournament if not already registered.
        Return False if a player is already added.
        """
        if self.check_already_added_player(player):
            return False
        self.players_list.append(player)
        return True

    def check_already_added_player(self, player):
        """Checks if a player is already registered for the tournament.
        Return True if already added.
        """
        for p in self.players_list:
            if p.chess_id == player.chess_id:
                return True

    def check_players_numbers(self):
        """Checks if the registered player is enough to start a tournament.
        Return True if it does.
        """
        if len(self.players_list) >= 2 and len(self.players_list) % 2 == 0:
            return False
        return True

    def get_sorted_players(self):
        """Return players sorted by score,
        with random order for tied scores.
        """
        shuffled_players = self.players_list.copy()
        random.shuffle(shuffled_players)
        scoreboard = sorted(shuffled_players, key=lambda player: player.score, reverse=True)
        return scoreboard
