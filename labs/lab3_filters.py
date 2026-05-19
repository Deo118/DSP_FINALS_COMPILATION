import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_file_picker, create_labeled_entry

from config import *


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="⧖",
        title="Audio Filtering",
        subtitle=(
            "Apply Butterworth low-pass, high-pass, band-pass, "
            "and band-stop filters to an audio signal."
        ),
        accent="#818CF8",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]

    section = create_section(control_panel, "Filter Parameters")
    section.pack(fill="x", padx=16, pady=16)

    file_row, path_var, _browse = create_file_picker(
        section,
        "Audio File (.wav / .mp3)",
        [("Audio files", "*.wav *.mp3")],
    )
    file_row.pack(fill="x", padx=14, pady=(0, 12))

    low_row,   low_entry   = create_labeled_entry(section, "Low Cut Frequency (Hz)", "1000")
    low_row.pack(fill="x", padx=14, pady=(0, 12))

    high_row,  high_entry  = create_labeled_entry(section, "High Cut Frequency (Hz)", "3000")
    high_row.pack(fill="x", padx=14, pady=(0, 12))

    order_row, order_entry = create_labeled_entry(section, "Filter Order", "4")
    order_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Graph area ────────────────────────────────────────────────────────
    graph_frame = tk.Frame(graph_panel, bg=BG_CARD)
    graph_frame.pack(fill="both", expand=True, padx=16, pady=16)

    plot_titles = [
        "Original Signal",
        "Low-pass Filtered",
        "High-pass Filtered",
        "Band-pass Filtered",
        "Band-stop Filtered",
    ]

    # placeholder label shown before first run
    placeholder = tk.Label(
        graph_frame,
        text="Select an audio file and click Apply Filters.",
        font=("Helvetica", 12),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        justify="center",
    )
    placeholder.pack(expand=True)

    canvas_ref = {"canvas": None, "fig": None}

    def _build_canvas():
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        placeholder.pack_forget()

        if canvas_ref["canvas"]:
            canvas_ref["canvas"].get_tk_widget().destroy()

        fig  = Figure(figsize=(9, 10), dpi=100, facecolor=BG_CARD)
        axes = fig.subplots(5, 1)
        cv   = FigureCanvasTkAgg(fig, master=graph_frame)
        cv.get_tk_widget().pack(fill="both", expand=True)
        canvas_ref["canvas"] = cv
        canvas_ref["fig"]    = fig
        return fig, axes, cv

    def apply_filters():
        import numpy as np
        import scipy.signal as signal
        from core.dsp_utils import load_audio_file, style_axes

        path = path_var.get()
        if not path or path == "No file selected":
            messagebox.showerror("Invalid Input", "Please select an audio file first.")
            return

        try:
            low_cut  = float(low_entry.get())
            high_cut = float(high_entry.get())
            order    = int(order_entry.get())

            if order < 1 or low_cut <= 0 or high_cut <= 0:
                raise ValueError
            if low_cut >= high_cut:
                raise ValueError("Low cut must be less than high cut.")

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid positive frequencies and filter order (≥ 1).\n"
                "Low cut must be less than high cut.",
            )
            return

        try:
            audio, sample_rate = load_audio_file(path)
        except Exception as exc:
            messagebox.showerror("Invalid Input", f"Could not load audio:\n{exc}")
            return

        nyquist = 0.5 * sample_rate
        if high_cut >= nyquist:
            messagebox.showerror(
                "Invalid Input",
                f"High cut must be below Nyquist ({nyquist:.0f} Hz).",
            )
            return

        low  = low_cut  / nyquist
        high = high_cut / nyquist

        b_low,  a_low  = signal.butter(order, low,          btype="low")
        b_high, a_high = signal.butter(order, low,          btype="high")
        b_band, a_band = signal.butter(order, [low, high],  btype="bandpass")
        b_stop, a_stop = signal.butter(order, [low, high],  btype="bandstop")

        signals = [
            audio,
            signal.filtfilt(b_low,  a_low,  audio),
            signal.filtfilt(b_high, a_high, audio),
            signal.filtfilt(b_band, a_band, audio),
            signal.filtfilt(b_stop, a_stop, audio),
        ]

        time = np.linspace(0, len(audio) / sample_rate, len(audio))

        fig, axes, cv = _build_canvas()

        for ax, sig, title in zip(axes, signals, plot_titles):
            ax.clear()
            style_axes(ax, title=title, xlabel="Time (s)", ylabel="Amplitude")
            ax.plot(time, sig, color="#00D4FF", linewidth=0.8)

        fig.tight_layout(pad=1.5)
        cv.draw_idle()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Apply Filters", apply_filters, padx=(0, 0))
