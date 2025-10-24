import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time

ser = None
running = True

def log(msg):
    terminal.insert(tk.END, msg + "\n")
    terminal.see(tk.END)

def list_ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    port_menu["values"] = ports
    if ports:
        port_menu.current(0)

def connect_modem():
    global ser
    port = port_var.get()
    baud = baud_var.get()
    if not port:
        messagebox.showerror("Error", "Select a COM port")
        return
    try:
        ser = serial.Serial(port, baudrate=int(baud), timeout=1)
        log(f"✅ Connected to {port} at {baud} baud")
        connect_btn.config(state="disabled")
        disconnect_btn.config(state="normal")
        threading.Thread(target=initialize_sim, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def disconnect_modem():
    global ser
    if ser and ser.is_open:
        ser.close()
        log("🔌 Disconnected from modem")
        connect_btn.config(state="normal")
        disconnect_btn.config(state="disabled")
    else:
        log("⚠️ No active connection to disconnect.")

def initialize_sim():
    cmds = [
        "AT", "ATE0", "AT+CPIN?", "AT+CFUN=1", "AT+CREG?",
        "AT+CSQ", "AT+COPS=?", "AT+COPS=0"
    ]
    for cmd in cmds:
        send_at(cmd)
        time.sleep(1)
    log("📶 SIM initialized and network registration attempted.")

def send_at(cmd):
    if ser and ser.is_open:
        ser.write((cmd + "\r\n").encode())
        time.sleep(0.5)
        response = ser.read_all().decode(errors='ignore').strip()
        if response:
            log(f">> {cmd}\n{response}")
        return response
    else:
        log("⚠️ Serial not connected.")
        return None

def call_number():
    number = phone_var.get().strip()
    if not number:
        messagebox.showwarning("Warning", "Enter phone number")
        return
    send_at(f"ATD+{number};")

def hang_up():
    send_at("ATH")

def send_sms():
    number = phone_var.get().strip()
    message = sms_text.get("1.0", tk.END).strip()
    if not number or not message:
        messagebox.showwarning("Warning", "Enter number and message")
        return
    send_at('AT+CMGF=1')
    time.sleep(0.5)
    if ser:
        ser.write((f'AT+CMGS="{number}"\r\n').encode())
        time.sleep(0.5)
        ser.write((message + "\x1A").encode())  # Ctrl+Z
        log(f"📩 Sending SMS to {number}...")
        time.sleep(2)
        response = ser.read_all().decode(errors='ignore').strip()
        if response:
            log(response)

def on_close():
    global running
    running = False
    if ser and ser.is_open:
        ser.close()
    root.destroy()

# --- GUI ---
root = tk.Tk()
root.title("SIM800L Control Panel")
root.geometry("780x540")
root.resizable(False, False)

# Center the window
root.update_idletasks()
w = 780
h = 540
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Title
title = ttk.Label(main_frame, text="📡 SIM800L CONTROL PANEL", font=("Segoe UI", 14, "bold"))
title.pack(pady=(0, 15))

# Connection frame
conn_frame = ttk.Frame(main_frame)
conn_frame.pack(pady=5)

ttk.Label(conn_frame, text="COM Port:").grid(row=0, column=0, padx=5)
port_var = tk.StringVar()
port_menu = ttk.Combobox(conn_frame, textvariable=port_var, width=15)
port_menu.grid(row=0, column=1, padx=5)
ttk.Button(conn_frame, text="Refresh", command=list_ports).grid(row=0, column=2, padx=5)

ttk.Label(conn_frame, text="Baud Rate:").grid(row=0, column=3, padx=5)
baud_var = tk.StringVar(value="9600")
ttk.Entry(conn_frame, textvariable=baud_var, width=10).grid(row=0, column=4, padx=5)

connect_btn = ttk.Button(conn_frame, text="🔗 Connect", command=connect_modem)
connect_btn.grid(row=0, column=5, padx=10)

disconnect_btn = ttk.Button(conn_frame, text="❌ Disconnect", command=disconnect_modem, state="disabled")
disconnect_btn.grid(row=0, column=6, padx=10)

# Phone controls
phone_frame = ttk.Frame(main_frame)
phone_frame.pack(pady=10)

ttk.Label(phone_frame, text="Phone Number:").grid(row=0, column=0, padx=5)
phone_var = tk.StringVar()
ttk.Entry(phone_frame, textvariable=phone_var, width=25, justify="center").grid(row=0, column=1, padx=5)
ttk.Button(phone_frame, text="📞 Call", command=call_number, width=10).grid(row=0, column=2, padx=5)
ttk.Button(phone_frame, text="✋ Hang Up", command=hang_up, width=10).grid(row=0, column=3, padx=5)

# SMS section
sms_frame = ttk.Frame(main_frame)
sms_frame.pack(pady=10)

ttk.Label(sms_frame, text="SMS Message:").pack(anchor="center")
sms_text = tk.Text(sms_frame, height=3, width=70)
sms_text.pack(pady=5)
ttk.Button(sms_frame, text="📩 Send SMS", command=send_sms, width=15).pack(pady=5)

# Terminal output
ttk.Label(main_frame, text="Terminal Output:").pack(anchor="center", pady=(10, 5))
terminal = tk.Text(main_frame, height=10, width=90, bg="black", fg="lime", insertbackground="lime")
terminal.pack(anchor="center", pady=5)

list_ports()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
