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

    def _create_section(self, parent, title, content):

        section = tk.Frame(
            parent,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        section.pack(
            fill="x",
            pady=(0, 14)
        )

        tk.Label(
            section,
            text=title,
            font=("Helvetica", 10, "bold"),
            bg=BG_CARD,
            fg=ACCENT,
            anchor="w",
            padx=20
        ).pack(
            fill="x",
            pady=(16, 4)
        )

        tk.Label(
            section,
            text=content,
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=920,
            padx=20
        ).pack(
            fill="x",
            pady=(0, 16)
        )

    def _build(self):

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

        tk.Label(
            body,
            text="◈",
            font=("Georgia", 38),
            bg=BG_DARK,
            fg=ACCENT2
        ).pack(anchor="w")

        tk.Label(
            body,
            text="About This Project",
            font=("Georgia", 24, "bold"),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(
            anchor="w",
            pady=(6, 4)
        )

        tk.Label(
            body,
            text=(
                "Integrated Digital Signal Processing laboratory "
                "environment with embedded visualization support."
            ),
            font=("Helvetica", 10),
            bg=BG_DARK,
            fg=TEXT_MUTED
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        SectionBar(
            body,
            240
        ).pack(
            anchor="w",
            pady=(0, 24)
        )

        about_sections = [

            (
                "Project Overview",

                (
                    "This application serves as the final project "
                    "output for Digital Signal Processing (DSP). "
                    "The system consolidates multiple DSP laboratory "
                    "activities into a single desktop-based learning "
                    "environment designed for experimentation, "
                    "analysis, visualization, and simulation.\n\n"

                    "The application was developed to provide an "
                    "interactive platform where users can explore "
                    "core DSP concepts through modular laboratory "
                    "implementations integrated into one unified GUI "
                    "system. Each laboratory module operates in its "
                    "own dedicated interface while maintaining a "
                    "consistent workflow and embedded visualization "
                    "environment.\n\n"

                    "The project focuses on practical implementation "
                    "of DSP principles including signal generation, "
                    "sampling, aliasing analysis, digital filtering, "
                    "frequency-domain transformation, windowing "
                    "techniques, and Z-transform operations. "
                    "Visualization components are integrated directly "
                    "inside the application to support real-time "
                    "analysis, parameter manipulation, waveform "
                    "comparison, and frequency spectrum observation.\n\n"

                    "The system architecture follows a modular design "
                    "approach for maintainability, scalability, and "
                    "organized laboratory separation. The project also "
                    "emphasizes interactive learning by allowing users "
                    "to dynamically modify DSP parameters and observe "
                    "corresponding signal behavior directly within the "
                    "application environment."
                )
            ),

            (
                "DSP Functionalities",

                (
                    "• Signal Generation\n"
                    "• Sampling and Aliasing Simulation\n"
                    "• Digital Filtering (LPF, HPF, BPF, BSF)\n"
                    "• DFT and FFT Spectrum Analysis\n"
                    "• Windowing Functions\n"
                    "• Z-Transform Analysis\n"
                    "• Embedded Signal Visualization\n"
                    "• Real-Time DSP Parameter Manipulation"
                )
            ),

            (
                "Laboratory Modules",

                (
                    "Lab 01 — Sampling & Aliasing\n"
                    "Lab 02 — Digital Image Processing\n"
                    "Lab 03 — Audio Filtering\n"
                    "Lab 04 — Z-Transform\n"
                    "Lab 05 & 06 — DFT & FFT\n"
                    "Lab 07 — Window Functions & FFT"
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
            )
        ]

        for title, content in about_sections:

            self._create_section(
                body,
                title,
                content
            )