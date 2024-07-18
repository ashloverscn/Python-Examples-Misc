@ echo off
pip install pyinstaller
pyinstaller --clean --onefile Split-O-Splice.py
move /y .\dist\*.exe .\
del /f /q /a .\*.spec
rmdir /s /q .\build .\dist

rem #### This are also valid commands ####
rem #for non-gui without any disp icon# pyinstaller --clean --onefile script_name.py
rem #for non-gui with only disp icon# pyinstaller --clean --onefile --icon=icon_file_name.ico script_name.py
rem #for non-gui with disp and MIMEPASS icon#
rem pyinstaller --clean --onefile --icon=icon_file_name.ico --add-data "icon_file_name.ico;." script_name.py
rem #for gui with disp and MIMEPASS icon#
rem pyinstaller --clean --noconsole --onefile --icon=icon_file_name.ico --add-data "icon_file_name.ico;." script_name.py

rem move /y .\dist\*.exe .\
rem move /y .\dist\*.exe
rem move /y dist\*.exe .\
rem move /y dist\*.exe

rem copy /b /y .\dist\*.exe .\
rem copy /b /y .\dist\*.exe
rem copy /b /y dist\*.exe .\
rem copy /b /y dist\*.exe

rem del /f /q /a .\*.spec
rem del /f /q /a *.spec

rem rmdir /s /q .\build\ .\dist\
rem rmdir /s /q .\build\ .\dist\
rem rmdir /s /q build\ dist\
rem rmdir /s /q build dist
