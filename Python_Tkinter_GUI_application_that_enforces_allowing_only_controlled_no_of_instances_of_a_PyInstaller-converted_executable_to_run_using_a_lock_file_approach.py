import os
import sys
import tkinter as tk
from tkinter import messagebox

MAX_INSTANCES = 4  # Maximum number of allowed instances

root = tk.Tk()

def check_lock_file():
    lock_file = "app.lock"
    if os.path.isfile(lock_file):
        with open(lock_file, "r") as f:
            instance_count = int(f.read())
            if instance_count >= MAX_INSTANCES:
                messagebox.showinfo("Info", "Maximum instances reached.")
                sys.exit(0)
            else:
                with open(lock_file, "w") as f:
                    f.write(str(instance_count + 1))
    else:
        with open(lock_file, "w") as f:
            f.write("1")

def decrement_instance_count():
    lock_file = "app.lock"
    if os.path.isfile(lock_file):
        with open(lock_file, "r+") as f:
            instance_count = int(f.read())
            if instance_count > 0:
                f.seek(0)
                f.write(str(instance_count - 1))
                f.truncate()

def on_exit():
    decrement_instance_count()
    root.destroy()


if __name__ == "__main__":
    check_lock_file()

    root.title("Multiple Instance App")

    label = tk.Label(root, text="Application is running...")
    label.pack(padx=20, pady=20)

    button_exit = tk.Button(root, text="Exit", command=on_exit)
    button_exit.pack(padx=20, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_exit)

    root.mainloop()
