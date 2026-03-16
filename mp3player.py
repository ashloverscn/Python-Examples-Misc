import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Audio Player")
        self.root.geometry("400x450")
        self.root.configure(bg="#2c3e50")

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # State Variables
        self.playlist = []
        self.current_index = 0
        self.paused = False

        # --- GUI Elements ---
        
        # Title Label
        self.label = tk.Label(root, text="Now Playing", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.label.pack(pady=10)

        # Playlist Box
        self.listbox = tk.Listbox(root, bg="#34495e", fg="white", width=45, height=10, selectbackground="#1abc9c")
        self.listbox.pack(pady=5, padx=20)

        # Control Frame
        controls_frame = tk.Frame(root, bg="#2c3e50")
        controls_frame.pack(pady=20)

        # Buttons
        self.btn_prev = tk.Button(controls_frame, text="⏮", command=self.prev_song, width=5)
        self.btn_play = tk.Button(controls_frame, text="▶", command=self.play_song, width=5)
        self.btn_pause = tk.Button(controls_frame, text="⏸", command=self.pause_song, width=5)
        self.btn_next = tk.Button(controls_frame, text="⏭", command=self.next_song, width=5)

        self.btn_prev.grid(row=0, column=0, padx=5)
        self.btn_play.grid(row=0, column=1, padx=5)
        self.btn_pause.grid(row=0, column=2, padx=5)
        self.btn_next.grid(row=0, column=3, padx=5)

        # Volume Slider
        self.volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, 
                                     label="Volume", bg="#2c3e50", fg="white", command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)

        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.load_music)

    def load_music(self):
        directory = filedialog.askdirectory()
        if directory:
            os.chdir(directory)
            songs = os.listdir(directory)
            self.playlist = [song for song in songs if song.endswith(".mp3")]
            
            self.listbox.delete(0, tk.END)
            for song in self.playlist:
                self.listbox.insert(tk.END, song)

    def play_song(self):
        try:
            selected_song = self.listbox.curselection()
            if selected_song:
                self.current_index = selected_song[0]
                song_name = self.listbox.get(self.current_index)
                
                pygame.mixer.music.load(song_name)
                pygame.mixer.music.play()
                self.label.config(text=f"Playing: {song_name}")
                self.paused = False
        except Exception as e:
            messagebox.showerror("Error", f"Could not play file: {e}")

    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.play_song()

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.play_song()

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Player(root)
    root.mainloop()