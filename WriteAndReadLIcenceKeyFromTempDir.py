from pathlib import Path
import platform
import tempfile
import pandas as pd
import os.path

key = ''
user = ''
LicenceKeyPath = str(Path('/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir())) + '\Gmail-API-X-Licence.key'
if os.path.exists(LicenceKeyPath):
    LicenceKey = pd.read_csv(LicenceKeyPath)
    key = LicenceKey.at[int(0), 'key']
    user = LicenceKey.at[int(0), 'user']
else:
    user = input("Enter UserName: ")
    key = input("Enter LicenceKey: ")
    LicenceData = {'user': [user], 'key': [key]}
    LicenceKey = pd.DataFrame(LicenceData)
    LicenceKey.to_csv(LicenceKeyPath, sep=',', index=None, na_rep='', header=['user', 'key'])

print(key)
print(user)
input()
