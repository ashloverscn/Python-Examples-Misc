import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os

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
root = tk.Tk()
root.title("File Browser Example")

# Set the style to use the 'clam' theme (Windows theme)
style = ttk.Style()
style.theme_use("clam")

# Create a bottom-aligned listbox for console output
console_listbox = tk.Listbox(root, width=70, height=10, justify=tk.LEFT)
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
    button = tk.Button(root, text=button_text, command=command_func)
    button.pack(side=tk.LEFT)

# Create a "Send" button with initial text "Send" and color red
send_button = tk.Button(root, text="Send", command=send_data, fg="red")
send_button.pack(side=tk.BOTTOM, pady=10)

# Run the Tkinter event loop
root.mainloop()
