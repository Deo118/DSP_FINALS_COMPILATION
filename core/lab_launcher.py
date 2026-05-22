import tkinter as tk
from tkinter import messagebox
import importlib
import traceback
import pkgutil

from config import *
from ui.components.lab_window import LabWindow


def launch_lab(parent, lab_data):
    if lab_data.get("disabled"):
        messagebox.showinfo(
            "Lab Unavailable",
            f"Lab {lab_data['id']} content is still being prepared."
        )
        return

    try:
        # DEBUG: show what packages are available
        available = [m.name for m in pkgutil.iter_modules()]

        if "labs" not in available:
            messagebox.showerror(
                "Debug",
                "Package 'labs' was not bundled into the executable.\n\n"
                f"Found {len(available)} top-level packages."
            )
            return

        window = LabWindow(parent, lab_data)

        module_name = f"labs.{lab_data['module']}"

        lab_module = importlib.import_module(module_name)

        lab_module.launch(window)

    except Exception:
        traceback.print_exc()

        messagebox.showerror(
            "Lab Error",
            traceback.format_exc()
        )