import tkinter as tk
from tkinter import ttk

from config import *


def create_labeled_entry(parent, label_text, default_value=""):
    container = tk.Frame(parent, bg=BG_CARD)

    tk.Label(
        container,
        text=label_text,
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        anchor="w"
    ).pack(fill="x", pady=(0, 4))

    entry = ttk.Entry(container)
    entry.insert(0, default_value)
    entry.pack(fill="x", ipady=5)

    return container, entry


def create_dropdown(parent, label_text, values):
    container = tk.Frame(parent, bg=BG_CARD)

    tk.Label(
        container,
        text=label_text,
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        anchor="w"
    ).pack(fill="x", pady=(0, 4))

    combo = ttk.Combobox(
        container,
        values=values,
        state="readonly"
    )

    combo.current(0)
    combo.pack(fill="x", ipady=4)

    return container, combo