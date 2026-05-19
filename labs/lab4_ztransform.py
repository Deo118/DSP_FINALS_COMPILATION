import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_labeled_entry

from config import *


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="Z",
        title="Z-Transform",
        subtitle=(
            "Enter a space-separated integer sequence "
            "to compute its Z-transform expression."
        ),
        accent="#A78BFA",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]
    status_left    = shell["status_left"]

    section = create_section(control_panel, "Sequence Input")
    section.pack(fill="x", padx=16, pady=16)

    seq_row, seq_entry = create_labeled_entry(
        section, "Sequence (space-separated integers)", "1 2 -1 3"
    )
    seq_row.pack(fill="x", padx=14, pady=(0, 8))

    # ── Output display ────────────────────────────────────────────────────
    output_frame = tk.Frame(graph_panel, bg=BG_CARD)
    output_frame.pack(fill="both", expand=True, padx=24, pady=24)

    tk.Label(
        output_frame,
        text="Z-Transform Result",
        font=("Helvetica", 12, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE,
        anchor="w",
    ).pack(fill="x", pady=(0, 16))

    result_label = tk.Label(
        output_frame,
        text="X(z) = —",
        font=("Courier", 16),
        bg=BG_CARD,
        fg=ACCENT,
        anchor="nw",
        justify="left",
        wraplength=520,
    )
    result_label.pack(fill="both", expand=True, anchor="nw")

    status_label = tk.Label(
        status_left,
        text="Enter a sequence and click Compute Z-Transform.",
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        anchor="w",
    )
    status_label.pack(anchor="w")

    def compute():
        from core.dsp_utils import parse_int_sequence, z_transform

        try:
            values = parse_int_sequence(seq_entry.get())
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        expression = z_transform(values)
        result_label.config(text=f"X(z) = {expression}")
        status_label.config(
            text=f"Input: [{', '.join(str(v) for v in values)}]",
            fg=TEXT_WHITE,
        )

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Compute Z-Transform", compute, padx=(0, 0))
