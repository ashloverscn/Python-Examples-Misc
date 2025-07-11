#https://pythonassets.com/posts/window-icon-in-tk-tkinter/
#https://stackoverflow.com/questions/33137829/how-to-replace-the-icon-in-a-tkinter-app
#https://www.freeconvert.com/png-to-ico
#https://www.base64-image.de/
#https://base64-viewer.onrender.com/
#https://stackoverflow.com/questions/42474560/pyinstaller-single-exe-file-ico-image-in-title-of-tkinter-main-window

import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk,ImageFont, ImageDraw
import base64
from base64 import b64encode, b64decode

# Create the main window
window = tk.Tk()
window.title("tk window base64 icon logo")
window.geometry("400x200")
# to use Sysem executable icon compile with pyinstaller as follows to pack the ico file in the exe :
# pyinstaller --clean --noconsole --onefile --icon=X2.ico --add-data "X2.ico;." python_tk_window-base64_encoded_icon.py
#window.iconbitmap(sys.executable) # did not work for me
# the unSmarter way is to rely only on the MEIPASS temp_dir for the icon file path, available only afer the exe is ready
#window.iconbitmap(True, default=str(sys._MEIPASS) +"/"+ "X2.ico")
# the Smarter way is to keep a fail-Safe using a function for the icon file path, packed in the exe and as well from the present working directory
def icon_path(ico_file_path):    
    try:       
        root_path = sys._MEIPASS
    except Exception:
        root_path = os.path.abspath(".")
    return os.path.join(root_path, ico_file_path)
window.iconbitmap(True, default=icon_path("X2.ico"))
# True=AllWindow False=ThisWindow
#window.iconbitmap(True, "X2.ico")
#window.iconphoto(True, tk.PhotoImage(file="X2.png"))
# using large and small icons for different use cases ex: L=32-TaskBar S=16-TkWindow
#window.iconphoto(True, tk.PhotoImage(file="X2-32.png"), ImageTk.PhotoImage(file="X2-16.png"))
# using base64 encoded image
#window.iconphoto(True, tk.PhotoImage(data=b64decode("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")))

# Universal way using PILlow calsse's ImageTk function for using unsupported image format
#window.iconphoto(True, ImageTk.PhotoImage(file="X2.ico"))
#window.iconphoto(True, ImageTk.PhotoImage(file="X2.png"))
#window.iconphoto(True, ImageTk.PhotoImage(file="X2.jpg"))
#window.iconphoto(True, ImageTk.PhotoImage(file="X2.jpeg"))
# using large and small icons for different use cases ex: L=32-TaskBar S=16-TkWindow
#window.iconphoto(True, ImageTk.PhotoImage(file="X2-32.png"), ImageTk.PhotoImage(file="X2-16.png"))
# using base64 encoded image
#window.iconphoto(True, ImageTk.PhotoImage(data=b64decode("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")))

# Set the style to use the 'clam' theme (Windows theme)
style = ttk.Style()
style.theme_use("winnative")
#style.theme_use("vista")
#style.theme_use("xpnative")

# Run the Tkinter event loop
window.mainloop()
