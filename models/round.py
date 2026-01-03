from models.match import Match


class Round:
    """Data and business logic of the round."""

    def __init__(self, name, start_date=None, end_date=None):
        """Initiate all the data needed for the round."""
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches_list = []

    def to_dict(self):
        """Transform a Round model to a round's dictionnary datas."""
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": [m.to_dict() for m in self.matches_list],
        }

    @classmethod
    def from_dict(cls, round_data, players_dict):
        """Rebuilds round from a dictionary.."""
        round = Round(round_data["name"], round_data["start_date"], round_data["end_date"])
        round.matches_list = [Match.from_dict(m, players_dict) for m in round_data.get("matches", [])]
        return round
