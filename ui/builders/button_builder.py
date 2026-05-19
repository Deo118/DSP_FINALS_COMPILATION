import tkinter as tk
 
from config import *
 
 
BUTTON_BG    = ACCENT
BUTTON_HOVER = "#00A9CC"
 
 
def apply_button_hover(button):
 
    def on_enter(event):
        button.config(bg=BUTTON_HOVER)
 
    def on_leave(event):
        button.config(bg=BUTTON_BG)
 
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
 
 
def create_action_button(parent, text, command=None):
 
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", 10, "bold"),
        bg=BUTTON_BG,
        fg=TEXT_WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT_WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=10,        # increased slightly to compensate for removed ipady
    )
 
    apply_button_hover(button)
 
    return button
 
 
def create_return_button(parent, window):
 
    button = tk.Button(
        parent,
        text="Return",
        command=window.destroy,
        font=("Helvetica", 10, "bold"),
        bg="#2B3445",
        fg=TEXT_WHITE,
        activebackground="#3A465C",
        activeforeground=TEXT_WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=24,
        pady=10,
    )
 
    def on_enter(event):
        button.config(bg="#3A465C")
 
    def on_leave(event):
        button.config(bg="#2B3445")
 
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
 
    return button
 