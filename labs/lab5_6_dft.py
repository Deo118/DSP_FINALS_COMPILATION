import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_labeled_entry

from config import *


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="∑",
        title="Lab 5 & 6 — DFT & FFT",
        subtitle=(
            "Compute the Discrete Fourier Transform of a "
            "space-separated input sequence."
        ),
        accent="#22C55E",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]
    status_left    = shell["status_left"]

    section = create_section(control_panel, "Sequence Input")
    section.pack(fill="x", padx=16, pady=16)

    seq_row, seq_entry = create_labeled_entry(
        section, "Sequence (e.g. 1 1 0 0)", "1 1 0 0"
    )
    seq_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Graph area ────────────────────────────────────────────────────────
    graph_frame = tk.Frame(graph_panel, bg=BG_CARD)
    graph_frame.pack(fill="both", expand=True, padx=16, pady=16)

    canvas_ref = {"canvas": None}

    def _build_canvas():
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        if canvas_ref["canvas"]:
            canvas_ref["canvas"].get_tk_widget().destroy()

        fig = Figure(figsize=(8, 5), dpi=100, facecolor=BG_CARD)
        ax  = fig.add_subplot(111)
        cv  = FigureCanvasTkAgg(fig, master=graph_frame)
        cv.get_tk_widget().pack(fill="both", expand=True)
        canvas_ref["canvas"] = cv
        return fig, ax, cv

    # ── Status labels ─────────────────────────────────────────────────────
    info_frame = tk.Frame(status_left, bg=BG_CARD)
    info_frame.pack(anchor="w", fill="x")

    input_label = tk.Label(
        info_frame, text="Input: —",
        font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_MUTED, anchor="w",
    )
    input_label.pack(anchor="w", pady=2)

    dft_label = tk.Label(
        info_frame, text="DFT: —",
        font=("Courier", 10), bg=BG_CARD, fg=ACCENT, anchor="w",
    )
    dft_label.pack(anchor="w", pady=2)

    def compute():
        import numpy as np
        from core.dsp_utils import parse_int_sequence, format_dft_sequence, style_axes

        try:
            values = parse_int_sequence(seq_entry.get())
            x = np.array(values, dtype=float)
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        N           = len(x)
        X           = np.fft.fft(x)
        frequencies = np.fft.fftfreq(N)

        input_label.config(text=f"Input sequence x[n]: {list(values)}", fg=TEXT_WHITE)
        dft_label.config(text=f"DFT: {format_dft_sequence(X)}")

        fig, ax, cv = _build_canvas()

        style_axes(ax, title="Frequency-Domain Representation",
                   xlabel="Frequency", ylabel="Amplitude")

        amplitude = np.abs(X)
        markerline, stemlines, _ = ax.stem(
            frequencies, amplitude, linefmt="#00D4FF", markerfmt="o", basefmt=" "
        )
        markerline.set_markerfacecolor("#00D4FF")
        markerline.set_markeredgecolor("#00D4FF")
        try:
            stemlines.set_color("#00D4FF")
        except Exception:
            pass

        ax.plot(frequencies, amplitude, color="#0099FF", linewidth=1.5)
        cv.draw_idle()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Compute DFT/FFT", compute, padx=(0, 0))

    compute()
