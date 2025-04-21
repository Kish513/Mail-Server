import tkinter as tk
import tkinter.font as tkFont
from email_classes.email import email
# REMOVED: from .main_screen import main_screen # Avoid circular import at top level

class send_mail_screen(tk.Frame):
    # --- Constants defined at CLASS LEVEL ---
    BG_COLOR = "#2E3440"  # Nord Polar Night
    FG_COLOR = "#ECEFF4"  # Nord Snow Storm
    ENTRY_BG = "#3B4252"  # Slightly lighter Nord Polar Night
    ENTRY_FG = "#ECEFF4"
    READONLY_BG = "#434C5E" # Dimmer background for readonly fields
    LABEL_COLOR = "#D8DEE9" # Lighter gray for labels
    BTN_BG_COLOR = "#5E81AC" # Nord Frost (Blue)
    BTN_FG_COLOR = "#ECEFF4"
    BTN_HOVER_BG = "#81A1C1" # Lighter Nord Frost
    SUCCESS_COLOR = "#A3BE8C" # Nord Frost - Aurora (Green)
    ERROR_COLOR = "#BF616A" # Nord Frost - Aurora (Red)
    TITLE_FONT_FAMILY = "Helvetica"
    DEFAULT_FONT_FAMILY = "Helvetica"

    def __init__(self, manager, client):
        super().__init__(manager)
        self.manager = manager
        self.client = client

        # --- Apply Background Color to the main frame ---
        self.config(bg=self.BG_COLOR)

        # --- Define Fonts ---
        self.label_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11)
        self.entry_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11)
        self.button_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11, weight="bold")
        self.message_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=10)

        # --- Set Window Title (Optional - manager might handle) ---
        self.manager.title("SMTP Client - Compose Email")
        self.manager.geometry("650x550") # Adjusted size

        # --- Create a content frame with padding ---
        content_frame = tk.Frame(self, bg=self.BG_COLOR, padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # --- Configure Grid Layout Weights ---
        content_frame.grid_columnconfigure(1, weight=1) # Allow column 1 to expand
        content_frame.grid_rowconfigure(3, weight=1) # Allow row 3 (body) to expand

        # --- Styling Options ---
        label_options = {
            "font": self.label_font,
            "bg": self.BG_COLOR,
            "fg": self.LABEL_COLOR,
        }
        entry_options = {
            "font": self.entry_font,
            "bg": self.ENTRY_BG,
            "fg": self.ENTRY_FG,
            "relief": tk.FLAT,
            "borderwidth": 2,
            "insertbackground": self.FG_COLOR,
        }
        readonly_entry_options = {
            "font": self.entry_font,
            "bg": self.READONLY_BG,
            "fg": self.LABEL_COLOR,
            "relief": tk.FLAT,
            "borderwidth": 2,
            "readonlybackground": self.READONLY_BG,
        }
        text_options = {
            "font": self.entry_font,
            "bg": self.ENTRY_BG,
            "fg": self.ENTRY_FG,
            "relief": tk.FLAT,
            "borderwidth": 2,
            "insertbackground": self.FG_COLOR,
            "height": 15,
            "width": 60
        }
        button_style = {
            "font": self.button_font,
            "bg": self.BTN_BG_COLOR,
            "fg": self.BTN_FG_COLOR,
            "activebackground": "#4C566A",
            "activeforeground": self.FG_COLOR,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "width": 12,
            "pady": 6
        }

        # --- Labels and Entry Fields using Grid ---
        tk.Label(content_frame, text="Sender:", **label_options).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.sender_var = tk.StringVar(value=self.client.get_email_address())
        self.sender_entry = tk.Entry(content_frame, textvariable=self.sender_var, state="readonly", **readonly_entry_options)
        self.sender_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=8)

        tk.Label(content_frame, text="To:", **label_options).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.receiver_entry = tk.Entry(content_frame, **entry_options)
        self.receiver_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=8)

        tk.Label(content_frame, text="Subject:", **label_options).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        self.subject_entry = tk.Entry(content_frame, **entry_options)
        self.subject_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=8)

        tk.Label(content_frame, text="Body:", **label_options).grid(row=3, column=0, sticky="nw", padx=5, pady=8)
        self.body_text = tk.Text(content_frame, **text_options)
        self.body_text.grid(row=3, column=1, sticky="nsew", padx=5, pady=8)

        # --- Frame for Buttons ---
        button_frame = tk.Frame(content_frame, bg=self.BG_COLOR)
        button_frame.grid(row=4, column=1, sticky="e", pady=10)

        # --- Back Button ---
        self.back_button = tk.Button(button_frame, text="Back", command=self.go_back, **button_style)
        self.back_button.pack(side=tk.LEFT, padx=(0, 10))

        # --- Send Button ---
        self.send_button = tk.Button(button_frame, text="Send Email", command=self.send_email, **button_style)
        self.send_button.pack(side=tk.LEFT)

        # --- Message Label ---
        self.message_label = tk.Label(
            content_frame,
            text="",
            font=self.message_font,
            bg=self.BG_COLOR,
            wraplength=500
        )
        self.message_label.grid(row=5, column=1, sticky="ew", pady=(5, 10), padx=5)

        # --- Hover Effects ---
        def on_enter(e):
            e.widget['background'] = self.BTN_HOVER_BG

        def on_leave(e):
            e.widget['background'] = self.BTN_BG_COLOR

        self.send_button.bind("<Enter>", on_enter)
        self.send_button.bind("<Leave>", on_leave)
        self.back_button.bind("<Enter>", on_enter)
        self.back_button.bind("<Leave>", on_leave)

    def send_email(self):
        sender = self.client.get_email_address()
        receiver = self.receiver_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", 'end-1c').strip()
        mail = email(sender, receiver, subject, body)
        # Basic validation
        if not receiver or not subject:
            self.message_label.config(text="Receiver and Subject fields cannot be empty.", fg=self.ERROR_COLOR)
            return

        # Indicate sending attempt
        self.message_label.config(text="Sending...", fg=self.LABEL_COLOR)
        self.update_idletasks()

        # --- Original Logic: Direct call ---
        self.client.send_email_message(mail)

        # --- Provide optimistic feedback ---
        self.message_label.config(text="Email send request initiated.", fg=self.SUCCESS_COLOR)

        # Optionally clear fields:
        # self.receiver_entry.delete(0, tk.END)
        # self.subject_entry.delete(0, tk.END)
        # self.body_text.delete("1.0", tk.END)


    def go_back(self):
        """Navigates back to the main screen."""
        # Import main_screen HERE, only when needed, to prevent circular import
        from .main_screen import main_screen
        self.manager.change_screen(main_screen, self.client)