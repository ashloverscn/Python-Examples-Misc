import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import os
import base64
from base64 import b64decode, b64decode

def import_content_html():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_Content_HTML: {file_path}")

def import_credentials_json():
    if directory_path:
        console_listbox.insert(tk.END, f"Import_Credentials.JSON from directory: {directory_path}")

        # Call the import_credentials function with the selected directory path
        import_credentials(directory_path)

def import_credentials(directory_path):
    # Ensure the output directory exists
    os.makedirs('./credentials', exist_ok=True)

    # Iterate through all files in the selected directory with the .json extension
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)

            # Read the contents of the selected file in binary mode
            with open(file_path, 'rb') as file:
                binary_data = file.read()

            # Write the binary contents to the ./credentials/ directory
            output_file_path = os.path.join(f'./credentials/', filename)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(binary_data)
                console_listbox.insert(tk.END, f"File successfully written as binary to {output_file_path}")

def import_credentials_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_Credentials.XLSX: {file_path}")

def import_from_name_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_FromName.XLSX: {file_path}")

def import_contacts_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_Contacts.CSV: {file_path}")

def import_body_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_Body.XLSX: {file_path}")

def import_subject_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_Subject.XLSX: {file_path}")

def import_tfn_phone_no_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_listbox.insert(tk.END, f"Import_TFN_PHONE_NO.XLSX: {file_path}")

def send_data():
    if send_button.cget("text") == "Send":
        send_button.config(text="Sending", fg="green")
        console_listbox.insert(tk.END, "Sending...")
        print("Data sent!")
        # Add additional logic if needed
    else:
        send_button.config(text="Send", fg="red")
        console_listbox.insert(tk.END, "Sending stopped.")

# Create the main window
window = tk.Tk()
window.title("Gmail-API-X Email Sender")
#window.iconphoto(True, tk.PhotoImage(file="X2.png"))
window.iconphoto(True, tk.PhotoImage(data=b64decode("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")))

# Set the style to use the 'clam' theme (Windows theme)
style = ttk.Style()
style.theme_use("winnative")
#style.theme_use("vista")
#style.theme_use("xpnative")

# Create a bottom-aligned listbox for console output
console_listbox = tk.Listbox(window, width=70, height=10, justify=tk.LEFT)
console_listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create and pack buttons
buttons_info = [
    ("Import_Content_HTML", import_content_html),
    ("Import_Credentials.JSON", import_credentials_json),
    ("Import_Credentials.XLSX", import_credentials_xlsx),
    ("Import_FromName.XLSX", import_from_name_xlsx),
    ("Import_Contacts.CSV", import_contacts_csv),
    ("Import_Body.XLSX", import_body_xlsx),
    ("Import_Subject.XLSX", import_subject_xlsx),
    ("Import_TFN_PHONE_NO.XLSX", import_tfn_phone_no_xlsx),
]

for button_text, command_func in buttons_info:
    button = tk.Button(window, text=button_text, command=command_func)
    button.pack(side=tk.LEFT)

# Create a "Send" button with initial text "Send" and color red
send_button = tk.Button(window, text="Send", command=send_data, fg="red")
send_button.pack(side=tk.BOTTOM, pady=10)

# Run the Tkinter event loop
window.mainloop()
