#============================================================================================
from licensing.models import *
from licensing.methods import Key, Helpers
import base64
import re
import pandas as pd
import random
from random import randint, choices
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from jinja2 import Template
import ssl
import smtplib
import logging
import time
import sys
import pdfkit
import imgkit
import img2pdf
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import os.path
from pathlib import Path
import platform
import tempfile
import string
from datetime import date
import uuid
import datetime
from faker import Faker
import names
import tkinter as tk
from tkinter import messagebox
#============================================================================================
RSAPubKey = "<RSAKeyValue><Modulus>m8Fwe6Kmm72kg8IYNhkzaThD37lNwtQzkC6ihUS+OcOLnCQD9VPtbJsWfcQPTxsgvGMvaPaLDRpjOp9X5drUuESMixR1DxCxTHfQx7Fe1BDif2vOds6O7XnqHqXM5XgHMovVADl5sMFKdLFpuSmqkq6lE/Gz1HmthsffgcI1eGx5WbOMjTzBpJ1/4HKgkvJTS5J8vW1NRqyLHy5YMsm+l4bmav1qnchFTLc/bFhB39LtdWLN24PTalKE6x9Hn6vDI+i+b0rFWncQNc83Ryh8kglw2RW2HLRv1r+qeCoBD2F5rJ2wEmriqZbvkorxHTDvosNWbPsPFT7JYglxC+QVDQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIxMDAxNzUxMDgiLCJoeVlGWkNRaTJuT0JPbjhYcE1nTkZiNm5JeEpxQmxXZFRJSzhBSWxJIl0="
product_id = "28327"
#============================================================================================
class ListboxRedirector:
    def __init__(self, listbox):
        self.listbox = listbox
    def write(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.yview(tk.END)
    def flush(self):
        pass
#============================================================================================
root = tk.Tk()
root.title("License Key Validation")
root.geometry("800x600")
listbox_frame = tk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
sys.stdout = ListboxRedirector(listbox)
#============================================================================================
key = ''
user = ''
LicenceKeyPath = str(Path('/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir())) + '\Gmail-API-X-Licence.key'
#============================================================================================
def validate_license(user, key):
    global activation
    result = Key.activate(token=auth, rsa_pub_key=RSAPubKey, product_id=int(product_id), key=key, machine_code=Helpers.GetMachineCode(v=2))
    if result[0] is None or not Helpers.IsOnRightMachine(result[0], v=2):
        activation = False
        os.remove(LicenceKeyPath)
        print(str(user) + " license does not work: {0}".format(result[1]))
        return False
    else:
        activation = True
        print(str(user) + " license is valid!")
        license_key = result[0]
        print(str(user) + " license expires: " + str(license_key.expires))
        return True
def show_login_window():
    root.withdraw()
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")
    tk.Label(login_window, text="Username:").pack(pady=5)
    user_entry = tk.Entry(login_window)
    user_entry.pack(pady=5)
    tk.Label(login_window, text="License Key:").pack(pady=5)
    key_entry = tk.Entry(login_window, show="*")
    key_entry.pack(pady=5)
    def submit_login():
        global user, key
        user = user_entry.get()
        key = key_entry.get()
        if user and key:
            LicenceData = {'user': [user], 'key': [key]}
            LicenceKey = pd.DataFrame(LicenceData)
            LicenceKey.to_csv(LicenceKeyPath, sep=',', index=None, na_rep='', header=['user', 'key'])
            login_window.destroy()
            if validate_license(user, key):
                root.deiconify()
            else:
                messagebox.showerror("Login Failed", "Login failed. Please check if the key entered is valid or if the device limit has been reached.")
                root.destroy()
        else:
            messagebox.showerror("Login Failed", "Both fields are required!")
    tk.Button(login_window, text="Submit", command=submit_login).pack(pady=10)
    login_window.mainloop()
if os.path.exists(LicenceKeyPath):
    LicenceKey = pd.read_csv(LicenceKeyPath)
    key = LicenceKey.at[int(0), 'key']
    user = LicenceKey.at[int(0), 'user']
    if not validate_license(user, key):
        messagebox.showerror("Login Failed", "Login failed. Please check if the key entered is valid or if the device limit has been reached.")
        root.destroy()
else:
    show_login_window()

root.mainloop()
