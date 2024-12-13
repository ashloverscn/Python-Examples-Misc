import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

def run_exe(exe_path):
    try:
        if os.access(exe_path, os.X_OK):
            subprocess.run([exe_path], cwd='./', check=True)
            print(f"Gmail-API-X.exe Started Successfully")
            #print(f"Successfully ran {exe_path}")
        else:
            print(f"Error file not executable or not accessible.")
            #print(f"Error: {exe_path} is not executable or not accessible.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running Gmail-API-X.exe: {e}")
        #print(f"Error occurred while running {exe_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    exe_path = os.path.join(sys._MEIPASS, "Gmail-API-X", "Gmail-API-X.exe")
    #exe_path = "C:\\Users\\ashlo\\AppData\\Local\\Temp\\_MEI241562\\Gmail-API-X\\Gmail-API-X.exe"  
    #print(f"Checking for executable at: {exe_path}")
    if os.path.exists(exe_path):
        #print(f"Executable found at: {exe_path}")
        run_exe(exe_path)
    else:
        print(f"Executable Not found")
        #print(f"Executable Not found at: {exe_path}")
   
    #print(f"Final executable path: {exe_path}")
    os.system("pause")
    
if __name__ == "__main__":
    main()
