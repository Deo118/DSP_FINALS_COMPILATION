import tkinter as tk

from config import *


class LabWindow(tk.Toplevel):
    def __init__(self, parent, lab):
        super().__init__(parent)
        
        self.state("zoomed")

        self.title(f"Lab {lab['id']} · {lab['title']}")
        self.geometry("860x600")

        self.configure(bg=BG_DARK)

        hdr = tk.Frame(
            self,
            bg=lab["color"],
            height=6
        )

        hdr.pack(fill="x")