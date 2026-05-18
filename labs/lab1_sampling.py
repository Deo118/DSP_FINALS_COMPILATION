import tkinter as tk
from tkinter import messagebox

import numpy as np

from ui.builders.lab_layout import create_lab_workspace
from ui.builders.section_builder import create_section
from ui.builders.control_builder import (
    create_labeled_entry,
    create_dropdown
)
from ui.builders.button_builder import (
    create_action_button,
    create_return_button
)
from ui.builders.status_builder import create_status_row
from ui.builders.graph_builder import create_graph

from config import *


def launch(parent):

    body = tk.Frame(parent, bg=BG_DARK)

    body.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=30
    )

    # Header

    header = tk.Frame(body, bg=BG_DARK)

    header.pack(
        fill="x",
        pady=(0, 20)
    )

    tk.Label(
        header,
        text="◎",
        font=("Georgia", 42),
        bg=BG_DARK,
        fg="#00D4FF"
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Sampling & Aliasing",
        font=("Georgia", 22, "bold"),
        bg=BG_DARK,
        fg=TEXT_WHITE
    ).pack(anchor="w", pady=(2, 4))

    tk.Label(
        header,
        text=(
            "Generate continuous and sampled signals "
            "while demonstrating Nyquist sampling theory."
        ),
        font=("Helvetica", 11),
        bg=BG_DARK,
        fg=TEXT_MUTED
    ).pack(anchor="w")

    # Workspace

    workspace, control_panel, graph_panel, status_panel = (
        create_lab_workspace(body)
    )

    # Controls

    signal_section = create_section(
        control_panel,
        "Signal Parameters"
    )

    signal_section.pack(
        fill="x",
        padx=16,
        pady=16
    )

    wave_container, wave_dropdown = create_dropdown(
        signal_section,
        "Wave Type",
        ["Sine", "Cosine"]
    )

    wave_container.pack(
        fill="x",
        padx=14,
        pady=(0, 12)
    )

    amp_container, amp_entry = create_labeled_entry(
        signal_section,
        "Amplitude",
        "1"
    )

    amp_container.pack(
        fill="x",
        padx=14,
        pady=(0, 12)
    )

    freq_container, freq_entry = create_labeled_entry(
        signal_section,
        "Signal Frequency (Hz)",
        "5"
    )

    freq_container.pack(
        fill="x",
        padx=14,
        pady=(0, 12)
    )

    sample_container, sample_entry = create_labeled_entry(
        signal_section,
        "Sampling Frequency (Hz)",
        "50"
    )

    sample_container.pack(
        fill="x",
        padx=14,
        pady=(0, 12)
    )

    duration_container, duration_entry = create_labeled_entry(
        signal_section,
        "Duration (seconds)",
        "1"
    )

    duration_container.pack(
        fill="x",
        padx=14,
        pady=(0, 12)
    )

    phase_container, phase_entry = create_labeled_entry(
        signal_section,
        "Phase Shift (degrees)",
        "0"
    )

    phase_container.pack(
        fill="x",
        padx=14,
        pady=(0, 20)
    )

    # Graph

    graph_container, fig, ax, canvas = create_graph(graph_panel)

    graph_container.pack(
        fill="both",
        expand=True,
        padx=16,
        pady=16
    )

    # Status

    status_title = tk.Label(
        status_panel,
        text="Signal Analysis",
        font=("Helvetica", 11, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE
    )

    status_title.pack(
        anchor="w",
        padx=16,
        pady=(12, 10)
    )

    status_content = tk.Frame(
        status_panel,
        bg=BG_CARD
    )

    status_content.pack(
        fill="x",
        padx=16,
        pady=(0, 12)
    )

    column_1 = tk.Frame(
        status_content,
        bg=BG_CARD
    )

    column_1.pack(
        side="left",
        padx=(0, 50)
    )

    column_2 = tk.Frame(
        status_content,
        bg=BG_CARD
    )

    column_2.pack(
        side="left",
        padx=(0, 50)
    )

    right_actions = tk.Frame(
        status_content,
        bg=BG_CARD
    )

    right_actions.pack(
        side="right",
        anchor="e"
    )

    return_button = create_return_button(
        right_actions,
        parent
    )

    return_button.pack(
        anchor="e"
    )

    nyquist_row, nyquist_value = create_status_row(
        column_1,
        "Nyquist Status"
    )

    nyquist_row.pack(
        fill="x",
        pady=2
    )

    alias_row, alias_value = create_status_row(
        column_1,
        "Aliasing"
    )

    alias_row.pack(
        fill="x",
        pady=2
    )

    samplecount_row, samplecount_value = create_status_row(
        column_1,
        "Samples Generated"
    )

    samplecount_row.pack(
        fill="x",
        pady=2
    )

    detected_row, detected_value = create_status_row(
        column_2,
        "Detected Frequency"
    )

    detected_row.pack(
        fill="x",
        pady=2
    )

    # Signal generation

    def generate_signal():

        try:

            amplitude = float(amp_entry.get())
            frequency = float(freq_entry.get())
            sampling_rate = float(sample_entry.get())
            duration = float(duration_entry.get())
            phase_deg = float(phase_entry.get())

            if sampling_rate <= 0 or duration <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )

            return

        phase_rad = np.deg2rad(phase_deg)

        continuous_time = np.linspace(
            0,
            duration,
            2000
        )

        sampled_time = np.arange(
            0,
            duration,
            1 / sampling_rate
        )

        wave_type = wave_dropdown.get()

        if wave_type == "Sine":

            continuous_signal = (
                amplitude *
                np.sin(
                    2 * np.pi * frequency * continuous_time
                    + phase_rad
                )
            )

            sampled_signal = (
                amplitude *
                np.sin(
                    2 * np.pi * frequency * sampled_time
                    + phase_rad
                )
            )

        else:

            continuous_signal = (
                amplitude *
                np.cos(
                    2 * np.pi * frequency * continuous_time
                    + phase_rad
                )
            )

            sampled_signal = (
                amplitude *
                np.cos(
                    2 * np.pi * frequency * sampled_time
                    + phase_rad
                )
            )

        nyquist_rate = sampling_rate / 2
        aliasing = frequency > nyquist_rate

        if aliasing:

            nyquist_value.config(
                text="VIOLATED",
                fg="#FF5C5C"
            )

            alias_value.config(
                text="YES",
                fg="#FF5C5C"
            )

        else:

            nyquist_value.config(
                text="VALID",
                fg="#00E676"
            )

            alias_value.config(
                text="NO",
                fg="#00E676"
            )

        samplecount_value.config(
            text=str(len(sampled_time))
        )

        detected_value.config(
            text=f"{frequency:.2f} Hz"
        )

        # Plot update

        ax.clear()

        ax.set_facecolor(BG_CARD)

        ax.plot(
            continuous_time,
            continuous_signal,
            linewidth=2,
            label="Continuous Signal",
            color="#0099FF"
        )

        markerline, stemlines, baseline = ax.stem(
            sampled_time,
            sampled_signal,
            linefmt="#00D4FF",
            markerfmt="o",
            basefmt=" "
        )

        markerline.set_markerfacecolor("#00D4FF")
        markerline.set_markeredgecolor("#00D4FF")

        try:
            stemlines.set_color("#00D4FF")
        except:
            pass

        ax.set_title(
            "Sampling Visualization",
            color=TEXT_WHITE
        )

        ax.set_xlabel(
            "Time (s)",
            color=TEXT_MUTED
        )

        ax.set_ylabel(
            "Amplitude",
            color=TEXT_MUTED
        )

        ax.tick_params(colors=TEXT_MUTED)

        for spine in ax.spines.values():
            spine.set_color(BORDER)

        ax.grid(
            True,
            alpha=0.2
        )

        legend = ax.legend(
            facecolor=BG_CARD,
            edgecolor=BORDER
        )

        for text in legend.get_texts():
            text.set_color(TEXT_WHITE)

        ax.margins(x=0)

        canvas.draw_idle()

    # Reset

    def reset_fields():

        amp_entry.delete(0, tk.END)
        amp_entry.insert(0, "1")

        freq_entry.delete(0, tk.END)
        freq_entry.insert(0, "5")

        sample_entry.delete(0, tk.END)
        sample_entry.insert(0, "50")

        duration_entry.delete(0, tk.END)
        duration_entry.insert(0, "1")

        phase_entry.delete(0, tk.END)
        phase_entry.insert(0, "0")

        wave_dropdown.current(0)

        generate_signal()

    # Buttons

    button_frame = tk.Frame(
        signal_section,
        bg=BG_CARD
    )

    button_frame.pack(
        fill="x",
        padx=14,
        pady=(0, 16)
    )

    generate_button = create_action_button(
        button_frame,
        "Generate Signal",
        generate_signal
    )

    generate_button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 6)
    )

    reset_button = create_action_button(
        button_frame,
        "Reset",
        reset_fields
    )

    reset_button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(6, 0)
    )

    generate_signal()