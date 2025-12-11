import json
from pathlib import Path
from models.player import Player


class PlayerController():

    def __init__(self, view):
        """Initiate a view for the controller
        and keep track of saved players"""
        self.view = view
        self.saved_players_list = []
        self.filepath = Path("data/players/players.json")

    def save_new_player(self):
        """Save a new player to the program
        Return a Player to be added to a tournament"""
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
        """Load the saved players lists"""
        try:
            with open(self.filepath, "r") as file:
                self.saved_players_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_players_list = []

    def dict_datas_to_player_model(self, player_datas):
        """Transform a player's dictionnary datas to a
        proper player model"""
        return Player(player_datas["last_name"],
                      player_datas["first_name"],
                      player_datas["birthdate"],
                      player_datas["chess_id"]
                      )

    def add_player_by_id(self):
        """Allows to add saved players to a tournament
        via their chess ID."""
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        input_id = self.view.display_add_player_by_id_message()
        for player_datas in self.saved_players_list:
            if player_datas["chess_id"] == input_id.strip().upper():
                return self.dict_datas_to_player_model(player_datas)
        self.view.display_no_id_match_error()
        return None

    def add_players_by_list(self):
        """Display the list of saved players
        and allows to add one to a tournament"""
        self.load_saved_players_list()
        if self.check_no_saved_players():
            return None
        self.view.display_saved_players_list(self.saved_players_list)
        player_datas = (
            self.view.get_saved_player_choice(self.saved_players_list))
        return self.dict_datas_to_player_model(player_datas)

    def check_no_saved_players(self):
        """Check if there are any saved players."""
        return len(self.saved_players_list) == 0
