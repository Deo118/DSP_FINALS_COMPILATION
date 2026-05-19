import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_labeled_entry, create_dropdown

from config import *

WINDOWS = {
    "Rectangular": lambda n: None,   # ones — built inline to avoid numpy at import
    "Hamming":     "hamming",
    "Hanning":     "hanning",
    "Blackman":    "blackman",
}


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="⌇",
        title="Window Functions & FFT",
        subtitle=(
            "Compare original, windowed, and FFT spectra "
            "for common window functions."
        ),
        accent="#FBBF24",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]

    section = create_section(control_panel, "Signal Parameters")
    section.pack(fill="x", padx=16, pady=16)

    n_row,  n_entry  = create_labeled_entry(section, "N (signal length)", "64")
    n_row.pack(fill="x", padx=14, pady=(0, 12))

    f1_row, f1_entry = create_labeled_entry(section, "Frequency 1", "5")
    f1_row.pack(fill="x", padx=14, pady=(0, 12))

    f2_row, f2_entry = create_labeled_entry(section, "Frequency 2", "15")
    f2_row.pack(fill="x", padx=14, pady=(0, 12))

    a2_row, a2_entry = create_labeled_entry(section, "Amplitude of f2", "0.5")
    a2_row.pack(fill="x", padx=14, pady=(0, 12))

    win_row, win_dropdown = create_dropdown(
        section, "Select Window", list(WINDOWS.keys())
    )
    win_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Graph area ────────────────────────────────────────────────────────
    graph_frame = tk.Frame(graph_panel, bg=BG_CARD)
    graph_frame.pack(fill="both", expand=True, padx=16, pady=16)

    canvas_ref = {"canvas": None}

    def _build_canvas():
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        if canvas_ref["canvas"]:
            canvas_ref["canvas"].get_tk_widget().destroy()

        fig  = Figure(figsize=(12, 4), dpi=100, facecolor=BG_CARD)
        axes = fig.subplots(1, 3)
        cv   = FigureCanvasTkAgg(fig, master=graph_frame)
        cv.get_tk_widget().pack(fill="both", expand=True)
        canvas_ref["canvas"] = cv
        return fig, axes, cv

    def analyze():
        import numpy as np
        from core.dsp_utils import style_axes, stem_with_line

        try:
            N  = int(n_entry.get())
            f1 = float(f1_entry.get())
            f2 = float(f2_entry.get())
            a2 = float(a2_entry.get())
            if N < 4:
                raise ValueError("N must be at least 4.")
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid numbers. N must be an integer ≥ 4.",
            )
            return

        window_name = win_dropdown.get()
        n = np.arange(N)
        x = np.sin(2 * np.pi * f1 * n / N) + a2 * np.sin(2 * np.pi * f2 * n / N)

        # Build window array
        if window_name == "Rectangular":
            w = np.ones(N)
        elif window_name == "Hamming":
            w = np.hamming(N)
        elif window_name == "Hanning":
            w = np.hanning(N)
        else:
            w = np.blackman(N)

        xw   = x * w
        X    = np.fft.fft(x)
        Xw   = np.fft.fft(xw)
        freq = np.fft.fftfreq(N)

        fig, axes, cv = _build_canvas()

        titles  = ["Original Signal", f"{window_name} Windowed Signal", "FFT Comparison"]
        xlabels = ["n", "n", "Frequency"]

        for ax, title, xlabel in zip(axes, titles, xlabels):
            ax.clear()
            style_axes(ax, title=title, xlabel=xlabel, ylabel="Amplitude")

        stem_with_line(axes[0], n,    x,       "#00D4FF", "#0099FF")
        stem_with_line(axes[1], n,    xw,      "#00D4FF", "#0099FF")
        stem_with_line(axes[2], freq, np.abs(X),  "#00D4FF", "#0099FF", label="Original")
        stem_with_line(axes[2], freq, np.abs(Xw), "#FBBF24", "#E6A800", label="Windowed")

        legend = axes[2].legend(facecolor=BG_CARD, edgecolor=BORDER, fontsize=8)
        for text in legend.get_texts():
            text.set_color(TEXT_WHITE)

        fig.suptitle(f"{window_name} Window Analysis", color=TEXT_WHITE, fontsize=13, y=1.02)
        fig.tight_layout(pad=1.5)
        cv.draw_idle()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Analyze", analyze, padx=(0, 0))

    analyze()
