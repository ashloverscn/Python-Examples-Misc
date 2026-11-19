import re
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

SECTOR_SIZE = 2352
MODE1_DATA_OFFSET = 16
MODE1_DATA_SIZE = 2048
MODE2_FORM1_DATA_OFFSET = 24
MODE2_FORM1_DATA_SIZE = 2048


def resolve_bin_and_track(cue_path: Path) -> tuple[Path, int, str]:
    """Resolve the .bin file in the same directory as cue_path plus (start_sector, mode)."""
    bin_filename = None
    current_mode = "MODE1/2352"
    first_data_mode = None
    first_index01_sector = None

    line_re = re.compile(r"^\s*([A-Z0-9]+)\s+(.*)$", re.IGNORECASE)
    index_re = re.compile(r"^\s*0?1\s+(\d+):(\d+):(\d+)\s*$")

    with cue_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            m = line_re.match(line)
            if not m:
                continue

            cmd = m.group(1).upper()
            rest = m.group(2).strip()

            if cmd == "FILE" and bin_filename is None:
                if rest.startswith('"'):
                    end_q = rest.find('"', 1)
                    if end_q != -1:
                        bin_filename = rest[1:end_q]
                else:
                    bin_filename = rest.split()[0]

            elif cmd == "TRACK":
                parts = rest.split()
                if len(parts) >= 2:
                    current_mode = parts[1].upper()
                    if "AUDIO" not in current_mode and first_data_mode is None:
                        first_data_mode = current_mode

            elif cmd == "INDEX":
                idx_match = index_re.match(rest)
                if idx_match and "AUDIO" not in current_mode and first_index01_sector is None:
                    minutes = int(idx_match.group(1))
                    seconds = int(idx_match.group(2))
                    frames = int(idx_match.group(3))
                    first_index01_sector = (minutes * 60 + seconds) * 75 + frames

    # Always look in the same directory as the selected .cue file
    candidates: list[Path] = []
    if bin_filename:
        candidates.append(cue_path.parent / Path(bin_filename).name)
    candidates.append(cue_path.with_suffix(".bin"))

    bin_path = next((p.resolve() for p in candidates if p.is_file()), None)
    if bin_path is None:
        checked = "\n".join(str(p.resolve()) for p in candidates)
        raise FileNotFoundError(f"Could not find matching BIN file in CUE folder:\n{checked}")

    mode = first_data_mode or "MODE1/2352"
    start_sector = first_index01_sector or 0
    return bin_path, start_sector, mode


class CueToIsoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CUE to ISO Converter")
        self.root.resizable(False, False)

        self.cue_var = tk.StringVar()
        self.iso_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Select a CUE file to begin.")
        self.is_converting = False

        self._build_ui()

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}
        frame = ttk.Frame(self.root, padding=14)
        frame.grid(row=0, column=0, sticky="nsew")

        # Row 0: CUE File Chooser
        ttk.Label(frame, text="CUE File:").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.cue_var, width=52).grid(row=0, column=1, **pad)
        ttk.Button(frame, text="Browse...", command=self.browse_cue).grid(row=0, column=2, **pad)

        # Row 1: Output ISO Chooser
        ttk.Label(frame, text="Output ISO:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.iso_var, width=52).grid(row=1, column=1, **pad)
        ttk.Button(frame, text="Save As...", command=self.browse_iso).grid(row=1, column=2, **pad)

        # Row 2: Progress bar
        self.progress = ttk.Progressbar(frame, mode="determinate", length=440)
        self.progress.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(12, 4))

        # Row 3: Status label
        ttk.Label(frame, textvariable=self.status_var, foreground="#333333").grid(
            row=3, column=0, columnspan=3, sticky="w", padx=10, pady=(2, 10)
        )

        # Row 4: Convert button
        self.convert_btn = ttk.Button(frame, text="Convert", command=self.start_conversion)
        self.convert_btn.grid(row=4, column=0, columnspan=3, pady=(4, 2), ipadx=20, ipady=4)

    def browse_cue(self) -> None:
        path_str = filedialog.askopenfilename(
            title="Select CUE File",
            filetypes=[("CUE Sheet Files", "*.cue"), ("All Files", "*.*")],
        )
        if not path_str:
            return

        cue_path = Path(path_str)
        self.cue_var.set(str(cue_path))
        self.iso_var.set(str(cue_path.with_suffix(".iso")))
        self.status_var.set(f"Ready: {cue_path.name}")

    def browse_iso(self) -> None:
        initial_name = "output.iso"
        if self.iso_var.get().strip():
            initial_name = Path(self.iso_var.get().strip()).name
        elif self.cue_var.get().strip():
            initial_name = Path(self.cue_var.get().strip()).with_suffix(".iso").name

        path_str = filedialog.asksaveasfilename(
            title="Save ISO File As",
            initialfile=initial_name,
            defaultextension=".iso",
            filetypes=[("ISO Disc Images", "*.iso"), ("All Files", "*.*")],
        )
        if path_str:
            self.iso_var.set(path_str)

    def start_conversion(self) -> None:
        if self.is_converting:
            return

        cue_str = self.cue_var.get().strip()
        iso_str = self.iso_var.get().strip()

        if not cue_str:
            messagebox.showerror("Missing CUE File", "Please select a .cue file.")
            return
        if not iso_str:
            messagebox.showerror("Missing Output Path", "Please choose an output .iso path.")
            return

        cue_path = Path(cue_str)
        if not cue_path.is_file():
            messagebox.showerror("File Not Found", f"CUE file not found:\n{cue_path}")
            return

        iso_path = Path(iso_str)

        self.is_converting = True
        self.convert_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_var.set("Resolving BIN file and converting...")

        threading.Thread(
            target=self._convert_worker,
            args=(cue_path, iso_path),
            daemon=True,
        ).start()

    def _convert_worker(self, cue_path: Path, iso_path: Path) -> None:
        try:
            bin_path, start_sector, mode = resolve_bin_and_track(cue_path)

            if "AUDIO" in mode:
                raise ValueError(f"Track mode '{mode}' is audio, not a CD-ROM data track.")

            if "MODE2/2352" in mode:
                offset, length = MODE2_FORM1_DATA_OFFSET, MODE2_FORM1_DATA_SIZE
            else:
                offset, length = MODE1_DATA_OFFSET, MODE1_DATA_SIZE

            file_size = bin_path.stat().st_size
            byte_offset = start_sector * SECTOR_SIZE
            if byte_offset >= file_size:
                raise ValueError("CUE start sector exceeds BIN file size.")

            total_sectors = (file_size - byte_offset) // SECTOR_SIZE
            if total_sectors <= 0:
                raise ValueError("No full 2352-byte sectors found in BIN file.")

            sectors_written = 0
            update_interval = max(1, total_sectors // 100)

            with bin_path.open("rb") as src, iso_path.open("wb") as dst:
                if byte_offset > 0:
                    src.seek(byte_offset)

                while True:
                    sector = src.read(SECTOR_SIZE)
                    if len(sector) < SECTOR_SIZE:
                        break
                    dst.write(sector[offset : offset + length])
                    sectors_written += 1

                    if sectors_written % update_interval == 0:
                        pct = min(100.0, (sectors_written / total_sectors) * 100.0)
                        self.root.after(0, self._update_progress, pct, sectors_written, total_sectors)

            size_mb = (sectors_written * length) / (1024 * 1024)
            self.root.after(0, self._on_success, iso_path, bin_path.name, sectors_written, size_mb, mode)

        except Exception as exc:
            self.root.after(0, self._on_error, str(exc))

    def _update_progress(self, pct: float, done: int, total: int) -> None:
        self.progress["value"] = pct
        self.status_var.set(f"Converting... {pct:.0f}% ({done:,} / {total:,} sectors)")

    def _on_success(self, iso_path: Path, bin_name: str, sectors: int, size_mb: float, mode: str) -> None:
        self.is_converting = False
        self.convert_btn.config(state="normal")
        self.progress["value"] = 100
        self.status_var.set(f"Done: {sectors:,} sectors ({size_mb:.2f} MB) from {bin_name}")
        messagebox.showinfo(
            "Conversion Complete",
            f"Created:\n{iso_path}\n\nSource BIN: {bin_name}\nMode: {mode}\nSize: {size_mb:.2f} MB",
        )

    def _on_error(self, error_msg: str) -> None:
        self.is_converting = False
        self.convert_btn.config(state="normal")
        self.status_var.set("Conversion failed.")
        messagebox.showerror("Conversion Error", error_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = CueToIsoApp(root)
    root.mainloop()
