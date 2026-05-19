import tkinter as tk
from tkinter import ttk

from config import *


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        self.canvas = tk.Canvas(
            self,
            bg=BG_DARK,
            bd=0,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scroll_frame = tk.Frame(
            self.canvas,
            bg=BG_DARK
        )

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # IMPORTANT
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Make frame resize properly
        self.canvas.bind(
            "<Configure>",
            self._resize_frame
        )

    def _resize_frame(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def _bind_mousewheel(self, event):
        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all(
            "<MouseWheel>"
        )