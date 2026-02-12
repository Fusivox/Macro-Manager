import sys
if sys.platform != "win32":
    raise Exception("This app sadly only works on Windows (for now hopefully :D)")
import json, keyboard, os, ui, utils, i18n
from win32com.client import Dispatch

def ressource_path(path):
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base, path)

i18n.load_path.append(ressource_path("locales"))
i18n.set("filename_format", "{locale}.yml")
i18n.set('locale', "en")
i18n.set("fallback", "fr")

_ = i18n.t

class Hotkeys():
    def __init__(self):
        
        self.appdata = os.getenv("APPDATA")

        if os.path.exists(f"{self.appdata}\\Macro Manager\\data.json"):

            ############ Not first launch ######################

            print(">Debug : Not first time oppening") 
            print(f">Debug : {self.appdata}")           
            with open(f"{self.appdata}\\Macro Manager\\data.json", "r") as f:
                data = json.load(f)
            print(data)
            for nb in data:
                keys = data[nb]["keys"]
                actions = data[nb]["actions"]
                keyboard.add_hotkey(keys, utils.make_callback, args=(actions,))
                print(f">Debug : new hotkey {keys}, do {actions}.")

            keyboard.wait()

        else: 

            #################### First launch #########################

            print(">Debug : First time oppening")
            print(f">Debug : {self.appdata}")
            os.mkdir(f"{self.appdata}\\Macro Manager")
            data = {
                0 : {
                    "keys" : "ctrl+alt+a",
                    "actions" : [
                        ("open", "gui")
                    ],
                    "comment" : None
                },
                1 : {
                    "keys" : "ctrl+alt+q",
                    "actions" : [
                        ("open", "cmd", None),
                        ("wait", 1),
                        ("write", "This is a hotkey exemple")
                    ],
                    "comment" : "This is a hotkey example and don't really do something"
                }
            }
            utils.actualise(data)
            self.create_shortcut_win32()  
            
            app = ui.Application()
            ask_confirm = ui.messagebox.askokcancel(
                title=_("htk.info_title"),
                message=_("htk.startup_msg")
            )
            if ask_confirm :
                ui.messagebox.showinfo(
                    title=_("htk.info_title"),
                    message=_("htk.thx_msg")
                    )
            else :
                dlt = utils.delete_win32()
                if dlt:
                    ui.messagebox.showinfo(
                        title=_("htk.info_title"),
                        message=_("htk.cancelled_msg")
                    )
                    app.destroy()
                else:
                    ui.messagebox.showerror(
                        title=_("htl.err_title"),
                        message=_("htk.err_inst")
                    )
            app.mainloop()
            
    def create_shortcut_win32(self):

        shortcut_path = f"{self.appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk"
        path = sys.executable
        dir = os.path.dirname(path)

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = path
        shortcut.WorkingDirectory = dir
        shortcut.IconLocation = path
        shortcut.save()

if __name__ == "__main__":
    hotkeys = Hotkeys()

# python -m PyInstaller --onefile --clean --noconsole -n "Macro Manager v*" hotkeys.py --add-data "locales;locales"
# import os ; appdata = os.getenv("APPDATA") ; os.remove(f"{appdata}\\Macro Manager\\data.json") ; os.rmdir(f"{appdata}\\Macro manager") ; os.remove(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk")