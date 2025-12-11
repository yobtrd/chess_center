from models.tournament import Tournament


class TournamentController():

    def __init__(self, view, player_controller):
        """Initiate a view for the controller and
        the player controller"""
        self.view = view
        self.player_controller = player_controller

    def run_new_tournament(self):
        """Start and retrieve new tournament data.
        Displays tournament menu."""
        tournament_datas = self.view.get_tournament_datas()
        new_tournament = Tournament(tournament_datas["tournament_name"],
                                    tournament_datas["tournament_place"],
                                    tournament_datas["tournament_start_date"],
                                    tournament_datas["tournament_comment"]
                                    )
        while True:
            choice = self.view.get_tournament_menu_choice()
            if choice == "1":
                if self.tournament_player_add_menu(new_tournament):
                    continue
            elif choice == "2":
                if self.tournament_start(new_tournament):
                    break
            elif choice == "3":
                if self.view.get_back_to_menu_choice():
                    return False
                continue
        self.view.display_tournament_summary(new_tournament)
        if self.view.get_new_round_start_choice():
            pass

    def tournament_player_add_menu(self, new_tournament):
        """Displays the menu for adding players to the tournament.
        Return True to return to the tournament menu"""
        while True:
            counter = len(new_tournament.players_list)
            choice = self.view.get_tournament_player_menu_choice(counter)
            if choice == "1":
                self.add_tournament_players_by_id(new_tournament)
            elif choice == "2":
                self.add_tournament_players_by_list(new_tournament)
            elif choice == "3":
                self.add_tournament_new_players(new_tournament)
            elif choice == "4":
                return True

    def add_tournament_players_by_id(self, new_tournament):
        """Manages the addition of players to a tournament
        by searching for Chess IDs."""
        while True:
            player = self.player_controller.add_player_by_id()
            if player is None:
                self.view.display_no_saved_players_error()
                break
            elif player:
                success = new_tournament.add_tournament_player(player)
                if success:
                    self.view.display_registered_player_succes()
                else:
                    self.view.display_already_added_player_error()
            if not self.view.get_add_another_player_choice():
                break

    def add_tournament_players_by_list(self, new_tournament):
        """Manages the addition of players to a tournament
        by searching through a list."""
        while True:
            player = self.player_controller.add_players_by_list()
            if player is None:
                self.view.display_no_saved_players_error()
                break
            success = new_tournament.add_tournament_player(player)
            if success:
                self.view.display_registered_player_succes()
            else:
                self.view.display_already_added_player_error()
            if not self.view.get_add_another_player_choice():
                break

    def add_tournament_new_players(self, new_tournament):
        """Manages the addition of players to a tournament
        by registering them in the program."""
        while True:
            player = self.player_controller.save_new_player()
            new_tournament.add_tournament_player(player)
            self.view.display_registered_player_succes()
            if not self.view.get_add_another_player_choice():
                break

    def tournament_start(self, new_tournament):
        """Manages choices and errors related to the start of the tournament.
        Return False to return to the tournament menu,
        True to start the tournament"""
        if new_tournament.check_players_numbers():
            self.view.display_players_numbers_error()
            return False
        if self.view.get_tournament_start_choice():
            return True
        return False
