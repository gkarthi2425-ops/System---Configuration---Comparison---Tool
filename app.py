import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import platform
import socket
import json
import os


# --------------------------------------------------
# GET SYSTEM INFORMATION
# --------------------------------------------------

def get_system_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    info = {
        "Computer Name": socket.gethostname(),
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "Total RAM": f"{round(memory.total / (1024 ** 3), 2)} GB",
        "Used RAM": f"{round(memory.used / (1024 ** 3), 2)} GB",
        "RAM Usage": f"{memory.percent}%",
        "Total Disk": f"{round(disk.total / (1024 ** 3), 2)} GB",
        "Used Disk": f"{round(disk.used / (1024 ** 3), 2)} GB",
        "Disk Usage": f"{disk.percent}%",
        "Python Version": platform.python_version()
    }

    return info


# --------------------------------------------------
# DISPLAY CURRENT SYSTEM INFORMATION
# --------------------------------------------------

def retrieve_system():
    global current_system

    current_system = get_system_info()

    for item in table.get_children():
        table.delete(item)

    for key, value in current_system.items():
        table.insert("", tk.END, values=(key, value))

    status_label.config(text="System information retrieved successfully.")


# --------------------------------------------------
# SAVE SYSTEM CONFIGURATION
# --------------------------------------------------

def save_configuration():
    if not current_system:
        messagebox.showwarning(
            "Warning",
            "Please retrieve system information first."
        )
        return

    try:
        with open("system_config.json", "w") as file:
            json.dump(current_system, file, indent=4)

        status_label.config(text="Configuration saved successfully.")

        messagebox.showinfo(
            "Saved",
            "System configuration saved as system_config.json"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------------------------------------------
# LOAD SAVED CONFIGURATION
# --------------------------------------------------

def load_configuration():
    global saved_system

    if not os.path.exists("system_config.json"):
        messagebox.showwarning(
            "Warning",
            "No saved configuration found."
        )
        return

    try:
        with open("system_config.json", "r") as file:
            saved_system = json.load(file)

        status_label.config(
            text="Saved configuration loaded successfully."
        )

        messagebox.showinfo(
            "Loaded",
            "Saved system configuration loaded."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------------------------------------------
# COMPARE SYSTEMS
# --------------------------------------------------

def compare_systems():

    if not current_system:
        messagebox.showwarning(
            "Warning",
            "Please retrieve the current system information."
        )
        return

    if not saved_system:
        messagebox.showwarning(
            "Warning",
            "Please load a saved configuration first."
        )
        return

    comparison_window = tk.Toplevel(root)

    comparison_window.title(
        "System Configuration Comparison"
    )

    comparison_window.geometry("900x600")

    title = tk.Label(
        comparison_window,
        text="System Configuration Comparison",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=15)

    columns = (
        "Parameter",
        "Saved System",
        "Current System",
        "Status"
    )

    comparison_table = ttk.Treeview(
        comparison_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        comparison_table.heading(
            column,
            text=column
        )

    comparison_table.column(
        "Parameter",
        width=180
    )

    comparison_table.column(
        "Saved System",
        width=220
    )

    comparison_table.column(
        "Current System",
        width=220
    )

    comparison_table.column(
        "Status",
        width=120
    )

    comparison_table.pack(
        fill=tk.BOTH,
        expand=True,
        padx=20,
        pady=10
    )

    # Compare every parameter
    all_keys = set(saved_system.keys()) | set(current_system.keys())

    for key in sorted(all_keys):

        saved_value = saved_system.get(
            key,
            "Not Available"
        )

        current_value = current_system.get(
            key,
            "Not Available"
        )

        if saved_value == current_value:
            status = "Same"
        else:
            status = "Different"

        comparison_table.insert(
            "",
            tk.END,
            values=(
                key,
                saved_value,
                current_value,
                status
            )
        )


# --------------------------------------------------
# CLEAR DATA
# --------------------------------------------------

def clear_data():

    global current_system
    global saved_system

    current_system = {}
    saved_system = {}

    for item in table.get_children():
        table.delete(item)

    status_label.config(
        text="Data cleared."
    )


# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()

root.title(
    "System Configuration Comparison Tool"
)

root.geometry("850x650")

root.resizable(True, True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

title_label = tk.Label(
    root,
    text="System Configuration Comparison Tool",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


subtitle_label = tk.Label(
    root,
    text="Retrieve, save and compare computer system configurations",
    font=("Arial", 11)
)

subtitle_label.pack(pady=5)


# --------------------------------------------------
# BUTTON FRAME
# --------------------------------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


retrieve_button = tk.Button(
    button_frame,
    text="Retrieve System",
    command=retrieve_system,
    width=18
)

retrieve_button.grid(
    row=0,
    column=0,
    padx=5
)


save_button = tk.Button(
    button_frame,
    text="Save Configuration",
    command=save_configuration,
    width=18
)

save_button.grid(
    row=0,
    column=1,
    padx=5
)


load_button = tk.Button(
    button_frame,
    text="Load Configuration",
    command=load_configuration,
    width=18
)

load_button.grid(
    row=0,
    column=2,
    padx=5
)


compare_button = tk.Button(
    button_frame,
    text="Compare Systems",
    command=compare_systems,
    width=18
)

compare_button.grid(
    row=0,
    column=3,
    padx=5
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_data,
    width=18
)

clear_button.grid(
    row=1,
    column=1,
    columnspan=2,
    pady=10
)


# --------------------------------------------------
# SYSTEM INFORMATION TABLE
# --------------------------------------------------

table_frame = tk.Frame(root)

table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=25,
    pady=10
)


columns = (
    "Parameter",
    "Value"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


table.heading(
    "Parameter",
    text="Parameter"
)

table.heading(
    "Value",
    text="Value"
)


table.column(
    "Parameter",
    width=250
)

table.column(
    "Value",
    width=500
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(
    yscrollcommand=scrollbar.set
)


table.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


# --------------------------------------------------
# STATUS
# --------------------------------------------------

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 10)
)

status_label.pack(
    pady=10
)


# --------------------------------------------------
# GLOBAL VARIABLES
# --------------------------------------------------

current_system = {}

saved_system = {}


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

root.mainloop()