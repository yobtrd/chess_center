class Match:
    """Data and business logic of the match."""

    def __init__(self, player1, player2):
        """Initiate all the data needed for the match."""
        self.player1 = player1
        self.player2 = player2
        self.match_result = ()

    def add_match_result(self, point_p1, points_p2):
        """Add the match's results by giving the players the correct score."""
        self.match_result = ([self.player1, point_p1],
                             [self.player2, points_p2])
        return self.match_result

    def to_dict(self):
        """Transform a Match model to a match's dictionnary datas."""
        result = {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict()
        }
        if self.match_result:
            result["match_result"] = {
                self.player1.chess_id: self.match_result[0][1],
                self.player2.chess_id: self.match_result[1][1]
            }
        return result

    @classmethod
    def from_dict(cls, match_data, players_dict):
        """Rebuilds matches from a dictionary."""
        player1 = players_dict[match_data["player1"]["chess_id"]]
        player2 = players_dict[match_data["player2"]["chess_id"]]
        match = Match(player1, player2)
        if "match_result" in match_data:
            points_p1 = match_data["match_result"][player1.chess_id]
            points_p2 = match_data["match_result"][player2.chess_id]
            match.add_match_result(points_p1, points_p2)
        return match
