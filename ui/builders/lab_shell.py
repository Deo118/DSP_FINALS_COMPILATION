import tkinter as tk

from ui.builders.lab_layout import create_lab_workspace
from ui.builders.button_builder import create_return_button

from config import *


def create_lab_body(parent, icon, title, subtitle, accent=None):
    """Standard lab page: header + workspace panels + return button row."""
    accent = accent or ACCENT

    body = tk.Frame(parent, bg=BG_DARK)
    body.pack(fill="both", expand=True, padx=40, pady=30)

    header = tk.Frame(body, bg=BG_DARK)
    header.pack(fill="x", pady=(0, 20))

    tk.Label(
        header,
        text=icon,
        font=("Georgia", 42),
        bg=BG_DARK,
        fg=accent,
    ).pack(anchor="w")

    tk.Label(
        header,
        text=title,
        font=("Georgia", 22, "bold"),
        bg=BG_DARK,
        fg=TEXT_WHITE,
    ).pack(anchor="w", pady=(2, 4))

    tk.Label(
        header,
        text=subtitle,
        font=("Helvetica", 11),
        bg=BG_DARK,
        fg=TEXT_MUTED,
    ).pack(anchor="w")

    workspace, control_panel, graph_panel, status_panel, control_footer = (
        create_lab_workspace(body)
    )

    status_bar = tk.Frame(status_panel, bg=BG_CARD)
    status_bar.pack(fill="x", padx=16, pady=12)

    status_left = tk.Frame(status_bar, bg=BG_CARD)
    status_left.pack(side="left", fill="x", expand=True)

    status_right = tk.Frame(status_bar, bg=BG_CARD)
    status_right.pack(side="right")

    return_btn = create_return_button(status_right, parent)
    return_btn.pack(anchor="e")

    return {
        "body": body,
        "workspace": workspace,
        "control_panel": control_panel,
        "graph_panel": graph_panel,
        "status_panel": status_panel,
        "control_footer": control_footer,
        "status_left": status_left,
        "status_right": status_right,
    }


def add_footer_button(footer, text, command, side="left", padx=(0, 6)):
    """Pack an action button in the lab control footer."""
    from ui.builders.button_builder import create_action_button

    btn = create_action_button(footer, text, command)
    btn.pack(side=side, fill="x", expand=True, padx=padx)
    return btn
