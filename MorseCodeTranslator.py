#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Morse Code Translator (Tkinter Desktop App)
-------------------------------------------------
This Python script builds a desktop app that mirrors a common
Morse translator layout: two side‑by‑side text areas with
clear headers, and action buttons centered between them.

Left  : Plain Text input
Right : Morse Code output (and vice‑versa)

Buttons:
- Text → Morse
- Morse → Text
- Swap (swap contents of the two panes)
- Copy Output
- Clear
- Play (audio beeps of Morse from the right pane)

If your original HTML had slightly different labels or button order,
you can tweak the strings in-place below to match your exact layout.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Optional audio (pure‑python) using winsound on Windows.
# On non‑Windows platforms, Play will degrade gracefully without audio.
try:
    import winsound
    HAVE_WINSOUND = True
except Exception:
    HAVE_WINSOUND = False

# ---------------------------
# Morse dictionaries
# ---------------------------
TEXT_TO_MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.',  '(': '-.--.',  ')': '-.--.-', '&': '.-...',  ':': '---...',
    ';': '-.-.-.', '=': '-...-',  '+': '.-.-.',  '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    # Space handled specially; we map it to '/' when encoding words
}

# Build reverse map for decoding
MORSE_TO_TEXT = {m: t for t, m in TEXT_TO_MORSE.items()}

# Settings for audio playback (in milliseconds and frequency Hertz)
DOT_DURATION = 90      # length of a dot
DASH_DURATION = DOT_DURATION * 3
INTRA_CHAR_GAP = DOT_DURATION   # between dots/dashes of same letter
LETTER_GAP = DOT_DURATION * 3
WORD_GAP = DOT_DURATION * 7
TONE_FREQ = 700


class MorseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morse Code Translator")
        self.geometry("980x520")
        self.minsize(820, 480)

        # Global style
        self._style = ttk.Style(self)
        try:
            self.tk.call("source", "sun-valley.tcl")  # if present
            self._style.theme_use("sun-valley-dark")
        except Exception:
            self._style.theme_use("clam")

        self._build_layout()

    # ---------------------------
    # UI construction
    # ---------------------------
    def _build_layout(self):
        outer = ttk.Frame(self, padding=16)
        outer.pack(fill=tk.BOTH, expand=True)

        # Top row: two labels
        header = ttk.Frame(outer)
        header.pack(fill=tk.X)

        self.left_label = ttk.Label(header, text="Plain Text", font=("Segoe UI", 12, "bold"))
        self.left_label.grid(row=0, column=0, sticky="w")

        self.right_label = ttk.Label(header, text="Morse Code", font=("Segoe UI", 12, "bold"))
        self.right_label.grid(row=0, column=2, sticky="e")

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=1)

        # Middle row: two text panes with a vertical button column
        mid = ttk.Frame(outer)
        mid.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        # Left Text (Plain)
        self.left_text = tk.Text(mid, wrap=tk.WORD, undo=True, height=16, font=("Consolas", 11))
        self.left_text.grid(row=0, column=0, sticky="nsew")

        # Center buttons
        ctr = ttk.Frame(mid)
        ctr.grid(row=0, column=1, sticky="ns", padx=10)

        self.btn_text_to_morse = ttk.Button(ctr, text="Text → Morse", command=self.text_to_morse)
        self.btn_morse_to_text = ttk.Button(ctr, text="Morse → Text", command=self.morse_to_text)
        self.btn_swap = ttk.Button(ctr, text="Swap", command=self.swap)
        self.btn_copy = ttk.Button(ctr, text="Copy Output", command=self.copy_output)
        self.btn_clear = ttk.Button(ctr, text="Clear", command=self.clear)
        self.btn_play = ttk.Button(ctr, text="Play", command=self.play_morse)

        for i, b in enumerate([
            self.btn_text_to_morse,
            self.btn_morse_to_text,
            self.btn_swap,
            self.btn_copy,
            self.btn_clear,
            self.btn_play,
        ]):
            b.grid(row=i, column=0, sticky="ew", pady=4)

        # Right Text (Morse)
        self.right_text = tk.Text(mid, wrap=tk.WORD, undo=True, height=16, font=("Consolas", 11))
        self.right_text.grid(row=0, column=2, sticky="nsew")

        # Configure responsive layout
        mid.columnconfigure(0, weight=1)
        mid.columnconfigure(1, weight=0)
        mid.columnconfigure(2, weight=1)
        mid.rowconfigure(0, weight=1)

        # Status bar
        self.status = ttk.Label(outer, text="Ready", anchor="w")
        self.status.pack(fill=tk.X, pady=(8, 0))

    # ---------------------------
    # Core logic
    # ---------------------------
    def normalize_text(self, s: str) -> str:
        # Keep characters we can encode; others are passed through as-is
        return s.replace("\u2013", "-").replace("\u2014", "-")

    def encode_to_morse(self, text: str) -> str:
        text = self.normalize_text(text)
        words = text.split()
        morse_words = []
        for w in words:
            letters = []
            for ch in w.upper():
                if ch == ' ':
                    continue
                code = TEXT_TO_MORSE.get(ch)
                if code is None:
                    # pass through unknowns in square brackets
                    letters.append(f"[{ch}]")
                else:
                    letters.append(code)
            morse_words.append(' '.join(letters))
        # separate words with ' / '
        return ' / '.join(morse_words)

    def decode_from_morse(self, morse: str) -> str:
        # Split words by '/' or 3+ spaces; split letters by single space
        # Normalize consecutive spaces
        morse = ' '.join(morse.strip().split())
        words_raw = [w for w in morse.replace('|', '/').split('/')]
        decoded_words = []
        for w in words_raw:
            chars = []
            for sym in w.strip().split(' '):
                if not sym:
                    continue
                letter = MORSE_TO_TEXT.get(sym)
                if letter is None:
                    chars.append(f"[{sym}]")
                else:
                    chars.append(letter)
            decoded_words.append(''.join(chars))
        return ' '.join(decoded_words)

    # ---------------------------
    # Button callbacks
    # ---------------------------
    def text_to_morse(self):
        src = self.left_text.get("1.0", tk.END).strip()
        out = self.encode_to_morse(src)
        self.right_text.delete("1.0", tk.END)
        self.right_text.insert(tk.END, out)
        self.status.configure(text=f"Encoded {len(src)} characters → Morse")

    def morse_to_text(self):
        src = self.right_text.get("1.0", tk.END).strip()
        out = self.decode_from_morse(src)
        self.left_text.delete("1.0", tk.END)
        self.left_text.insert(tk.END, out)
        self.status.configure(text=f"Decoded Morse → {len(out)} characters")

    def swap(self):
        left = self.left_text.get("1.0", tk.END)
        right = self.right_text.get("1.0", tk.END)
        self.left_text.delete("1.0", tk.END)
        self.right_text.delete("1.0", tk.END)
        self.left_text.insert(tk.END, right.strip())
        self.right_text.insert(tk.END, left.strip())
        self.status.configure(text="Swapped panes")

    def copy_output(self):
        out = self.right_text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(out.strip())
        self.status.configure(text="Copied output to clipboard")

    def clear(self):
        self.left_text.delete("1.0", tk.END)
        self.right_text.delete("1.0", tk.END)
        self.status.configure(text="Cleared")

    def play_morse(self):
        if not HAVE_WINSOUND:
            messagebox.showinfo("Play",
                                "Audio beeps are only available on Windows (winsound).\n"
                                "You can still copy the Morse and play it elsewhere.")
            return
        morse = self.right_text.get("1.0", tk.END).strip()
        self._play_morse_string(morse)

    # ---------------------------
    # Audio helpers (Windows only)
    # ---------------------------
    def _beep(self, duration):
        if HAVE_WINSOUND:
            winsound.Beep(TONE_FREQ, duration)

    def _sleep(self, duration):
        # Busy wait using after; keeps UI responsive
        done = tk.BooleanVar(value=False)
        self.after(duration, lambda: done.set(True))
        self.wait_variable(done)

    def _play_morse_string(self, morse: str):
        # Normalize spaces
        morse = ' '.join(morse.strip().split())
        words = morse.split('/') if '/' in morse else [morse]
        for w_i, w in enumerate(words):
            symbols = [s for s in w.strip().split(' ') if s]
            for i, sym in enumerate(symbols):
                for j, ch in enumerate(sym):
                    if ch == '.':
                        self._beep(DOT_DURATION)
                    elif ch == '-':
                        self._beep(DASH_DURATION)
                    self._sleep(INTRA_CHAR_GAP)
                if i != len(symbols) - 1:
                    self._sleep(LETTER_GAP - INTRA_CHAR_GAP)
            if w_i != len(words) - 1:
                self._sleep(WORD_GAP - LETTER_GAP)


if __name__ == "__main__":
    app = MorseApp()
    app.mainloop()
