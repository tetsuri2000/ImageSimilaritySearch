import os
import glob
import shutil
import subprocess
from send2trash import send2trash
from tkinter import messagebox

def open_file_location(path):
    if not os.path.exists(path):
        messagebox.showwarning("Warning", f"File not found:\n{path}")
        return
    path = os.path.normpath(path)
    try:
        subprocess.run(['explorer.exe', '/select,', path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open location: {str(e)}")

def get_safe_path(target_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(target_dir, filename)
    while os.path.exists(new_path):
        new_path = os.path.join(target_dir, f"{base}({counter}){ext}")
        counter += 1
    return new_path

def get_image_files(folder, include_subfolders, formats):
    files = []
    if include_subfolders:
        for ext in formats:
            files.extend(glob.glob(os.path.join(folder, '**', ext), recursive=True))
    else:
        for ext in formats:
            files.extend(glob.glob(os.path.join(folder, ext)))
    return [f for f in files if os.path.isfile(f)]

def delete_to_bin(path):
    try:
        send2trash(path)
        return True
    except:
        return False