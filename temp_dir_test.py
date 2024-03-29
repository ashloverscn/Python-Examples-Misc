#https://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
from pathlib import Path
import platform
import tempfile

tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())

print(tempdir)
