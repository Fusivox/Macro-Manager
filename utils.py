import json, os, shutil, pyautogui, time, ui, subprocess
from pathlib import Path

def make_callback(actions: list):
    def callback():
        for action, params in actions:
            if action == "open":

                if params.get("window") == "gui": #("open", {"window":"gui"})
                    app = ui.Application()
                    app.mainloop()

                elif params.get("window") == "cmd": #("open", {"window":"cmd", "folder":"Dossier dans lequel le cmd est ouvert si spécifié sinon celui par default"})
                    subprocess.Popen(["cmd.exe"], cwd=params.get("folder", None))         

                elif params.get("window") == "explorer": #("open", {"window":"explorer", "folder":"Dossier dans lequel le navigateur de fichier est ouvert si spécifié sinon celui par default"})
                    subprocess.Popen(["Explorer", params.get("folder", None)], shell=True)

            elif action == "wait": #("wait", #temps en secondes)
                time.sleep(params["time"])

            elif action == "write": #("write", {"text":"texte a ecrire", "interval":attente entre chaque lettre})
                pyautogui.write(params["text"], interval=params.get("interval", 0))

            elif action == "click": #("click", {"x":si rien x curseur, "y":si rien y curseur, "clicks":par default 1, "interval":par default 0, "button":"primary(default) ou secondary ou middle" , "duration":temps pour aller au cos spécifié 0 par default})
                pyautogui.click(x=params.get("x", None), y=params.get("y", None), clicks=params.get("clicks", 1), interval=params.get("interval", 0), button=params.get("button", "primary"), duration=params.get("duration", 0))

            elif action == "moveto": #("moveto", {"x":..., "y":..., "duration":0 par default})
                pyautogui.moveTo(x=params.get("x", None), y=params.get("y", None), duration=params.get("duration", 0))

            elif action == "move": #("move", {"x":+relatif a la souris, "y":+relatif a la souris, "duration":0 par default})
                pyautogui.move(xOffset=params.get("x", 0), yOffset=params.get("y", 0), duration=params.get("duration", 0))

            elif action == "press":  #("press", {"keys":touche a appuyer, presses=nb de fois appuyer, "interval":intervale entre les plusieurs presses}
                pyautogui.press(keys=params["keys"], presses=params.get("presses", 1), interval=params.get("interval", 0))
                
    return callback

def actualise(data: dict|None = None, settings: dict|None = None, abbreviation: dict|None = None, os_name="win32"):
    if os_name == "win32":
        appdata = os.getenv("APPDATA")
        if data:
            with open(f"{appdata}\\Macro Manager\\data.json", "w+") as f:
                json.dump(data, f, indent=4)
        if settings:
            with open(f"{appdata}\\Macro Manager\\settings.json", "w+") as f:
                json.dump(settings, f, indent=4)
        if abbreviation:
            with open(f"{appdata}\\Macro Manager\\abbreviation.json", "w+") as f:
                json.dump(abbreviation, f, indent=4)
    else:
        home = os.getenv("HOME")
        config = f"{home}/.config/Macro_Manager"
        if data:
            with open(f"{config}/data.json", "w+") as f:
                json.dump(data, f, indent=4)
        if settings:
            with open(f"{config}/settings.json", "w+") as f:
                json.dump(settings, f, indent=4)
        if abbreviation:
            with open(f"{config}/abbreviation.json", "w+") as f:
                json.dump(abbreviation, f, indent=4)


def add_mcr(data: dict, keys: str, actions: list, comment: str = None):
    data[str(len(data))] = {
        "keys": keys,
        "actions": actions,
        "comment": comment
    }

def add_abb(data: dict, source: str, text: str):
    data[str(len(data))] = {
        "source": source,
        "text": text
    }

def remove(data: dict, nb: str|int, id=True):
    try :
        if id: data.pop(nb)
        else: del data[nb]
        
        return True
        
    except Exception: return False
    
def delete_win32() -> bool:
        try:
            
            path = Path.home() / "AppData" / "Roaming" / "Macro Manager"
            lnk = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Macro Manager.lnk"

            if path.exists(): shutil.rmtree(path)
            
            if lnk.exists(): os.remove(lnk)

            if not path.exists() and not lnk.exists(): return True

            else: return False

        except Exception:
            return False

