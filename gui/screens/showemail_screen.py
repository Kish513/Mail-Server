import tkinter as tk
from tkinter import ttk # Import ttk for Treeview and Style
import tkinter.font as tkFont
# REMOVED: from .main_screen import main_screen # Avoid circular import at top level

class show_mail_screen(tk.Frame):
    # --- Constants defined at CLASS LEVEL ---
    BG_COLOR = "#2E3440"  # Nord Polar Night
    FG_COLOR = "#ECEFF4"  # Nord Snow Storm
    ENTRY_BG = "#3B4252"  # For Treeview rows, Text background
    ENTRY_FG = "#ECEFF4"
    SELECTED_BG = "#5E81AC" # Selection color in Treeview
    SELECTED_FG = "#ECEFF4"
    HEADER_BG = "#434C5E" # Treeview header background
    HEADER_FG = "#ECEFF4" # Treeview header text color
    LABEL_COLOR = "#D8DEE9" # Lighter gray for labels
    BTN_BG_COLOR = "#5E81AC" # Nord Frost (Blue)
    BTN_FG_COLOR = "#ECEFF4"
    BTN_HOVER_BG = "#81A1C1" # Lighter Nord Frost
    SUCCESS_COLOR = "#A3BE8C" # Nord Frost - Aurora (Green) - For potential status messages
    ERROR_COLOR = "#BF616A" # Nord Frost - Aurora (Red) - For potential status messages
    TITLE_FONT_FAMILY = "Helvetica"
    DEFAULT_FONT_FAMILY = "Helvetica"

    def __init__(self, manager, client):
        super().__init__(manager)
        self.manager = manager
        self.client = client
        self.email_cache = [] # Cache emails locally to avoid refetching issues

        # --- Apply Background Color to the main frame ---
        self.config(bg=self.BG_COLOR)

        # --- Define Fonts ---
        self.title_font = tkFont.Font(family=self.TITLE_FONT_FAMILY, size=16, weight="bold")
        self.default_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11)
        self.button_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=11, weight="bold")
        self.tree_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=10) # Font for tree items
        self.header_font = tkFont.Font(family=self.DEFAULT_FONT_FAMILY, size=10, weight="bold") # Font for tree headers

        # --- Set Window Title (Optional) ---
        self.manager.title("SMTP Client - Inbox")
        self.manager.geometry("800x600") # Adjust size

        # --- Configure ttk Style ---
        style = ttk.Style(self)
        style.theme_use("clam") # 'clam', 'alt', 'default', 'classic' - 'clam' is often good for custom colors

        # Configure Treeview colors and appearance
        style.configure("Treeview",
                        background=self.ENTRY_BG,
                        foreground=self.ENTRY_FG,
                        fieldbackground=self.ENTRY_BG,
                        rowheight=25, # Adjust row height
                        font=self.tree_font,
                        borderwidth=0,
                        relief=tk.FLAT)
        style.map('Treeview',
                  background=[('selected', self.SELECTED_BG)],
                  foreground=[('selected', self.SELECTED_FG)])

        # Configure Treeview heading colors and appearance
        style.configure("Treeview.Heading",
                        background=self.HEADER_BG,
                        foreground=self.HEADER_FG,
                        font=self.header_font,
                        borderwidth=1, # Add a slight border to headers
                        relief=tk.FLAT)
        style.map("Treeview.Heading",
                  background=[('active', self.BTN_HOVER_BG)], # Hover color for header
                  relief=[('active', tk.GROOVE), ('!active', tk.FLAT)])


        # Configure Scrollbar (optional, but good for consistency)
        style.configure("Vertical.TScrollbar", background=self.HEADER_BG, troughcolor=self.BG_COLOR, borderwidth=0, arrowcolor=self.FG_COLOR)
        style.map("Vertical.TScrollbar", background=[('active', self.BTN_HOVER_BG)])

        # --- Create a content frame with padding ---
        content_frame = tk.Frame(self, bg=self.BG_COLOR, padx=10, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title/Header Label ---
        title_label = tk.Label(content_frame, text="Inbox", font=self.title_font, bg=self.BG_COLOR, fg=self.FG_COLOR)
        title_label.pack(pady=(0, 10))

        # --- Frame for Buttons ---
        button_frame = tk.Frame(content_frame, bg=self.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=(0, 10)) # Place buttons above tree

        button_style = {
            "font": self.button_font, "bg": self.BTN_BG_COLOR, "fg": self.BTN_FG_COLOR,
            "activebackground": "#4C566A", "activeforeground": self.FG_COLOR,
            "relief": tk.FLAT, "borderwidth": 0, "width": 10, "pady": 5
        }

        # --- Back Button ---
        self.back_button = tk.Button(button_frame, text="Back", command=self.go_back, **button_style)
        self.back_button.pack(side=tk.LEFT, padx=(0, 10))

        # --- Refresh Button ---
        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.refresh_emails, **button_style)
        self.refresh_button.pack(side=tk.LEFT)

        # --- Status Label (Optional) ---
        self.status_label = tk.Label(button_frame, text="", font=self.default_font, bg=self.BG_COLOR, fg=self.LABEL_COLOR)
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # --- Frame for Treeview and Scrollbar ---
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(expand=True, fill="both")

        # --- Create Treeview ---
        self.tree = ttk.Treeview(tree_frame, columns=("Sender", "Receiver", "Subject"), show="headings", style="Treeview")
        self.tree.heading("Sender", text="Sender", anchor='w')
        self.tree.heading("Receiver", text="To", anchor='w') # Shortened heading
        self.tree.heading("Subject", text="Subject", anchor='w')

        # --- Configure Column Widths (adjust as needed) ---
        self.tree.column("Sender", width=200, minwidth=150, stretch=tk.YES)
        self.tree.column("Receiver", width=200, minwidth=150, stretch=tk.YES)
        self.tree.column("Subject", width=350, minwidth=200, stretch=tk.YES)

        # --- Add Scrollbar ---
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # --- Pack Treeview and Scrollbar ---
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        # --- Populate emails ---
        self.load_emails() # Initial load

        # --- Bind double-click event ---
        self.tree.bind("<Double-1>", self.show_email_body) # Double-left-click

        # --- Hover Effects for Buttons ---
        def on_enter(e): e.widget['background'] = self.BTN_HOVER_BG
        def on_leave(e): e.widget['background'] = self.BTN_BG_COLOR
        self.back_button.bind("<Enter>", on_enter); self.back_button.bind("<Leave>", on_leave)
        self.refresh_button.bind("<Enter>", on_enter); self.refresh_button.bind("<Leave>", on_leave)


    def clear_treeview(self):
        """Removes all items from the treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_emails(self):
        """Clears the treeview and loads emails from the client."""
        self.status_label.config(text="Loading emails...", fg=self.LABEL_COLOR)
        self.update_idletasks()
        self.clear_treeview()
        try:
            self.email_cache = self.client.get_emails() # Fetch and cache emails
            if not self.email_cache:
                 self.status_label.config(text="Inbox is empty.", fg=self.LABEL_COLOR)
                 return

            # Use enumerate to get index safely for the item id (iid)
            for index, email_message in enumerate(self.email_cache):
                # Use index as the item identifier (iid) for reliable lookup later
                self.tree.insert("", "end", iid=index, values=(
                    email_message.get_sender(),
                    email_message.get_receiver(),
                    email_message.get_subject()
                ))
            self.status_label.config(text=f"Loaded {len(self.email_cache)} emails.", fg=self.SUCCESS_COLOR)
        except Exception as e:
            self.status_label.config(text=f"Error loading emails: {e}", fg=self.ERROR_COLOR)
            print(f"Error in load_emails: {e}") # Log error


    def refresh_emails(self):
        """Called when the Refresh button is pressed."""
        self.load_emails()


    def show_email_body(self, event):
        """Displays the selected email body in a Toplevel window."""
        selected_items = self.tree.selection() # Can return multiple items if selection mode allows
        if not selected_items:
            return # No item selected

        # Get the iid (which we set as the index) from the selected item
        selected_iid = selected_items[0]
        try:
             # Retrieve the email from the cached list using the iid (index)
             email_index = int(selected_iid) # iid was set to the index
             if 0 <= email_index < len(self.email_cache):
                 email = self.email_cache[email_index]
             else:
                 self.status_label.config(text="Error: Selected email not found in cache.", fg=self.ERROR_COLOR)
                 return

             # --- Create and Style the Toplevel Popup ---
             body_window = tk.Toplevel(self)
             body_window.title(f"Email: {email.get_subject()}")
             body_window.geometry("500x400") # Set size for popup
             body_window.config(bg=self.BG_COLOR) # Apply background color

             # Use a frame inside Toplevel for padding
             popup_frame = tk.Frame(body_window, bg=self.BG_COLOR, padx=10, pady=10)
             popup_frame.pack(fill=tk.BOTH, expand=True)

             # Styling for labels and text in popup
             popup_label_opts = {"font": self.default_font, "bg": self.BG_COLOR, "fg": self.LABEL_COLOR, "anchor": "w"}
             popup_header_opts = {"font": self.default_font, "bg": self.BG_COLOR, "fg": self.FG_COLOR, "anchor": "w"} # Slightly brighter fg for headers
             popup_text_opts = {
                 "font": self.default_font, "wrap": "word", "height": 15, "width": 50,
                 "bg": self.ENTRY_BG, "fg": self.ENTRY_FG,
                 "relief": tk.FLAT, "borderwidth": 1, "state": "disabled", # Start disabled
                 "insertbackground": self.FG_COLOR # Cursor color if enabled later
             }

             # Add email details
             tk.Label(popup_frame, text=f"From: {email.get_sender()}", **popup_header_opts).pack(fill=tk.X)
             tk.Label(popup_frame, text=f"To: {email.get_receiver()}", **popup_header_opts).pack(fill=tk.X)
             tk.Label(popup_frame, text=f"Subject: {email.get_subject()}", **popup_header_opts).pack(fill=tk.X)
             tk.Label(popup_frame, text="-"*60, **popup_label_opts).pack(fill=tk.X, pady=5) # Separator

             # Body Text Area
             body_text = tk.Text(popup_frame, **popup_text_opts)
             body_text.pack(expand=True, fill="both", pady=(5, 0))

             # Insert content *after* packing, then disable
             body_text.config(state="normal") # Enable to insert
             body_text.delete("1.0", tk.END) # Clear previous content if any
             body_text.insert("1.0", email.get_body())
             body_text.config(state="disabled") # Disable editing

             body_window.transient(self.manager) # Make popup appear over main window
             body_window.grab_set() # Prevent interaction with main window until popup closed
             self.manager.wait_window(body_window) # Wait until popup is closed

        except (ValueError, IndexError) as e:
             self.status_label.config(text=f"Error displaying email: {e}", fg=self.ERROR_COLOR)
             print(f"Error in show_email_body: {e}") # Log error
        except Exception as e: # Catch other potential errors
             self.status_label.config(text=f"An unexpected error occurred: {e}", fg=self.ERROR_COLOR)
             print(f"Unexpected error in show_email_body: {e}")


    def go_back(self):
        """Navigates back to the main screen."""
        # Import main_screen HERE, only when needed, to prevent circular import
        from .main_screen import main_screen
        self.manager.change_screen(main_screen, self.client)