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
        text="◎",
        font=("Georgia", 48),
        bg=BG_DARK,
        fg="#00D4FF"
    ).pack(anchor="w")

    tk.Label(
        body,
        text="Sampling & Aliasing",
        font=("Georgia", 22, "bold"),
        bg=BG_DARK,
        fg=TEXT_WHITE
    ).pack(anchor="w", pady=(8, 4))

    tk.Label(
        body,
        text=(
            "This is the Lab 1 workspace.\n\n"
            "Your matplotlib DSP visualizations\n"
            "will be embedded here."
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

    placeholder.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        placeholder,
        text=(
            "[ Embedded Matplotlib Area ]\n\n"
            "FFT graphs, signal plots,\n"
            "and DSP controls go here."
        ),
        font=("Courier", 11),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        justify="center"
    ).pack(expand=True)