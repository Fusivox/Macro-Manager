#!/bin/bash

read -p "Choose an option: 1) build, 2) clean: " option

case "$option" in
    1)
        python3 -m PyInstaller --onefile \
                --clean \
                --noconsole \
                -n "Macro Manager v2" \
                --icon=logo.ico \
                hotkeys.py \
                --add-data "locales:locales" \
                --add-data "logo.ico:."
        ln -s 'dist/Macro Manager v2' MacroManager
        ;;
    2)
        rm -rf build *.spec dist MacroManager __pycache__
        rm -rf None*
        ;;
    *)
        echo "Invalid option. Please choose 1 or 2"
        exit 1
        ;;
esac