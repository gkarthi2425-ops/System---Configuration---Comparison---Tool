import tkinter as tk
from tkinter import ttk, messagebox
import platform
import psutil


def get_system_configuration():
    """Retrieve configuration information from the current computer."""

    memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)

    try:
        disk = psutil.disk_usage("/")
        storage_gb = round(disk.total / (1024 ** 3), 2)
    except:
        storage_gb = "N/A"

    return {
        "Operating System": platform.system() + " " + platform.release(),
        "Processor": platform.processor(),
        "RAM": f"{memory_gb} GB",
        "Storage": f"{storage_gb} GB",
        "Architecture": platform.machine()
    }


def capture_system_a():
    """Display the current computer configuration in System A."""

    config = get_system_configuration()

    for key in fields:
        system_a_entries[key].delete(0, tk.END)
        system_a_entries[key].insert(0, config[key])

    status_label.config(text="System A configuration captured successfully.")


def compare_systems():
    """Compare System A and System B configurations."""

    result_text.delete("1.0", tk.END)

    differences = 0

    result_text.insert(tk.END, "SYSTEM CONFIGURATION COMPARISON\n")
    result_text.insert(tk.END, "=" * 55 + "\n\n")

    for key in fields:

        value_a = system_a_entries[key].get().strip()
        value_b = system_b_entries[key].get().strip()

        if value_a.lower() == value_b.lower():
            result = "SAME"
        else:
            result = "DIFFERENT"
            differences += 1

        result_text.insert(
            tk.END,
            f"{key:<20} : {result}\n"
        )

        if result == "DIFFERENT":
            result_text.insert(
                tk.END,
                f"    System A: {value_a}\n"
            )
            result_text.insert(
                tk.END,
                f"    System B: {value_b}\n"
            )

        result_text.insert(tk.END, "\n")

    result_text.insert(tk.END, "-" * 55 + "\n")

    if differences == 0:
        result_text.insert(
            tk.END,
            "Result: Both systems have matching configurations."
        )
    else:
        result_text.insert(
            tk.END,
            f"Result: {differences} configuration parameter(s) differ."
        )


def clear_fields():
    """Clear all configuration fields and results."""

    for key in fields:
        system_a_entries[key].delete(0, tk.END)
        system_b_entries[key].delete(0, tk.END)

    result_text.delete("1.0", tk.END)
    status_label.config(text="Fields cleared.")


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()
root.title("System Configuration Comparison Tool")
root.geometry("1000x700")
root.minsize(900, 650)

# Title
title = tk.Label(
    root,
    text="System Configuration Comparison Tool",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Retrieve and compare computer system configurations",
    font=("Arial", 11)
)
subtitle.pack(pady=(0, 15))


# Fields to compare
fields = [
    "Operating System",
    "Processor",
    "RAM",
    "Storage",
    "Architecture"
]


# Main configuration frame
config_frame = tk.Frame(root)
config_frame.pack(padx=20, fill="x")


# System A
system_a_frame = tk.LabelFrame(
    config_frame,
    text="System A",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
system_a_frame.grid(row=0, column=0, padx=10, sticky="nsew")


# System B
system_b_frame = tk.LabelFrame(
    config_frame,
    text="System B",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
system_b_frame.grid(row=0, column=1, padx=10, sticky="nsew")


config_frame.columnconfigure(0, weight=1)
config_frame.columnconfigure(1, weight=1)


system_a_entries = {}
system_b_entries = {}


for row, field in enumerate(fields):

    tk.Label(
        system_a_frame,
        text=field,
        font=("Arial", 10)
    ).grid(row=row, column=0, padx=5, pady=8, sticky="w")

    entry_a = tk.Entry(
        system_a_frame,
        width=35
    )
    entry_a.grid(row=row, column=1, padx=5, pady=8)

    system_a_entries[field] = entry_a


    tk.Label(
        system_b_frame,
        text=field,
        font=("Arial", 10)
    ).grid(row=row, column=0, padx=5, pady=8, sticky="w")

    entry_b = tk.Entry(
        system_b_frame,
        width=35
    )
    entry_b.grid(row=row, column=1, padx=5, pady=8)

    system_b_entries[field] = entry_b


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)


capture_button = tk.Button(
    button_frame,
    text="Capture My System",
    command=capture_system_a,
    width=20
)
capture_button.grid(row=0, column=0, padx=10)


compare_button = tk.Button(
    button_frame,
    text="Compare Systems",
    command=compare_systems,
    width=20
)
compare_button.grid(row=0, column=1, padx=10)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=15
)
clear_button.grid(row=0, column=2, padx=10)


# Status
status_label = tk.Label(
    root,
    text="Click 'Capture My System' to retrieve your configuration.",
    font=("Arial", 10)
)
status_label.pack(pady=5)


# Results
result_frame = tk.LabelFrame(
    root,
    text="Comparison Result",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
result_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)


result_text = tk.Text(
    result_frame,
    height=12,
    font=("Consolas", 10)
)
result_text.pack(
    fill="both",
    expand=True
)


# Start application
root.mainloop()