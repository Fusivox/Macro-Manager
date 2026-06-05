@echo off

echo Choose an option 1) build 2) clean

set /p build=

if "%build%"=="1" (
    python -m PyInstaller --onefile ^
        --clean ^
        --noconsole ^
        -n "Macro Manager v2" ^
        --icon=logo.ico ^
        hotkeys.py ^
        --add-data "locales;locales" ^
        --add-data "logo.ico;."
    move "dist\Macro Manager v2.exe" "Macro Manager v2.exe"
    del /q /f *.spec build dist

) else if "%build%"=="2" (
    del /q /f *.spec build dist "%APPDATA%/Macro Manager"
    
) else (
    echo Invalid option. Please choose 1 or 2
    exit
)
pause