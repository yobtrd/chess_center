import datetime


class HelperController:
    """controller for function that cut across other controllers."""

    @staticmethod
    def get_actual_datetime():
        """Returns the updated date and time at any point when called."""
        return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
