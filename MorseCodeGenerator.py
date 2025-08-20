import tkinter as tk
from tkinter import messagebox, filedialog
import time
import winsound  # Only works on Windows
import threading

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',
    'D': '-..',   'E': '.',     'F': '..-.',
    'G': '--.',   'H': '....',  'I': '..',
    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',
    'S': '...',   'T': '-',     'U': '..-',
    'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': ' '
}

# Sound and timing
DOT_DURATION = 200  # milliseconds
DASH_DURATION = DOT_DURATION * 3
FREQUENCY = 750  # Hz
GAP_BETWEEN_SYMBOLS = DOT_DURATION / 1000
GAP_BETWEEN_LETTERS = DOT_DURATION * 3 / 1000
GAP_BETWEEN_WORDS = DOT_DURATION * 7 / 1000

def text_to_morse(text):
    return '   '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def blink_led(symbol):
    if symbol == '.':
        led.config(bg="yellow")
        time.sleep(DOT_DURATION / 1000)
    elif symbol == '-':
        led.config(bg="red")
        time.sleep(DASH_DURATION / 1000)
    led.config(bg="black")
    time.sleep(GAP_BETWEEN_SYMBOLS)

def play_morse(text):
    start_time = time.time()
    total_dots = 0  # Count dot units to estimate WPM

    for char in text.upper():
        if char not in MORSE_CODE_DICT:
            continue

        morse = MORSE_CODE_DICT[char]

        # Update current character label
        update_current_char(char, morse)

        if morse == ' ':
            time.sleep(GAP_BETWEEN_WORDS)
            continue

        for symbol in morse:
            # Count dots and dashes as dot units
            if symbol == '.':
                total_dots += 1
                winsound.Beep(FREQUENCY, DOT_DURATION)
                blink_led(symbol)
            elif symbol == '-':
                total_dots += 3
                winsound.Beep(FREQUENCY, DASH_DURATION)
                blink_led(symbol)

        time.sleep(GAP_BETWEEN_LETTERS)

    end_time = time.time()
    duration_sec = end_time - start_time
    wpm = calculate_wpm(total_dots, duration_sec)
    update_wpm_display(wpm)
    update_current_char("", "")  # Clear after done

def calculate_wpm(total_dots, duration_sec):
    # 50 dot units per word (standard "PARIS" word)
    if duration_sec == 0:
        return 0
    words = total_dots / 50
    minutes = duration_sec / 60
    wpm = words / minutes
    return round(wpm, 2)

def update_wpm_display(wpm):
    wpm_label.config(text=f"WPM: {wpm}")

def update_current_char(char, morse):
    current_char_label.config(text=f"Now Playing: {char}   Morse: {morse}")

def on_submit(event=None):
    text = entry.get().strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    morse = text_to_morse(text)

    # Show in terminal
    terminal.configure(state='normal')
    terminal.insert(tk.END, f"Text : {text}\n", "bold")
    terminal.insert(tk.END, f"Morse: {morse}\n\n", "bold")
    terminal.see(tk.END)
    terminal.configure(state='disabled')

    global last_morse_output
    last_morse_output = morse

    # Clear WPM display before starting
    update_wpm_display(0)

    threading.Thread(target=play_morse, args=(text,), daemon=True).start()

def copy_to_clipboard():
    if not last_morse_output:
        messagebox.showinfo("Clipboard", "No Morse code to copy yet.")
        return
    root.clipboard_clear()
    root.clipboard_append(last_morse_output)
    messagebox.showinfo("Clipboard", "Morse code copied to clipboard.")

def save_log():
    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Text Files", "*.txt")],
                                         title="Save Morse Log")
    if not file:
        return
    try:
        content = terminal.get("1.0", tk.END)
        with open(file, 'w') as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Log saved to {file}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Morse Code Terminal")

# Entry
entry = tk.Entry(root, width=40, font=("Consolas", 12))
entry.pack(pady=10)
entry.focus_set()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Play Morse Code", command=on_submit).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Copy to Clipboard", command=copy_to_clipboard).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Save Log to File", command=save_log).pack(side=tk.LEFT, padx=5)

# Terminal display
terminal = tk.Text(root, height=15, width=60, bg="black", fg="white", font=("Consolas", 12, "bold"))
terminal.pack(padx=10, pady=10)
terminal.tag_config("bold", font=("Consolas", 12, "bold"))
terminal.configure(state='disabled')

# Scrollbar
scroll = tk.Scrollbar(root, command=terminal.yview)
terminal.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# LED display
led = tk.Label(root, bg="black", width=10, height=2, relief=tk.SUNKEN)
led.pack(pady=10)

# Now playing character display
current_char_label = tk.Label(root, text="Now Playing: ", font=("Consolas", 14, "bold"))
current_char_label.pack(pady=(0, 10))

# WPM display
wpm_label = tk.Label(root, text="WPM: 0", font=("Consolas", 14, "bold"))
wpm_label.pack(pady=(0, 10))

# Bind Enter key
root.bind('<Return>', on_submit)

# Global for clipboard
last_morse_output = ""

root.mainloop()
