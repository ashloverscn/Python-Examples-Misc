import tkinter as tk
from tkinter import messagebox, ttk
import serial
import serial.tools.list_ports
import threading
import time

class SIM800L_Ultra:
    def __init__(self, root):
        self.root = root
        self.root.title("SIM800L Advanced Controller")
        self.root.geometry("600x750")
        self.ser = None
        self.running = False

        # --- Connection Header ---
        frame_conn = tk.LabelFrame(root, text="Hardware Connection", padx=10, pady=10)
        frame_conn.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_conn, text="Port:").grid(row=0, column=0)
        self.port_combo = ttk.Combobox(frame_conn, values=self.get_ports(), width=15)
        self.port_combo.grid(row=0, column=1, padx=5)
        
        tk.Button(frame_conn, text="🔄", command=self.refresh_ports).grid(row=0, column=2)

        tk.Label(frame_conn, text="Baud:").grid(row=0, column=3, padx=5)
        self.baud_combo = ttk.Combobox(frame_conn, values=[9600, 19200, 38400, 57600, 115200], width=10)
        self.baud_combo.set(9600)
        self.baud_combo.grid(row=0, column=4)

        self.btn_connect = tk.Button(frame_conn, text="Connect", bg="#FF9800", command=self.toggle_conn)
        self.btn_connect.grid(row=0, column=5, padx=10)

        # --- Status Dashboard ---
        frame_status = tk.LabelFrame(root, text="Live Module Status", padx=10, pady=10)
        frame_status.pack(fill="x", padx=10, pady=5)

        self.lbl_signal = tk.Label(frame_status, text="Signal: --", font=("Arial", 10, "bold"))
        self.lbl_signal.grid(row=0, column=0, padx=20)

        self.lbl_net = tk.Label(frame_status, text="Network: --", font=("Arial", 10))
        self.lbl_net.grid(row=0, column=1, padx=20)

        self.lbl_volt = tk.Label(frame_status, text="Voltage: --", font=("Arial", 10))
        self.lbl_volt.grid(row=0, column=2, padx=20)

        # --- Main Controls ---
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1: Calls & SMS
        tab1 = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(tab1, text="Calls & SMS")

        tk.Label(tab1, text="Recipient Number:").pack(anchor="w")
        self.entry_num = tk.Entry(tab1, font=("Consolas", 14), width=25)
        self.entry_num.insert(0, "+918777246851")
        self.entry_num.pack(fill="x", pady=5)

        f_btns = tk.Frame(tab1)
        f_btns.pack(pady=10)
        tk.Button(f_btns, text="📞 Start Call", bg="#4CAF50", fg="white", width=12, command=self.make_call).pack(side="left", padx=5)
        tk.Button(f_btns, text="🛑 Hang Up", bg="#f44336", fg="white", width=12, command=self.hang_up).pack(side="left", padx=5)
        tk.Button(f_btns, text="🔊 Vol Up", command=lambda: self.send_raw("AT+CLVL=100")).pack(side="left", padx=5)

        tk.Label(tab1, text="SMS Message:").pack(anchor="w")
        self.txt_msg = tk.Text(tab1, height=5)
        self.txt_msg.pack(fill="x", pady=5)
        tk.Button(tab1, text="✉️ Send Message", bg="#2196F3", fg="white", command=self.send_sms).pack(fill="x")

        # Tab 2: Terminal / Manual
        tab2 = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(tab2, text="Advanced Terminal")
        
        self.terminal = tk.Text(tab2, bg="black", fg="#00FF00", height=15, font=("Consolas", 10))
        self.terminal.pack(fill="both", expand=True)

        f_cmd = tk.Frame(tab2)
        f_cmd.pack(fill="x", pady=5)
        self.entry_cmd = tk.Entry(f_cmd, font=("Consolas", 10))
        self.entry_cmd.pack(side="left", fill="x", expand=True)
        tk.Button(f_cmd, text="Send AT", command=self.send_manual_cmd).pack(side="right")

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- Core Logic ---
    def get_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def refresh_ports(self):
        self.port_combo['values'] = self.get_ports()

    def log(self, text):
        self.terminal.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.terminal.see(tk.END)

    def toggle_conn(self):
        if self.ser and self.ser.is_open:
            self.running = False
            self.ser.close()
            self.btn_connect.config(text="Connect", bg="#FF9800")
            self.log("Disconnected.")
        else:
            try:
                self.ser = serial.Serial(self.port_combo.get(), int(self.baud_combo.get()), timeout=0.1)
                self.running = True
                self.btn_connect.config(text="Disconnect", bg="#9E9E9E")
                self.log(f"Connected to {self.port_combo.get()}")
                threading.Thread(target=self.monitor_thread, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def monitor_thread(self):
        """Background thread to update status and read incoming data"""
        while self.running:
            if self.ser and self.ser.is_open:
                # 1. Update Signal (CSQ)
                self.ser.write(b"AT+CSQ\r\n")
                time.sleep(0.2)
                # 2. Update Network (CREG)
                self.ser.write(b"AT+CREG?\r\n")
                time.sleep(0.2)
                # 3. Update Battery (CBC)
                self.ser.write(b"AT+CBC\r\n")
                
                # Read all responses
                while self.ser.in_waiting:
                    line = self.ser.readline().decode(errors='ignore').strip()
                    if line:
                        self.parse_line(line)
            time.sleep(5)

    def parse_line(self, line):
        self.log(f"<< {line}")
        if "+CSQ:" in line:
            val = line.split(":")[1].split(",")[0].strip()
            self.lbl_signal.config(text=f"Signal: {val}/31", fg="green" if int(val)>15 else "orange")
        elif "+CREG:" in line:
            status = line.split(",")[1].strip()
            text = "Home" if status == "1" else "Roaming" if status == "5" else "Searching..."
            self.lbl_net.config(text=f"Network: {text}")
        elif "+CBC:" in line:
            volt = line.split(",")[-1].strip()
            self.lbl_volt.config(text=f"Battery: {volt}mV")

    def send_raw(self, cmd):
        if self.ser and self.ser.is_open:
            self.log(f">> {cmd}")
            self.ser.write((cmd + '\r\n').encode())

    def make_call(self): self.send_raw(f"ATD{self.entry_num.get()};")
    
    def hang_up(self): self.send_raw("ATH")

    def send_sms(self):
        num = self.entry_num.get()
        msg = self.txt_msg.get("1.0", tk.END).strip()
        self.send_raw("AT+CMGF=1")
        time.sleep(0.2)
        self.send_raw(f'AT+CMGS="{num}"')
        time.sleep(0.2)
        self.ser.write((msg + chr(26)).encode())
        self.log("SMS Buffer Sent.")

    def send_manual_cmd(self):
        cmd = self.entry_cmd.get()
        self.send_raw(cmd)
        self.entry_cmd.delete(0, tk.END)

    def on_close(self):
        self.running = False
        if self.ser: self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SIM800L_Ultra(root)
    root.mainloop()