import datetime

DATETIME = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")


class Round:
    """Data and business logic of the round"""
    def __init__(self, name, round_start_date=DATETIME, round_end_date=None):
        """Initiate all the data needed for the round"""
        self.name = name
        self.round_start_date = round_start_date
        self.round_end_date = round_end_date
        self.matches_list = []

    def end_round(self, round_end_date=DATETIME):
        """End the actual round"""
        self.round_end_date = round_end_date
        # Faire un generate_match auto ?
