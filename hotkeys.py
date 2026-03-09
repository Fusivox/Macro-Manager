import sys
if sys.platform == "win32": from win32com.client import Dispatch
elif sys.platform != "linux":raise Exception("This app sadly only works on Windows and linux (for now hopefully :D)")
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
        if sys.platform == "win32":
            
            self.appdata = f"{os.getenv("APPDATA")}\\Macro Manager"

            if os.path.exists(f"{self.appdata}\\data.json"):

                ############ Not first launch ######################

                print(">Debug : Not first time oppening") 
                print(f">Debug : {self.appdata}")           
                with open(f"{self.appdata}\\data.json", "r") as f:
                    self.data = json.load(f)
                with open(f"{self.appdata}\\abbreviation.json", "r") as f:
                    self.abbreviation = json.load(f)
                with open(f"{self.appdata}\\settings.json", "r") as f:
                    self.settings = json.load(f)

                i18n.set('locale', self.settings["lang"])
                i18n.set("fallback", self.settings["fallback"])

                print(self.data)
                self.init_background()

                keyboard.wait()

            else: 

                #################### First launch #########################

                print(">Debug : First time oppening")
                print(f">Debug : {self.appdata}")
                os.mkdir(f"{self.appdata}")
                self.data = {
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
                            ("open", {"window": "cmd", "folder": None}),
                            ("wait", {"time": 1}),
                            ("write", {"text": "This is a hotkey exemple", "interval": 0})
                        ],
                        "comment" : "This is a hotkey example and don't really do something"
                    },
                    2: {
                        "keys" : None,
                        "actions" : [
                            ("open", {"window": "cmd", "folder": None})
                        ],
                        "comment" : "it's just a test"
                    }
                }
                self.settings = {
                    "lang": "en",
                    "fallback": "fr"
                }
                self.abbreviation = {
                    0: {
                        "source": "@@",
                        "text": "example.mail@gmail.com"
                    }
                }
                utils.actualise(self.data, self.settings, self.abbreviation)
                
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

                self.init_background() # pour que les macros et abreviation test marchent des l'ouverture de l'ui
                app.mainloop()

                keyboard.unhook_all() # quand l'ui est fermé enleve puis remet toutes les macros et abreviations pour eviter les probleme et/ou bugs
                self.init_background()
                keyboard.wait()

        elif sys.platform == "linux":
            self.home = os.getenv("HOME")
            if os.geteuid() != 0:
                print("You have to be root to run this program")
                exit(1)
            self.config = f"{self.home}/.config/Macro_Manager"

            if os.path.exists(f"{self.config}/data.json"):

            ############ Not first launch ######################

                print(">Debug : Not first time oppening") 
                print(f">Debug : {self.home}")           
                with open(f"{self.config}/data.json", "r") as f:
                    self.data = json.load(f)
                with open(f"{self.config}/abbreviation.json", "r") as f:
                    self.abbreviation = json.load(f)
                with open(f"{self.config}/settings.json", "r") as f:
                    self.settings = json.load(f)

                i18n.set('locale', self.settings["lang"])
                i18n.set("fallback", self.settings["fallback"])

                print(self.data)
                self.init_background()

                keyboard.wait()

            else: 

                #################### First launch #########################

                print(">Debug : First time oppening")
                print(f">Debug : {self.home}")
                os.mkdir(f"{self.config}")
                lang = os.environ['LANG'][:2]

                self.data = {
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
                            ("open", {"window": "shell", "folder": None}),
                            ("wait", {"time": 1}),
                            ("write", {"text": "This is a hotkey exemple", "interval": 0})
                        ],
                        "comment" : "This is a hotkey example and don't really do something"
                    },
                    2: {
                        "keys" : None,
                        "actions" : [
                            ("open", {"window": "shell", "command": None})
                        ],
                        "comment": "it's just a test"
                    }
                }
                self.settings = {
                    "lang": f"{lang if lang in ['en', 'fr'] else 'en'}",
                    "fallback": "fr"
                }
                self.abbreviation = {
                    0: {
                        "source": "@@",
                        "text": "example.mail@gmail.com"
                    }
                }
                utils.actualise(self.data, self.settings, self.abbreviation, os_name="linux")
                self.create_service_linux()
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
                    self.create_service_linux()  
                else:
                    ui.messagebox.showinfo(
                        title=_("htk.info_title"),
                        message=_("htk.cancelled_msg")
                    )
                    app.destroy()

                self.init_background()
                app.mainloop()
                
                keyboard.unhook_all()
                self.init_background()
                keyboard.wait()
                
    def create_shortcut_win32(self) -> None:
        """creer le raccourci de l'app dans le dossier startup de windows pour que l'app se lance au démarage de windows pour ne pas avoir besoin de la lancer a chaque fois"""

        shortcut_path = f"{os.getenv("APPDATA")}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk"
        path = sys.executable

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = path
        shortcut.WorkingDirectory = self.appdata
        shortcut.IconLocation = path
        shortcut.save()
                
    def create_service_linux(self) -> None:
        """creer le service linux de l'app pour que l'app se lance au démarage de linux pour ne pas avoir besoin de la lancer a chaque fois"""

        path = "/opt/Macro_Manager/"
        service = """[Unit]
Description=MacroManager
After=network.target

[Service]
Type=simple
ExecStart=/opt/Macro_Manager/Macro_Manager
WorkingDirectory=/opt/Macro_Manager
Restart=always
RestartSec=5
User=root
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target"""
        service_file = "/etc/systemd/system/macro_manager.service"
        if not os.path.exists(path): os.mkdir(path)
        os.system(f"cp '{sys.executable}' '{path}Macro_Manager' && chmod +x '{path}Macro_Manager'")
        with open(service_file, 'w') as f:
            f.write(service)
        os.system("systemctl enable macro_manager.service")

        # Ajout permanent de l'autorisation X pour root (cote utilisateur)
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user:
            user_home = os.path.expanduser(f"~{sudo_user}")
            bashrc_path = os.path.join(user_home, ".bashrc")
            xhost_cmd = "xhost +SI:localuser:root\n"

            if os.path.exists(bashrc_path):
                with open(bashrc_path, "r") as f:
                    lines = f.readlines()
                if not any("xhost +SI:localuser:root" in line for line in lines):
                    with open(bashrc_path, "a") as f:
                        f.write("\n" + xhost_cmd)
            else:
                with open(bashrc_path, "w") as f:
                    f.write(xhost_cmd)
        else:
            print("SUDO_USER non defini: impossible de modifier le .bashrc utilisateur.")
        return 0
    
    def init_background(self) -> None: 
        """creer les macros et abreviations stockées dans les fichier json pour les utiliser"""

        for nb in self.data:
            keys = self.data[nb]["keys"]
            actions = self.data[nb]["actions"]
            if keys is not None:
                callback = utils.make_callback(actions)
                keyboard.add_hotkey(keys, callback)
                print(f">Debug : new hotkey {keys}, do {actions}.")
            else : print(f">Debug : action that has no keys : {actions}")

        for nb in self.abbreviation:
            source = self.abbreviation[nb]["source"]
            text = self.abbreviation[nb]["text"]
            keyboard.add_abbreviation(source, text)
            print(f">Debug : New abbreviation {source}, replaced by {text}")


if __name__ == "__main__":
    hotkeys = Hotkeys()
