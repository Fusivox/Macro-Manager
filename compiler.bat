@echo off
python -m PyInstaller --onefile ^
    --clean ^
    --noconsole ^
    -n "Macro Manager v2" ^
    --icon=logo.ico ^
    hotkeys.py ^
    --add-data "locales;locales" ^
    --add-data "logo.ico;."

pause
