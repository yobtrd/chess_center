from views.user import UserView
from controllers.menu import MenuController
from controllers.tournament import TournamentController
from controllers.player import PlayerController
from controllers.round import RoundController
from controllers.report import ReportController


def main():
    view = UserView()
    player_controller = PlayerController(view)
    round_controller = RoundController(view)
    tournament_controller = TournamentController(view,
                                                 player_controller,
                                                 round_controller)
    report_controller = ReportController(view,
                                         player_controller,
                                         tournament_controller)
    menu_controller = MenuController(view,
                                     tournament_controller,
                                     player_controller,
                                     report_controller)
    menu_controller.main_menu()


if __name__ == "__main__":
    main()
