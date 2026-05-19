import tkinter as tk

from config import *
from core.lab_launcher import launch_lab


class LabCard(tk.Frame):
    def __init__(self, parent, lab_data):
        super().__init__(
            parent,
            bg=BG_CARD,
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.lab = lab_data

        self.disabled = lab_data.get(
            "disabled",
            False
        )

        self.color = (
            TEXT_MUTED
            if self.disabled
            else lab_data["color"]
        )

        self._build()

    def _build(self):
        # Top strip
        self.strip = tk.Frame(
            self,
            bg=self.color,
            height=4
        )

        self.strip.pack(fill="x")

        self.inner = tk.Frame(
            self,
            bg=BG_CARD,
            padx=20,
            pady=16
        )

        self.inner.pack(
            fill="both",
            expand=True
        )

        # Header row
        self.hrow = tk.Frame(
            self.inner,
            bg=BG_CARD
        )

        self.hrow.pack(fill="x")

        # ICON
        self.icon_label = tk.Label(
            self.hrow,
            text=self.lab["icon"],
            font=("Georgia", 22),
            bg=BG_CARD,
            fg=self.color
        )

        self.icon_label.pack(side="left")

        # LAB ID
        self.id_label = tk.Label(
            self.hrow,
            text=f"Lab {self.lab['id']}",
            font=("Helvetica", 9, "bold"),
            bg=BG_CARD,
            fg=self.color,
            padx=8
        )

        self.id_label.pack(
            side="right",
            anchor="n"
        )

        # TITLE
        self.title_label = tk.Label(
            self.inner,
            text=self.lab["title"],
            font=("Georgia", 13, "bold"),
            bg=BG_CARD,
            fg=(
                TEXT_WHITE
                if not self.disabled
                else TEXT_MUTED
            ),
            anchor="w"
        )

        self.title_label.pack(
            fill="x",
            pady=(8, 4)
        )

        # DESCRIPTION
        self.desc_label = tk.Label(
            self.inner,
            text=self.lab["desc"],
            font=("Helvetica", 9),
            bg=BG_CARD,
            fg=TEXT_MUTED,
            wraplength=310,
            justify="left",
            anchor="w"
        )

        self.desc_label.pack(fill="x")

        # BUTTON
        btn_text = (
            "COMING SOON"
            if self.disabled
            else "LAUNCH →"
        )

        btn_fg = (
            TEXT_MUTED
            if self.disabled
            else BG_DARK
        )

        btn_bg = (
            BORDER
            if self.disabled
            else self.color
        )

        self.button = tk.Label(
            self.inner,
            text=btn_text,
            font=("Helvetica", 9, "bold"),
            bg=btn_bg,
            fg=btn_fg,
            padx=14,
            pady=6,
            cursor=(
                "arrow"
                if self.disabled
                else "hand2"
            )
        )

        self.button.pack(
            anchor="w",
            pady=(14, 0)
        )

        self._bind_events()

    def _bind_events(self):
        widgets = [
            self,
            self.inner,
            self.strip,
            self.hrow,
            self.icon_label,
            self.id_label,
            self.title_label,
            self.desc_label,
            self.button
        ]

        for widget in widgets:
            widget.bind(
                "<Enter>",
                self.on_enter
            )

            widget.bind(
                "<Leave>",
                self.on_leave
            )

            widget.bind(
                "<Button-1>",
                self.on_click
            )

    def on_enter(self, event):
        if self.disabled:
            return

        self.configure(
            highlightbackground=self.color
        )

        self.inner.configure(bg=BG_HOVER)

        self.hrow.configure(bg=BG_HOVER)

        self.button.configure(
            bg=BG_DARK,
            fg=self.color
        )

        labels = [
            self.icon_label,
            self.id_label,
            self.title_label,
            self.desc_label
        ]

        for label in labels:
            label.configure(bg=BG_HOVER)

    def on_leave(self, event):
        if self.disabled:
            return

        self.configure(
            highlightbackground=BORDER
        )

        self.inner.configure(bg=BG_CARD)

        self.hrow.configure(bg=BG_CARD)

        self.button.configure(
            bg=self.color,
            fg=BG_DARK
        )

        labels = [
            self.icon_label,
            self.id_label,
            self.title_label,
            self.desc_label
        ]

        for label in labels:
            label.configure(bg=BG_CARD)

    def on_click(self, event):
        launch_lab(self, self.lab)