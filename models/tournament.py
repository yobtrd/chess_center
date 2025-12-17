import datetime
from models.round import Round


class Tournament:
    """Data and business logic of the tournament."""

    def __init__(self, name, place, tournament_start_date, description=None,
                 total_round=4):
        """Initiate all the data needed for the tournament.
        players_list lists all registered players in the tournament.
        rounds_list list all the Round instance of the tournament."""
        self.name = name
        self.place = place
        self.description = description
        self.tournament_start_date = tournament_start_date
        self.total_round = total_round
        self.players_list = []
        self.rounds_list = []
        self.actual_round_index = 0

    @property
    def tournament_end_date(self):
        """Returns the updated date and time at any point when called."""
        return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")

    def add_tournament_player(self, player):
        """Add player to tournament if not already registered.
        Return False if a player is already added."""
        if self.check_already_added_player(player):
            return False
        self.players_list.append(player)
        return True

    def check_already_added_player(self, player):
        """Checks if a player is already registered for the tournament.
        Return True if already added."""
        for p in self.players_list:
            if (p.chess_id == player.chess_id):
                return True

    def check_players_numbers(self):
        """Checks if the registered player is enough to start a tournament.
        Return True if it does."""
        if len(self.players_list) >= 2 and len(self.players_list) % 2 == 0:
            return False
        return True

    def generate_round(self):
        """Instance and return a round, add it to the tournament list."""
        round = Round(f"Round {len(self.rounds_list) + 1}")
        self.rounds_list.append(round)
        self.actual_round_index = len(self.rounds_list)
        return round

    def get_sorted_players(self):
        """Return a list of sorted players according to their score."""
        scoreboard = sorted(self.players_list,
                            key=lambda player: player.score,
                            reverse=True)
        return scoreboard
