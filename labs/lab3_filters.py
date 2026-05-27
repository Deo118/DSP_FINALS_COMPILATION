import tkinter as tk
import threading
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_file_picker, create_labeled_entry

from config import *

MAX_PLOT_SAMPLES = 8_000


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="⧖",
        title="Lab 3 — Audio Filtering",
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

    low_row,  low_entry  = create_labeled_entry(section, "Low Cut Frequency (Hz)",  "1000")
    low_row.pack(fill="x", padx=14, pady=(0, 12))

    high_row, high_entry = create_labeled_entry(section, "High Cut Frequency (Hz)", "3000")
    high_row.pack(fill="x", padx=14, pady=(0, 12))

    order_row, order_entry = create_labeled_entry(section, "Filter Order", "4")
    order_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Graph + playback area ─────────────────────────────────────────────
    graph_frame = tk.Frame(graph_panel, bg=BG_CARD)
    graph_frame.pack(fill="both", expand=True, padx=16, pady=16)

    PLOT_TITLES = [
        "Original Signal",
        "Low-pass Filtered",
        "High-pass Filtered",
        "Band-pass Filtered",
        "Band-stop Filtered",
    ]
    PLOT_COLORS = ["#00D4FF", "#818CF8", "#34D399", "#FBBF24", "#F87171"]

    placeholder = tk.Label(
        graph_frame,
        text="Select an audio file and click Apply Filters.",
        font=("Helvetica", 12),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        justify="center",
    )
    placeholder.pack(expand=True)

    # ─────────────────────────────────────────────────────────────────────
    # Playback state
    # ─────────────────────────────────────────────────────────────────────
    playback = {
        "thread":         None,
        "stop_flag":      False,
        "playing_idx":    None,
        "play_btns":      [],
        "audio_data":     [],
        "total_samples":  0,
        "sample_rate":    44100,
        "generation":     0,
    }

    # ── Helpers ───────────────────────────────────────────────────────────
    def _kill_all_audio():
        """Hard-stop every sounddevice stream (kills overlapping audio)."""
        try:
            import sounddevice as sd
            sd.stop()
        except Exception:
            pass

    def _reset_play_buttons():
        for btn in playback["play_btns"]:
            try:
                btn.config(text="▶  Play", bg="#2B3445", fg=TEXT_WHITE)
            except Exception:
                pass

    def _apply_button_states(active_idx):
        for i, btn in enumerate(playback["play_btns"]):
            try:
                if i == active_idx:
                    btn.config(text="■  Stop", bg="#818CF8", fg="#000000")
                else:
                    btn.config(text="▶  Play", bg="#2B3445", fg=TEXT_WHITE)
            except Exception:
                pass

    def _stop_playback(reset_buttons=True):
        """Signal current thread to stop; kill audio hardware immediately."""
        playback["stop_flag"]   = True
        playback["playing_idx"] = None
        playback["generation"] += 1
        _kill_all_audio()
        if reset_buttons:
            _reset_play_buttons()


    # ── Core play function ────────────────────────────────────────────────
    def _play_audio(idx, start_sample=None):
        import sounddevice as sd

        if not playback["audio_data"]:
            return

        if (
            playback["playing_idx"] == idx
            and start_sample is None
        ):
            _stop_playback(reset_buttons=True)
            return

        # Stop whatever is playing RIGHT NOW (including hardware)
        _stop_playback(reset_buttons=False)

        # ── Wait for the old stream thread to actually exit ──────────────────
        old_thread = playback["thread"]
        if old_thread is not None and old_thread.is_alive():
            old_thread.join(timeout=0.5)
        # ─────────────────────────────────────────────────────────────────────

        if start_sample is None:
            start_sample = 0

        # --- Set up new session BEFORE starting thread ---
        playback["stop_flag"]   = False
        playback["playing_idx"] = idx
        my_gen = playback["generation"]   

        # Visuals: update immediately so button shows "Stop" right away
        _apply_button_states(idx)

        audio, sr = playback["audio_data"][idx]
        audio_f32 = audio.astype("float32")
        if len(audio_f32) == 0:
            return
        CHUNK     = 2048

        def _stream_thread():
            import traceback
            pos = max(0, min(int(start_sample), len(audio_f32) - 1))

            try:
                # Open a NEW stream for this session
                with sd.OutputStream(samplerate=sr, channels=1, dtype="float32") as stream:
                    stream.start()
                    while pos < len(audio_f32):
                        if playback["stop_flag"]:
                            break
                        chunk = audio_f32[pos: pos + CHUNK]
                        stream.write(chunk)
                        pos  += CHUNK
            except Exception:
                traceback.print_exc()

            # Clean up UI only if no newer session has taken over
            def _maybe_reset():
                if playback["generation"] == my_gen:
                    playback["playing_idx"] = None
                    _reset_play_buttons()
            graph_frame.after(0, _maybe_reset)

        t = threading.Thread(target=_stream_thread, daemon=True)
        playback["thread"] = t
        t.start()

    # ── Canvas ────────────────────────────────────────────────────────────
    canvas_ref       = {"canvas": None, "fig": None, "axes": None}
    playback_bar_ref = {"frame": None}

    def _ensure_canvas():
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        if canvas_ref["canvas"] is not None:
            return canvas_ref["fig"], canvas_ref["axes"], canvas_ref["canvas"]

        placeholder.pack_forget()

        fig = Figure(
            figsize=(10, 6),
            dpi=80,
            facecolor=BG_CARD,
            constrained_layout=True,
        )

        axes = fig.subplots(5, 1, sharex=True)

        cv = FigureCanvasTkAgg(fig, master=graph_frame)

        cv.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        canvas_ref.update({
            "canvas": cv,
            "fig": fig,
            "axes": axes,
        })

        graph_frame.bind(
            "<Configure>",
            lambda e: cv.draw_idle()
        )

        return fig, axes, cv

    def _build_playback_bar(audio_list, sample_rate):
        if playback_bar_ref["frame"] is not None:
            try:
                playback_bar_ref["frame"].destroy()
            except Exception:
                pass

        bar = tk.Frame(graph_frame, bg=BG_DARK)
        bar.pack(fill="x", pady=(6, 0))
        playback_bar_ref["frame"] = bar

        playback["play_btns"]      = []
        playback["audio_data"]     = audio_list
        playback["sample_rate"]    = sample_rate

        if audio_list:
            playback["total_samples"] = len(audio_list[0][0])

        for idx, (title, color) in enumerate(zip(PLOT_TITLES, PLOT_COLORS)):
            col_frame = tk.Frame(bar, bg=BG_DARK)
            col_frame.pack(side="left", expand=True, fill="both", padx=2, pady=4)

            tk.Label(col_frame, text=title,
                     font=("Helvetica", 7), bg=BG_DARK, fg=color,
                     anchor="center").pack(fill="x")

            

            btn = tk.Button(
                col_frame, text="▶  Play",
                font=("Helvetica", 9, "bold"),
                bg="#2B3445", fg=TEXT_WHITE,
                activebackground="#3A465C", activeforeground=TEXT_WHITE,
                relief="flat", bd=0, cursor="hand2", padx=8, pady=5,
                command=lambda i=idx: _play_audio(i),
            )
            btn.pack(fill="x")
            playback["play_btns"].append(btn)   

    # ── Stop audio when leaving this tab / destroying the frame ──────────
    def _on_destroy(event):
        if event.widget is graph_frame:
            _stop_playback(reset_buttons=False)
    graph_frame.bind("<Destroy>", _on_destroy)

    # ── Heavy DSP work ────────────────────────────────────────────────────
    def _heavy_work(path, low_cut, high_cut, order, result):
        import numpy as np
        import scipy.signal as sig
        from core.dsp_utils import load_audio_file

        try:
            audio, sample_rate = load_audio_file(path)
        except Exception as exc:
            result["error"] = f"Could not load audio:\n{exc}"
            return

        nyquist = 0.5 * sample_rate
        if high_cut >= nyquist:
            result["error"] = f"High cut must be below Nyquist ({nyquist:.0f} Hz)."
            return

        low  = low_cut  / nyquist
        high = high_cut / nyquist

        try:
            b_lp, a_lp = sig.butter(order, low,         btype="low")
            b_hp, a_hp = sig.butter(order, high,        btype="high")
            b_bp, a_bp = sig.butter(order, [low, high], btype="bandpass")
            b_bs, a_bs = sig.butter(order, [low, high], btype="bandstop")

            filtered_full = [
                audio,
                sig.filtfilt(b_lp, a_lp, audio),
                sig.filtfilt(b_hp, a_hp, audio),
                sig.filtfilt(b_bp, a_bp, audio),
                sig.filtfilt(b_bs, a_bs, audio),
            ]
        except Exception as exc:
            result["error"] = f"Filter computation failed:\n{exc}"
            return

        time_full = np.linspace(0, len(audio) / sample_rate, len(audio))

        def _ds(arr):
            if len(arr) <= MAX_PLOT_SAMPLES:
                return arr
            return arr[:: max(1, len(arr) // MAX_PLOT_SAMPLES)]

        result["audio_list"]   = [(f, sample_rate) for f in filtered_full]
        result["plot_signals"] = [_ds(f) for f in filtered_full]
        result["time"]         = _ds(time_full)
        result["sample_rate"]  = sample_rate

    # ── Apply button ──────────────────────────────────────────────────────
    def apply_filters():
        from core.dsp_utils import style_axes

        path = path_var.get()
        if not path or path == "No file selected":
            messagebox.showerror("Invalid Input", "Please select an audio file first.")
            return

        try:
            low_cut  = float(low_entry.get())
            high_cut = float(high_entry.get())
            order    = int(order_entry.get())
            if order < 1 or low_cut <= 0 or high_cut <= 0 or low_cut >= high_cut:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid positive frequencies and filter order (≥ 1).\n"
                "Low cut must be less than high cut.",
            )
            return

        _stop_playback()

        placeholder.pack_forget()
        loading = tk.Label(
            graph_frame, text="⏳  Processing audio, please wait…",
            font=("Helvetica", 13), bg=BG_CARD, fg="#00D4FF",
        )
        loading.place(relx=0.5, rely=0.5, anchor="center")
        graph_frame.update_idletasks()

        result = {}

        def _on_done():
            loading.place_forget()
            if "error" in result:
                messagebox.showerror("Error", result["error"])
                return

            fig, axes, cv = _ensure_canvas()
            for idx, (ax, sig_plot, title, color) in enumerate(zip(
                axes, result["plot_signals"], PLOT_TITLES, PLOT_COLORS
            )):
                ax.clear()
                style_axes(
                    ax,
                    title=title,
                    xlabel="Time (s)" if idx == len(axes) - 1 else "",
                    ylabel="Amp",
                )
                ax.plot(result["time"], sig_plot, color=color, linewidth=0.6)

            cv.draw_idle()

            _build_playback_bar(
                result["audio_list"],
                result["sample_rate"]
            )

        def _run():
            _heavy_work(path, low_cut, high_cut, order, result)
            graph_frame.after(0, _on_done)

        threading.Thread(target=_run, daemon=True).start()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Apply Filters", apply_filters, padx=(0, 0))