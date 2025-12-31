import datetime


@staticmethod
def get_actual_datetime():
    """Returns the updated date and time at any point when called."""
    return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
