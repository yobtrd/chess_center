import datetime

DATETIME = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")


class Tournament:
    """Data and business logic of the tournament"""

    def __init__(self, name, place, description=None,
                 tournament_start_date=DATETIME,
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
        """Add player to tournament if not already registered"""
        if self.check_already_added_player(player):
            return False
        self.players_list.append(player)
        return True

    def check_already_added_player(self, player):
        """Method for checking if a player
        is already registered for the tournament"""
        for p in self.players_list:
            if (p.last_name == player.last_name and
               p.first_name == player.first_name):
                return True

    def check_existing_players(self):
        """Method for checking if there is a player
        registered for the tournament"""
        if not self.players_list:
            return True
        return False
