class Player:
    """Data and business logic of the player"""

    def __init__(self, last_name, first_name, birthdate, chess_id, score=0.0):
        """Initializes all the data needed for the player."""
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.chess_id = chess_id
        self.score = score

    def add_score(self, points):
        """Add points to the player's score."""
        self.score += float(points)

    def to_dict(self):
        """Transforms a Player model to a minimal dictionnary datas."""
        return {
            "chess_id": self.chess_id,
        }

    @classmethod
    def from_dict(cls, datas):
        """Rebuilds players from a dictionary."""
        return Player(
            datas["last_name"], datas["first_name"], datas["birthdate"], datas["chess_id"], datas.get("score", 0.0)
        )
