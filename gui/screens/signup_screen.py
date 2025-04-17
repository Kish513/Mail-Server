import tkinter as tk
import tkinter.font as tkFont

# Assuming these exist in their respective paths
from client.client import Client # Make sure this path is correct
from .main_screen import main_screen # Make sure this path is correct

class signup_screen(tk.Frame):
    # --- Constants defined at CLASS LEVEL ---
    BG_COLOR = "#2E3440"  # Nord Polar Night
    FG_COLOR = "#ECEFF4"  # Nord Snow Storm
    ENTRY_BG = "#3B4252"  # Slightly lighter Nord Polar Night
    ENTRY_FG = "#ECEFF4"
    PLACEHOLDER_COLOR = "#4C566A" # Dim color for placeholder text (if needed)
    LABEL_COLOR = "#D8DEE9" # Lighter gray for labels - ACCESSIBLE NOW
    BTN_BG_COLOR = "#5E81AC" # Nord Frost (Blue)
    BTN_FG_COLOR = "#ECEFF4"
    BTN_HOVER_BG = "#81A1C1" # Lighter Nord Frost
    SUCCESS_COLOR = "#A3BE8C" # Nord Frost - Aurora (Green) - ACCESSIBLE NOW
    ERROR_COLOR = "#BF616A" # Nord Frost - Aurora (Red) - ACCESSIBLE NOW
    TITLE_FONT_FAMILY = "Helvetica"
    DEFAULT_FONT_FAMILY = "Helvetica"

    def __init__(self, manager):
        super().__init__(manager)  # Initialize the frame
        self.manager = manager
        self.user = None # Initialize user attribute

        # --- Apply Background Color ---
        self.config(bg=self.BG_COLOR) # Access via self

        # --- Define Fonts ---
        self.title_font = tkFont.Font(family=self.TITLE_FONT_FAMILY, size=20, weight="bold")
        self.label_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11)
        self.entry_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11)
        self.button_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=12, weight="bold")
        self.message_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=10)

        # --- Set Window Properties via Manager ---
        self.manager.title("SMTP Client - Create Account")
        self.manager.geometry("400x450") # Increased size for better spacing

        # --- Create a central frame ---
        center_frame = tk.Frame(self, bg=self.BG_COLOR)
        center_frame.pack(pady=20, padx=30, expand=True) # Added padding

        # --- Title Label ---
        label = tk.Label(
            center_frame,
            text="Create Account",
            font=self.title_font,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        label.pack(pady=(10, 25)) # Padding below title

        # --- Input Fields Styling ---
        label_options = {
            "font": self.label_font,
            "bg": self.BG_COLOR,
            "fg": self.LABEL_COLOR, # Access constant
            "anchor": "w" # Align label text to the west (left)
        }
        entry_options = {
            "font": self.entry_font,
            "bg": self.ENTRY_BG, # Access constant
            "fg": self.ENTRY_FG, # Access constant
            "relief": tk.FLAT,
            "borderwidth": 2, # Subtle border
            "insertbackground": self.FG_COLOR, # Cursor color
            "width": 35 # Increased width
        }

        # --- Server IP ---
        tk.Label(center_frame, text="Server Domain/IP:", **label_options).pack(fill=tk.X, pady=(10, 2))
        self.entry_server_ip = tk.Entry(center_frame, **entry_options)
        self.entry_server_ip.pack(fill=tk.X, ipady=4) # ipady for internal padding

        # --- Email (Username part only) ---
        tk.Label(center_frame, text="Username (before @):", **label_options).pack(fill=tk.X, pady=(10, 2))
        self.entry_email_user = tk.Entry(center_frame, **entry_options)
        self.entry_email_user.pack(fill=tk.X, ipady=4)

        # --- Password ---
        tk.Label(center_frame, text="Password:", **label_options).pack(fill=tk.X, pady=(10, 2))
        self.entry_password = tk.Entry(center_frame, show="*", **entry_options)
        self.entry_password.pack(fill=tk.X, ipady=4)

        # --- Message Label (for feedback) ---
        self.message_label = tk.Label(
            center_frame,
            text="", # Initially empty
            font=self.message_font,
            bg=self.BG_COLOR, # Access constant
            # fg color will be set dynamically
            wraplength=300 # Wrap text if message is long
        )
        self.message_label.pack(pady=(15, 5)) # Space before the button

        # --- Signup Button ---
        button_options_signup = {
            "font": self.button_font,
            "bg": self.BTN_BG_COLOR, # Access constant
            "fg": self.BTN_FG_COLOR, # Access constant
            "activebackground": "#4C566A", # Could be a constant too
            "activeforeground": self.FG_COLOR, # Access constant
            "relief": tk.FLAT,
            "borderwidth": 0,
            "width": 15,
            "pady": 8 # Internal padding
        }

        signup_button = tk.Button(
            center_frame,
            text="Sign Up",
            command=self.signup, # Call method directly
            **button_options_signup
        )
        signup_button.pack(pady=(10, 20)) # More space around the button

        # --- Hover Effects ---
        def on_enter(e):
            e.widget['background'] = self.BTN_HOVER_BG # Access via self

        def on_leave(e):
            e.widget['background'] = self.BTN_BG_COLOR # Access via self

        signup_button.bind("<Enter>", on_enter)
        signup_button.bind("<Leave>", on_leave)


    def signup(self):
        # Get values directly from instance attributes
        server_ip = self.entry_server_ip.get().strip()
        email_user = self.entry_email_user.get().strip()
        password = self.entry_password.get() # No strip for password

        if not server_ip or not email_user or not password:
            # Access ERROR_COLOR via self
            self.message_label.config(text="All fields are required.", fg=self.ERROR_COLOR)
            return

        # Construct full email
        user_name = f"{email_user}@{server_ip}"

        # Access LABEL_COLOR via self
        self.message_label.config(text="Attempting signup...", fg=self.LABEL_COLOR)
        self.update_idletasks() # Ensure message updates immediately

        try:
            # Create Client instance
            self.user = Client(user_name, password, server_ip)
            is_signed_up = self.user.sign_up() # Assuming returns True/False or raises Exception

            if is_signed_up:
                # Access SUCCESS_COLOR via self
                self.message_label.config(text="Signup successful!\nLoading main screen...", fg=self.SUCCESS_COLOR)
                # Use 'after' to give time for the user to see the message
                self.manager.after(1500, self.load_main_screen) # Delay in ms
            else:
                # Access ERROR_COLOR via self
                self.message_label.config(text="Signup failed. User might already exist or server error.", fg=self.ERROR_COLOR)

        except Exception as e:
            # Access ERROR_COLOR via self
            self.message_label.config(text=f"Error: {e}", fg=self.ERROR_COLOR)
            print(f"Signup Error: {e}") # Log detailed error to console


    def load_main_screen(self):
        # Pass the created user object to the main screen
        self.manager.change_screen(main_screen, self.user)