import tkinter as tk
import tkinter.font as tkFont

# Assuming these exist in their respective paths
from client.client import Client # Although client object is passed, import might be needed for type hinting or checks if used more extensively
from .showemail_screen import show_mail_screen # Make sure this path is correct
from .sendmail_screen import send_mail_screen # Make sure this path is correct

class main_screen(tk.Frame):
    def __init__(self, manager, client):
        super().__init__(manager)  # Initialize the frame
        self.manager = manager
        self.client = client # Store the passed client object

        # --- Configuration (Consistent with other screens) ---
        BG_COLOR = "#2E3440"  # Nord Polar Night
        FG_COLOR = "#ECEFF4"  # Nord Snow Storm
        LABEL_COLOR = "#D8DEE9" # Lighter gray for secondary labels
        WELCOME_COLOR = "#EBCB8B" # Nord Frost - Aurora (Yellow) for emphasis
        BTN_BG_COLOR = "#5E81AC" # Nord Frost (Blue)
        BTN_FG_COLOR = "#ECEFF4"
        BTN_HOVER_BG = "#81A1C1" # Lighter Nord Frost
        TITLE_FONT_FAMILY = "Helvetica"
        DEFAULT_FONT_FAMILY = "Helvetica"

        # --- Apply Background Color ---
        self.config(bg=BG_COLOR)

        # --- Define Fonts ---
        self.title_font = tkFont.Font(family=TITLE_FONT_FAMILY, size=24, weight="bold")
        self.welcome_font = tkFont.Font(family=DEFAULT_FONT_FAMILY, size=12)
        self.button_font = tkFont.Font(family=DEFAULT_FONT_FAMILY, size=14, weight="bold") # Slightly larger buttons

        # --- Set Window Properties (Optional - manager might handle this) ---
        self.manager.title("SMTP Client - Main Menu")
        # Adjust size as needed, maybe make it larger for future content
        self.manager.geometry("500x400")

        # --- Create a central frame ---
        center_frame = tk.Frame(self, bg=BG_COLOR)
        center_frame.pack(pady=30, padx=40, expand=True) # Generous padding

        # --- Title Label ---
        title_label = tk.Label(
            center_frame,
            text="Main Menu",
            font=self.title_font,
            bg=BG_COLOR,
            fg=FG_COLOR
        )
        title_label.pack(pady=(10, 5))

        # --- Welcome Message ---
        user_email = "Unknown User" # Default text
        try:
            # Attempt to get email from client object
            if self.client and hasattr(self.client, 'email'):
                user_email = self.client.email
        except Exception as e:
            print(f"Could not retrieve client email: {e}") # Log error if needed

        welcome_text = f"Welcome, {user_email}"
        welcome_label = tk.Label(
            center_frame,
            text=welcome_text,
            font=self.welcome_font,
            bg=BG_COLOR,
            fg=WELCOME_COLOR # Use the distinct welcome color
        )
        welcome_label.pack(pady=(0, 40)) # More space below welcome message

        # --- Button Styling ---
        button_options = {
            "font": self.button_font,
            "bg": BTN_BG_COLOR,
            "fg": BTN_FG_COLOR,
            "activebackground": "#4C566A",
            "activeforeground": FG_COLOR,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "width": 18, # Wider buttons
            "pady": 12  # Taller buttons
        }

        # --- Send Email Button ---
        button_sendemail = tk.Button(
            center_frame,
            text="📧 Send Email", # Added icon
            command=self.load_sendemail_screen,
            **button_options
        )
        button_sendemail.pack(pady=15) # Spacing between buttons

        # --- Show Email Button ---
        button_showemail = tk.Button(
            center_frame,
            text="📬 Show Emails", # Added icon
            command=self.load_showemail_screen,
            **button_options
        )
        button_showemail.pack(pady=15)

        # --- Hover Effects ---
        def on_enter(e):
            e.widget['background'] = BTN_HOVER_BG

        def on_leave(e):
            e.widget['background'] = BTN_BG_COLOR

        button_sendemail.bind("<Enter>", on_enter)
        button_sendemail.bind("<Leave>", on_leave)
        button_showemail.bind("<Enter>", on_enter)
        button_showemail.bind("<Leave>", on_leave)

        # --- Optional: Logout Button ---
        # logout_button = tk.Button(center_frame, text="Logout", command=self.logout, ...)
        # logout_button.pack(pady=(30, 10)) # More space before logout


    def load_sendemail_screen(self):
        # Manager handles destroying the current frame
        self.manager.change_screen(send_mail_screen, self.client)


    def load_showemail_screen(self):
        # Manager handles destroying the current frame
        self.manager.change_screen(show_mail_screen, self.client)

    # --- Optional: Logout Method ---
    # def logout(self):
    #     # Add any client-side logout cleanup if needed (e.g., disconnecting)
    #     # try:
    #     #     if self.client:
    #     #         self.client.disconnect() # Assuming a disconnect method exists
    #     # except Exception as e:
    #     #     print(f"Error during logout cleanup: {e}")
    #
    #     from .start_screen import start_screen # Local import to avoid circular issues
    #     self.manager.change_screen(start_screen) # Go back to start screen