import os, shutil, sys
from pathlib import Path

try :

    if sys.platform == "win32":

        path = Path.home() / "AppData" / "Roaming" / "Macro Manager"
        lnk = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Macro Manager.lnk"

        if path.exists(): shutil.rmtree(path)
        else: print("The data folder doesn't exist")

        if lnk.exists() : os.remove(lnk)
        else: print("The link doesn't exist")

        if not path.exists() and not lnk.exists():
            print("Succesfully Uninstalled")

        else : print("Something went wrong, Uninstallation failed")

    else:
        path = Path.home() / ".config" / "Macro_Manager"

        if path.exists(): shutil.rmtree(path)

        if not path.exists(): print("Succesfully Uninstalled")

        else: print("Something went wrong, Uninstallation failed")

except Exception as e:
    print(f"Something went wrong : {e}")