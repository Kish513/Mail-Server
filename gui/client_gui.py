import tkinter as tk
from tkinter import ttk
from client.client import Client
from time import sleep

class SMTP_client_gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_screen = None
        self.geometry("600x450")  # Increased default size
        self.title("SMTP Client")
        self.configure(bg="#f4f4f4")
        
    def change_screen(self, screen, client=None):
        if self.current_screen:
            self.current_screen.destroy()
        
        if client is not None:
            self.current_screen = screen(self, client)
        else:
            self.current_screen = screen(self)
        
        self.current_screen.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_idletasks()  # Ensures proper rendering
        
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def get_root(self):
        return self

class StyledFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
        self.pack_propagate(False)
        self.configure(width=500, height=400)  # Ensures a uniform size for screens

class StyledButton(ttk.Button):
    def __init__(self, parent, text, command=None):
        super().__init__(parent, text=text, command=command, style="TButton")

class StyledLabel(tk.Label):
    def __init__(self, parent, text, font=("Arial", 12, "bold")):
        super().__init__(parent, text=text, font=font, bg="#ffffff", fg="#333", pady=5)

class StyledEntry(tk.Entry):
    def __init__(self, parent):
        super().__init__(parent, font=("Arial", 12), bd=2, relief="solid", width=40)
