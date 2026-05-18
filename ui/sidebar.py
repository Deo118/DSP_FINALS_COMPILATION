import tkinter as tk

from config import *


class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg="#080C16",
            width=SIDEBAR_WIDTH
        )

        self.pack_propagate(False)

        self.nav_buttons = {}
        self.callback = None

        self._build()

    def set_navigation_callback(self, callback):
        self.callback = callback

    def _build(self):
        # Brand section
        brand = tk.Frame(self, bg="#080C16")
        brand.pack(fill="x", padx=20, pady=(30, 10))

        # Left icon
        icon_label = tk.Label(
            brand,
            text="∿",
            font=("Georgia", 32),
            bg="#080C16",
            fg=ACCENT
        )

        icon_label.pack(side="left", padx=(0, 12))

        # Right text block
        text_container = tk.Frame(
            brand,
            bg="#080C16"
        )

        text_container.pack(side="left")

        tk.Label(
            text_container,
            text="DSP",
            font=("Georgia", 20, "bold"),
            bg="#080C16",
            fg=TEXT_WHITE
        ).pack(anchor="w")

        tk.Label(
            text_container,
            text="Final Project",
            font=("Helvetica", 9),
            bg="#080C16",
            fg=TEXT_MUTED
        ).pack(anchor="w")

        nav_items = [
            ("◉  Dashboard", "dashboard"),
            ("◈  About", "about"),
        ]

        for label, key in nav_items:
            btn = tk.Label(
                self,
                text=label,
                font=("Helvetica", 10),
                bg="#080C16",
                fg=TEXT_MUTED,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2"
            )

            btn.pack(fill="x", padx=8, pady=1)

            btn.bind(
                "<Button-1>",
                lambda e, k=key: self.callback(k)
            )

            self.nav_buttons[key] = btn

    def activate(self, key):
        btn = self.nav_buttons[key]

        btn.configure(
            bg=BG_HOVER,
            fg=ACCENT,
            font=("Helvetica", 10, "bold")
        )

    def deactivate(self, key):
        btn = self.nav_buttons[key]

        btn.configure(
            bg="#080C16",
            fg=TEXT_MUTED,
            font=("Helvetica", 10)
        )