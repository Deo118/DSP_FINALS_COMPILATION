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

    # Footer is packed FIRST (side=bottom) so it always stays visible
    control_footer = tk.Frame(
        control_panel,
        bg=BG_CARD,
        height=64        # increased from 56 — ensures buttons are never clipped
    )

    control_footer.pack(
        side="bottom",
        fill="x",
        padx=16,
        pady=(8, 16)
    )

    control_footer.pack_propagate(False)

    scroll_container = tk.Frame(
        control_panel,
        bg=BG_CARD
    )

    scroll_container.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        scroll_container,
        bg=BG_CARD,
        highlightthickness=0,
        bd=0
    )

    scrollbar = tk.Scrollbar(
        scroll_container,
        orient="vertical",
        command=canvas.yview
    )

    control_content = tk.Frame(
        canvas,
        bg=BG_CARD
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=control_content,
        anchor="nw"
    )

    def _update_scroll_region(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _resize_canvas_width(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    def _on_mousewheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def _bind_mousewheel(_event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_mousewheel(_event):
        canvas.unbind_all("<MouseWheel>")

    control_content.bind("<Configure>", _update_scroll_region)
    canvas.bind("<Configure>", _resize_canvas_width)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    control_panel.bind("<Enter>", _bind_mousewheel)
    control_panel.bind("<Leave>", _unbind_mousewheel)

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
        control_content,
        graph_panel,
        status_panel,
        control_footer
    )
