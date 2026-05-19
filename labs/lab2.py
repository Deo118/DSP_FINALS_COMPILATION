import tkinter as tk
from tkinter import messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_file_picker
from ui.builders.button_builder import create_action_button

from config import *

THUMB_W = 320
THUMB_H = 220

IMAGE_FILETYPES = [
    ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"),
    ("All files", "*.*"),
]


def _load_image_bgr(path):
    from PIL import Image, ImageOps
    import numpy as np
    import cv2

    path = str(path).strip()
    if not path:
        return None
    try:
        pil_img = Image.open(path)
        pil_img = ImageOps.exif_transpose(pil_img)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        rgb = np.array(pil_img)
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    except Exception:
        pass
    try:
        data = np.fromfile(path, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception:
        return None


def _to_pil(image_bgr_or_gray):
    from PIL import Image
    import cv2

    if image_bgr_or_gray is None:
        return None
    if len(image_bgr_or_gray.shape) == 2:
        return Image.fromarray(image_bgr_or_gray)
    rgb = cv2.cvtColor(image_bgr_or_gray, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def _make_thumbnail(pil_image):
    from PIL import Image
    copy = pil_image.copy()
    copy.thumbnail((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
    return copy


def launch(parent):
    shell = create_lab_body(
        parent,
        icon="◫",
        title="Digital Image Processing",
        subtitle=(
            "Upload an image to see original, grayscale, threshold, "
            "median blur, and Laplacian edge detection."
        ),
        accent="#38BDF8",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]
    status_left    = shell["status_left"]

    section = create_section(control_panel, "Image Input")
    section.pack(fill="x", padx=16, pady=16)

    status_label = tk.Label(
        status_left,
        text="No image loaded.",
        font=("Helvetica", 10),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        anchor="w",
    )
    status_label.pack(anchor="w")

    outer   = tk.Frame(graph_panel, bg=BG_CARD)
    outer.pack(fill="both", expand=True, padx=12, pady=12)

    canvas_scroll = tk.Canvas(outer, bg=BG_CARD, highlightthickness=0)
    scrollbar     = tk.Scrollbar(outer, orient="vertical", command=canvas_scroll.yview)
    results_frame = tk.Frame(canvas_scroll, bg=BG_CARD)

    results_frame.bind(
        "<Configure>",
        lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")),
    )

    canvas_window = canvas_scroll.create_window((0, 0), window=results_frame, anchor="nw")
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_canvas_resize(event):
        canvas_scroll.itemconfig(canvas_window, width=event.width)

    canvas_scroll.bind("<Configure>", _on_canvas_resize)

    state = {"image_bgr": None, "photo_refs": []}

    def _clear_results():
        for child in results_frame.winfo_children():
            child.destroy()
        state["photo_refs"] = []

    def _show_placeholder():
        _clear_results()
        tk.Label(
            results_frame,
            text=(
                "No image yet.\n\n"
                "Click Browse to select an image.\n"
                "Results appear here automatically."
            ),
            font=("Helvetica", 12),
            bg=BG_CARD,
            fg=TEXT_MUTED,
            justify="center",
            pady=80,
        ).pack(fill="both", expand=True)

    def _show_results(outputs):
        from PIL import ImageTk
        _clear_results()

        grid = tk.Frame(results_frame, bg=BG_CARD)
        grid.pack(fill="both", expand=True, padx=8, pady=8)

        for col in range(3):
            grid.grid_columnconfigure(col, weight=1)

        for index, (img_array, title) in enumerate(outputs):
            row, col = divmod(index, 3)
            cell = tk.Frame(grid, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
            cell.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(cell, text=title, font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=TEXT_WHITE).pack(pady=(8, 4))

            pil_img = _to_pil(img_array)
            if pil_img is None:
                continue
            thumb = _make_thumbnail(pil_img)
            photo = ImageTk.PhotoImage(thumb)
            state["photo_refs"].append(photo)
            tk.Label(cell, image=photo, bg=BG_CARD).pack(padx=8, pady=(0, 12))

        results_frame.update_idletasks()
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        canvas_scroll.yview_moveto(0)

    def _run_processing():
        import cv2
        import numpy as np

        image = state["image_bgr"]
        if image is None:
            messagebox.showerror("Invalid Input", "Please select an image file first.")
            return False

        try:
            gray      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, bw     = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            median    = cv2.medianBlur(gray, 5)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian = np.uint8(np.absolute(laplacian))

            _show_results([
                (image,     "Original"),
                (gray,      "Grayscale"),
                (bw,        "Black & White (127)"),
                (median,    "Median Blurred"),
                (laplacian, "Laplacian Edge Detection"),
            ])
            status_label.config(text="Done — 5 processed versions shown.", fg="#00E676")
            return True

        except Exception as exc:
            messagebox.showerror("Processing Error", f"Could not process the image:\n\n{exc}")
            status_label.config(text="Processing failed.", fg="#FF5C5C")
            return False

    def on_file_selected(path):
        try:
            image = _load_image_bgr(path)
            if image is None:
                messagebox.showerror(
                    "Invalid Input",
                    "Could not read the image.\nTry PNG or JPG.",
                )
                state["image_bgr"] = None
                status_label.config(text="Failed to load image.", fg="#FF5C5C")
                return

            state["image_bgr"] = image
            name = path.replace("\\", "/").split("/")[-1]
            status_label.config(text=f"Loaded: {name} — processing…", fg=TEXT_WHITE)
            parent.update_idletasks()
            _run_processing()

        except Exception as exc:
            messagebox.showerror("Error", f"Something went wrong:\n\n{exc}")
            status_label.config(text="Error loading image.", fg="#FF5C5C")

    file_row, path_var, _browse = create_file_picker(
        section, "Image File", IMAGE_FILETYPES, command=on_file_selected,
    )
    file_row.pack(fill="x", padx=14, pady=(0, 8))

    def process_image():
        path = path_var.get()
        if state["image_bgr"] is None and path and path != "No file selected":
            img = _load_image_bgr(path)
            if img is not None:
                state["image_bgr"] = img
        _run_processing()

    def reset_lab():
        path_var.set("No file selected")
        state["image_bgr"] = None
        status_label.config(text="No image loaded.", fg=TEXT_MUTED)
        _show_placeholder()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)

    add_footer_button(btn_frame, "Process Image", process_image, padx=(0, 6))

    reset_btn = create_action_button(btn_frame, "Reset", reset_lab)
    reset_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

    _show_placeholder()
