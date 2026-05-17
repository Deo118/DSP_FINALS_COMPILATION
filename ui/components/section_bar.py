import tkinter as tk

from config import *


class SectionBar(tk.Canvas):
    def __init__(self, parent, width=320):
        super().__init__(
            parent,
            height=3,
            width=width,
            bg=BG_DARK,
            bd=0,
            highlightthickness=0
        )

        self.create_rectangle(
            0, 0,
            width // 2,
            3,
            fill=ACCENT,
            outline=""
        )

        self.create_rectangle(
            width // 2,
            0,
            width,
            3,
            fill=ACCENT2,
            outline=""
        )