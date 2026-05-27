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
        title="Lab 1 — Sampling & Aliasing",
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
    # We use TWO subplots: top = sampling viz, bottom = frequency spectrum
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    graph_container = tk.Frame(graph_panel, bg=BG_CARD)
    graph_container.pack(fill="both", expand=True, padx=16, pady=16)

    fig = Figure(figsize=(8, 6), dpi=80, facecolor=BG_CARD)
    ax_time, ax_freq = fig.subplots(2, 1)
    fig.subplots_adjust(hspace=0.45)

    canvas = FigureCanvasTkAgg(fig, master=graph_container)
    canvas.get_tk_widget().pack(fill="both", expand=True)

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

    # ── Waveform Analysis status labels ──────────────────────────────────
    analysis_title = tk.Label(
        status_left,
        text="Waveform Analysis",
        font=("Helvetica", 11, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE,
    )
    analysis_title.pack(anchor="w", pady=(14, 6))

    analysis_content = tk.Frame(status_left, bg=BG_CARD)
    analysis_content.pack(fill="x")

    col_a = tk.Frame(analysis_content, bg=BG_CARD)
    col_a.pack(side="left", padx=(0, 30))

    col_b = tk.Frame(analysis_content, bg=BG_CARD)
    col_b.pack(side="left", padx=(0, 30))

    col_c = tk.Frame(analysis_content, bg=BG_CARD)
    col_c.pack(side="left")

    peak_row,   peak_value   = create_status_row(col_a, "Peak Amplitude")
    peak_row.pack(fill="x", pady=2)
    rms_row,    rms_value    = create_status_row(col_a, "RMS Value")
    rms_row.pack(fill="x", pady=2)
    peak2_row,  peak2_value  = create_status_row(col_b, "Peak-to-Peak")
    peak2_row.pack(fill="x", pady=2)
    power_row,  power_value  = create_status_row(col_b, "Signal Power")
    power_row.pack(fill="x", pady=2)
    dom_row,    dom_value    = create_status_row(col_c, "Dominant Freq")
    dom_row.pack(fill="x", pady=2)
    alias_explain_row, alias_explain_value = create_status_row(col_c, "Alias Frequency")
    alias_explain_row.pack(fill="x", pady=2)

    # ── Signal generation ─────────────────────────────────────────────────
    def generate_signal():
        import numpy as np

        try:
            amplitude     = float(amp_entry.get())
            frequency     = float(freq_entry.get())
            sampling_rate = float(sample_entry.get())
            duration      = float(duration_entry.get())
            phase_deg     = float(phase_entry.get())

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

        # Alias frequency: the apparent frequency when aliasing occurs
        if aliasing:
            alias_freq = abs(frequency - sampling_rate * round(frequency / sampling_rate))
            nyquist_value.config(text="VIOLATED", fg="#FF5C5C")
            alias_value.config(text="YES",        fg="#FF5C5C")
            alias_explain_value.config(
                text=f"{alias_freq:.2f} Hz",
                fg="#FF5C5C"
            )
        else:
            nyquist_value.config(text="VALID", fg="#00E676")
            alias_value.config(text="NO",     fg="#00E676")
            alias_explain_value.config(text="None", fg="#00E676")

        samplecount_value.config(text=str(len(sampled_time)))
        detected_value.config(text=f"{frequency:.2f} Hz")

        # ── Waveform Analysis ─────────────────────────────────────────────
        peak_amp   = np.max(np.abs(continuous_signal))
        rms        = np.sqrt(np.mean(continuous_signal ** 2))
        p2p        = np.max(continuous_signal) - np.min(continuous_signal)
        power      = np.mean(continuous_signal ** 2)

        # Dominant frequency via FFT
        fft_vals   = np.fft.rfft(sampled_signal)
        fft_freqs  = np.fft.rfftfreq(len(sampled_signal), 1 / sampling_rate)
        dominant   = fft_freqs[np.argmax(np.abs(fft_vals))] if len(fft_vals) > 0 else frequency

        peak_value.config(text=f"{peak_amp:.4f}")
        rms_value.config(text=f"{rms:.4f}")
        peak2_value.config(text=f"{p2p:.4f}")
        power_value.config(text=f"{power:.4f}")
        dom_value.config(text=f"{dominant:.2f} Hz")

        # ── Time-domain Plot ──────────────────────────────────────────────
        ax_time.clear()
        ax_time.set_facecolor(BG_CARD)

        ax_time.plot(
            continuous_time, continuous_signal,
            linewidth=2, label="Continuous Signal", color="#0099FF",
        )

        markerline, stemlines, _ = ax_time.stem(
            sampled_time, sampled_signal,
            linefmt="#00D4FF", markerfmt="o", basefmt=" ",
        )
        markerline.set_markerfacecolor("#00D4FF")
        markerline.set_markeredgecolor("#00D4FF")
        try:
            stemlines.set_color("#00D4FF")
        except Exception:
            pass

        ax_time.set_title("Sampling Visualization", color=TEXT_WHITE, fontsize=10)
        ax_time.set_xlabel("Time (s)",   color=TEXT_MUTED, fontsize=8)
        ax_time.set_ylabel("Amplitude",  color=TEXT_MUTED, fontsize=8)
        ax_time.tick_params(colors=TEXT_MUTED, labelsize=7)
        for spine in ax_time.spines.values():
            spine.set_color(BORDER)
        ax_time.grid(True, alpha=0.2)
        legend = ax_time.legend(facecolor=BG_CARD, edgecolor=BORDER, fontsize=7)
        for text in legend.get_texts():
            text.set_color(TEXT_WHITE)
        ax_time.margins(x=0)

        # ── Frequency-domain Plot (Waveform Analysis) ─────────────────────
        ax_freq.clear()
        ax_freq.set_facecolor(BG_CARD)

        # FFT of the continuous signal for a clean spectrum
        N        = len(continuous_signal)
        fft_cont = np.fft.rfft(continuous_signal * np.hanning(N))
        freqs    = np.fft.rfftfreq(N, continuous_time[1] - continuous_time[0])
        mag      = (2.0 / N) * np.abs(fft_cont)

        ax_freq.plot(freqs, mag, color="#818CF8", linewidth=1.5, label="Frequency Spectrum")
        ax_freq.axvline(x=frequency, color="#00E676", linestyle="--",
                        linewidth=1, label=f"Signal: {frequency:.1f} Hz")
        ax_freq.axvline(x=nyquist_rate, color="#FBBF24", linestyle=":",
                        linewidth=1, label=f"Nyquist: {nyquist_rate:.1f} Hz")

        if aliasing:
            ax_freq.axvline(x=alias_freq, color="#FF5C5C", linestyle="--",
                            linewidth=1, label=f"Alias: {alias_freq:.1f} Hz")

        ax_freq.set_title(
            "Waveform Analysis — Frequency Spectrum"
            + (" ⚠ ALIASING DETECTED" if aliasing else ""),
            color="#FF5C5C" if aliasing else TEXT_WHITE,
            fontsize=10,
        )
        ax_freq.set_xlabel("Frequency (Hz)", color=TEXT_MUTED, fontsize=8)
        ax_freq.set_ylabel("Magnitude",      color=TEXT_MUTED, fontsize=8)
        ax_freq.tick_params(colors=TEXT_MUTED, labelsize=7)
        for spine in ax_freq.spines.values():
            spine.set_color(BORDER)
        ax_freq.grid(True, alpha=0.2)
        ax_freq.set_xlim(left=0, right=min(sampling_rate, freqs[-1] if len(freqs) else sampling_rate))
        legend2 = ax_freq.legend(facecolor=BG_CARD, edgecolor=BORDER, fontsize=7)
        for text in legend2.get_texts():
            text.set_color(TEXT_WHITE)

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

    # ── Footer buttons ────────────────────────────────────────────────────
    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)

    add_footer_button(btn_frame, "Generate Signal", generate_signal, padx=(0, 6))

    reset_btn = create_action_button(btn_frame, "Reset", reset_fields)
    reset_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

    generate_signal()