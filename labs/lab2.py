import tkinter as tk
from tkinter import filedialog, messagebox

from ui.builders.lab_shell import create_lab_body, add_footer_button
from ui.builders.section_builder import create_section
from ui.builders.control_builder import create_file_picker
from ui.builders.button_builder import create_action_button

from config import *

THUMB_W = 200
THUMB_H = 140

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


def _make_thumbnail(pil_image, w=THUMB_W, h=THUMB_H):
    from PIL import Image
    copy = pil_image.copy()
    copy.thumbnail((w, h), Image.Resampling.LANCZOS)
    return copy

def launch(parent):
    shell = create_lab_body(
        parent,
        icon="◫",
        title="Lab 2 — Digital Image Processing",
        subtitle=(
            "Upload an image, then click Apply Filters to see processed versions."
        ),
        accent="#38BDF8",
    )

    control_panel  = shell["control_panel"]
    graph_panel    = shell["graph_panel"]
    control_footer = shell["control_footer"]
    status_left    = shell["status_left"]

    # ── Left-panel controls ───────────────────────────────────────────────
    section = create_section(control_panel, "Image Input")
    section.pack(fill="x", padx=16, pady=(16, 8))

    # (Removed global B&W Threshold slider — per-image controls moved to preview)

    # Status label
    status_label = tk.Label(
        status_left,
        text="No image loaded.",
        font=("Helvetica", 10),
        bg=BG_CARD, fg=TEXT_MUTED, anchor="w",
    )
    status_label.pack(anchor="w")

    # ── Scrollable results panel ──────────────────────────────────────────
    outer = tk.Frame(graph_panel, bg=BG_CARD)
    outer.pack(fill="both", expand=True, padx=12, pady=12)

    canvas_scroll = tk.Canvas(outer, bg=BG_CARD, highlightthickness=0)
    results_frame = tk.Frame(canvas_scroll, bg=BG_CARD)

    results_frame.bind(
        "<Configure>",
        lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")),
    )

    canvas_window = canvas_scroll.create_window((0, 0), window=results_frame, anchor="nw")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    canvas_scroll.bind(
        "<Configure>",
        lambda e: canvas_scroll.itemconfig(canvas_window, width=e.width),
    )
    
    # Large preview replaces the results area only when a result is selected.
    preview_section = tk.Frame(
        outer,
        bg=BG_CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    preview_header = tk.Frame(
        preview_section,
        bg=BG_CARD
    )
    preview_header.pack(fill="x", padx=12, pady=(10, 4))

    preview_title = tk.Label(
        preview_header,
        text="Selected Image Preview",
        font=("Helvetica", 11, "bold"),
        bg=BG_CARD,
        fg=TEXT_WHITE
    )
    preview_title.pack(side="left")

    close_preview_btn = create_action_button(
        preview_header,
        "Close",
        lambda: close_preview()
    )
    close_preview_btn.pack(side="right")

    save_preview_btn = create_action_button(
        preview_header,
        "Save Image",
        lambda: save_preview_image()
    )
    try:
        save_preview_btn.configure(width=10)
        save_preview_btn.configure(height=1)
    except Exception:
        pass
    save_preview_btn.pack(side="right", padx=(0, 8))

    # Layout: canvas container (left) and a taller sidebar (right) for sliders
    canvas_container = tk.Frame(preview_section, bg=BG_CARD)
    canvas_container.pack(side="left", fill="both", expand=True, pady=(0, 10))

    preview_canvas = tk.Canvas(canvas_container, bg=BG_CARD, highlightthickness=0)
    preview_canvas.pack(side="left", fill="both", expand=True)

    # Sidebar for preview controls (long vertical area)
    sidebar_frame = tk.Frame(preview_section, bg=BG_CARD, width=340)
    sidebar_frame.pack(side="right", fill="y")
    sidebar_frame.pack_propagate(False)

    # Move zoom controls into sidebar and stack vertically
    zoom_row = tk.Frame(sidebar_frame, bg=BG_CARD)
    zoom_row.pack(fill="x", padx=10, pady=(10, 6))

    tk.Label(
        zoom_row,
        text="Zoom",
        bg=BG_CARD,
        fg=TEXT_MUTED
    ).pack(side="left")

    zoom_value_label = tk.Label(
        zoom_row,
        text="100%",
        bg=BG_CARD,
        fg="#38BDF8"
    )

    zoom_value_label.pack(side="right")

    zoom_var = tk.IntVar(value=100)

    zoom_border = tk.Frame(
        sidebar_frame,
        bg=BORDER,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    zoom_border.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    # Ensure preview is hidden initially
    preview_section.pack_forget()

    # Preview-specific slider area (populated when an image is selected)
    preview_slider_frame = tk.Frame(sidebar_frame, bg=BG_CARD)
    preview_slider_frame.pack(fill="x", padx=10, pady=(8, 8))

    # Scrollbars placed in the sidebar under the sliders area
    preview_vscroll = tk.Scrollbar(sidebar_frame, orient="vertical", command=preview_canvas.yview)
    preview_hscroll = tk.Scrollbar(sidebar_frame, orient="horizontal", command=preview_canvas.xview)
    preview_canvas.configure(yscrollcommand=preview_vscroll.set, xscrollcommand=preview_hscroll.set)

    # Place scrollbars directly under the sliders in the sidebar so they occupy the leftover space
    preview_vscroll.config(width=12)
    preview_hscroll.config(width=12)
    preview_vscroll.pack(side="right", fill="y", padx=(6, 6), pady=(8, 8))
    preview_hscroll.pack_forget()

    from PIL import ImageTk

    def show_results_view():
        preview_section.pack_forget()
        canvas_scroll.pack(side="left", fill="both", expand=True)
        

    def show_preview_view():
        canvas_scroll.pack_forget()
        preview_section.pack(fill="both", expand=True)

    def close_preview():
        state["selected_pil"] = None
        state["preview_photo"] = None
        try:
            preview_canvas.delete("IMG")
            preview_canvas.xview_moveto(0)
            preview_canvas.yview_moveto(0)
        except Exception:
            pass
        zoom_var.set(100)
        zoom_value_label.config(text="100%")
        show_results_view()

    def save_preview_image():
        _save_pil_image_dialog(state.get("selected_pil"))

    def _save_pil_image_dialog(pil_img):
        if pil_img is None:
            messagebox.showerror("Save Image", "Select a filtered image before saving.")
            return

        path = filedialog.asksaveasfilename(
            title="Save image",
            defaultextension=".png",
            filetypes=[
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg;*.jpeg"),
                ("Bitmap image", "*.bmp"),
                ("All files", "*.*"),
            ],
        )
        # Regardless of save/cancel, bring the lab window to front (OS dialogs may push it back)
        try:
            top = preview_section.winfo_toplevel()
            try:
                top.lift()
                top.focus_force()
                top.attributes('-topmost', True)
                top.update()
                top.attributes('-topmost', False)
            except Exception:
                try:
                    top.lift()
                    top.focus_force()
                except Exception:
                    pass
        except Exception:
            pass

        if not path:
            return

        try:
            save_img = pil_img
            if path.lower().endswith((".jpg", ".jpeg")) and save_img.mode != "RGB":
                save_img = save_img.convert("RGB")
            save_img.save(path)
            saved_name = path.replace("\\", "/").split("/")[-1]
            status_label.config(text=f"Saved: {saved_name}", fg="#00E676")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save the image:\n\n{exc}")

    def update_preview():
        pil_img = state["selected_pil"]

        if pil_img is None:
            return

        pct = int(zoom_var.get())
        pct = max(10, min(pct, 200))

        zoom_value_label.config(text=f"{pct}%")

        w = max(1, int(pil_img.width * pct / 100))
        h = max(1, int(pil_img.height * pct / 100))

        resized = pil_img.resize((w, h))

        photo = ImageTk.PhotoImage(resized)

        state["preview_photo"] = photo

        # update canvas image, keep within canvas using scrollregion
        preview_canvas.delete("IMG")
        # center if smaller than canvas
        try:
            canvas_w = preview_canvas.winfo_width()
            canvas_h = preview_canvas.winfo_height()
        except Exception:
            canvas_w = None
            canvas_h = None

        if canvas_w and w < canvas_w:
            x = (canvas_w - w) // 2
        else:
            x = 0
        if canvas_h and h < canvas_h:
            y = (canvas_h - h) // 2
        else:
            y = 0

        preview_canvas.create_image(x, y, anchor="nw", image=photo, tags="IMG")
        preview_canvas.config(scrollregion=(0, 0, w, h))
        # Show horizontal scrollbar only when image wider than canvas
        try:
            canvas_w = preview_canvas.winfo_width()
            if w > canvas_w:
                preview_hscroll.pack(in_=sidebar_frame, side="bottom", fill="x", padx=(6, 6))
            else:
                preview_hscroll.pack_forget()
        except Exception:
            pass

    def _clear_preview_slider():
        for child in preview_slider_frame.winfo_children():
            child.destroy()

    def _build_preview_slider():
        import cv2
        import numpy as np

        _clear_preview_slider()

        idx = state.get("selected_index")
        if idx is None:
            return

        # index 0 = Original (no slider)
        if idx == 0:
            return

        gray_arr = state.get("gray_array")
        if gray_arr is None and state.get("image_bgr") is not None:
            try:
                gray_arr = cv2.cvtColor(state.get("image_bgr"), cv2.COLOR_BGR2GRAY)
                state["gray_array"] = gray_arr
            except Exception:
                gray_arr = None

        is_median = idx == 3

        # Label row
        lbl_row = tk.Frame(preview_slider_frame, bg=BG_CARD)
        lbl_row.pack(fill="x")

        if is_median:
            slider_text = "Blur Kernel"
            default_text = "5"
        elif idx == 1:
            slider_text = "Clip Level"
            default_text = "127"
        elif idx == 2:
            slider_text = "Threshold"
            default_text = "127"
        elif idx == 4:
            slider_text = "Sensitivity"
            default_text = "127"
        else:
            slider_text = "Value"
            default_text = "127"

        tk.Label(lbl_row, text=slider_text, font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")
        val_lbl = tk.Label(lbl_row, text=default_text, font=("Helvetica", 9, "bold"), bg=BG_CARD, fg="#38BDF8")
        val_lbl.pack(side="right")

        if is_median:
            slider_var = tk.IntVar(value=5)
            from_val, to_val = 1, 11
        else:
            slider_var = tk.IntVar(value=127)
            from_val, to_val = 0, 255

        def _on_preview_slide(val):
            v = int(float(val))
            val_lbl.config(text=str(v if not is_median else max(1, v * 2 - 1)))

            if gray_arr is None:
                return

            if idx == 1:
                result = np.where(gray_arr < v, 0, gray_arr).astype(np.uint8)
                new_pil = _to_pil(result)

            elif idx == 2:
                _, bw_new = cv2.threshold(gray_arr, v, 255, cv2.THRESH_BINARY)
                new_pil = _to_pil(bw_new)

            elif idx == 3:
                kernel = max(1, v * 2 - 1)
                blurred = cv2.medianBlur(gray_arr, kernel)
                new_pil = _to_pil(blurred)

            elif idx == 4:
                lap = cv2.Laplacian(gray_arr, cv2.CV_64F)
                lap = np.uint8(np.absolute(lap))
                lap = np.where(lap < v, 0, lap).astype(np.uint8)
                new_pil = _to_pil(lap)

            else:
                return

            if new_pil:
                state["selected_pil"] = new_pil.copy()
                update_preview()

        slider_border = tk.Frame(preview_slider_frame, bg=BORDER, highlightthickness=1, highlightbackground=BORDER)
        slider_border.pack(fill="x", pady=(4, 0))

        tk.Scale(
            slider_border,
            from_=from_val,
            to=to_val,
            orient="horizontal",
            variable=slider_var,
            command=_on_preview_slide,
            bg=BG_CARD,
            fg=TEXT_WHITE,
            troughcolor="#2B3445",
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            activebackground="#38BDF8",
            showvalue=False,
        ).pack(fill="x", padx=4, pady=4)

    tk.Scale(
        zoom_border,
        from_=10,
        to=200,
        orient="horizontal",
        variable=zoom_var,
        command=lambda v: update_preview(),
        bg=BG_CARD,
        fg=TEXT_WHITE,
        troughcolor="#2B3445",
        highlightthickness=0,
        bd=0,
        sliderrelief="flat",
        activebackground="#38BDF8",
        showvalue=False
    ).pack(
        fill="x",
        padx=4,
        pady=4
    )

    state = {
        "image_bgr": None,
        "photo_refs": [],
        "gray_array": None,

        "selected_pil": None,
        "preview_photo": None,
        "results_meta": [],
        "selected_index": None,
    }

    def _clear_results():
        for child in results_frame.winfo_children():
            child.destroy()
        state["photo_refs"] = []

    def _show_placeholder():
        _clear_results()
        close_preview()
        tk.Label(
            results_frame,
            text=(
                "No image yet.\n\n"
                "1. Click Browse to select an image.\n"
                "2. Click Apply Filters to see processed versions.\n"
                "3. Use per-image sliders in the preview to tweak results.\n\n"
                "Click any result image to preview or save it."
            ),
            font=("Helvetica", 12),
            bg=BG_CARD, fg=TEXT_MUTED, justify="center", pady=60,
        ).pack(fill="both", expand=True)

    def _show_results(outputs, gray_arr):
        from PIL import ImageTk
        import cv2
        import numpy as np
        _clear_results()
        close_preview()

        # store result metadata for preview adjustments
        state["results_meta"] = []

        grid = tk.Frame(results_frame, bg=BG_CARD)
        grid.pack(fill="both", expand=True, padx=8, pady=8)
        for col in range(3):
            grid.grid_columnconfigure(col, weight=1)
            
        first_image = True

        for index, (img_array, title) in enumerate(outputs):
            row, col = divmod(index, 3)
            cell = tk.Frame(grid, bg=BG_CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            cell.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(cell, text=title,
                    font=("Helvetica", 10, "bold"),
                    bg=BG_CARD, fg=TEXT_WHITE).pack(pady=(8, 2))

            pil_img = _to_pil(img_array)
            if pil_img is None:
                continue

            pil_full = [pil_img.copy()]  # mutable so slider can update it
            state["results_meta"].append({"array": img_array, "pil_full": pil_full, "title": title})
            if first_image:
                first_image = False

            is_original  = index == 0
            is_grayscale = index == 1
            is_bw        = index == 2
            is_median    = index == 3
            is_laplacian = index == 4

            if is_original:
                thumb = _make_thumbnail(pil_img, w=THUMB_W+80, h=THUMB_H+60)
            else:
                thumb = _make_thumbnail(pil_img)
            photo_ref = [ImageTk.PhotoImage(thumb)]
            state["photo_refs"].append(photo_ref[0])

            img_lbl = tk.Label(cell, image=photo_ref[0], bg=BG_CARD, cursor="hand2")
            img_lbl.pack(padx=8, pady=(0, 2))

            is_original  = index == 0
            is_grayscale = index == 1
            is_bw        = index == 2
            is_median    = index == 3
            is_laplacian = index == 4

            # ── Per-image threshold slider (skip Original) ────────────────────
            if not is_original:
                slider_label_row = tk.Frame(cell, bg=BG_CARD)
                slider_label_row.pack(fill="x", padx=8)

                if is_median:
                    slider_text = "Blur Kernel"
                elif is_grayscale:
                    slider_text = "Clip Level"
                elif is_bw:
                    slider_text = "Threshold"
                elif is_laplacian:
                    slider_text = "Sensitivity"
                else:
                    slider_text = "Threshold"

                tk.Label(slider_label_row, text=slider_text,
                        font=("Helvetica", 7), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")

                val_lbl = tk.Label(slider_label_row, text="127" if not is_median else "5",
                                font=("Helvetica", 7, "bold"), bg=BG_CARD, fg="#38BDF8")
                val_lbl.pack(side="right")

                if is_median:
                    # Kernel size must be odd: 1,3,5,...,21
                    slider_var = tk.IntVar(value=5)
                    from_val, to_val = 1, 11  # maps to 1,3,5,...,21 via *2-1
                else:
                    slider_var = tk.IntVar(value=127)
                    from_val, to_val = 0, 255

                def _make_callback(i=index, lbl=val_lbl, var=slider_var,
                                img_lbl=img_lbl, pil_full=pil_full,
                                photo_ref=photo_ref):
                    def _on_slide(val):
                        v = int(float(val))

                        if i == 1:  # Grayscale clip
                            lbl.config(text=str(v))
                            result = np.where(gray_arr < v, 0, gray_arr).astype(np.uint8)
                            new_pil = _to_pil(result)

                        elif i == 2:  # B&W threshold
                            lbl.config(text=str(v))
                            _, bw_new = cv2.threshold(gray_arr, v, 255, cv2.THRESH_BINARY)
                            new_pil = _to_pil(bw_new)

                        elif i == 3:  # Median blur — kernel = v*2-1 (odd)
                            kernel = max(1, v * 2 - 1)
                            lbl.config(text=str(kernel))
                            blurred = cv2.medianBlur(gray_arr, kernel)
                            new_pil = _to_pil(blurred)

                        elif i == 4:  # Laplacian sensitivity
                            lbl.config(text=str(v))
                            lap = cv2.Laplacian(gray_arr, cv2.CV_64F)
                            lap = np.uint8(np.absolute(lap))
                            lap = np.where(lap < v, 0, lap).astype(np.uint8)
                            new_pil = _to_pil(lap)

                        else:
                            return

                        if new_pil:
                            pil_full[0] = new_pil.copy()
                            thumb_new = _make_thumbnail(new_pil)
                            photo_new = ImageTk.PhotoImage(thumb_new)
                            photo_ref[0] = photo_new
                            state["photo_refs"].append(photo_new)
                            img_lbl.config(image=photo_new)

                    return _on_slide

                slider_border = tk.Frame(
                    cell,
                    bg=BORDER,
                    highlightthickness=1,
                    highlightbackground=BORDER
                )
                slider_border.pack(fill="x", padx=8, pady=(0, 4))

                tk.Scale(
                    slider_border,
                    from_=from_val,
                    to=to_val,
                    orient="horizontal",
                    variable=slider_var,
                    command=_make_callback(),
                    bg=BG_CARD,
                    fg=TEXT_WHITE,
                    troughcolor="#2B3445",
                    highlightthickness=0,
                    bd=0,
                    sliderrelief="flat",
                    activebackground="#38BDF8",
                    showvalue=False,
                ).pack(fill="x", padx=4, pady=4)

            # ── Enlarge hint ──────────────────────────────────────────────────
            hint = "🔍 Click to preview"
            tk.Label(cell, text=hint,
                    font=("Helvetica", 7), bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(0, 8))

            # Per-result Save button (rectangular) — skip for original
            if not is_original:
                try:
                    save_btn = create_action_button(cell, "Save Image", lambda pf=pil_full: _save_pil_image_dialog(pf[0]))
                    try:
                        save_btn.configure(width=10)
                        save_btn.configure(height=1)
                    except Exception:
                        pass
                    save_btn.pack(pady=(0, 4))
                except Exception:
                    # Fallback to a simple button if styled builder fails
                    tk.Button(cell, text="Save Image", width=10, height=1, command=lambda pf=pil_full: _save_pil_image_dialog(pf[0])).pack(pady=(0, 4))

            def _select_image(event, pf=pil_full, idx=index):
                state["selected_index"] = idx
                state["selected_pil"] = pf[0]
                zoom_var.set(100)
                # Show preview first so canvas has proper size for centering
                show_preview_view()
                preview_canvas.update_idletasks()
                _build_preview_slider()
                update_preview()

            img_lbl.bind("<Button-1>", _select_image)

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

        # Use a default threshold for generating the B&W output; preview has per-image sliders
        threshold_val = 127

        try:
            gray      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, bw     = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY)
            median    = cv2.medianBlur(gray, 5)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian = np.uint8(np.absolute(laplacian))

            state["gray_array"] = gray  # store for popup live-slider

            _show_results([
                (image,     "Original"),
                (gray,      "Grayscale"),
                (bw,        "Black & White"),
                (median,    "Median Blurred"),
                (laplacian, "Laplacian Edge Detection"),
            ], gray)
            status_label.config(
                text=f"Done — 5 versions shown.  Threshold: {threshold_val}",
                fg="#00E676",
            )
            return True

        except Exception as exc:
            messagebox.showerror("Processing Error", f"Could not process the image:\n\n{exc}")
            status_label.config(text="Processing failed.", fg="#FF5C5C")
            return False

    def on_file_selected(path):
        try:
            image = _load_image_bgr(path)
            if image is None:
                messagebox.showerror("Invalid Input", "Could not read the image.\nTry PNG or JPG.")
                state["image_bgr"] = None
                status_label.config(text="Failed to load image.", fg="#FF5C5C")
                return

            state["image_bgr"]  = image
            state["gray_array"] = None
            name = path.replace("\\", "/").split("/")[-1]
            status_label.config(
                text=f"Loaded: {name} — click Apply Filters to process.",
                fg="#38BDF8",
            )
            _show_placeholder()

        except Exception as exc:
            messagebox.showerror("Error", f"Something went wrong:\n\n{exc}")
            status_label.config(text="Error loading image.", fg="#FF5C5C")

    file_row2, path_var2, _browse2 = create_file_picker(
        section, "Image File", IMAGE_FILETYPES, command=on_file_selected,
    )
    file_row2.pack(fill="x", padx=14, pady=(0, 8))

    def process_image():
        path = path_var2.get()
        if state["image_bgr"] is None and path and path != "No file selected":
            img = _load_image_bgr(path)
            if img is not None:
                state["image_bgr"] = img
        _run_processing()

    def reset_lab():
        # Close any open preview and clear state
        try:
            close_preview()
        except Exception:
            pass

        path_var2.set("No file selected")
        state["image_bgr"]  = None
        state["gray_array"] = None
        state["selected_pil"] = None
        state["preview_photo"] = None
        try:
            preview_canvas.delete("IMG")
        except Exception:
            pass
        zoom_var.set(100)
        zoom_value_label.config(text="100%")
        state["results_meta"] = []
        state["selected_index"] = None
        status_label.config(text="No image loaded.", fg=TEXT_MUTED)
        show_results_view()
        _show_placeholder()

    btn_frame = tk.Frame(control_footer, bg=BG_CARD)
    btn_frame.pack(fill="both", expand=True)

    add_footer_button(btn_frame, "Apply Filters", process_image, padx=(0, 6))
    reset_btn = create_action_button(btn_frame, "Reset", reset_lab)
    reset_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

    _show_placeholder()
