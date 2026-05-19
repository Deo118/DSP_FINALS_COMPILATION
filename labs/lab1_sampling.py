import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_labeled_entry, create_dropdown
from ui.builders.button_builder import create_action_button
from ui.builders.status_builder import create_status_row
from ui.builders.graph_builder import create_graph

from config import *


def launch(parent):

    shell = create_lab_body(
        parent,
        icon="◎",
        title="Sampling & Aliasing",
        subtitle=(
            "Generate continuous and sampled signals "
            "while demonstrating Nyquist sampling theory."
        ),
        accent="#00D4FF",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]
    status_left    = shell["status_left"]

    # ── Controls ──────────────────────────────────────────────────────────
    signal_section = create_section(control_panel, "Signal Parameters")
    signal_section.pack(fill="x", padx=16, pady=16)

    wave_container, wave_dropdown = create_dropdown(
        signal_section, "Wave Type", ["Sine", "Cosine"]
    )
    wave_container.pack(fill="x", padx=14, pady=(0, 12))

    amp_container, amp_entry = create_labeled_entry(
        signal_section, "Amplitude", "1"
    )
    amp_container.pack(fill="x", padx=14, pady=(0, 12))

    freq_container, freq_entry = create_labeled_entry(
        signal_section, "Signal Frequency (Hz)", "5"
    )
    freq_container.pack(fill="x", padx=14, pady=(0, 12))

    sample_container, sample_entry = create_labeled_entry(
        signal_section, "Sampling Frequency (Hz)", "50"
    )
    sample_container.pack(fill="x", padx=14, pady=(0, 12))

    duration_container, duration_entry = create_labeled_entry(
        signal_section, "Duration (seconds)", "1"
    )
    duration_container.pack(fill="x", padx=14, pady=(0, 12))

    phase_container, phase_entry = create_labeled_entry(
        signal_section, "Phase Shift (degrees)", "0"
    )
    phase_container.pack(fill="x", padx=14, pady=(0, 14))

    # ── Graph ─────────────────────────────────────────────────────────────
    graph_container, fig, ax, canvas = create_graph(graph_panel)
    graph_container.pack(fill="both", expand=True, padx=16, pady=16)

    # ── Status row (inside status_left panel) ─────────────────────────────
    status_title = tk.Label(
        status_left,
        text="Signal Analysis",
        font=("Helvetica", 11, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE,
    )
    status_title.pack(anchor="w", pady=(0, 6))

    status_content = tk.Frame(status_left, bg=BG_CARD)
    status_content.pack(fill="x")

    column_1 = tk.Frame(status_content, bg=BG_CARD)
    column_1.pack(side="left", padx=(0, 40))

    column_2 = tk.Frame(status_content, bg=BG_CARD)
    column_2.pack(side="left")

    nyquist_row, nyquist_value = create_status_row(column_1, "Nyquist Status")
    nyquist_row.pack(fill="x", pady=2)

    alias_row, alias_value = create_status_row(column_1, "Aliasing")
    alias_row.pack(fill="x", pady=2)

    samplecount_row, samplecount_value = create_status_row(column_1, "Samples Generated")
    samplecount_row.pack(fill="x", pady=2)

    detected_row, detected_value = create_status_row(column_2, "Detected Frequency")
    detected_row.pack(fill="x", pady=2)

    # ── Signal generation ─────────────────────────────────────────────────
    def generate_signal():
        import numpy as np  # lazy import — avoids startup crash if numpy missing

        try:
            amplitude    = float(amp_entry.get())
            frequency    = float(freq_entry.get())
            sampling_rate = float(sample_entry.get())
            duration     = float(duration_entry.get())
            phase_deg    = float(phase_entry.get())

            if sampling_rate <= 0 or duration <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )
            return

        phase_rad = np.deg2rad(phase_deg)

        continuous_time = np.linspace(0, duration, 2000)
        sampled_time    = np.arange(0, duration, 1 / sampling_rate)

        wave_type = wave_dropdown.get()

        if wave_type == "Sine":
            continuous_signal = amplitude * np.sin(
                2 * np.pi * frequency * continuous_time + phase_rad
            )
            sampled_signal = amplitude * np.sin(
                2 * np.pi * frequency * sampled_time + phase_rad
            )
        else:
            continuous_signal = amplitude * np.cos(
                2 * np.pi * frequency * continuous_time + phase_rad
            )
            sampled_signal = amplitude * np.cos(
                2 * np.pi * frequency * sampled_time + phase_rad
            )

        nyquist_rate = sampling_rate / 2
        aliasing     = frequency > nyquist_rate

        if aliasing:
            nyquist_value.config(text="VIOLATED", fg="#FF5C5C")
            alias_value.config(text="YES",        fg="#FF5C5C")
        else:
            nyquist_value.config(text="VALID", fg="#00E676")
            alias_value.config(text="NO",     fg="#00E676")

        samplecount_value.config(text=str(len(sampled_time)))
        detected_value.config(text=f"{frequency:.2f} Hz")

        # ── Plot ──────────────────────────────────────────────────────────
        ax.clear()
        ax.set_facecolor(BG_CARD)

        ax.plot(
            continuous_time, continuous_signal,
            linewidth=2, label="Continuous Signal", color="#0099FF",
        )

        markerline, stemlines, _ = ax.stem(
            sampled_time, sampled_signal,
            linefmt="#00D4FF", markerfmt="o", basefmt=" ",
        )
        markerline.set_markerfacecolor("#00D4FF")
        markerline.set_markeredgecolor("#00D4FF")
        try:
            stemlines.set_color("#00D4FF")
        except Exception:
            pass

        ax.set_title("Sampling Visualization", color=TEXT_WHITE)
        ax.set_xlabel("Time (s)",   color=TEXT_MUTED)
        ax.set_ylabel("Amplitude",  color=TEXT_MUTED)
        ax.tick_params(colors=TEXT_MUTED)
        for spine in ax.spines.values():
            spine.set_color(BORDER)
        ax.grid(True, alpha=0.2)

        legend = ax.legend(facecolor=BG_CARD, edgecolor=BORDER)
        for text in legend.get_texts():
            text.set_color(TEXT_WHITE)

        ax.margins(x=0)
        canvas.draw_idle()

    # ── Reset ─────────────────────────────────────────────────────────────
    def reset_fields():
        for entry, default in [
            (amp_entry,    "1"),
            (freq_entry,   "5"),
            (sample_entry, "50"),
            (duration_entry, "1"),
            (phase_entry,  "0"),
        ]:
            entry.delete(0, tk.END)
            entry.insert(0, default)

        wave_dropdown.current(0)
        generate_signal()

    # ── Footer buttons (always visible, never clipped) ────────────────────
    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)

    add_footer_button(btn_frame, "Generate Signal", generate_signal, padx=(0, 6))

    reset_btn = create_action_button(btn_frame, "Reset", reset_fields)
    reset_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

    generate_signal()
