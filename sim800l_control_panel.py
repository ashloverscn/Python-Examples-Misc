import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
import re

# --- Global Variables ---
ser = None
running = True

# --- Utility Functions ---
def log(msg):
    """Thread-safe logging to the terminal."""
    root.after(0, lambda: _unsafe_log(msg))

def _unsafe_log(msg):
    terminal.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    terminal.see(tk.END)

def decode_ucs2(hex_str):
    """Converts HEX (UCS2) strings to readable Bengali/Hindi/English text."""
    try:
        # Clean the string of any non-hex characters
        clean_hex = "".join(c for c in hex_str if c in "0123456789ABCDEFabcdef")
        return bytes.fromhex(clean_hex).decode('utf-16-be')
    except Exception:
        return hex_str # Return original if decoding fails

def list_ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    port_menu["values"] = ports
    if ports: port_menu.current(0)
    log(f"Found {len(ports)} ports.")

# --- Serial Communication ---
def send_at(cmd, wait_time=0.5):
    if ser and ser.is_open:
        ser.write((cmd + "\r\n").encode())
        time.sleep(wait_time)
        response = ser.read_all().decode(errors='ignore').strip()
        if response: log(f">> {cmd}\n{response}")
        return response
    return None

def connect_modem():
    global ser
    port = port_var.get()
    baud = baud_var.get()
    try:
        ser = serial.Serial(port, baudrate=int(baud), timeout=1)
        log(f"✅ Connected to {port}")
        connect_btn.config(state="disabled")
        disconnect_btn.config(state="normal")
        threading.Thread(target=initialize_sim, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Connection Failed: {e}")

def disconnect_modem():
    global ser
    if ser and ser.is_open:
        ser.close()
        log("🔌 Disconnected.")
        connect_btn.config(state="normal")
        disconnect_btn.config(state="disabled")

def initialize_sim():
    log("🔄 Configuring Modem...")
    send_at("AT")
    send_at("ATE0")       # Echo off
    send_at("AT+CMGF=1")  # Text mode
    send_at('AT+CSCS="GSM"') # Default charset
    log("📶 Modem Ready.")

# --- Feature Functions ---
def call_number():
    number = phone_var.get().strip()
    if not number: return
    log(f"📞 Dialing {number}...")
    send_at(f"ATD{number};")

def hang_up():
    send_at("ATH")
    log("🛑 Call Ended.")

def send_sms():
    number = phone_var.get().strip()
    message = sms_text.get("1.0", tk.END).strip()
    if not number or not message: return

    def _sms_thread():
        log("📨 Sending SMS...")
        send_at('AT+CMGF=1')
        if ser and ser.is_open:
            ser.write((f'AT+CMGS="{number}"\r\n').encode())
            time.sleep(0.5)
            ser.write((message + "\x1A").encode())
            time.sleep(3)
            log("✅ SMS Processed.")

    threading.Thread(target=_sms_thread, daemon=True).start()

def read_inbox():
    def _read_thread():
        log("📥 Reading Inbox...")
        send_at("AT+CMGF=1") 
        # Increase wait time for large inboxes
        response = send_at('AT+CMGL="ALL"', wait_time=2.5)
        
        if not response or "+CMGL:" not in response:
            log("📭 Inbox empty.")
            return

        # Create Popup Window
        popup = tk.Toplevel(root)
        popup.title("Inbox (Decoded)")
        popup.geometry("600x450")
        
        txt = tk.Text(popup, wrap="word", padx=10, pady=10, font=("Segoe UI", 10))
        txt.pack(fill="both", expand=True)
        
        # Regex to split messages by header
        # Pattern: +CMGL: index,"status","sender",,"date"
        segments = re.split(r'\+CMGL: \d+,', response)
        
        for seg in segments:
            if not seg.strip(): continue
            try:
                lines = seg.strip().split('\n')
                header = lines[0]
                body = "".join(lines[1:]).strip()
                
                # Parse Header
                h_parts = header.split(',')
                sender = h_parts[1].replace('"', '')
                date = h_parts[3].replace('"', '') + " " + h_parts[4].replace('"', '')
                
                # Detect and Decode UCS2/Hex
                if all(c in '0123456789ABCDEFabcdef' for c in body) and len(body) > 8:
                    body = decode_ucs2(body)

                txt.insert(tk.END, f"FROM: {sender}\nDATE: {date}\nMSG: {body}\n", "bold")
                txt.insert(tk.END, "-"*50 + "\n")
            except: continue
            
        txt.config(state="disabled")

    threading.Thread(target=_read_thread, daemon=True).start()

def on_close():
    global running
    running = False
    if ser and ser.is_open: ser.close()
    root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("SIM800L Controller Pro")
root.geometry("800x650")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Connection Frame
conn_frame = ttk.LabelFrame(main_frame, text=" Connection Setup ", padding=10)
conn_frame.pack(fill="x", pady=5)

port_var = tk.StringVar()
port_menu = ttk.Combobox(conn_frame, textvariable=port_var, width=15, state="readonly")
port_menu.grid(row=0, column=0, padx=5)
ttk.Button(conn_frame, text="Refresh", command=list_ports).grid(row=0, column=1, padx=5)

baud_var = tk.StringVar(value="9600")
ttk.Entry(conn_frame, textvariable=baud_var, width=10).grid(row=0, column=2, padx=5)

connect_btn = ttk.Button(conn_frame, text="🔗 Connect", command=connect_modem)
connect_btn.grid(row=0, column=3, padx=5)

disconnect_btn = ttk.Button(conn_frame, text="❌ Disconnect", command=disconnect_modem, state="disabled")
disconnect_btn.grid(row=0, column=4, padx=5)

# Action Frame
action_frame = ttk.LabelFrame(main_frame, text=" Controls ", padding=10)
action_frame.pack(fill="x", pady=10)

phone_var = tk.StringVar(value="+91")
ttk.Entry(action_frame, textvariable=phone_var, font=("Consolas", 12), width=20).grid(row=0, column=0, padx=5)

ttk.Button(action_frame, text="📞 Call", command=call_number).grid(row=0, column=1, padx=2)
ttk.Button(action_frame, text="🛑 Hang Up", command=hang_up).grid(row=0, column=2, padx=2)
ttk.Button(action_frame, text="📥 Read Inbox", command=read_inbox).grid(row=0, column=3, padx=10)

sms_text = tk.Text(action_frame, height=4, width=50, font=("Segoe UI", 10))
sms_text.grid(row=1, column=0, columnspan=3, pady=10)
ttk.Button(action_frame, text="📩 Send SMS", command=send_sms).grid(row=1, column=3, padx=10)

# Terminal
terminal = tk.Text(main_frame, height=15, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10), padx=10, pady=10)
terminal.pack(fill="both", expand=True, pady=5)

list_ports()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()