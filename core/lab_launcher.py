import tkinter as tk
from tkinter import messagebox
import importlib

from config import *
from ui.components.lab_window import LabWindow


def launch_lab(parent, lab_data):
    # Disabled lab
    if lab_data.get("disabled"):
        messagebox.showinfo(
            "Lab Unavailable",
            f"Lab {lab_data['id']} content is still being prepared."
        )
        return

    try:
        # Create lab window
        window = LabWindow(parent, lab_data)

        # Dynamic import
        module_name = f"labs.{lab_data['module']}"

        lab_module = importlib.import_module(module_name)

        # Launch module UI
        lab_module.launch(window)

    except Exception as e:
        messagebox.showerror(
            "Lab Error",
            f"Failed to load lab:\n\n{str(e)}"
        )