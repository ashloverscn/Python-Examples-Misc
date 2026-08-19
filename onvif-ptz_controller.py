import threading
import tkinter as tk
from tkinter import ttk, messagebox
from onvif import ONVIFClient

class SimplePTZGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple ONVIF PTZ Controller")
        self.root.geometry("380x480")
        self.root.resizable(False, False)

        # ONVIF variables
        self.client = None
        self.ptz_service = None
        self.profile_token = None

        self.setup_ui()

    def setup_ui(self):
        # --- Connection Panel ---
        conn_frame = ttk.LabelFrame(self.root, text=" Camera Connection ", padding=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(conn_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ent_ip = ttk.Entry(conn_frame, width=18)
        self.ent_ip.insert(0, "192.168.29.251")
        self.ent_ip.grid(row=0, column=1, pady=2)

        ttk.Label(conn_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ent_port = ttk.Entry(conn_frame, width=18)
        self.ent_port.insert(0, "8000")
        self.ent_port.grid(row=1, column=1, pady=2)

        ttk.Label(conn_frame, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.ent_user = ttk.Entry(conn_frame, width=18)
        self.ent_user.insert(0, "admin")
        self.ent_user.grid(row=2, column=1, pady=2)

        ttk.Label(conn_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.ent_pwd = ttk.Entry(conn_frame, width=18, show="*")
        self.ent_pwd.insert(0, "admin")
        self.ent_pwd.grid(row=3, column=1, pady=2)

        self.btn_connect = ttk.Button(conn_frame, text="Connect to Camera", command=self.connect_camera)
        self.btn_connect.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # --- PTZ Control Panel ---
        self.ptz_frame = ttk.LabelFrame(self.root, text=" PTZ Controls ", padding=10)
        self.ptz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Directional Grid
        self.btn_up = ttk.Button(self.ptz_frame, text="▲ Up", state=tk.DISABLED)
        self.btn_down = ttk.Button(self.ptz_frame, text="▼ Down", state=tk.DISABLED)
        self.btn_left = ttk.Button(self.ptz_frame, text="◀ Left", state=tk.DISABLED)
        self.btn_right = ttk.Button(self.ptz_frame, text="▶ Right", state=tk.DISABLED)

        self.btn_up.grid(row=0, column=1, padx=5, pady=5, ipadx=10)
        self.btn_left.grid(row=1, column=0, padx=5, pady=5, ipadx=5)
        self.btn_right.grid(row=1, column=2, padx=5, pady=5, ipadx=5)
        self.btn_down.grid(row=2, column=1, padx=5, pady=5, ipadx=5)

        # Bind Press (Start Move) and Release (Stop Move) events
        self.bind_hold_button(self.btn_up, 0, 0.5, 0)
        self.bind_hold_button(self.btn_down, 0, -0.5, 0)
        self.bind_hold_button(self.btn_left, -0.5, 0, 0)
        self.bind_hold_button(self.btn_right, 0.5, 0, 0)

        # Zoom Controls
        zoom_frame = ttk.Frame(self.ptz_frame)
        zoom_frame.grid(row=3, column=0, columnspan=3, pady=(15, 0), sticky="ew")

        self.btn_zoom_in = ttk.Button(zoom_frame, text="🔍+ Zoom In", state=tk.DISABLED)
        self.btn_zoom_out = ttk.Button(zoom_frame, text="🔍- Zoom Out", state=tk.DISABLED)
        self.btn_zoom_in.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.btn_zoom_out.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

        self.bind_hold_button(self.btn_zoom_in, 0, 0, 0.5)
        self.bind_hold_button(self.btn_zoom_out, 0, 0, -0.5)

        # --- Status Footer ---
        self.lbl_status = ttk.Label(self.root, text="Status: Disconnected", foreground="red")
        self.lbl_status.pack(side=tk.BOTTOM, pady=5)

    def bind_hold_button(self, button, pan, tilt, zoom):
        button.bind("<ButtonPress-1>", lambda e: self.send_move(pan, tilt, zoom))
        button.bind("<ButtonRelease-1>", lambda e: self.send_stop())

    def connect_camera(self):
        ip = self.ent_ip.get().strip()
        port_str = self.ent_port.get().strip()
        user = self.ent_user.get().strip()
        pwd = self.ent_pwd.get().strip()

        if not ip or not port_str:
            messagebox.showerror("Error", "IP and Port cannot be empty.")
            return

        self.lbl_status.config(text="Status: Connecting...", foreground="orange")
        self.btn_connect.config(state=tk.DISABLED)

        def worker():
            try:
                port = int(port_str)
                self.client = ONVIFClient(ip, port, user, pwd)
                media_service = self.client.media()
                profiles = media_service.GetProfiles()
                
                if not profiles:
                    raise Exception("No media profiles found.")

                self.profile_token = profiles[0].token
                self.ptz_service = self.client.ptz()
                
                self.root.after(0, self.connection_success)
            except Exception as e:
                self.root.after(0, lambda: self.connection_failed(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def connection_success(self):
        self.lbl_status.config(text="Status: Connected & Ready", foreground="green")
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_up.config(state=tk.NORMAL)
        self.btn_down.config(state=tk.NORMAL)
        self.btn_left.config(state=tk.NORMAL)
        self.btn_right.config(state=tk.NORMAL)
        self.btn_zoom_in.config(state=tk.NORMAL)
        self.btn_zoom_out.config(state=tk.NORMAL)

    def connection_failed(self, error_msg):
        self.lbl_status.config(text="Status: Connection Failed", foreground="red")
        self.btn_connect.config(state=tk.NORMAL)
        messagebox.showerror("Connection Error", f"Could not connect to camera:\n{error_msg}")

    def send_move(self, pan, tilt, zoom):
        if not self.ptz_service or not self.profile_token:
            return
        def worker():
            try:
                # Correct keyword parameter signature for onvif-python
                self.ptz_service.ContinuousMove(
                    ProfileToken=self.profile_token,
                    Velocity={
                        'PanTilt': {'x': pan, 'y': tilt},
                        'Zoom': {'x': zoom}
                    }
                )
            except Exception as e:
                print(f"Move error: {e}")
        threading.Thread(target=worker, daemon=True).start()

    def send_stop(self):
        if not self.ptz_service or not self.profile_token:
            return
        def worker():
            try:
                # Correct keyword parameter signature for Stop
                self.ptz_service.Stop(
                    ProfileToken=self.profile_token
                )
            except Exception as e:
                print(f"Stop error: {e}")
        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePTZGUI(root)
    root.mainloop()