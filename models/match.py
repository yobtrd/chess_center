class Match:
    """Data and business logic of the match."""

    def __init__(self, player1, player2):
        """Initiate all the data needed for the match."""
        self.player1 = player1
        self.player2 = player2
        self.match_result = ()

    def add_match_result(self, score1, score2):
        """Add the match's results by giving the players the correct score."""
        self.match_result = ([self.player1, score1], [self.player2, score2])
        return self.match_result
