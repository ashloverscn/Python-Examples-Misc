import os
import time
import json
import threading
import http.server
import socketserver
import functools
import av
import vlc
import customtkinter as ctk

# --- CONFIG MANAGEMENT ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORD_DIR = os.path.join(BASE_DIR, "nvr_storage")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {"rtsp_url": "rtsp://your_camera_url_here", "record_dir": RECORD_DIR, "dvr_window_hours": 12.0}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f: return {**DEFAULT_CONFIG, **json.load(f)}
        except: pass
    return DEFAULT_CONFIG.copy()

def save_config(config_data):
    with open(CONFIG_FILE, "w") as f: json.dump(config_data, f, indent=4)

CONFIG = load_config()
os.makedirs(CONFIG["record_dir"], exist_ok=True)

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass

class HLSEngine:
    def __init__(self):
        self.config = CONFIG
        self.is_running = False
        self._url_lock = threading.Lock()
        self.http_port = 8554
        threading.Thread(target=self._start_http_server, daemon=True).start()

    def _start_http_server(self):
        handler = functools.partial(QuietHTTPRequestHandler, directory=self.config["record_dir"])
        try:
            with socketserver.TCPServer(("127.0.0.1", self.http_port), handler) as httpd:
                httpd.serve_forever()
        except OSError: pass

    def start(self):
        self.is_running = True
        threading.Thread(target=self._recording_loop, daemon=True).start()

    def update_settings(self, new_url):
        with self._url_lock:
            self.config["rtsp_url"] = new_url
            save_config(self.config)

    def _recording_loop(self):
        while self.is_running:
            with self._url_lock:
                url = self.config["rtsp_url"]
                record_dir = self.config["record_dir"]
                max_segments = int((self.config["dvr_window_hours"] * 3600) / 4)
            if not url or "your_camera" in url: time.sleep(2); continue
            os.makedirs(record_dir, exist_ok=True)
            try:
                in_c = av.open(url, options={'rtsp_transport': 'tcp', 'stimeout': '5000000'})
                in_s = in_c.streams.video[0]
                out_c = av.open(os.path.join(record_dir, "live.m3u8"), mode='w', format='hls', options={
                    'hls_time': '4', 'hls_list_size': str(max_segments), 'hls_flags': 'delete_segments', 
                    'hls_segment_filename': os.path.join(record_dir, "seg_%05d.ts")
                })
                out_s = out_c.add_stream_from_template(in_s)
                for pkt in in_c.demux(in_s):
                    if not self.is_running: break
                    if pkt.dts is not None: pkt.stream = out_s; out_c.mux(pkt)
            except: pass
            finally: 
                try: out_c.close(); in_c.close()
                except: pass
            time.sleep(4)

class NVRGui(ctk.CTk):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.title("Enterprise HLS NVR | Workstation")
        if os.name == 'nt': self.state('zoomed')
        else: self.attributes('-zoomed', True)
        self.view_mode = "live"
        ctk.set_appearance_mode("Dark")
        self.vlc_instance = vlc.Instance('--no-xlib', '--quiet', '--network-caching=300')
        self.player = self.vlc_instance.media_player_new()
        self.setup_ui()
        self.bind("<Configure>", self.on_window_resize)
        self.engine.start()
        self.after(800, self.apply_config)
        self.update_time_label()

    def setup_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=10, fg_color="#181818")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(self.sidebar, text="RTSP URL", font=("Arial", 12, "bold")).pack(pady=10)
        self.url_in = ctk.CTkEntry(self.sidebar)
        self.url_in.pack(padx=20, fill="x")
        self.url_in.insert(0, self.engine.config["rtsp_url"])
        ctk.CTkButton(self.sidebar, text="UPDATE & RESTART", command=self.apply_config, fg_color="#1f538d").pack(padx=20, pady=15)
        ctk.CTkButton(self.sidebar, text="🟢 LIVE MONITORING", fg_color="#163e26", command=self.switch_to_live).pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="⚡ SCRUB ARCHIVE", fg_color="#8c581a", command=self.switch_to_archive).pack(padx=20, pady=5, fill="x")
        
        self.workspace = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=10)
        self.workspace.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        self.video_vp = ctk.CTkFrame(self.workspace, fg_color="#000000")
        self.video_vp.pack(fill="both", expand=True, padx=5, pady=5)
        self.pb = ctk.CTkFrame(self.workspace, height=60, fg_color="#121212", corner_radius=0)
        self.lbl_time = ctk.CTkLabel(self.pb, text="00:00:00", font=("Consolas", 14))
        self.lbl_time.pack(side="left", padx=15)
        self.slider = ctk.CTkSlider(self.pb, from_=0, to=1000, command=self.on_scrub)
        self.slider.pack(side="left", fill="x", expand=True, padx=15)

    def update_time_label(self):
        if self.view_mode == "archive":
            t = self.player.get_time()
            if t >= 0:
                seconds = (t // 1000) % 60
                minutes = (t // 60000) % 60
                hours = (t // 3600000)
                self.lbl_time.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.after(1000, self.update_time_label)

    def on_window_resize(self, event):
        if event.widget == self: self.bind_vlc()

    def bind_vlc(self):
        self.update()
        if os.name == 'nt': self.player.set_hwnd(self.video_vp.winfo_id())
        else: self.player.set_xwindow(self.video_vp.winfo_id())

    def apply_config(self):
        self.engine.update_settings(self.url_in.get().strip())
        self.switch_to_live()

    def switch_to_live(self):
        self.view_mode = "live"
        self.player.stop()
        self.pb.pack_forget()
        self.bind_vlc()
        media = self.vlc_instance.media_new(self.engine.config["rtsp_url"])
        self.player.set_media(media)
        self.player.play()

    def switch_to_archive(self):
        self.view_mode = "archive"
        self.player.stop()
        self.pb.pack(fill="x", side="bottom")
        self.bind_vlc()
        media = self.vlc_instance.media_new(f"http://127.0.0.1:{self.engine.http_port}/live.m3u8")
        self.player.set_media(media)
        self.player.play()

    def on_scrub(self, val):
        if self.view_mode == "archive": self.player.set_position(float(val) / 1000.0)

if __name__ == "__main__":
    app = NVRGui(HLSEngine())
    app.mainloop()