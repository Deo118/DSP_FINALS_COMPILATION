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

    # Output mode selector: Solution (step-by-step) or Graph
    output_mode = tk.StringVar(value="solution")
    mode_row = tk.Frame(section, bg=BG_CARD)
    tk.Label(mode_row, text="Output:", bg=BG_CARD, fg=TEXT_WHITE).pack(side="left", padx=(0, 8))
    tk.Radiobutton(
        mode_row,
        text="Solution",
        variable=output_mode,
        value="solution",
        bg=BG_CARD,
        fg=TEXT_WHITE,
        selectcolor=BORDER,
        activebackground=BG_CARD,
    ).pack(side="left", padx=(0, 8))
    tk.Radiobutton(
        mode_row,
        text="Graph",
        variable=output_mode,
        value="graph",
        bg=BG_CARD,
        fg=TEXT_WHITE,
        selectcolor=BORDER,
        activebackground=BG_CARD,
    ).pack(side="left")
    mode_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Graph area ────────────────────────────────────────────────────────
    graph_frame = tk.Frame(graph_panel, bg=BG_CARD)
    graph_frame.pack(fill="both", expand=True, padx=16, pady=16)

    # Solution container: split canvas into two halves for DFT (left) and FFT (right)
    solution_container = tk.Frame(graph_frame, bg=BG_CARD)
    solution_container.pack(fill="both", expand=True, padx=2, pady=(6, 0))

    left_frame = tk.Frame(solution_container, bg=BG_CARD)
    left_frame.pack(fill="both", expand=True)

    # Left: DFT solution text
    left_text = tk.Text(
        left_frame,
        font=("Courier", 11),
        bg=BG_CARD,
        fg=ACCENT,
        bd=0,
        highlightthickness=0,
        wrap="word",
    )
    left_vscroll = tk.Scrollbar(left_frame, orient="vertical", command=left_text.yview)
    left_text.configure(yscrollcommand=left_vscroll.set)
    # Start hidden; show only when content overflows
    try:
        left_vscroll.pack_forget()
    except Exception:
        pass
    left_text.pack(fill="both", expand=True)

    # Right FFT column removed; left pane will occupy full solution area.

    # Container where the matplotlib canvas will be placed for Graph mode
    plot_frame = tk.Frame(graph_frame, bg=BG_CARD)
    plot_frame.pack(fill="both", expand=True)
    # If default mode is Solution, hide the empty plot frame so steps occupy full area
    if output_mode.get() != "graph":
        try:
            plot_frame.pack_forget()
        except Exception:
            pass

    canvas_ref = {"canvas": None}

    def _build_canvas():
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        if canvas_ref["canvas"]:
            canvas_ref["canvas"].get_tk_widget().destroy()

        fig = Figure(figsize=(8, 5), dpi=100, facecolor=BG_CARD)
        ax  = fig.add_subplot(111)
        cv  = FigureCanvasTkAgg(fig, master=plot_frame)
        cv.get_tk_widget().pack(fill="both", expand=True)
        canvas_ref["canvas"] = cv
        return fig, ax, cv

    # ── Status labels ─────────────────────────────────────────────────────
    # Status area intentionally left empty (only Return button remains)
    info_frame = tk.Frame(status_left, bg=BG_CARD)
    info_frame.pack(anchor="w", fill="x")

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

        # The detailed DFT/FFT final output is shown inline in Solution mode panes.
        # Prepare aggregate final string for titles and panes.
        final_agg = format_dft_sequence(X)

        # If Graph mode requested, build the canvas and plot. Otherwise keep plot hidden.
        cv = None
        if output_mode.get() == "graph":
            # Ensure plot_frame is visible before creating the canvas
            try:
                plot_frame.pack(fill="both", expand=True)
            except Exception:
                pass
            fig, ax, cv = _build_canvas()

            # Show final aggregate in the plot title for Graph mode
            style_axes(
                ax,
                title=f"Frequency-Domain Representation — X(n) = {final_agg}",
                xlabel="Frequency",
                ylabel="Amplitude",
            )

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
            # ensure solution area is hidden when showing graph
            try:
                solution_container.pack_forget()
            except Exception:
                pass
        else:
            # Hide any existing plot canvas and the whole plot_frame when in Solution mode
            if canvas_ref["canvas"]:
                try:
                    canvas_ref["canvas"].get_tk_widget().pack_forget()
                except Exception:
                    pass
            try:
                plot_frame.pack_forget()
            except Exception:
                pass
            try:
                # Ensure solution_container (split panes) fills the available graph area
                solution_container.pack(fill="both", expand=True, padx=2, pady=(6, 0))
            except Exception:
                pass

        # Build aggregate final string to show inside each pane (also used for Graph)
        final_agg = format_dft_sequence(X)

        # Build step-by-step DFT computation for display
        def fmt_complex(c):
            re = float(np.real(c))
            im = float(np.imag(c))
            re_s = f"{re:.4g}"
            im_s = f"{abs(im):.4g}"
            if abs(im) < 1e-12:
                return f"{re_s}"
            sign = "+" if im >= 0 else "-"
            return f"{re_s} {sign} {im_s}j"

        # Build DFT (direct) step-by-step on left pane
        left_steps = []
        left_steps.append(f"N = {N}\n")
        for k in range(N):
            left_steps.append("k=" + str(k) + ": compute X[k] = Σ_{n=0}^{N-1} x[n] * e^(-j*2π*k*n/N)")
            partial = 0+0j
            for n in range(N):
                term = x[n] * np.exp(-2j * np.pi * k * n / N)
                partial += term
                left_steps.append(f"  n={n}: x[{n}]={x[n]}  term={fmt_complex(term)}  partial={fmt_complex(partial)}")
            left_steps.append(f"  => X[{k}] = {fmt_complex(partial)}  |X[{k}]|={np.abs(partial):.4g}\n")

        # FFT step-by-step removed from right pane (column eliminated). If you want
        # FFT steps shown they will be integrated into the left pane or displayed elsewhere.

        # Insert into left_text and right_text and apply tags
        left_text.config(state="normal")
        left_text.delete("1.0", "end")
        left_text.insert("1.0", "\n".join(left_steps))
        try:
            left_text.tag_configure("iter", foreground=TEXT_WHITE, background=BORDER, font=("Courier", 11, "bold"))
            left_text.tag_configure("final", foreground=TEXT_WHITE, background=BORDER, font=("Courier", 11, "bold"))
        except Exception:
            pass
        # Tag k=... lines and final lines in left_text
        left_lines = left_text.get("1.0", "end-1c").splitlines()
        for i, line in enumerate(left_lines, start=1):
            if line.startswith("k="):
                left_text.tag_add("iter", f"{i}.0", f"{i}.end")
            if line.strip().startswith("=> X["):
                left_text.tag_add("final", f"{i}.0", f"{i}.end")
        # Append aggregate final line to left pane and tag it
        left_text.insert("end", "\nFinal X = " + final_agg)
        try:
            last_index = left_text.index("end-1c linestart")
            left_text.tag_add("final", last_index, "end-1c")
        except Exception:
            pass
        # Show scrollbar only if needed. Use bbox of the last character
        # to reliably detect overflow (more robust than yview alone).
        left_text.update_idletasks()
        try:
            bbox = left_text.bbox("end-1c")
            height = left_text.winfo_height()
            if bbox is not None:
                y_end = bbox[1] + bbox[3]
                if y_end > height:
                    left_vscroll.pack(side="right", fill="y")
                else:
                    left_vscroll.pack_forget()
            else:
                # Empty or no layout yet, hide scrollbar
                left_vscroll.pack_forget()
        except Exception:
            # Fallback to previous yview method if bbox fails
            try:
                top, bot = left_text.yview()
                if bot - top < 1.0:
                    left_vscroll.pack(side="right", fill="y")
                else:
                    left_vscroll.pack_forget()
            except Exception:
                pass
        left_text.config(state="disabled")

        # Right pane removed; nothing to update there.

        # Ensure correct visibility after building steps
        if output_mode.get() == "graph":
            try:
                solution_container.pack_forget()
            except Exception:
                pass
            if cv:
                try:
                    # Ensure plot_frame is visible then pack the canvas widget
                    try:
                        plot_frame.pack(fill="both", expand=True)
                    except Exception:
                        pass
                    cv.get_tk_widget().pack(fill="both", expand=True)
                except Exception:
                    pass
        else:
            try:
                solution_container.pack(fill="both", expand=True, padx=2, pady=(6, 0))
            except Exception:
                pass

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Compute DFT/FFT", compute, padx=(0, 0))

    compute()
