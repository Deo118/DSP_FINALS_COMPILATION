import tkinter as tk

from config import *


def create_section(parent, title):
    section = tk.Frame(
        parent,
        bg=BG_CARD,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    tk.Label(
        section,
        text=title,
        font=("Helvetica", 11, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE,
        anchor="w"
    ).pack(fill="x", padx=14, pady=(12, 8))

    divider = tk.Frame(
        section,
        bg=BORDER,
        height=1
    )

    divider.pack(fill="x", padx=12, pady=(0, 12))

    return section