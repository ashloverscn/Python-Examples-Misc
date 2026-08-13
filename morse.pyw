import tkinter as tk
import random
import time
import threading
import sys
import urllib.request
import json

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    "'": '.----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.---.', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.',
    ' ': '   '
}

REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items() if k != ' '}

FALLBACK_SENTENCES = [
    "CQ CQ DE NET!",
    "PSE QSL HW?",
    "XZQW JMPV KLYF BCPG",
    "THE QUICK FOX (123)",
    "TEST / CHECK + OK",
    "EMAIL@TEST.COM $100",
    "PRM-TNS_XYZ/123+ABC"
]

DIT_DURATION = 0.100  # 100 ms
DAH_DURATION = 0.300  # 300 ms
FREQ = 750            # Hz

class TelegraphTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telegraph Trainer")
        self.root.geometry("780x435")
        self.root.minsize(650, 410)

        self.press_start = 0
        self.k_is_down = False
        self.current_symbol = ""
        self.last_press_time = 0

        self.current_target_text = ""
        self.current_target_morse = ""

        # Robust State Tracking for Complete Synchronization
        self.sequence_history = []  # List of tuples: (morse_string, translated_char)

        self.setup_theme()
        self.create_layout()
        self.load_new_sentence()

        self.root.after(100, self.update_loop)
        self.root.after(100, lambda: self.root.focus_force())

    def setup_theme(self):
        self.bg = "#11121d"
        self.card_bg = "#1a1b26"
        self.accent = "#7aa2f7"
        self.fg = "#c0caf5"
        self.dim = "#414868"
        self.green = "#9ece6a"
        self.red = "#f7768e"
        self.root.configure(bg=self.bg)

    def create_layout(self):
        main = tk.Frame(self.root, bg=self.bg, padx=10, pady=6)
        main.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(main, text="TELEGRAPH TRAINER", font=("Consolas", 12, "bold"), bg=self.bg, fg=self.accent)
        title.pack(anchor="w", pady=(0, 1))

        # --- Target Random Sentence ---
        lbl1 = tk.Label(main, text="Target Sentence (Copy this):", font=("Consolas", 8, "bold"), bg=self.bg, fg=self.fg)
        lbl1.pack(anchor="w")
        self.box_target_text = tk.Text(main, height=4, font=("Consolas", 10, "bold"), bg=self.card_bg, fg=self.green, bd=0, highlightthickness=1, highlightbackground=self.dim, wrap=tk.WORD)
        self.box_target_text.pack(fill=tk.X, pady=(0, 2))
        self.box_target_text.config(state=tk.DISABLED)

        # --- Reference Morse Code ---
        lbl2 = tk.Label(main, text="Reference Morse Code:", font=("Consolas", 8, "bold"), bg=self.bg, fg=self.fg)
        lbl2.pack(anchor="w")
        self.box_target_morse = tk.Text(main, height=4, font=("Consolas", 9), bg=self.card_bg, fg=self.accent, bd=0, highlightthickness=1, highlightbackground=self.dim, wrap=tk.WORD)
        self.box_target_morse.pack(fill=tk.X, pady=(0, 2))
        self.box_target_morse.config(state=tk.DISABLED)

        # --- Real-Time Translated Text Output ---
        lbl_realtime = tk.Label(main, text="Real-Time Translated Text Output:", font=("Consolas", 8, "bold"), bg=self.bg, fg=self.fg)
        lbl_realtime.pack(anchor="w")
        self.box_realtime_text = tk.Text(main, height=4, font=("Consolas", 10, "bold"), bg=self.card_bg, fg=self.green, bd=0, highlightthickness=1, highlightbackground=self.dim, wrap=tk.WORD)
        self.box_realtime_text.pack(fill=tk.X, pady=(0, 2))
        self.box_realtime_text.config(state=tk.DISABLED)

        # --- Your Live Morse Input ---
        lbl3 = tk.Label(main, text="Your Morse Input ('K'=Dit/Dah | 'C'=Clear | 'M'=Check | 'N'=Next | Backspace=Erase):", font=("Consolas", 8, "bold"), bg=self.bg, fg=self.fg)
        lbl3.pack(anchor="w")
        self.box_user_morse = tk.Text(main, height=4, font=("Consolas", 9), bg=self.card_bg, fg=self.fg, insertbackground=self.fg, bd=0, highlightthickness=1, highlightbackground=self.dim, wrap=tk.WORD)
        self.box_user_morse.pack(fill=tk.X, pady=(0, 3))

        # Bind global and text-box keys to capture only permitted inputs
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        self.box_user_morse.bind("<KeyPress>", self.text_box_key_press)
        self.box_user_morse.bind("<KeyRelease>", self.text_box_key_release)

        # --- Status Label Only ---
        ctrl_frame = tk.Frame(main, bg=self.bg)
        ctrl_frame.pack(fill=tk.X, pady=(0, 0))

        self.status_lbl = tk.Label(ctrl_frame, text="STATUS: READY (Press & Hold 'K')", font=("Consolas", 8, "bold"), bg=self.bg, fg=self.accent)
        self.status_lbl.pack(side=tk.LEFT)

    def load_new_sentence(self):
        self.status_lbl.configure(fg=self.accent, text="STATUS: FETCHING ONLINE SENTENCE...")
        self.root.update_idletasks()
        
        threading.Thread(target=self._fetch_online_sentence_thread, daemon=True).start()

    def _fetch_online_sentence_thread(self):
        sentence = ""
        try:
            # Fetching random sentences from an open public JSON API
            url = "https://api.quotable.io/random?maxLength=30"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                sentence = data.get("content", "")
        except Exception:
            pass

        if not sentence:
            sentence = random.choice(FALLBACK_SENTENCES)
        
        # Clean and uppercase to fit standard Morse rules
        sentence = ''.join(c for c in sentence.upper() if c in MORSE_CODE_DICT or c.isalpha() or c.isspace() or c in ".,?!'-_")
        if not sentence.strip():
            sentence = random.choice(FALLBACK_SENTENCES)

        self.root.after(0, lambda: self._apply_new_sentence(sentence))

    def _apply_new_sentence(self, sentence):
        self.current_target_text = sentence
        self.current_target_morse = self.text_to_morse(self.current_target_text)

        self.box_target_text.config(state=tk.NORMAL)
        self.box_target_text.delete("1.0", tk.END)
        self.box_target_text.insert("1.0", self.current_target_text)
        self.box_target_text.config(state=tk.DISABLED)

        self.box_target_morse.config(state=tk.NORMAL)
        self.box_target_morse.delete("1.0", tk.END)
        self.box_target_morse.insert("1.0", self.current_target_morse)
        self.box_target_morse.config(state=tk.DISABLED)

        self.clear_input()

    def text_to_morse(self, text):
        cipher = []
        for char in text.upper():
            if char in MORSE_CODE_DICT:
                cipher.append(MORSE_CODE_DICT[char])
        return ' '.join(cipher)

    def play_sound(self, symbol):
        def _beep():
            duration_ms = int(DIT_DURATION * 1000) if symbol == '.' else int(DAH_DURATION * 1000)
            if HAS_WINSOUND and sys.platform == "win32":
                try: winsound.Beep(FREQ, duration_ms)
                except Exception: pass
            else:
                try:
                    import os
                    sec = DIT_DURATION if symbol == '.' else DAH_DURATION
                    os.system(f'play -n synth {sec} sin {FREQ} > /dev/null 2>&1')
                except Exception: pass
        threading.Thread(target=_beep, daemon=True).start()

    def refresh_displays(self):
        morse_string_parts = []
        text_string_parts = []

        for morse_char, text_char in self.sequence_history:
            morse_string_parts.append(morse_char)
            text_string_parts.append(text_char)

        self.box_user_morse.delete("1.0", tk.END)
        if morse_string_parts:
            self.box_user_morse.insert("1.0", " ".join(morse_string_parts))

        self.box_realtime_text.config(state=tk.NORMAL)
        self.box_realtime_text.delete("1.0", tk.END)
        if text_string_parts:
            self.box_realtime_text.insert("1.0", "".join(text_string_parts))
        self.box_realtime_text.see(tk.END)
        self.box_realtime_text.config(state=tk.DISABLED)

    def key_press(self, event):
        key = event.keysym.upper()
        
        if key not in ('K', 'C', 'M', 'N', 'BACKSPACE', 'DELETE'):
            return

        if key == 'C':
            self.clear_input()
            return
        if key == 'M':
            self.check_match()
            return
        if key == 'N':
            self.load_new_sentence()
            return

        if key in ('BACKSPACE', 'DELETE'):
            self.erase_last_item()
            return

        if key == 'K':
            if event.state & 0x0002 or self.k_is_down:
                return
            if not self.k_is_down:
                self.k_is_down = True
                self.press_start = time.time()
                self.status_lbl.configure(fg=self.green, text="STATUS: TRANSMITTING...")

    def key_release(self, event):
        key = event.keysym.upper()
        if key == 'K' and self.k_is_down:
            self.k_is_down = False
            pulse = time.time() - self.press_start
            symbol = '.' if pulse < 0.25 else '-'
            
            self.current_symbol += symbol
            self.play_sound(symbol)

            morse_string_parts = [m for m, t in self.sequence_history]
            if self.current_symbol:
                morse_string_parts.append(self.current_symbol)
            
            self.box_user_morse.delete("1.0", tk.END)
            self.box_user_morse.insert("1.0", " ".join(morse_string_parts))

            self.status_lbl.configure(fg=self.accent, text="STATUS: READY")
            self.last_press_time = time.time()

    def text_box_key_press(self, event):
        self.key_press(event)
        return "break"

    def text_box_key_release(self, event):
        self.key_release(event)
        return "break"

    def update_loop(self):
        if self.current_symbol and not self.k_is_down:
            if time.time() - self.last_press_time > 0.5:
                translated_char = REVERSE_MORSE_DICT.get(self.current_symbol, '?')
                
                self.sequence_history.append((self.current_symbol, translated_char))
                self.current_symbol = ""
                
                self.refresh_displays()
                
        self.root.after(100, self.update_loop)

    def erase_last_item(self):
        if self.current_symbol:
            self.current_symbol = ""
            self.refresh_displays()
            self.status_lbl.configure(fg=self.accent, text="STATUS: READY")
            return

        if self.sequence_history:
            self.sequence_history.pop()
            self.refresh_displays()

    def clear_input(self):
        self.sequence_history.clear()
        self.current_symbol = ""
        self.refresh_displays()
        self.status_lbl.configure(fg=self.accent, text="STATUS: READY")

    def check_match(self):
        user_input_text = self.box_realtime_text.get("1.0", tk.END).strip()
        clean_target = "".join(self.current_target_text.split())
        clean_user = "".join(user_input_text.split())

        if clean_user == clean_target:
            self.status_lbl.configure(fg=self.green, text="STATUS: PERFECT MATCH! EXCELLENT JOB!")
        else:
            self.status_lbl.configure(fg=self.red, text="STATUS: MISMATCH. CHECK YOUR DITS & DAHS!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TelegraphTrainerApp(root)
    root.mainloop()