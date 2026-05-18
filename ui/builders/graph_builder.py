import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config import *


def create_graph(parent):
    graph_container = tk.Frame(
        parent,
        bg=BG_CARD,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    fig = Figure(
        figsize=(7, 5),
        dpi=100,
        facecolor=BG_CARD
    )

    ax = fig.add_subplot(111)

    ax.set_facecolor(BG_CARD)

    ax.tick_params(colors=TEXT_MUTED)

    for spine in ax.spines.values():
        spine.set_color(BORDER)

    canvas = FigureCanvasTkAgg(fig, master=graph_container)

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    return graph_container, fig, ax, canvas