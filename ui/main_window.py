import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Scrollbar, ttk
from PIL import ImageTk, Image
import threading
import os
import shutil

from config import *
from core.feature_extractor import FeatureExtractor
from core.index_manager import IndexManager
from core.search_engine import SearchEngine
from utils.file_utils import *
from utils.ui_utils import *

class ImageSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Similar Image Search V1.0  Designed By Li Zhe | NTU FYP")
        self.geometry("1000x700")

        self.extractor = FeatureExtractor()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.query_path = None
        self.search_dir = None
        self.include_subfolders = tk.BooleanVar(value=True)
        self.include_subfolders.trace_add("write", self.on_subfolder_changed)
        self.images_per_row = tk.IntVar(value=8)
        self.min_similarity = tk.IntVar(value=DEFAULT_MIN_SIM)
        self.tk_images = []
        self.items = []
        self.checked = []
        self.disabled = set()
        self.total_result = 0

        self.click_timer = None
        self.click_delay = CLICK_DELAY

        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)

        self.row1 = tk.Frame(self, padx=10, pady=5)
        self.row1.pack(fill=tk.X)
        tk.Label(self.row1, text="Similarity ≥", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=2)
        self.min_sim_entry = ttk.Entry(self.row1, width=5)
        self.min_sim_entry.insert(0, str(DEFAULT_MIN_SIM))
        self.min_sim_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(self.row1, text="%", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Label(self.row1, text="  |  Images per row:", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        self.column_spinbox = ttk.Spinbox(self.row1, from_=2, to=20, textvariable=self.images_per_row, width=5)
        self.column_spinbox.pack(side=tk.LEFT, padx=5)

        self.row2 = tk.Frame(self, padx=10, pady=5)
        self.row2.pack(fill=tk.X)
        self.select_query_btn = tk.Button(self.row2, text="Select Query Image", command=self.select_query_image, font=("Arial", 10, "bold"), bg="#e0e0e0")
        self.select_query_btn.pack(side=tk.LEFT)
        self.query_path_label = tk.Label(self.row2, text="No query image", font=("Arial", 9), fg="gray")
        self.query_path_label.pack(side=tk.LEFT, padx=10)

        self.row3 = tk.Frame(self, padx=10, pady=5)
        self.row3.pack(fill=tk.X)
        self.select_dir_btn = tk.Button(self.row3, text="Select Search Folder", command=self.select_search_dir, font=("Arial", 10, "bold"), bg="#e0e0e0")
        self.select_dir_btn.pack(side=tk.LEFT)
        self.dir_path_label = tk.Label(self.row3, text="No folder selected", font=("Arial", 9), fg="gray")
        self.dir_path_label.pack(side=tk.LEFT, padx=10)

        self.row4 = tk.Frame(self, padx=10, pady=5)
        self.row4.pack(fill=tk.X)
        self.subfolder_check = tk.Checkbutton(self.row4, text="Include subfolders", variable=self.include_subfolders, font=("Arial", 10))
        self.subfolder_check.pack(side=tk.LEFT, padx=5)
        self.build_index_btn = tk.Button(self.row4, text="Build Index", command=self.start_build_index, font=("Arial", 10, "bold"), bg="#ffdd55", fg="black", padx=10)
        self.build_index_btn.pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(self.row4, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.progress_label = tk.Label(self.row4, text="Ready to build index", font=("Arial", 9))
        self.progress_label.pack(side=tk.LEFT)

        self.row5 = tk.Frame(self, padx=10, pady=5)
        self.row5.pack(fill=tk.X)
        self.search_btn = tk.Button(self.row5, text="Start Search", command=self.run_search, font=("Arial", 10, "bold"), bg="#55aa55", fg="white", padx=10, state=tk.DISABLED)
        self.search_btn.pack(side=tk.RIGHT)

        self.preview_frame = tk.Frame(self, padx=10, pady=5)
        self.preview_frame.pack(fill=tk.X)
        self.preview_label = tk.Label(self.preview_frame, text="Query Preview", font=("Arial", 10, "bold"))
        self.preview_label.pack()
        self.query_img_label = tk.Label(self.preview_frame)
        self.query_img_label.pack(pady=5)

        self.result_parent = tk.Frame(self, padx=10, pady=5)
        self.result_parent.pack(fill=tk.BOTH, expand=True)
        self.result_count_label = tk.Label(self.result_parent, text="Results (Double-click to open, Single-click to select)", font=("Arial", 10, "bold"))
        self.result_count_label.pack(fill=tk.X)

        self.btn_frame = tk.Frame(self.result_parent, padx=10, pady=5)
        self.btn_frame.pack(fill=tk.X, pady=(0, 5))
        self.btn_inner_frame = tk.Frame(self.btn_frame)
        self.btn_inner_frame.pack(anchor='center')

        self.copy_btn = tk.Button(self.btn_inner_frame, text="Copy Selected", command=self.copy_selected, bg="#2196F3", fg="white", font=("Arial",10,"bold"))
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        self.move_btn = tk.Button(self.btn_inner_frame, text="Move Selected", command=self.move_selected, bg="#FF9800", fg="white", font=("Arial",10,"bold"))
        self.move_btn.pack(side=tk.LEFT, padx=5)
        self.del_btn = tk.Button(self.btn_inner_frame, text="Delete Selected", command=self.delete_selected, bg="#F44336", fg="white", font=("Arial",10,"bold"))
        self.del_btn.pack(side=tk.LEFT, padx=5)
        self.select_all_btn = tk.Button(self.btn_inner_frame, text="Select All", command=self.select_all, font=("Arial",10))
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        self.clear_all_btn = tk.Button(self.btn_inner_frame, text="Deselect All", command=self.clear_all, font=("Arial",10))
        self.clear_all_btn.pack(side=tk.LEFT, padx=5)
        self.clear_result_btn = tk.Button(self.btn_inner_frame, text="Clear Results", command=self.clear_search_results, font=("Arial",10), bg="#9E9E9E", fg="white")
        self.clear_result_btn.pack(side=tk.LEFT, padx=5)

        self.select_count_label = tk.Label(self.btn_frame, text="Selected: 0 / 0", font=("Arial", 10, "bold"), fg="#2196F3")
        self.select_count_label.pack(pady=(5, 0))

        self.scroll_container = tk.Frame(self.result_parent)
        self.scroll_container.pack(fill=tk.BOTH, expand=True)
        self.canvas = Canvas(self.scroll_container, bg="white")
        self.v_scroll = Scrollbar(self.scroll_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = Scrollbar(self.scroll_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_select_count(self):
        total = self.total_result
        selected = sum(self.checked)
        self.select_count_label.config(text=f"Selected: {selected} / {total}")

    def toggle_check(self, idx):
        if idx == 0:
            return
        if idx < len(self.checked) and idx not in self.disabled:
            self.checked[idx] = not self.checked[idx]
            self.redraw_item(idx)
            self.update_select_count()

    def redraw_item(self, idx):
        if idx >= len(self.items):
            return
        sim, path, x, y, img_w, img_h, item_h = self.items[idx]
        bg = "#e6f7ff" if self.checked[idx] else "white"
        self.canvas.create_rectangle(x-2, y-2, x+img_w+2, y+img_h+2, fill=bg, outline="")
        if idx in self.disabled:
            self.canvas.create_rectangle(x, y, x+img_w, y+img_h, fill="#f0f0f0", stipple="gray50", outline="")
            color = "#999999"
            bd = 1
        else:
            color = "black"
            bd = 3 if self.checked[idx] else 1

        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail((img_w, img_h), Image.Resampling.LANCZOS)
            if idx in self.disabled:
                img = img.convert("L")
            tk_img = ImageTk.PhotoImage(img)
            self.tk_images[idx] = tk_img
            self.canvas.create_image(x + img_w//2, y + img_h//2, image=tk_img)
        except:
            pass

        if idx == 0:
            self.canvas.create_rectangle(x, y, x+img_w, y+img_h, outline="#4CAF50", width=4)
        else:
            self.canvas.create_rectangle(x, y, x+img_w, y+img_h, outline="#2196F3" if self.checked[idx] else "#cccccc", width=bd)

        filename = os.path.basename(path)
        display_name = wrap_filename_with_ellipsis(filename, MAX_NAME_LENGTH_PER_LINE, MAX_NAME_LINES)
        if idx == 0:
            text = display_name
        else:
            text = f"[{idx}] {display_name}\nSim: {sim:.2f}%"
        self.canvas.create_text(x + img_w//2, y + img_h + 8, text=text, font=("Arial",9), width=img_w, anchor=tk.N, fill=color)

    def select_all(self):
        for i in range(1, len(self.checked)):
            if i not in self.disabled:
                self.checked[i] = True
                self.redraw_item(i)
        self.update_select_count()

    def clear_all(self):
        for i in range(1, len(self.checked)):
            self.checked[i] = False
            self.redraw_item(i)
        self.update_select_count()

    def copy_selected(self):
        selected = [i for i in range(len(self.checked)) if self.checked[i] and i not in self.disabled]
        if not selected:
            messagebox.showwarning("Warning", "No images selected")
            return
        target = filedialog.askdirectory(title="Select destination folder")
        if not target:
            return
        count = 0
        for i in selected:
            src = self.items[i][1]
            if not os.path.exists(src):
                continue
            fname = os.path.basename(src)
            dst = get_safe_path(target, fname)
            shutil.copy2(src, dst)
            count += 1
        messagebox.showinfo("Complete", f"Copied {count} images")

    def move_selected(self):
        selected = [i for i in range(len(self.checked)) if self.checked[i] and i not in self.disabled]
        if not selected:
            messagebox.showwarning("Warning", "No images selected")
            return
        target = filedialog.askdirectory(title="Select destination folder")
        if not target:
            return
        count = 0
        for i in selected:
            src = self.items[i][1]
            if not os.path.exists(src):
                continue
            fname = os.path.basename(src)
            dst = get_safe_path(target, fname)
            shutil.move(src, dst)
            self.disabled.add(i)
            self.checked[i] = False
            count += 1
        self.redraw_all()
        self.update_select_count()
        messagebox.showinfo("Complete", f"Moved {count} images")

    def delete_selected(self):
        selected = [i for i in range(len(self.checked)) if self.checked[i] and i not in self.disabled]
        if not selected:
            messagebox.showwarning("Warning", "No images selected")
            return
        n = len(selected)
        if not messagebox.askyesno("Confirm", f"Move {n} items to Recycle Bin?"):
            return
        count = 0
        for i in selected:
            try:
                path = self.items[i][1]
                path = os.path.normpath(path)
                if not os.path.exists(path):
                    continue
                send2trash(path)
                self.disabled.add(i)
                self.checked[i] = False
                count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed: {str(e)}")
        self.redraw_all()
        self.update_select_count()
        messagebox.showinfo("Complete", f"Moved {count} items to Recycle Bin")

    def redraw_all(self):
        for i in range(len(self.items)):
            self.redraw_item(i)

    def on_subfolder_changed(self, *args):
        self.search_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Settings changed, rebuild index")

    def on_close(self):
        try:
            if os.path.exists(TEMP_FOLDER):
                shutil.rmtree(TEMP_FOLDER)
        except:
            pass
        self.destroy()

    def select_query_image(self):
        path = filedialog.askopenfilename(
            title="Select Query Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp;*.ppm;*.pgm")]
        )
        if path:
            self.query_path = path
            self.query_path_label.config(text=path)
            img = Image.open(path).convert("RGB")
            img.thumbnail((150, 150))
            tk_img = ImageTk.PhotoImage(img)
            self.query_img_label.config(image=tk_img)
            self.query_img_label.image = tk_img
            if os.path.exists(INDEX_FILE):
                self.search_btn.config(state=tk.NORMAL)

    def select_search_dir(self):
        path = filedialog.askdirectory(title="Select Folder to Search")
        if path:
            self.search_dir = path
            self.dir_path_label.config(text=path)

    def start_build_index(self):
        if not self.search_dir:
            messagebox.showwarning("Warning", "Select a folder first")
            return
        self.build_index_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.build_index, daemon=True).start()

    def build_index(self):
        files = get_image_files(self.search_dir, self.include_subfolders.get(), SUPPORTED_FORMATS)
        if not files:
            messagebox.showwarning("Warning", "No images found in folder")
            self.build_index_btn.config(state=tk.NORMAL)
            return
        feats = []
        valid_paths = []
        total = len(files)
        for i, f in enumerate(files):
            ft = self.extractor.extract(f)
            if ft is not None:
                feats.append(ft)
                valid_paths.append(f)
            progress = int((i+1)/total * 100)
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f"Building... {i+1}/{total}")
        if not feats:
            messagebox.showwarning("Warning", "No valid features extracted")
            self.build_index_btn.config(state=tk.NORMAL)
            return
        IndexManager.build_index(feats, INDEX_FILE, PATHS_FILE, valid_paths)
        self.progress_label.config(text=f"Index built: {len(valid_paths)} images")
        self.build_index_btn.config(state=tk.NORMAL)
        if self.query_path:
            self.search_btn.config(state=tk.NORMAL)

    def run_search(self):
        if not self.query_path or not os.path.exists(INDEX_FILE):
            messagebox.showwarning("Warning", "Select image and build index first")
            return
        self.tk_images.clear()
        self.canvas.delete("all")
        self.items = []
        self.checked = []
        self.disabled = set()
        try:
            min_sim = float(self.min_sim_entry.get())
            images_per_row = int(self.images_per_row.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers")
            return
        q_feat = self.extractor.extract(self.query_path)
        index, paths = IndexManager.load_index(INDEX_FILE, PATHS_FILE)
        results = SearchEngine.search(index, paths, q_feat, min_sim)
        self.total_result = len(results)
        self.result_count_label.config(text=f"Results: {len(results)} matches")
        self.update_select_count()
        if not results:
            self.canvas.create_text(500, 200, text=f"No matches ≥ {min_sim}%", font=("Arial", 12))
            return
        img_w = FIXED_IMAGE_SIZE
        img_h = FIXED_IMAGE_SIZE
        margin = 20
        text_margin = 12
        item_height = img_h + text_margin + 60
        all_items = [(100.0, self.query_path)] + results
        self.items = all_items
        self.checked = [False]*len(self.items)

        for i, (sim, path) in enumerate(all_items):
            row = i // images_per_row
            col = i % images_per_row
            x = margin + col * (img_w + margin)
            y = margin + row * item_height
            self.items[i] = (sim, path, x, y, img_w, img_h, item_height)
            self.tk_images.append(None)
            self.redraw_item(i)

        total_rows = (len(all_items) + images_per_row - 1) // images_per_row
        total_height = margin + total_rows * item_height + 20
        total_width = margin + images_per_row * (img_w + margin)
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

        def on_click(event):
            if self.click_timer is not None:
                self.after_cancel(self.click_timer)
                self.click_timer = None
            cx = self.canvas.canvasx(event.x)
            cy = self.canvas.canvasy(event.y)
            hit_idx = None
            for idx, (s, p, x, y, w, h, ih) in enumerate(self.items):
                if x <= cx <= x + w and y <= cy <= y + h:
                    hit_idx = idx
                    break
            if hit_idx is not None:
                self.click_timer = self.after(self.click_delay, lambda: self.toggle_check(hit_idx))

        def on_double_click(event):
            if self.click_timer is not None:
                self.after_cancel(self.click_timer)
                self.click_timer = None
            cx = self.canvas.canvasx(event.x)
            cy = self.canvas.canvasy(event.y)
            for idx, (s, p, x, y, w, h, ih) in enumerate(self.items):
                if x <= cx <= x + w and y <= cy <= y + h:
                    open_file_location(p)
                    return

        self.canvas.bind("<Button-1>", on_click)
        self.canvas.bind("<Double-Button-1>", on_double_click)

    def clear_search_results(self):
        self.canvas.delete("all")
        self.items = []
        self.checked = []
        self.tk_images = []
        self.disabled = set()
        self.total_result = 0
        self.result_count_label.config(text="Results (Double-click to open, Single-click to select)")
        self.update_select_count()
        messagebox.showinfo("Info", "Results cleared")