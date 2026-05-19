import tkinter as tk
from tkinter import filedialog, ttk

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
    entry.pack(fill="x", pady=(0, 2))   # ipady removed — not valid for ttk.Entry pack()

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
    combo.pack(fill="x", pady=(0, 2))   # ipady removed — not valid for ttk.Combobox pack()

    return container, combo


def create_file_picker(parent, label_text, filetypes, command=None):
    """Labeled file path display with Browse button."""
    container = tk.Frame(parent, bg=BG_CARD)

    tk.Label(
        container,
        text=label_text,
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        anchor="w",
    ).pack(fill="x", pady=(0, 4))

    row = tk.Frame(container, bg=BG_CARD)
    row.pack(fill="x")

    path_var = tk.StringVar(value="No file selected")

    entry = ttk.Entry(row, textvariable=path_var, state="readonly")
    entry.pack(side="left", fill="x", expand=True)   # ipady removed

    def browse():
        path = filedialog.askopenfilename(filetypes=filetypes)
        if not path:
            return
        path_var.set(path)
        if command:
            command(path)

    browse_btn = tk.Button(
        row,
        text="Browse",
        command=browse,
        font=("Helvetica", 9, "bold"),
        bg="#2B3445",
        fg=TEXT_WHITE,
        activebackground="#3A465C",
        activeforeground=TEXT_WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=6,
    )
    browse_btn.pack(side="left", padx=(8, 0))

    return container, path_var, browse_btn
