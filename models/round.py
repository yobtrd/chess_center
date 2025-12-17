import datetime


class Round:
    """Data and business logic of the round."""

    def __init__(self, name):
        """Initiate all the data needed for the round."""
        self.name = name
        self.matches_list = []

    @property
    def round_start_date(self):
        """Returns the updated date and time at any point when called."""
        return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")

    @property
    def round_end_date(self):
        """Returns the updated date and time at any point when called."""
        return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
