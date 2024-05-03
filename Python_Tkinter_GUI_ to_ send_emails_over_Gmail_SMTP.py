import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import os

def browse_file():
    initial_dir = os.getcwd()  # Get the current working directory
    filename = filedialog.askopenfilename(initialdir=initial_dir, title="Select Excel File", filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*")))
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(tk.END, filename)

def send_emails():
    global running
    running = True
    stop_button.config(state=tk.NORMAL)
    send_button.config(state=tk.DISABLED)

    file_path = entry_file_path.get()
    if not file_path or not os.path.isfile(file_path):  # Check if file path is empty or invalid
        status_label.config(text="Invalid file path.")
        stop_button.config(state=tk.DISABLED)
        send_button.config(state=tk.NORMAL)
        return

    console_output.config(state=tk.NORMAL)  # Enable console textbox edit
    console_output.insert(tk.END, "Email send Started\n")
    console_output.config(state=tk.DISABLED)  # Disable console textbox edit
    console_output.update()
    print("Email send Started")
    
    status_label.config(text="Email sending started.")  # Update status label

    smtp_id = entry_smtp_id.get()
    password = entry_password.get()

    if smtp_id and password:
        try:
            df = pd.read_excel(file_path)
            smtp_server = 'smtp.gmail.com'
            port = 587
            sender_email = smtp_id
            message = """\
            Subject: Your Subject Here

            This is a test email sent using Python."""

            for index, row in df.iterrows():
                if not running:
                    break
                name = row['name']
                email = row['email']
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = "Your Subject Here"
                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP(smtp_server, port)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, email, msg.as_string())
                server.quit()

                console_output.config(state=tk.NORMAL)  # Enable console textbox edit
                console_output.insert(tk.END, f"Email sent to {name} at {email}\n")
                console_output.config(state=tk.DISABLED)  # Disable console textbox edit
                console_output.update()
                print(f"Email sent to {name} at {email}")

            if running:
                status_label.config(text="Emails sent successfully!")
            else:
                status_label.config(text="Email sending stopped.")
                console_output.config(state=tk.NORMAL)  # Enable console textbox edit
                console_output.insert(tk.END, "Email sending stopped.\n")
                console_output.config(state=tk.DISABLED)  # Disable console textbox edit
                console_output.update()

        except Exception as e:
            status_label.config(text="Error occurred")  # Update status label with error message
            console_output.config(state=tk.NORMAL)  # Enable console textbox edit
            console_output.insert(tk.END, str(e) + "\n")
            console_output.config(state=tk.DISABLED)  # Disable console textbox edit
            console_output.update()
            print("Error:", e)
    else:
        status_label.config(text="Please fill in all fields.")

    stop_button.config(state=tk.DISABLED)
    send_button.config(state=tk.NORMAL)

def stop_emails():
    global running
    running = False

# Create the main window
window = tk.Tk()
window.title("Send Email from Excel List")

# Set default sender email and password
default_sender_email = "ashloverscn@gmail.com"
default_password = "knnr bofy sbaa zwxe"

# Create widgets
label_file_path = tk.Label(window, text="Select Excel File:")
label_file_path.pack()

entry_file_path = tk.Entry(window, width=50)
entry_file_path.insert(tk.END, os.path.join(os.getcwd(), "contacts.xlsx"))  # Autofill with current working directory and "contacts.xlsx"
entry_file_path.pack()

button_browse = tk.Button(window, text="Browse", command=browse_file)
button_browse.pack()

label_smtp_id = tk.Label(window, text="SMTP ID:")
label_smtp_id.pack()

entry_smtp_id = tk.Entry(window, width=50)
entry_smtp_id.insert(0, default_sender_email)  # Set default sender email
entry_smtp_id.pack()

label_password = tk.Label(window, text="Password:")
label_password.pack()

entry_password = tk.Entry(window, width=50, show="*")
entry_password.insert(0, default_password)  # Set default password
entry_password.pack()

send_button = tk.Button(window, text="Send Emails", command=lambda: threading.Thread(target=send_emails).start())
send_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_emails, state=tk.DISABLED)
stop_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

console_output = ScrolledText(window, width=80, height=20)
console_output.pack()

# Run the main loop
running = False
window.mainloop()
