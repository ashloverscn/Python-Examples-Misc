#!/usr/bin/env python3

import tkinter as tk
import subprocess
import configparser
import os
import socket
import urllib.request
import threading
import time
import sys

# ---------------- CONFIG ----------------
PING_INTERVAL = 1.0
TTL_VALUE = 64
INI_FILE = "ping.ini"
COMMON_PORTS = [22, 80, 443, 3389, 53]

# Windows flag to suppress flashing command windows
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


# ---------------- LIVENESS CHECK ----------------
def check_alive(host):
    # ICMP Ping
    try:
        cmd = ["ping", "-c", "1", "-W", "1", "-t", str(TTL_VALUE), host] if sys.platform != "win32" \
              else ["ping", "-n", "1", "-w", "1000", host]
        if subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          creationflags=CREATE_NO_WINDOW).returncode == 0:
            return "green"
    except:
        pass

    # TCP probe
    for port in COMMON_PORTS:
        try:
            with socket.create_connection((host, port), timeout=1):
                return "yellow"
        except:
            pass

    # HTTP/HTTPS probe
    for proto in ("http", "https"):
        try:
            req = urllib.request.Request(f"{proto}://{host}", method="HEAD")
            urllib.request.urlopen(req, timeout=2)
            return "yellow"
        except:
            pass

    # ARP probe (Linux only)
    try:
        if sys.platform != "win32":
            result = subprocess.run(
                ["ip", "neigh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            if host in result.stdout:
                return "yellow"
    except:
        pass

    return "red"


def fast_ping(host):
    try:
        cmd = ["ping", "-c", "1", "-W", "1", host] if sys.platform != "win32" \
              else ["ping", "-n", "1", "-w", "1000", host]
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              creationflags=CREATE_NO_WINDOW).returncode == 0
    except:
        return False


# ---------------- ROW ----------------
class PingRow:
    def __init__(self, parent, host="", save_callback=None):
        self.parent = parent
        self.save_callback = save_callback
        self.running = False

        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.X, pady=3)

        # Host input
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.insert(0, host)
        self.entry.bind("<FocusOut>", lambda e: self.save_callback())

        # Indicator canvas
        self.canvas = tk.Canvas(self.frame, width=30, height=30, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10)
        self.indicator = self.canvas.create_oval(5, 5, 25, 25, fill="red")

        # Ping button
        self.button = tk.Button(self.frame, text="Ping", width=8, command=self.toggle)
        self.button.pack(side=tk.LEFT, padx=5)

    def toggle(self):
        if not self.running:
            self.running = True
            self.button.config(text="Stop")
            threading.Thread(target=self.worker, daemon=True).start()
        else:
            self.running = False
            self.button.config(text="Ping")
            self.set_indicator("red")

    def worker(self):
        while self.running:
            host = self.entry.get().strip()
            color = check_alive(host) if host else "red"
            self.parent.after(0, self.set_indicator, color)
            time.sleep(PING_INTERVAL)

    def set_indicator(self, color):
        self.canvas.itemconfig(self.indicator, fill=color)

    def get_host(self):
        return self.entry.get().strip()


# ---------------- MAIN APP ----------------
class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Server Liveness Monitor")

        self.rows = []

        # Rows container
        self.rows_frame = tk.Frame(root)
        self.rows_frame.pack(padx=10, pady=10)

        # Control buttons
        control = tk.Frame(root)
        control.pack(pady=5)

        self.add_btn = tk.Button(control, text="+ Add Ping", width=12, command=self.add_row)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        # Load saved hosts from INI
        self.load_ini()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_row(self, host=""):
        if host and host in [r.get_host() for r in self.rows]:
            return
        row = PingRow(self.rows_frame, host, self.save_ini)
        self.rows.append(row)
        self.save_ini()

    # ---------------- INI ----------------
    def load_ini(self):
        config = configparser.ConfigParser()
        if os.path.exists(INI_FILE):
            config.read(INI_FILE)
            if "pings" in config:
                for _, host in config["pings"].items():
                    self.add_row(host)

    def save_ini(self):
        config = configparser.ConfigParser()
        config["pings"] = {}
        for i, row in enumerate(self.rows, start=1):
            host = row.get_host()
            if host:
                config["pings"][f"host{i}"] = host
        with open(INI_FILE, "w") as f:
            config.write(f)

    def on_close(self):
        for row in self.rows:
            row.running = False
        self.save_ini()
        self.root.destroy()


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()
