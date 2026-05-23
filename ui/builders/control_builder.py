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
    entry.pack(side="left", fill="x", expand=True)

    def _get_top_window(widget):
        """Walk up the widget tree to find the nearest Toplevel or Tk root."""
        w = widget
        while w is not None:
            if isinstance(w, (tk.Toplevel, tk.Tk)):
                return w
            w = w.master
        return None

    def browse():
        # Always pass parent= so the dialog stays on top of the lab window
        # and focus returns to it after selection — not the root window.
        top = _get_top_window(container)
        path = filedialog.askopenfilename(
            parent=top,
            filetypes=filetypes,
        )
        if not path:
            return
        path_var.set(path)
        # Bring the lab window back to front after dialog closes
        if top is not None:
            top.lift()
            top.focus_force()
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