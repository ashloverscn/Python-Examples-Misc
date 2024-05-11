# encode_icon.py
from base64 import b64encode
import sys
import pyperclip

# for example when using filename = sys.argv[1]
# from Shell or CMD type : python encode_icon.py X2.png

#filename = sys.argv[1]
filename = "X2.png"
with open(filename, "rb") as f:
    pyperclip.copy(b64encode(f.read()).decode("ascii"))
    print("Copied to clipboard.")
