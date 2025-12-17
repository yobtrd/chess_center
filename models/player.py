class Player:
    """Data and business logic of the player"""

    def __init__(self, last_name, first_name, birthdate, chess_id, score=0.0):
        """Initiate all the data needed for the player."""
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.chess_id = chess_id
        self.score = float(score)

    def add_score(self, points):
        """Add points to the player's score."""
        self.score += float(points)
