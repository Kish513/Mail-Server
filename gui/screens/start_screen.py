import tkinter as tk
import tkinter.font as tkFont  # Import font module

# Assuming these exist in the specified relative paths
from .login_screen import login_screen
from .signup_screen import signup_screen

class start_screen(tk.Frame):
    def __init__(self, manager):
        super().__init__(manager) # Initialize as a Frame with the manager as the parent
        self.manager = manager

        # --- Configuration ---
        BG_COLOR = "#2E3440"  # Nord Polar Night (Dark Blue/Gray)
        FG_COLOR = "#ECEFF4"  # Nord Snow Storm (Light Gray/White)
        BTN_BG_COLOR = "#5E81AC" # Nord Frost (Blue)
        BTN_FG_COLOR = "#ECEFF4" # Nord Snow Storm
        BTN_HOVER_BG = "#81A1C1" # Lighter Nord Frost
        TITLE_FONT_FAMILY = "Helvetica" # Or "Arial", "Verdana" etc.
        DEFAULT_FONT_FAMILY = "Helvetica"

        # --- Apply Background Color ---
        self.config(bg=BG_COLOR)

        # --- Define Fonts ---
        self.title_font = tkFont.Font(family=TITLE_FONT_FAMILY, size=28, weight="bold")
        self.button_font = tkFont.Font(family=DEFAULT_FONT_FAMILY, size=14, weight="bold")

        # --- Create a central frame for better alignment ---
        # This frame will hold the content and be centered
        center_frame = tk.Frame(self, bg=BG_COLOR)
        # Place the center_frame in the middle of the start_screen frame
        # It will expand vertically and horizontally if the window is resized
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        # --- Title Label ---
        # Place the label inside the center_frame
        label = tk.Label(
            center_frame,
            text="📧 SMTP Client Pro 📧", # Added emojis for fun
            font=self.title_font,
            bg=BG_COLOR,       # Match background
            fg="#88C0D0"       # Nord Frost - Aurora (Cyan/Light Blue) for title
        )
        # Use pack within the center_frame
        label.pack(pady=(0, 60)) # More padding below the title

        # --- Button Styling ---
        button_options = {
            "font": self.button_font,
            "bg": BTN_BG_COLOR,
            "fg": BTN_FG_COLOR,
            "activebackground": "#4C566A", # Nord Polar Night (Slightly Lighter) - Click color
            "activeforeground": FG_COLOR,
            "relief": tk.FLAT,       # Flat button look
            "borderwidth": 0,        # No border
            "width": 15,             # Fixed width for buttons
            "pady": 10               # Internal vertical padding
        }

        # --- Login Button ---
        login_button = tk.Button(
            center_frame,
            text="Login",
            command=self.load_login_screen,
            **button_options # Apply styles
        )
        login_button.pack(pady=15) # Spacing between buttons

        # --- Sign Up Button ---
        signup_button = tk.Button(
            center_frame,
            text="Sign Up",
            command=self.load_signup_screen,
            **button_options # Apply styles
        )
        signup_button.pack(pady=15) # Spacing below last button

        # --- Hover Effects (Optional but nice) ---
        def on_enter(e):
            e.widget['background'] = BTN_HOVER_BG # Change color on hover

        def on_leave(e):
            e.widget['background'] = BTN_BG_COLOR # Change back on leave

        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)
        signup_button.bind("<Enter>", on_enter)
        signup_button.bind("<Leave>", on_leave)


        # --- Footer/Status (Example of adding more elements) ---
        footer_label = tk.Label(
            self, # Place directly in the main frame, not center_frame
            text="Ready",
            font=(DEFAULT_FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#4C566A" # Dim color
        )
        # Pack it at the bottom, stretching horizontally
        footer_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)


    def load_login_screen(self):
        # Load the login screen using the manager (logic unchanged)
        self.manager.change_screen(login_screen)

    def load_signup_screen(self):
        # Load the signup screen using the manager (logic unchanged)
        self.manager.change_screen(signup_screen)
