class MenuController:
    """controller for managing the main menu."""

    def __init__(self, view, tournament_controller, player_controller):
        """Initialization of the main menu.
        Initialize the view and the needed controllers."""
        self.view = view
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def run_menu(self):
        """Manages menu selection."""
        while True:
            menu_choice = self.view.get_menu_choice()
            if menu_choice == "1":
                if self.view.get_tournament_choice():
                    while self.tournament_controller.run_new_tournament():
                        continue
            elif menu_choice == "2":
                if self.view.get_save_players_choice():
                    while True:
                        self.player_controller.save_new_player()
                        if not self.view.get_save_another_player_choice():
                            break
                continue
            elif menu_choice == "3":
                continue
            elif menu_choice == "4":
                continue
            elif menu_choice == "5":
                if self.view.get_quit_choice():
                    quit()
                continue
