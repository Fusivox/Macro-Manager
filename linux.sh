#!/bin/bash
# Fix PyInstaller warning: force output in English
export LANG=C

if [ -d "env" ]; then
    source env/bin/activate
else
    python3 -m venv env
    source env/bin/activate
    pip install -r requirement_linux.txt
fi
read -p "Choose an option: 1) build, 2) clean: " option

case "$option" in
    1)
        python3 -m PyInstaller --onefile \
                --clean \
                --noconsole \
                -n "Macro Manager v2" \
                hotkeys.py \
                --add-data "locales:locales" \
                --add-data "logo.png:." 
        ln -s 'dist/Macro Manager v2' MacroManager
        ;;
    2)
        sudo systemctl stop macro_manager.service
        sudo rm -rf build *.spec dist MacroManager __pycache__ /root/.config/Macro_Manager /etc/systemd/system/macro_manager.service /opt/Macro_Manager
        rm -rf None*
        ;;
    *)
        echo "Invalid option. Please choose 1 or 2"
        exit 1
        ;;
esac