import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

def import_credentials_json():
    current_working_directory = os.getcwd().replace("\\", "/")
    json_directory_path = filedialog.askdirectory(title="Select JSON File's Directory")
    json_count = 0
    if json_directory_path:
        console_output.insert(tk.END, f"Importing Credential JSON Files from directory: {json_directory_path}\n")
        json_files_list = [f for f in os.listdir(json_directory_path) if f.endswith('.json')]
        for json_file in json_files_list:
            console_output.insert(tk.END, f"{json_file}\n")
        for filename in os.listdir(json_directory_path):
            if filename.endswith(".json"):
                json_file_path = os.path.join(json_directory_path, filename)
                with open(json_file_path, 'rb') as json_file:
                    json_file_binary_data = json_file.read()
                os.makedirs('./credentials', exist_ok=True)
                json_file_output_path = os.path.join(f'./credentials/', filename)
                with open(json_file_output_path, 'wb') as output_json_file:
                    output_json_file.write(json_file_binary_data)
                    json_count = json_count + 1
        console_output.insert(tk.END, f"{json_count} Credential JSON Files Imported to: {current_working_directory}/credentials\n")

def import_credentials_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_output.insert(tk.END, f"Import_Credentials.XLSX: {file_path}\n")

def import_subject_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_output.insert(tk.END, f"Import_Subject.XLSX: {file_path}\n")

def import_from_name_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_output.insert(tk.END, f"Import_FromName.XLSX: {file_path}\n")

def import_body_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_output.insert(tk.END, f"Import_Body.XLSX: {file_path}\n")

def import_contacts_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        console_output.insert(tk.END, f"Import_Contacts.CSV: {file_path}\n")

def import_tfn_phone_no_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
    if file_path:
        console_output.insert(tk.END, f"Import_TFN_PHONE_NO.XLSX: {file_path}\n")

def import_content_html():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        console_output.insert(tk.END, f"Import_Content_HTML: {file_path}\n")

def en_dis_unnec_buttons(state):
    if state == "NORMAL":
        import_credentials_json_button.config(state=tk.NORMAL)
        import_credentials_xlsx_button.config(state=tk.NORMAL)
        import_subject_xlsx_button.config(state=tk.NORMAL)
        import_from_name_xlsx_button.config(state=tk.NORMAL)
        import_body_xlsx_button.config(state=tk.NORMAL)
        import_contacts_csv_button.config(state=tk.NORMAL)
        import_tfn_phone_no_xlsx_button.config(state=tk.NORMAL)
    if state == "DISABLED":
        import_credentials_json_button.config(state=tk.DISABLED)
        import_credentials_xlsx_button.config(state=tk.DISABLED)
        import_subject_xlsx_button.config(state=tk.DISABLED)
        import_from_name_xlsx_button.config(state=tk.DISABLED)
        import_body_xlsx_button.config(state=tk.DISABLED)
        import_contacts_csv_button.config(state=tk.DISABLED)
        import_tfn_phone_no_xlsx_button.config(state=tk.DISABLED)

def send_data():
    if send_button.cget("text") == "Send":
        en_dis_unnec_buttons("DISABLED")
        send_button.config(text="Sending", fg="green")
        console_output.insert(tk.END, "Sending...\n")
        console_output.update()
        print("Data sent!")
        # Add additional logic if needed
    else:
        en_dis_unnec_buttons("NORMAL")
        send_button.config(text="Send", fg="red")
        console_output.insert(tk.END, "Sending stopped.\n")
        console_output.update()
        
# Create the main window
window = tk.Tk()
window.title("Gmail-API-X Email Sender")
# to use Sysem executable icon compile with pyinstaller as follows to pack the ico file in the exe :
# pyinstaller --clean --noconsole --onefile --icon=Gmail-API-X.ico --add-data "Gmail-API-X.ico;." test__gui.py
#window.iconbitmap(sys.executable) # did not work for me
# the unSmarter way is to rely only on the MEIPASS temp_dir for the icon file path, available only afer the exe is ready
#window.iconbitmap(True, default=str(sys._MEIPASS) +"/"+ "Gmail-API-X.ico")
# the Smarter way is to keep a fail-Safe using a function for the icon file path, packed in the exe and as well from the present working directory
def icon_path(ico_file_path):    
    try:       
        root_path = sys._MEIPASS
    except Exception:
        root_path = os.path.abspath(".")
    return os.path.join(root_path, ico_file_path)
window.iconbitmap(True, default=icon_path("Gmail-API-X.ico"))

# Set the style to use the 'clam' theme (Windows theme)
style = ttk.Style()
style.theme_use("winnative")
#style.theme_use("vista")
#style.theme_use("xpnative")

# Create and pack buttons using grid with padding set to 0
import_credentials_json_button = tk.Button(window, text="Import_Credentials.JSON", command=import_credentials_json)
import_credentials_json_button.grid(row=0, column=0, padx=0, pady=0)

import_credentials_xlsx_button = tk.Button(window, text="Import_Credentials.XLSX", command=import_credentials_xlsx)
import_credentials_xlsx_button.grid(row=0, column=1, padx=0, pady=0)

import_subject_xlsx_button = tk.Button(window, text="Import_Subject.XLSX", command=import_subject_xlsx)
import_subject_xlsx_button.grid(row=0, column=2, padx=0, pady=0)

import_from_name_xlsx_button = tk.Button(window, text="Import_FromName.XLSX", command=import_from_name_xlsx)
import_from_name_xlsx_button.grid(row=0, column=3, padx=0, pady=0)

import_body_xlsx_button = tk.Button(window, text="Import_Body.XLSX", command=import_body_xlsx)
import_body_xlsx_button.grid(row=0, column=4, padx=0, pady=0)

import_contacts_csv_button = tk.Button(window, text="Import_Contacts.CSV", command=import_contacts_csv)
import_contacts_csv_button.grid(row=0, column=5, padx=0, pady=0)

import_tfn_phone_no_xlsx_button = tk.Button(window, text="Import_TFN_PHONE_NO.XLSX", command=import_tfn_phone_no_xlsx)
import_tfn_phone_no_xlsx_button.grid(row=0, column=6, padx=0, pady=0)

import_content_html_button = tk.Button(window, text="Import_Content_HTML", command=import_content_html)
import_content_html_button.grid(row=0, column=7, padx=0, pady=0)

# Create and pack the Send button using grid, placed in row 0 and right-aligned
send_button = tk.Button(window, text="Send", width=8, height=0,  command=send_data)
send_button.grid(row=0, column=8, padx=0, pady=0)

# Create a bottom-aligned listbox for console output using grid
console_output = ScrolledText(window, width=70, height=10)
console_output.grid(row=1, column=0, columnspan=9, padx=5, pady=5, sticky="nsew")

# Configure row and column to expand with window resizing
window.rowconfigure(1, weight=1)
##window.columnconfigure(0, weight=1)

# Run the Tkinter event loop
window.mainloop()
