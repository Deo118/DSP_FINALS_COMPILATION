import tkinter as tk

from config import *


def launch(parent):
    body = tk.Frame(
        parent,
        bg=BG_DARK
    )

    body.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=30
    )

    tk.Label(
        body,
        text="⊶",
        font=("Georgia", 48),
        bg=BG_DARK,
        fg="#F87171"
    ).pack(anchor="w")

    tk.Label(
        body,
        text="IIR & FIR Filters",
        font=("Georgia", 22, "bold"),
        bg=BG_DARK,
        fg=TEXT_WHITE
    ).pack(anchor="w", pady=(8, 4))

    tk.Label(
        body,
        text=(
            "Compare Infinite and Finite\n"
            "Impulse Response filters."
        ),
        font=("Helvetica", 11),
        bg=BG_DARK,
        fg=TEXT_MUTED,
        justify="left"
    ).pack(anchor="w", pady=(0, 24))

    separator = tk.Frame(
        body,
        bg=BORDER,
        height=1
    )

    separator.pack(fill="x", pady=(0, 20))

    placeholder = tk.Frame(
        body,
        bg=BG_CARD
    )

    placeholder.pack(fill="both", expand=True)

    tk.Label(
        placeholder,
        text=(
            "[ IIR / FIR Workspace ]\n\n"
            "Filter response plots,\n"
            "comparisons,\n"
            "and scipy.signal tools go here."
        ),
        font=("Courier", 11),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        justify="center"
    ).pack(expand=True)