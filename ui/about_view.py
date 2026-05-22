import tkinter as tk

from config import *

from ui.components.section_bar import SectionBar
from ui.components.scrollable_frame import ScrollableFrame


class AboutView(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=BG_DARK
        )

        self._build()

    def _build(self):
        # Scrollable container
        scroll = ScrollableFrame(self)

        scroll.pack(
            fill="both",
            expand=True
        )

        body = tk.Frame(
            scroll.scroll_frame,
            bg=BG_DARK
        )

        body.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=40
        )

        # Icon
        tk.Label(
            body,
            text="◈",
            font=("Georgia", 40),
            bg=BG_DARK,
            fg=ACCENT2
        ).pack(anchor="w")

        # Title
        tk.Label(
            body,
            text="About This Project",
            font=("Georgia", 24, "bold"),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(anchor="w", pady=(8, 4))

        # Gradient bar
        SectionBar(
            body,
            240
        ).pack(anchor="w", pady=(0, 20))

        # About sections
        about_sections = [
            (
                "Project Overview",
                (
                    "This application is the final project output "
                    "for Digital Signal Processing (DSP). "
                    "It compiles all laboratory activities "
                    "(Labs 1–7) into a single executable "
                    "Python desktop application.\n\n"
                    "Each lab opens in its own dedicated window "
                    "with embedded visualization support "
                    "for DSP experimentation and analysis."
                )
            ),

            (
                "Technologies Used",
                (
                    "• Python 3\n"
                    "• Tkinter GUI Framework\n"
                    "• NumPy\n"
                    "• SciPy\n"
                    "• Matplotlib\n"
                    "• OpenCV\n"
                    "• Embedded DSP Visualizations"
                )
            ),

            (
                "Laboratory Modules",
                (
                    "Lab 01 — Sampling & Aliasing\n"
                    "Lab 02 — Digital Image Processing\n"
                    "Lab 03 — Digital Filters\n"
                    "Lab 04 — Z-Transform\n"
                    "Lab 05 — Manual DFT & FFT\n"
                    "Lab 06 — DFT in Python\n"
                    "Lab 07 — Windowing Functions"
                )
            ),

            (
                "Application Goals",
                (
                    "• Embedded DSP visualizations\n"
                    "• Modular laboratory architecture\n"
                    "• Real-time signal experimentation\n"
                    "• Interactive DSP controls\n"
                    "• Educational DSP simulations\n"
                    "• Scalable software structure"
                )
            ),

            (
                "Group Members",
                (
                    "• Aguilar, Johann Carl M.\n"
                    "• Dizon, Deo Benedict M.\n"
                    "• Dizon, Mark Adrian D.\n"
                    "• Orlanda, Glendel H."
                )
            ),
        ]

        # Render sections
        for title, content in about_sections:
            section = tk.Frame(
                body,
                bg=BG_CARD,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            section.pack(
                fill="x",
                pady=(0, 12)
            )

            tk.Label(
                section,
                text=title,
                font=("Helvetica", 10, "bold"),
                bg=BG_CARD,
                fg=ACCENT,
                padx=20,
                anchor="w"
            ).pack(
                fill="x",
                pady=(14, 2)
            )

            tk.Label(
                section,
                text=content,
                font=("Helvetica", 10),
                bg=BG_CARD,
                fg=TEXT_MUTED,
                padx=20,
                anchor="w",
                justify="left",
                wraplength=680
            ).pack(
                fill="x",
                pady=(0, 14)
            )