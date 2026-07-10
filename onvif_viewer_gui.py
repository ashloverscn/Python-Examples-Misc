import threading
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import urllib.parse
from PIL import Image, ImageTk
from wsdiscovery import WSDiscovery
from onvif import ONVIFClient

class ONVIFCameraViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robust ONVIF Camera Viewer & PTZ Controller")
        self.root.geometry("1100x750")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Thread management & Video state
        self.discovery_thread = None
        self.video_thread = None
        self.cap = None
        self.is_streaming = False
        self.discovered_devices = []
        
        # ONVIF Core Client & PTZ references
        self.client = None
        self.ptz_service = None
        self.media_profiles = []
        self.selected_profile_token = None

        self.setup_ui()

    def setup_ui(self):
        # --- Control & Input Panel (Left) ---
        control_panel = ttk.LabelFrame(self.root, text=" Camera Controls ", padding=10)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Discovery Button
        self.btn_discover = ttk.Button(control_panel, text="🔍 Discover Cameras", command=self.start_discovery)
        self.btn_discover.pack(fill=tk.X, pady=(0, 10))

        # Discovered Dropdown
        ttk.Label(control_panel, text="Discovered Devices:").pack(anchor=tk.W)
        self.cb_devices = ttk.Combobox(control_panel, state="readonly")
        self.cb_devices.pack(fill=tk.X, pady=(0, 15))
        self.cb_devices.bind("<<ComboboxSelected>>", self.on_device_selected)

        # Manual Credentials Panel
        ttk.Label(control_panel, text="Camera IP / Host:").pack(anchor=tk.W)
        self.ent_ip = ttk.Entry(control_panel)
        self.ent_ip.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="ONVIF Port:").pack(anchor=tk.W)
        self.ent_port = ttk.Entry(control_panel)
        self.ent_port.insert(0, "8000")
        self.ent_port.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Username:").pack(anchor=tk.W)
        self.ent_user = ttk.Entry(control_panel)
        self.ent_user.insert(0, "admin")
        self.ent_user.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Password:").pack(anchor=tk.W)
        self.ent_pwd = ttk.Entry(control_panel, show="*")
        self.ent_pwd.insert(0, "admin")
        self.ent_pwd.pack(fill=tk.X, pady=(0, 15))

        # Phase 1: Connect to Camera & Get Profiles
        self.btn_connect = ttk.Button(control_panel, text="🔗 Connect & Fetch Streams", command=self.connect_to_camera)
        self.btn_connect.pack(fill=tk.X, pady=3)

        # Phase 2: Select Profile & Play
        ttk.Label(control_panel, text="Available Streams:").pack(anchor=tk.W, pady=(10, 0))
        self.cb_streams = ttk.Combobox(control_panel, state="disabled")
        self.cb_streams.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_play = ttk.Button(control_panel, text="▶ Play Selected Stream", command=self.start_stream, state=tk.DISABLED)
        self.btn_play.pack(fill=tk.X, pady=3)

        self.btn_stop = ttk.Button(control_panel, text="⏹ Stop Stream", command=self.stop_stream, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X, pady=(3, 15))

        # --- PTZ Control Section ---
        ptz_frame = ttk.LabelFrame(control_panel, text=" PTZ Controls ", padding=10)
        ptz_frame.pack(fill=tk.X, pady=10)

        self.btn_up = ttk.Button(ptz_frame, text="▲ Up")
        self.btn_down = ttk.Button(ptz_frame, text="▼ Down")
        self.btn_left = ttk.Button(ptz_frame, text="◀ Left")
        self.btn_right = ttk.Button(ptz_frame, text="▶ Right")
        
        self.btn_up.grid(row=0, column=1, padx=5, pady=5)
        self.btn_left.grid(row=1, column=0, padx=5, pady=5)
        self.btn_right.grid(row=1, column=2, padx=5, pady=5)
        self.btn_down.grid(row=2, column=1, padx=5, pady=5)

        self.btn_up.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(0, 0.5, 0))
        self.btn_up.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())
        self.btn_down.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(0, -0.5, 0))
        self.btn_down.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())
        self.btn_left.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(-0.5, 0, 0))
        self.btn_left.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())
        self.btn_right.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(0.5, 0, 0))
        self.btn_right.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())

        zoom_frame = ttk.Frame(ptz_frame)
        zoom_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        self.btn_zoom_in = ttk.Button(zoom_frame, text="🔍+ Zoom In")
        self.btn_zoom_out = ttk.Button(zoom_frame, text="🔍- Zoom Out")
        self.btn_zoom_in.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.btn_zoom_out.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

        self.btn_zoom_in.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(0, 0, 0.5))
        self.btn_zoom_in.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())
        self.btn_zoom_out.bind("<ButtonPress-1>", lambda e: self.send_ptz_command(0, 0, -0.5))
        self.btn_zoom_out.bind("<ButtonRelease-1>", lambda e: self.send_ptz_stop())

        # Status Label
        self.lbl_status = ttk.Label(control_panel, text="Status: Idle", wraplength=180, foreground="blue")
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # --- Video Panel (Right) ---
        self.video_panel = ttk.LabelFrame(self.root, text=" Live Video Feed ", padding=5)
        self.video_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.video_panel, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    # --- Discovery Operations ---
    def start_discovery(self):
        self.btn_discover.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Scanning network...", foreground="orange")
        self.discovery_thread = threading.Thread(target=self.network_discovery_worker, daemon=True)
        self.discovery_thread.start()

    def network_discovery_worker(self):
        try:
            wsd = WSDiscovery()
            wsd.start()
            services = wsd.searchServices()
            
            self.discovered_devices = []
            dropdown_values = []

            for service in services:
                if 'NetworkVideoTransmitter' in str(service.getTypes()):
                    xaddrs = service.getXAddrs()
                    if xaddrs:
                        url = xaddrs[0]
                        parsed = urllib.parse.urlparse(url)
                        host = parsed.hostname
                        port = parsed.port or 80
                        self.discovered_devices.append({'host': host, 'port': port})
                        dropdown_values.append(f"{host}:{port}")
            
            wsd.stop()
            self.root.after(0, self.finish_discovery, dropdown_values)
        except Exception as e:
            self.root.after(0, self.show_error, f"Discovery error: {e}")

    def finish_discovery(self, values):
        self.btn_discover.config(state=tk.NORMAL)
        if values:
            self.cb_devices['values'] = values
            self.cb_devices.current(0)
            self.on_device_selected(None)
            self.lbl_status.config(text=f"Status: Found {len(values)} camera(s)", foreground="green")
        else:
            self.lbl_status.config(text="Status: No cameras found.", foreground="red")

    def on_device_selected(self, event):
        idx = self.cb_devices.current()
        if idx >= 0:
            device = self.discovered_devices[idx]
            self.ent_ip.delete(0, tk.END)
            self.ent_ip.insert(0, device['host'])
            self.ent_port.delete(0, tk.END)
            self.ent_port.insert(0, str(device['port']))

    # --- Phase 1: Connect & Fetch Profiles ---
    def connect_to_camera(self):
        ip = self.ent_ip.get().strip()
        port = self.ent_port.get().strip()
        user = self.ent_user.get().strip()
        pwd = self.ent_pwd.get().strip()

        if not ip or not port:
            messagebox.showwarning("Validation Error", "Please specify a valid IP address and Port.")
            return

        self.lbl_status.config(text="Status: Fetching Profiles...", foreground="orange")
        self.btn_connect.config(state=tk.DISABLED)
        
        threading.Thread(target=self.fetch_profiles_worker, args=(ip, port, user, pwd), daemon=True).start()

    def fetch_profiles_worker(self, ip, port, user, pwd):
        try:
            self.client = ONVIFClient(ip, int(port), user, pwd)
            media_service = self.client.media()
            self.media_profiles = media_service.GetProfiles()
            
            if not self.media_profiles:
                self.root.after(0, self.show_error, "No media profiles found on device.")
                return

            try:
                self.ptz_service = self.client.ptz()
            except Exception:
                self.ptz_service = None

            stream_labels = []
            for profile in self.media_profiles:
                name = getattr(profile, 'Name', 'Unknown')
                token = getattr(profile, 'token', '')
                stream_labels.append(f"{name} ({token})")

            self.root.after(0, self.populate_streams_dropdown, stream_labels)

        except Exception as e:
            self.root.after(0, self.show_error, f"Handshake Failed:\n{e}")

    def populate_streams_dropdown(self, stream_labels):
        self.btn_connect.config(state=tk.NORMAL)
        self.cb_streams.config(state="readonly")
        self.cb_streams['values'] = stream_labels
        self.cb_streams.current(0)
        self.btn_play.config(state=tk.NORMAL)
        self.lbl_status.config(text="Status: Streams Loaded", foreground="green")

    # --- Phase 2: Stream Selection & Playback ---
    def start_stream(self):
        idx = self.cb_streams.current()
        if idx < 0:
            return

        selected_profile = self.media_profiles[idx]
        self.selected_profile_token = selected_profile.token
        
        user = self.ent_user.get().strip()
        pwd = self.ent_pwd.get().strip()

        self.lbl_status.config(text="Status: Requesting Stream URI...", foreground="orange")
        self.btn_play.config(state=tk.DISABLED)
        
        threading.Thread(target=self.play_worker, args=(user, pwd), daemon=True).start()

    def play_worker(self, user, pwd):
        try:
            media_service = self.client.media()
            stream_setup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
            uri_response = media_service.GetStreamUri(StreamSetup=stream_setup, ProfileToken=self.selected_profile_token)
            rtsp_url = uri_response.Uri

            if user and pwd and "rtsp://" in rtsp_url:
                safe_user = urllib.parse.quote_plus(user)
                safe_pwd = urllib.parse.quote_plus(pwd)
                rtsp_url = rtsp_url.replace("rtsp://", f"rtsp://{safe_user}:{safe_pwd}@")

            self.root.after(0, self.initiate_video_loop, rtsp_url)
        except Exception as e:
            self.root.after(0, self.show_error, f"Failed to get Stream Link:\n{e}")

    def initiate_video_loop(self, rtsp_url):
        if self.is_streaming:
            self.stop_stream()

        self.cap = cv2.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            self.show_error("OpenCV could not open the RTSP stream.")
            return

        self.is_streaming = True
        self.btn_play.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.lbl_status.config(text="Status: Streaming Live", foreground="green")
        
        self.video_thread = threading.Thread(target=self.video_render_worker, daemon=True)
        self.video_thread.start()

    def video_render_worker(self):
        while self.is_streaming:
            ret, frame = self.cap.read()
            if not ret:
                self.root.after(0, self.stop_stream)
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 10 and canvas_height > 10:
                img = Image.fromarray(frame)
                img_width, img_height = img.size
                
                # --- Dynamic 1:1 Aspect Ratio Scaling Logic ---
                # Calculate the scaling factor for both width and height
                ratio_w = canvas_width / img_width
                ratio_h = canvas_height / img_height
                scaling_factor = min(ratio_w, ratio_h)
                
                # Determine the absolute new dimensions required to perfectly fill the canvas maximums
                new_width = int(img_width * scaling_factor)
                new_height = int(img_height * scaling_factor)
                
                # Perform the structural sizing frame conversion 
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(image=img)
                
                self.root.after(0, self.update_canvas, img_tk, canvas_width, canvas_height)

    def update_canvas(self, img_tk, w, h):
        if not self.is_streaming:
            return
        self.current_frame_ref = img_tk 
        self.canvas.delete("all")
        self.canvas.create_image(w//2, h//2, anchor=tk.CENTER, image=img_tk)

    # --- PTZ Mechanics ---
    def send_ptz_command(self, pan, tilt, zoom):
        if not self.ptz_service or not self.selected_profile_token:
            return
        
        def ptz_worker():
            try:
                velocity = {
                    'PanTilt': {'x': pan, 'y': tilt},
                    'Zoom': {'x': zoom}
                }
                self.ptz_service.ContinuousMove(ProfileToken=self.selected_profile_token, Velocity=velocity)
            except Exception as e:
                print(f"PTZ Command failed: {e}")

        threading.Thread(target=ptz_worker, daemon=True).start()

    def send_ptz_stop(self):
        if not self.ptz_service or not self.selected_profile_token:
            return

        def ptz_stop_worker():
            try:
                self.ptz_service.Stop(ProfileToken=self.selected_profile_token, PanTilt=True, Zoom=True)
            except Exception as e:
                print(f"PTZ Stop failed: {e}")

        threading.Thread(target=ptz_stop_worker, daemon=True).start()

    def stop_stream(self):
        self.is_streaming = False
        if self.cap:
            self.cap.release()
        self.canvas.delete("all")
        self.btn_play.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Stream Stopped", foreground="blue")

    def show_error(self, message):
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_play.config(state=tk.NORMAL)
        self.lbl_status.config(text="Status: Error Encountered", foreground="red")
        messagebox.showerror("Error", message)

    def on_closing(self):
        self.stop_stream()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ONVIFCameraViewerGUI(root)
    root.mainloop()