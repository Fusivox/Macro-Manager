python3 -m PyInstaller --onefile \
    --clean \
    --noconsole \
    -n "Macro Manager v2" \
    --icon=logo.ico \
    hotkeys.py \
    --add-data "locales:locales" \
    --add-data "logo.ico:."

rm -rf build *.spec
ln -s 'dist/Macro Manager v2' MacroManager