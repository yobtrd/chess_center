class MenuController:
    """controller for managing the main menu."""

    def __init__(self, view, tournament_controller, player_controller, report_controller):
        """Initialization of the main menu.
        Initializes the view and the needed controllers.
        """
        self.view = view
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller
        self.report_controller = report_controller

    def main_menu(self):
        """Manages main menu selection."""
        while True:
            menu_choice = self.view.get_main_menu_choice()
            if menu_choice == "1":
                if self.are_saved_tournament() and self.are_saved_tournament_unfinished():
                    self.view.display_last_tournament_overwrite_warning()
                if self.view.get_start_new_tournament_choice():
                    self.start_new_tournament()
            elif menu_choice == "2":
                if self.view.get_save_players_choice():
                    self.save_new_players()
            elif menu_choice == "3":
                if self.view.get_resume_last_tournament_choice():
                    self.resume_last_tournament()
            elif menu_choice == "4":
                if self.view.get_generate_report_choice():
                    self.report_controller.reports_main_menu()
            elif menu_choice == "5":
                if self.view.get_quit_choice():
                    quit()

    def start_new_tournament(self):
        """Manages new tournament start selection."""
        tournament = self.tournament_controller.create_new_tournament()
        while self.tournament_controller.tournament_menu(tournament):
            continue

    def save_new_players(self):
        """Manages save new player selection."""
        while True:
            self.player_controller.save_new_player()
            if not self.view.get_save_another_player_choice():
                break

    def resume_last_tournament(self):
        """Manages the resumption of tournaments based on the last save."""
        tournament = self.tournament_controller.load_last_tournament()
        if tournament is None:
            self.view.display_no_saved_tournament_error()
            self.view.get_back_to_main_menu_validation()
        elif self.are_saved_tournament_unfinished() is False:
            self.view.display_finished_tournament_error()
            self.view.get_back_to_main_menu_validation()
        elif tournament.actual_round_index == 0:
            while self.tournament_controller.tournament_menu(tournament):
                continue
        else:
            self.tournament_controller.run_tournament_flow(tournament)

    def are_saved_tournament(self):
        """Returns True if a tournament is saved, False otherwise."""
        if self.tournament_controller.saved_tournaments_list:
            return True
        else:
            return False

    def are_saved_tournament_unfinished(self):
        """Returns True if a currently saved tournament is not finished.
        Rertuns False if not.
        """
        last_saved_tournament = self.tournament_controller.saved_tournaments_list[-1]
        if last_saved_tournament["tournament_datas"]["end_date"]:
            return False
        else:
            return True
