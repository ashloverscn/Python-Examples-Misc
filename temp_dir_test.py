#https://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
#https://java2blog.com/get-temp-directory-python/
from pathlib import Path
import platform
import tempfile

tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())

print(tempdir)

import tempfile
path = tempfile.gettempdir()
print(path)

import tempfile
path = tempfile.gettempdirb()
print(path)

import tempfile
path = tempfile.tempdir
print(path)

