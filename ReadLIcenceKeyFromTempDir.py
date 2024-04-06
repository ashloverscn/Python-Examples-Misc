from pathlib import Path
import platform
import tempfile
import pandas as pd
LicenceKeyPath = str(Path('/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir())) + '\Gmail-API-X-Licence.key'
LicenceKey = pd.read_csv(LicenceKeyPath)
key = LicenceKey.at[int(0), 'key']
user = LicenceKey.at[int(0), 'user']
print(key)
print(user)
