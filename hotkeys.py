import sys
if sys.platform == "win32":
    from win32com.client import Dispatch
elif sys.platform == "linux":
    from lib.linux32com import Dispatch
else:
    raise Exception("This app sadly only works on Windows and linux (for now hopefully :D)")

import json, os, ui, utils, i18n, keyboard

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
            with open(f"{self.appdata}\\Macro Manager\\abbreviation.json", "r") as f:
                abbreviation = json.load(f)
            with open(f"{self.appdata}\\Macro Manager\\settings.json", "r") as f:
                settings = json.load(f)

            i18n.set('locale', settings["lang"])
            i18n.set("fallback", settings["fallback"])

            print(data)
            for nb in data:
                keys = data[nb]["keys"]
                actions = data[nb]["actions"]
                keyboard.add_hotkey(keys, utils.make_callback, args=(actions,))
                print(f">Debug : new hotkey {keys}, do {actions}.")

            for nb in abbreviation:
                source = abbreviation[nb]["source"]
                text = abbreviation[nb]["text"]
                keyboard.add_abbreviation(source, text)
                print(f">Debug : New abbreviation {source}, replaced by {text}")

            keyboard.wait()

        else: 

            #################### First launch #########################

            print(">Debug : First time oppening")
            print(f">Debug : {self.appdata}")
            os.mkdir(f"{self.appdata}\\Macro Manager")
            data = {
                0: {
                    "keys" : "ctrl+alt+a",
                    "actions" : [
                        ("open", {"window":"gui"})
                    ],
                    "comment" : None
                },
                1: {
                    "keys" : "ctrl+alt+q",
                    "actions" : [
                        ("open", {"window": "cmd"}),
                        ("wait", 1),
                        ("write", {"text": "This is a hotkey exemple"})
                    ],
                    "comment" : "This is a hotkey example and don't really do something"
                }
            }
            settings = {
                "lang": "en",
                "fallback": "fr"
            }
            abbreviation = {
                0: {
                    "source": "@@",
                    "text": "example.mail@gmail.com"
                }
            }
            utils.actualise(data, settings, abbreviation)
            
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
                self.create_shortcut_win32()  
            else:
                ui.messagebox.showinfo(
                    title=_("htk.info_title"),
                    message=_("htk.cancelled_msg")
                )
                app.destroy()

            app.mainloop()
            
    def create_shortcut_win32(self):

        shortcut_path = f"{self.appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk"
        path = sys.executable
        dir = f"{self.appdata}\\Macro Manager"

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = path
        shortcut.WorkingDirectory = dir
        shortcut.IconLocation = path
        shortcut.save()

if __name__ == "__main__":

    hotkeys = Hotkeys()
