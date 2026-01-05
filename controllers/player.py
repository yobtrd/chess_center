import json
from pathlib import Path

from models.player import Player


class PlayerController:
    """Controller for managing the players datas and database."""

    def __init__(self, view):
        """Initialization of the player controller with view.
        Store saved players and the save path.
        """
        self.view = view
        self.filepath = Path("data/players/players.json")
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.saved_players_list = []
        self.load_saved_players_list()

    def save_new_player(self):
        """Save a new player to the program.
        Returns a Player when used for adding one to a tournament.
        """
        while True:
            intitial_player_datas = self.view.get_player_datas()
            player_datas = self.transform_players_datas(intitial_player_datas)
            self.load_saved_players_list()
            self.saved_players_list.append(player_datas)
            with open(self.filepath, "w") as file:
                json.dump(self.saved_players_list, file)
            self.view.display_saved_player_success()
            return Player.from_dict(player_datas)

    def load_saved_players_list(self):
        """Load the saved players list.
        Reset the list in case of corrupt file or no players saved.
        """
        try:
            with open(self.filepath, "r") as file:
                self.saved_players_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_players_list = []

    def add_player_by_id(self):
        """Allows to add saved players to a tournament via their chess ID.
        Returns None if there are no saved players.
        Returns False if the ID in incorrect.
        """
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        input_id = self.view.get_add_player_by_id_id()
        for player_datas in self.saved_players_list:
            if player_datas["chess_id"] == input_id.strip().upper():
                return Player.from_dict(player_datas)
        return False

    def add_players_by_list(self):
        """Allows to add saved players to a tournament via a list.
        Returns None if there are no saved players.
        """
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        self.view.display_saved_players_list(self.saved_players_list)
        player_datas = self.view.get_saved_player_choice(self.saved_players_list)
        return Player.from_dict(player_datas)

    def check_no_saved_players(self):
        """Returns True if there are no saved players."""
        return len(self.saved_players_list) == 0

    def transform_players_datas(self, initial_player_datas):
        """Transforms player data to ensure the same format for all players."""
        formatted_data = initial_player_datas.copy()
        for name_field in ["last_name", "first_name"]:
            formatted_data[name_field] = formatted_data[name_field].capitalize()
        return formatted_data
