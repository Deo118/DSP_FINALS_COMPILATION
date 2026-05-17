import tkinter as tk

from config import *
from data.labs_data import LABS

from ui.lab_card import LabCard
from ui.components.stat_card import StatCard
from ui.components.section_bar import SectionBar
from ui.components.scrollable_frame import ScrollableFrame


class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        self._build()

    def _build(self):
        hero = tk.Frame(self, bg=BG_DARK)
        hero.pack(fill="x", padx=40, pady=(36, 0))

        tk.Label(
            hero,
            text="Digital Signal Processing",
            font=FONT_TITLE,
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Select a laboratory module below to launch it in a new window.",
            font=FONT_SUBTITLE,
            bg=BG_DARK,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(4, 0))

        SectionBar(hero).pack(anchor="w", pady=(12, 0))

        stats = tk.Frame(self, bg=BG_DARK)
        stats.pack(fill="x", padx=40, pady=(20, 0))

        StatCard(stats, "8", "Labs Included").pack(side="left", padx=(0, 12))
        StatCard(stats, "8", "Total Modules").pack(side="left", padx=(0, 12))
        StatCard(stats, "100%", "Python-Based").pack(side="left")

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=40, pady=20)

        for i, lab in enumerate(LABS):
            row, col = divmod(i, 2)

            card = LabCard(scroll.scroll_frame, lab)

            card.grid(
                row=row,
                column=col,
                padx=8,
                pady=8,
                sticky="nsew"
            )