from db.UserDBInterface import UserDBInterface
from HelperClasses.User import User
from client.client import Client
from gui.client_gui import SMTP_client_gui
from gui.screens.start_screen import start_screen


def main():
    client_gui = SMTP_client_gui()
    client_gui.change_screen(start_screen) 
    client_gui.mainloop()
if __name__ == "__main__":
    main()