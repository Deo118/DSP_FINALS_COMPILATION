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
        text="∑",
        font=("Georgia", 48),
        bg=BG_DARK,
        fg="#22C55E"
    ).pack(anchor="w")

    tk.Label(
        body,
        text="Manual DFT & FFT",
        font=("Georgia", 22, "bold"),
        bg=BG_DARK,
        fg=TEXT_WHITE
    ).pack(anchor="w", pady=(8, 4))

    tk.Label(
        body,
        text=(
            "Perform handwritten-style DFT and FFT solving\n"
            "using twiddle factors, sine/cosine theta,\n"
            "and discrete input sequences."
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
            "[ Manual DFT / FFT Workspace ]\n\n"
            "Step-by-step handwritten computations,\n"
            "twiddle factor derivations,\n"
            "and sequence solving visualizations go here."
        ),
        font=("Courier", 11),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        justify="center"
    ).pack(expand=True)