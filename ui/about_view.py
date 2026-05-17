import tkinter as tk

from config import *
from ui.components.section_bar import SectionBar


class AboutView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=60, pady=40)

        tk.Label(
            body,
            text="About This Project",
            font=("Georgia", 24, "bold"),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(anchor="w")

        SectionBar(body, 240).pack(anchor="w", pady=(12, 20))