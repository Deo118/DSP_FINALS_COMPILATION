import tkinter as tk

from config import *


def create_status_row(parent, label, value="---"):
    row = tk.Frame(parent, bg=BG_CARD)

    tk.Label(
        row,
        text=f"{label}:",
        font=("Helvetica", 10, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE,
        width=18,
        anchor="w"
    ).pack(side="left")

    value_label = tk.Label(
        row,
        text=value,
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg="#00D4FF",
        anchor="w"
    )

    value_label.pack(side="left", fill="x", expand=True)

    return row, value_label