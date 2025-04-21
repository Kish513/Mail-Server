import tkinter as tk  # tkinter is how we build windows and GUI in Python
from client.client import Client  # this is the email client logic
from time import sleep  # might be used for delays or loading effects

# this is the main app window
class SMTP_client_gui(tk.Tk):
    def __init__(self):
        super().__init__()  # setup the window

        self.current_screen = None  # holds whatever screen is showing right now

        self.geometry("600x450")  # sets window size
        self.title("SMTP Client")  # sets the text in the title bar
        self.configure(bg="#f4f4f4")  # light grey background

    #switches the current screen to a new one
    def change_screen(self, screen, client=None):
        if self.current_screen:
            self.current_screen.destroy()  # removes old screen

        # create the new screen, might need the client object
        if client is not None:
            self.current_screen = screen(self, client)
        else:
            self.current_screen = screen(self)

        # show the screen and stretch it to fill space with some padding
        self.current_screen.pack(fill="both", expand=True, padx=20, pady=20)

        self.update_idletasks()  # makes sure layout updates right away

    # clears everything from the window
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    #gives back the main window object
    def get_root(self):
        return self
