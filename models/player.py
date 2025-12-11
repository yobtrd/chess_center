class Player:
    """Data and business logic of the player"""

    def __init__(self, last_name, first_name, birthdate, chess_id):
        """Initiate all the data needed for the player"""
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.chess_id = chess_id

    def score(self, actual_score):
        """update and link a player to a score"""
        self.actual_score = actual_score
        actual_score = 0
