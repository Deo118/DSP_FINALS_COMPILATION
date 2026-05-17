import tkinter as tk

from config import *


class StatCard(tk.Frame):
    def __init__(self, parent, value, label):
        super().__init__(
            parent,
            bg=BG_CARD,
            padx=18,
            pady=10
        )

        tk.Label(
            self,
            text=value,
            font=("Georgia", 18, "bold"),
            bg=BG_CARD,
            fg=ACCENT
        ).pack()

        tk.Label(
            self,
            text=label,
            font=("Helvetica", 8),
            bg=BG_CARD,
            fg=TEXT_MUTED
        ).pack()