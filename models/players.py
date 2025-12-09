class Player:
    """Data and business logic of the player"""

    def __init__(self, last_name, first_name, birthdate, chess_id=None):
        """Initiate all the data needed for the player"""
        self.last_name = last_name.strip()
        self.first_name = first_name.strip()
        self.birthdate = birthdate
        self.chess_id = chess_id

    def score(self, actual_score):
        """update and link a player to a score"""
        self.actual_score = actual_score
        actual_score = 0
