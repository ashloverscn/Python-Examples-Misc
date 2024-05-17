import os
import sys
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()

def check_lock_file():
    lock_file = "app.lock"
    if os.path.isfile(lock_file):
        messagebox.showinfo("Info", "Another instance is already running.")
        sys.exit(0)
    else:
        with open(lock_file, "w") as f:
            f.write("Lock file created.")

def delete_lock_file():
    lock_file = "app.lock"
    if os.path.isfile(lock_file):
        os.remove(lock_file)

def on_exit():
    delete_lock_file()
    window.destroy()

if __name__ == "__main__":
    check_lock_file()

    window.title("Single Instance App")

    label = tk.Label(window, text="Application is running...")
    label.pack(padx=20, pady=20)

    button_exit = tk.Button(window, text="Exit", command=on_exit)
    button_exit.pack(padx=20, pady=10)

    window.protocol("WM_DELETE_WINDOW", on_exit)  # Handle window close event

    window.mainloop()
