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
        title="Lab 4 — Z-Transform",
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

    # Optional: let user declare which element corresponds to x[0]
    x0_row, x0_entry = create_labeled_entry(
        section, "Which element is x[0]?", ""
    )
    x0_row.pack(fill="x", padx=14, pady=(0, 2))
    # additional helper line below the entry
    tk.Label(section, text="(Enter 1-based index; leave empty to assume first element)",
             font=("Helvetica", 8), bg=BG_CARD, fg=TEXT_MUTED).pack(fill="x", padx=14, pady=(0, 8))

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

    # Use a Text widget so we can show multiline step-by-step output
    result_text = tk.Text(
        output_frame,
        font=("Courier", 12),
        bg=BG_CARD,
        fg=ACCENT,
        bd=0,
        highlightthickness=0,
        wrap="word",
        height=12,
    )
    result_text.pack(fill="both", expand=True, anchor="nw")
    result_text.insert("1.0", "X(z) = —")
    result_text.config(state="disabled")

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

        # determine which entered element is x[0] (1-based). Default to 1.
        x0_text = x0_entry.get().strip()
        if x0_text == "":
            x0_pos = 1
        else:
            try:
                x0_pos = int(x0_text)
            except Exception:
                messagebox.showerror("Invalid Input", "x[0] position must be an integer or empty.")
                return
        if x0_pos < 1 or x0_pos > len(values):
            messagebox.showerror("Invalid Input", f"x[0] position must be between 1 and {len(values)}")
            return

        import re

        # Helpers to render superscript digits and signs
        super_map = {
            "0": "\u2070",
            "1": "\u00B9",
            "2": "\u00B2",
            "3": "\u00B3",
            "4": "\u2074",
            "5": "\u2075",
            "6": "\u2076",
            "7": "\u2077",
            "8": "\u2078",
            "9": "\u2079",
            "-": "\u207B",
        }

        def to_superscript(num):
            s = str(num)
            out = []
            for ch in s:
                out.append(super_map.get(ch, ch))
            return "".join(out)

        def ascii_term(value, n):
            if n == 0:
                return str(abs(value))
            # Z-transform term is x[n] * z^{-n}; compute exponent = -n
            exp = -n
            return f"{abs(value)}z^{exp}"

        def ascii_to_display(expr_ascii: str) -> str:
            # normalize spacing
            s = expr_ascii
            s = re.sub(r"\s+", " ", s).strip()
            # collapse signs: '--' -> '+', '+ -' -> '-', '- +' -> '-', '+ +' -> '+'
            s = s.replace("- -", " + ")
            s = s.replace("--", "+")
            s = s.replace("+ -", " - ")
            s = s.replace("- +", " - ")
            s = s.replace("+ +", " + ")

            # Robustly convert z^N, z^-N, z ^ N (and optionally z^+N) to superscripts
            # Capture optional leading '+' or '-' and strip '+' when present
            s = re.sub(
                r"z\s*\^\s*([+-]?\d+)",
                lambda m: "z" + to_superscript(m.group(1).lstrip("+")),
                s,
            )

            return s

        def term_display(value, n):
            # display form derived from ascii term
            return ascii_to_display(ascii_term(value, n))

        # Build a step-by-step breakdown of the Z-transform
        lines = []
        expression = ""
        any_term = False

        # Map list indices to actual n values based on x0_pos (1-based)
        # index i (0-based) corresponds to n = i - (x0_pos - 1)
        def _normalize(expr: str) -> str:
            # collapse awkward signs like '- -' -> '+ ' and '+ -' -> '- '
            if not expr:
                return expr
            expr = expr.replace("+ -", " - ")
            expr = expr.replace("- -", " + ")
            expr = expr.replace("+ +", " + ")
            expr = expr.replace("- +", " - ")
            return expr

        expression_ascii = ""

        for i, v in enumerate(values):
            n = i - (x0_pos - 1)
            lines.append(f"n={n}: a[{n}] = {v}")
            if v == 0:
                lines.append("  term = 0 (skipped)")
            else:
                any_term = True
                if n == 0:
                    term_str = str(abs(v)) if v < 0 else str(v)
                    display_term = term_str
                    if expression_ascii == "":
                        expression_ascii = term_str if v >= 0 else f"-{term_str}"
                    else:
                        if v >= 0:
                            expression_ascii += f" + {term_str}"
                        else:
                            expression_ascii += f" - {term_str}"
                else:
                    ascii_t = ascii_term(v, n)
                    display_term = ascii_to_display(ascii_t)
                    if expression_ascii == "":
                        expression_ascii = ascii_t if v >= 0 else f"-{ascii_t}"
                    else:
                        if v >= 0:
                            expression_ascii += f" + {ascii_t}"
                        else:
                            expression_ascii += f" - {ascii_t}"

                lines.append(f"  term = {display_term}")

            # convert ascii expression to display and normalize signs
            partial_display = ascii_to_display(expression_ascii) if expression_ascii else '0'
            lines.append(f"Partial X(z) = {partial_display}")
            lines.append("")

        if not any_term:
            lines = ["All terms are zero.", "X(z) = 0"]

        # Display the step-by-step lines in the text widget and highlight final expression
        final_line = f"Final X(z) = {ascii_to_display(expression_ascii) if expression_ascii else '0'}"

        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        # Insert the step lines
        result_text.insert("1.0", "\n".join(lines))
        # If there were any step lines, append a blank line separator
        if lines:
            result_text.insert("end", "\n")
        # Insert final line
        result_text.insert("end", final_line)

        # configure tag for final output
        try:
            result_text.tag_configure("final", foreground=TEXT_WHITE, font=("Courier", 13, "bold"), background=BORDER, spacing1=4, spacing3=6)
        except Exception:
            pass

        # configure tag for iteration headers (n=...)
        try:
            result_text.tag_configure(
                "iter",
                foreground=TEXT_WHITE,
                background=BORDER,
                font=("Courier", 12, "bold"),
                spacing1=2,
                spacing3=2,
            )
        except Exception:
            pass

        # Apply 'iter' tag to each line starting with 'n=' (allow leading whitespace)
        try:
            total_lines = result_text.get("1.0", "end-1c").splitlines()
            for i, content in enumerate(total_lines, start=1):
                if content.lstrip().startswith("n="):
                    start = f"{i}.0"
                    end = f"{i}.end"
                    result_text.tag_add("iter", start, end)

            # apply final tag to the last line
            last_index = result_text.index("end-1c linestart")
            result_text.tag_add("final", last_index, "end-1c")
        except Exception:
            pass

        result_text.config(state="disabled")
        status_label.config(
            text=f"Input: [{', '.join(str(v) for v in values)}]",
            fg=TEXT_WHITE,
        )

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)
    add_footer_button(btn_frame, "Compute Z-Transform", compute, padx=(0, 0))
