import tkinter as tk
import time

# Morse code dictionary including letters, numbers, and some special characters
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
    '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&',
    '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-',
    '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@'
}

class MorseDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Decoder")
        self.mode = tk.StringVar(value="single")  # single or double paddle

        # GUI Layout
        tk.Label(root, text="Morse Code Decoder", font=("Arial", 16)).pack(pady=5)
        tk.Label(root, text="Mode:").pack()
        tk.Radiobutton(root, text="Single Paddle (K key)", variable=self.mode, value="single").pack()
        tk.Radiobutton(root, text="Double Paddle (K=dit, L=dah)", variable=self.mode, value="double").pack()

        # Label to show current symbol
        self.current_symbol_label = tk.Label(root, text="", font=("Arial", 18), fg="blue")
        self.current_symbol_label.pack(pady=5)

        # Read-only text box
        self.text_box = tk.Text(root, height=10, width=50, font=("Arial", 14), state="disabled")
        self.text_box.pack(pady=10)

        # Variables for Morse decoding
        self.current_symbol = ""
        self.last_press_time = 0
        self.press_start = 0
        self.in_letter = False

        # Key bindings
        root.bind("<KeyPress>", self.key_press)
        root.bind("<KeyRelease>", self.key_release)
        root.bind("<BackSpace>", self.erase_char)
        root.bind("<Delete>", self.erase_char)

        # Update loop for letter separation
        self.root.after(100, self.update_loop)

    def key_press(self, event):
        key = event.keysym.upper()
        if self.mode.get() == "single":
            if key == 'K' and not self.in_letter:
                self.press_start = time.time()
                self.in_letter = True
        else:  # double paddle mode
            if key == 'K':
                self.current_symbol += '.'
                self.update_symbol_label()
            elif key == 'L':
                self.current_symbol += '-'
                self.update_symbol_label()

    def key_release(self, event):
        key = event.keysym.upper()
        if self.mode.get() == "single" and key == 'K' and self.in_letter:
            pulse = time.time() - self.press_start
            if pulse < 0.25:  # short pulse = dit
                self.current_symbol += '.'
            else:           # long pulse = dah
                self.current_symbol += '-'
            self.update_symbol_label()
            self.in_letter = False
            self.last_press_time = time.time()

    def update_symbol_label(self):
        self.current_symbol_label.config(text=self.current_symbol)

    def update_loop(self):
        # Check for letter separation in single-paddle mode
        if self.mode.get() == "single" and not self.in_letter and self.current_symbol:
            if time.time() - self.last_press_time > 0.5:
                self.add_symbol_to_text()
        self.root.after(100, self.update_loop)

    def add_symbol_to_text(self):
        char = MORSE_CODE_DICT.get(self.current_symbol, '?')
        self.text_box.config(state="normal")       # enable temporarily
        self.text_box.insert(tk.END, char)
        self.text_box.see(tk.END)
        self.text_box.config(state="disabled")     # disable again
        self.current_symbol = ""
        self.update_symbol_label()  # clear label
        self.last_press_time = time.time()

    def erase_char(self, event):
        self.text_box.config(state="normal")
        text_content = self.text_box.get("1.0", tk.END)
        if len(text_content) > 1:  # remove one character before the END
            self.text_box.delete(f"{tk.END}-2c", tk.END)
        self.text_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseDecoder(root)
    root.mainloop()
