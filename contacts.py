import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os

FILE_NAME = "contact_data.xlsx"

def initialize_excel():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["First Name", "Middle Name", "Last Name", "Phone", "Address"])
        df.to_excel(FILE_NAME, index=False)

def add_entry():
    data = {k: v.get().strip() for k, v in combos.items()}
    if data["fname"] and data["lname"] and data["phone"] and data["address"]:
        df = pd.read_excel(FILE_NAME)
        new_row = {
            "First Name": data["fname"], "Middle Name": data["mname"], 
            "Last Name": data["lname"], "Phone": data["phone"], "Address": data["address"]
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(FILE_NAME, index=False)
        clear_fields()
        messagebox.showinfo("Success", "Contact added successfully!")
    else:
        messagebox.showwarning("Input Error", "Required: First, Last, Phone, Address")

def search_entry():
    # Gather search terms from any field that isn't empty
    search_criteria = {k: v.get().strip() for k, v in combos.items() if v.get().strip()}
    
    if not search_criteria:
        messagebox.showwarning("Input Error", "Enter data in any field to search.")
        return

    df = pd.read_excel(FILE_NAME)
    col_map = {"fname": "First Name", "mname": "Middle Name", "lname": "Last Name", "phone": "Phone", "address": "Address"}
    
    results = df
    for key, value in search_criteria.items():
        results = results[results[col_map[key]].astype(str).str.contains(value, case=False, na=False)]

    if results.empty:
        messagebox.showinfo("No Results", "No matching contacts found.")
    else:
        # 1. Update all dropdown lists with the full results set
        for key, col in col_map.items():
            combos[key]['values'] = results[col].fillna("").astype(str).tolist()
        
        # 2. Automatically show the FIRST result in the text region
        fill_form(results.iloc[0])
        
        if len(results) > 1:
            messagebox.showinfo("Multiple Found", f"Found {len(results)} matches. First one displayed; use dropdowns to see others.")

def on_select(event):
    # If user manually picks an item from a dropdown, sync all fields to that record
    caller = event.widget
    selected_val = caller.get()
    
    df = pd.read_excel(FILE_NAME)
    # Search for the full record matching the selected string
    # We check across all columns to find the row that contains this specific value
    results = df[df.apply(lambda row: row.astype(str).str.contains(selected_val, case=False).any(), axis=1)]
    
    if not results.empty:
        fill_form(results.iloc[0])

def fill_form(row):
    # Updates the text visible in the boxes
    combos["fname"].set(row["First Name"])
    combos["mname"].set(str(row["Middle Name"]) if pd.notna(row["Middle Name"]) else "")
    combos["lname"].set(row["Last Name"])
    combos["phone"].set(row["Phone"])
    combos["address"].set(row["Address"])

def delete_entry():
    f_name = combos["fname"].get().strip()
    l_name = combos["lname"].get().strip()
    
    if not f_name or not l_name:
        messagebox.showwarning("Delete Error", "Need First and Last Name to delete.")
        return

    df = pd.read_excel(FILE_NAME)
    initial_len = len(df)
    df = df[~((df['First Name'] == f_name) & (df['Last Name'] == l_name))]
    
    if len(df) < initial_len:
        df.to_excel(FILE_NAME, index=False)
        clear_fields()
        messagebox.showinfo("Deleted", "Contact removed.")
    else:
        messagebox.showerror("Error", "Contact not found.")

def clear_fields():
    for cb in combos.values():
        cb.set('')
        cb['values'] = []

# --- GUI Setup ---
root = tk.Tk()
root.title("Contact Manager - Auto-Fill Search")
root.geometry("500x420")
initialize_excel()

main_frame = ttk.Frame(root, padding="25")
main_frame.pack(expand=True, fill="both")

field_labels = [
    ("First Name:", "fname"),
    ("Middle Name (Opt):", "mname"),
    ("Last Name:", "lname"),
    ("Phone:", "phone"),
    ("Address:", "address")
]

combos = {}
for i, (label_text, key) in enumerate(field_labels):
    ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=8)
    # Each field is a Combobox
    cb = ttk.Combobox(main_frame, width=35)
    cb.grid(row=i, column=1, pady=8, padx=10)
    # Bind selection event
    cb.bind("<<ComboboxSelected>>", on_select)
    combos[key] = cb

# Buttons
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=6, column=0, columnspan=2, pady=25)

ttk.Button(btn_frame, text="Add", command=add_entry).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Search", command=search_entry).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Delete", command=delete_entry).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Clear", command=clear_fields).grid(row=0, column=3, padx=5)

root.mainloop()