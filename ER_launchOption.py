import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import json

CONFIG_FILE = "config.json"
INITIAL_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING"
DEFAULT_MAX_ADDITIONAL_CATEGORIES = 4

def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "max_additional_categories": DEFAULT_MAX_ADDITIONAL_CATEGORIES,
            "Normal": {"path": "C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe", "cwd": "C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"},
            "No EAC": {"path": "File to execute", "cwd": "Containing Folder of the File"},
            "Seamless Coop": {"path": "File to execute", "cwd": "Containing Folder of the File"},
            "File Manager": {"path": "File to execute", "cwd": "Containing Folder of the File"},
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def run_executable(config, key):
    executable_path = config[key]["path"]
    working_directory = config[key]["cwd"]
    try:
        if os.path.isfile(executable_path):
            subprocess.run([executable_path], cwd=working_directory, check=True)
        else:
            messagebox.showerror("Error", f"File not found: {executable_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_executable(config, key, path_var, cwd_var):
    path = filedialog.askopenfilename(initialdir=INITIAL_DIR, filetypes=[("Executable files", "*.exe")])
    if path:
        config[key]["path"] = path
        path_var.set(path)
        save_config(config)

    cwd = filedialog.askdirectory(initialdir=INITIAL_DIR)
    if cwd:
        config[key]["cwd"] = cwd
        cwd_var.set(cwd)
        save_config(config)

def add_category(config, frame):
    max_additional_categories = config.get("max_additional_categories", DEFAULT_MAX_ADDITIONAL_CATEGORIES)
    if len(config) - 5 >= max_additional_categories:
        messagebox.showerror("Error", "Maximum number of additional categories reached")
        return

    def confirm(event=None):
        name = entry.get()
        if name and name not in config:
            if len(config) - 5 < max_additional_categories:
                config[name] = {"path": "", "cwd": ""}
                create_category(frame, config, name, deletable=True)
                save_config(config)
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Maximum number of additional categories reached")
        elif name in config:
            messagebox.showerror("Error", "Category name already exists")

    add_window = tk.Toplevel()
    add_window.title("Add Category")
    add_window.resizable(False, False)
    tk.Label(add_window, text="Category Name:").pack(pady=10)
    entry = tk.Entry(add_window)
    entry.pack(pady=10)
    entry.focus_set()
    entry.bind("<Return>", confirm)
    tk.Button(add_window, text="Confirm", command=confirm).pack(pady=10)

def create_category(frame, config, key, deletable=False):
    path_var = tk.StringVar(value=config[key]["path"])
    cwd_var = tk.StringVar(value=config[key]["cwd"])

    row = len(frame.grid_slaves()) // 4 * 2

    tk.Button(frame, text=key, command=lambda k=key: run_executable(config, k)).grid(row=row, column=0, padx=10, pady=(20, 10))
    tk.Button(frame, text="...", command=lambda k=key, pv=path_var, cv=cwd_var: select_executable(config, k, pv, cv)).grid(row=row, column=1, padx=10, pady=(20, 10))
    tk.Entry(frame, textvariable=path_var, width=80).grid(row=row, column=2, padx=10, pady=(20, 10))
    tk.Entry(frame, textvariable=cwd_var, width=80).grid(row=row+1, column=2, padx=10, pady=(10, 20))
    
    if deletable:
        tk.Button(frame, text="🗑️", command=lambda k=key: remove_category(frame, config, k)).grid(row=row, column=3, padx=10, pady=(20, 10))

def remove_category(frame, config, key):
    del config[key]
    save_config(config)
    for widget in frame.grid_slaves():
        widget.grid_forget()
    for idx, k in enumerate(config):
        if k != "max_additional_categories":
            create_category(frame, config, k, deletable=k not in ["Normal", "No EAC", "Seamless Coop", "File Manager"])

def create_gui():
    config = load_config()
    
    root = tk.Tk()
    root.title("Elden Ring Launch Optioner")
    root.resizable(False, False)
    root.attributes("-fullscreen", False)

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    for key in ["Normal", "No EAC", "Seamless Coop", "File Manager"]:
        if key in config:
            create_category(frame, config, key, deletable=False)
        else:
            config[key] = {"path": "File to execute", "cwd": "Containing Folder of the File"}
            create_category(frame, config, key, deletable=False)

    for key in config:
        if key not in ["Normal", "No EAC", "Seamless Coop", "File Manager", "max_additional_categories"]:
            create_category(frame, config, key, deletable=True)

    tk.Button(root, text="Add more", command=lambda: add_category(config, frame)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
