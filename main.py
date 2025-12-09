from views.view import View
from controllers.controllers import Controller


def main():
    view = View()
    app = Controller(view)
    app.run_menu()


if __name__ == ("__main__"):
    main()
