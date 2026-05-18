import tkinter as tk

from config import *


def create_lab_workspace(parent):

    workspace = tk.Frame(
        parent,
        bg=BG_DARK
    )

    workspace.pack(
        fill="both",
        expand=True
    )

    main_content = tk.Frame(
        workspace,
        bg=BG_DARK
    )

    main_content.pack(
        fill="both",
        expand=True,
        pady=(0, 16)
    )

    control_panel = tk.Frame(
        main_content,
        bg=BG_CARD,
        width=380,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    control_panel.pack(
        side="left",
        fill="y",
        padx=(0, 16)
    )

    control_panel.pack_propagate(False)

    graph_panel = tk.Frame(
        main_content,
        bg=BG_CARD,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    graph_panel.pack(
        side="left",
        fill="both",
        expand=True
    )

    status_panel = tk.Frame(
        workspace,
        bg=BG_CARD,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    status_panel.pack(
        fill="x"
    )

    return (
        workspace,
        control_panel,
        graph_panel,
        status_panel
    )