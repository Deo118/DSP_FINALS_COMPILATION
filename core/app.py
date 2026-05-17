import tkinter as tk

from config import *
from ui.sidebar import Sidebar
from ui.dashboard_view import DashboardView
from ui.labs_view import LabsView
from ui.about_view import AboutView
from core.navigation import NavigationManager


class DSPApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DSP Final Project  ·  Digital Signal Processing")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)

        self._center_window()

        self.content = tk.Frame(self, bg=BG_DARK)
        self.content.pack(side="right", fill="both", expand=True)

        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        self.views = {
            "dashboard": DashboardView(self.content),
            "labs": LabsView(self.content),
            "about": AboutView(self.content),
        }

        self.navigation = NavigationManager(
            views=self.views,
            sidebar=self.sidebar
        )

        self.sidebar.set_navigation_callback(
            self.navigation.switch_view
        )

        self.navigation.initialize()

    def _center_window(self):
        self.update_idletasks()

        w = self.winfo_width()
        h = self.winfo_height()

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) // 2
        y = (sh - h) // 2

        self.geometry(f"{w}x{h}+{x}+{y}")