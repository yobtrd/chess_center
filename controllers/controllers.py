import json
import os
from models.tournament import Tournament
from models.players import Player


class Controller:
    """Initiate a view for the controller
    and manage the different controllers"""

    def __init__(self, view):
        """Initiate a view for the controller"""
        self.view = view

    def run_menu(self):
        """Run the menu, display and get the user's options"""
        menu_choice = self.view.get_menu_choice()
        while True:
            if menu_choice == "1":
                self.run_new_tournament()
            if menu_choice == "2":
                choice = self.view.get_save_players_choice()
                if choice == "y":
                    self.save_new_player()
                self.run_menu()
            if menu_choice == "3":
                self.run_menu()
            if menu_choice == "4":
                self.run_menu()
            if menu_choice == "5":
                choice = self.view.get_quit_confirmation()
                if choice == "y":
                    quit()
                self.run_menu()

    def save_new_player(self):
        """Save a new players to the program"""
        player_datas = self.view.get_player_datas()
        last_name = player_datas["last_name"]
        first_name = player_datas["first_name"]
        filepath = rf"data\players\{last_name}_{first_name}.json"
        with open(filepath, "w") as file:
            json.dump(player_datas, file)
        player = Player(player_datas["last_name"],
                        player_datas["first_name"],
                        player_datas["birthdate"],
                        player_datas["chess_id"]
                        )
        return player

    def add_saved_players(self):
        """Get and add a saved player to a tournament"""
        saved_players_list = [saved_player for saved_player
                              in os.listdir("data/players")]
        if not saved_players_list:
            self.view.display_no_saved_players_error()
        choice = self.view.get_saved_player_choice(saved_players_list)
        with open(rf"data\players\{choice}", "r") as file:
            player_datas = json.load(file)
            player = Player(player_datas["last_name"],
                            player_datas["first_name"],
                            player_datas["birthdate"],
                            player_datas["chess_id"]
                            )
            return player

    def run_new_tournament(self):
        """Start a new tournament, retrieve tournament data,
        manage player additions"""
        new_tournament_choice = self.view.get_tournament_choice()
        if new_tournament_choice == "y":
            tournament_datas = self.view.get_tournament_datas()
            new_tournament = Tournament(tournament_datas["tournament_name"],
                                        tournament_datas["tournament_place"],
                                        tournament_datas["tournament_comment"]
                                        )
            while True:
                add_tournament_players_choice = (
                    self.view.get_tournament_menu_choice())
                if add_tournament_players_choice == "1":
                    tournament_player_type_choice = (
                        self.view.get_tournament_player_type_choice())
                    if tournament_player_type_choice == "1":
                        player = self.save_new_player()
                        new_tournament.add_tournament_player(player)
                    elif tournament_player_type_choice == "2":
                        player = self.add_saved_players()
                        if new_tournament.add_tournament_player(player):
                            continue
                        else:
                            self.view.display_added_player_error()
                if add_tournament_players_choice == "2":
                    if new_tournament.check_existing_players():
                        self.view.display_no_player_error()
                        continue
                    start_choice = self.view.get_tournament_start_choice()
                    if start_choice == "n":
                        continue
                    if start_choice == "y":
                        break
            self.view.display_tournament_summary(new_tournament)
            self.view.get_new_round_start_choice()
        elif new_tournament_choice == "n":
            return self.run_menu()
