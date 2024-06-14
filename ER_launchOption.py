import tkinter as tk
from tkinter import messagebox
import os
import subprocess

def run_executable(executable_path):
    try:
        if os.path.isfile(executable_path):
            subprocess.run([executable_path], check=True)
        else:
            messagebox.showerror("Error", f"File not found: {executable_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    root = tk.Tk()
    root.title("Elden Launcher")

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    normal_button = tk.Button(frame, text="Normal", command=lambda: run_executable("C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"))
    normal_button.grid(row=0, column=0, padx=10, pady=10)

    no_eac_button = tk.Button(frame, text="No EAC", command=lambda: subprocess.run(["C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\EldenRingOfflineLauncher.exe"], cwd="C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"))
    no_eac_button.grid(row=0, column=1, padx=10, pady=10)

    seamless_coop_button = tk.Button(frame, text="Seamless Coop", command=lambda: subprocess.run(["C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\launch_elden_ring_seamlesscoop.exe"], cwd="C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"))
    seamless_coop_button.grid(row=1, column=0, padx=10, pady=10)

    file_manager_button = tk.Button(frame, text="File Manager", command=lambda: subprocess.run(["C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\save\EldenRing-Save-Manager\SaveManager.exe"], cwd="C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\save\EldenRing-Save-Manager"))
    file_manager_button.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()
    

if __name__ == "__main__":
    create_gui()
