import json
from pathlib import Path
from models.player import Player


class PlayerController():
    """Controller for managing the players datas and database."""

    def __init__(self, view):
        """Initialization of the player controller with view.
        Store saved players and the save path."""
        self.view = view
        self.saved_players_list = []
        self.filepath = Path("data/players/players.json")

    def save_new_player(self):
        """Save a new player to the program.
        Return a Player when used for adding one to a tournament."""
        while True:
            player_datas = self.view.get_player_datas()
            Path("data/players").mkdir(parents=True, exist_ok=True)
            self.load_saved_players_list()
            self.saved_players_list.append(player_datas)
            with open(self.filepath, "w") as file:
                json.dump(self.saved_players_list, file)
            self.view.display_saved_player_success()
            return self.dict_datas_to_player_model(player_datas)

    def load_saved_players_list(self):
        """Load the saved players list.
        Reset the list in case of corrupt file or no players saved."""
        try:
            with open(self.filepath, "r") as file:
                self.saved_players_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_players_list = []

    def dict_datas_to_player_model(self, player_datas):
        """Transform a player's dictionnary datas to a player model."""
        return Player(player_datas["last_name"],
                      player_datas["first_name"],
                      player_datas["birthdate"],
                      player_datas["chess_id"]
                      )

    def add_player_by_id(self):
        """Allows to add saved players to a tournament via their chess ID.
        Return None if there are no saved players.
        Return False if the ID in incorrect."""
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        input_id = self.view.display_add_player_by_id_message()
        for player_datas in self.saved_players_list:
            if player_datas["chess_id"] == input_id.strip().upper():
                return self.dict_datas_to_player_model(player_datas)
        return False

    def add_players_by_list(self):
        """Allows to add saved players to a tournament via a list.
        Return None if there are no saved players."""
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        self.view.display_saved_players_list(self.saved_players_list)
        player_datas = (
            self.view.get_saved_player_choice(self.saved_players_list))
        return self.dict_datas_to_player_model(player_datas)

    def check_no_saved_players(self):
        """Return True if there are no saved players."""
        return len(self.saved_players_list) == 0
