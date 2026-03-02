import json, os, shutil, pyautogui, time, ui, subprocess, sys
from pathlib import Path

POSSIBLE_KEYS = pyautogui.KEY_NAMES

def make_callback(actions: list):
    """permet de transformer la syntaxe programme en code executable pour les macros"""

    def callback():
        for action, params in actions:
            if action == "open":

                if params["window"] == "gui": #("open", {"window":"gui"}) sert a ouvrir l'ui pricipale
                    app = ui.Application()
                    app.mainloop()

                elif params["window"] == "cmd": #("open", {"window":"cmd", "folder":"Dossier dans lequel le cmd est ouvert si spécifié sinon celui par default"})
                    subprocess.Popen(["cmd.exe"], cwd=params["folder"])         

                elif params["window"] == "shell":#("open", {"window":"shell", "command":"commande a executer dans le shell"})
                    subprocess.Popen(["xterm"], shell=True)

                elif params["window"] == "explorer": #("open", {"window":"explorer", "folder":"Dossier dans lequel le navigateur de fichier est ouvert si spécifié sinon celui par default"})
                    subprocess.Popen(["Explorer", params["folder"]], shell=True)

                else:
                    path = params["window"]
                    if sys.platform == "win32":
                            os.startfile(path)
                    else:
                        subprocess.run(["xdg-open", path])
                    

            elif action == "wait": #("wait", #temps en secondes)
                time.sleep(params["time"])

            elif action == "write": #("write", {"text":"texte a ecrire", "interval":attente entre chaque lettre})
                pyautogui.write(params["text"], interval=params["interval"])

            elif action == "click": #("click", {"x":si rien x curseur, "y":si rien y curseur, "clicks":par default 1, "interval":par default 0, "button":"primary(default) ou secondary ou middle" , "duration":temps pour aller au cos spécifié 0 par default})
                pyautogui.click(x=params["x"], y=params["y"], clicks=params["clicks"], interval=params["interval"], button=params["button"], duration=params["duration"])

            elif action == "moveto": #("moveto", {"x":..., "y":..., "duration":0 par default})
                pyautogui.moveTo(x=params["x"], y=params["y"], duration=params["duration"])

            elif action == "move": #("move", {"x":+relatif a la souris, "y":+relatif a la souris, "duration":0 par default})
                pyautogui.move(xOffset=params["x"], yOffset=params["y"], duration=params["duration"])

            elif action == "press":  #("press", {"keys":touche a appuyer, presses=nb de fois appuyer, "interval":intervale entre les plusieurs presses}
                pyautogui.press(keys=params["keys"], presses=params["presses"], interval=params["interval"])
                
    return callback

def convert(value):
    """convertis un nombre sotcké en str en int ou float et si c'est pas un nombre le renvoie normalement"""

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
        
r"""
exemples syntaxe utilisateur :

wait : 10
write : Salut comment ça va ;; interval : 0.1
click : primary ;; x : 10 ;; y : 500 ;; clicks : 1
press : A ;; presses : 5 ;; interval : 1.5
open : cmd ;; folder : C:\User
moveto : 0.5 ;; x : 500
move : 0 ;; y : 100

exemple liste actions:
["write : Salut comment ça va ;; interval : 0.1", "press : A ;; presses : 5 ;; interval : 1.5", "wait : 10", "moveto : 0.5 ;; x : 500 ;; y : None"]
"""

def translate_to_callback(actions: list[str]) -> list[tuple]:
    """traduis la syntaxe utilisateur en syntaxe programme"""

    translated_actions = []
    
    for action in actions:          
        parts = {key: convert(value) for key, value in (part.split(" : ", 1) for part in action.split(" ;; "))} # transforme actions en un dictionnaire plus clair qui sépare comme il faut               
    
        if "wait" in parts:
            translated_actions.append(("wait", {"time": parts["wait"]}))
            
        elif "press" in parts:
            translated_actions.append(("press", {"keys": parts["press"], "presses": parts.get("presses", 1), "interval": parts.get("interval", 0)}))

        elif "write" in parts:
            translated_actions.append(("write", {"text": parts["write"], "interval": parts.get("interval", 0)}))

        elif "click" in parts:
            translated_actions.append(("click", {"x": parts.get("x", None), "y": parts.get("y", None), "clicks": parts.get("clicks", 1), "interval": parts.get("interval", 0), "button": parts["button"], "duration": parts.get("duration", 0)}))

        elif "moveto" in parts:
            translated_actions.append(("moveto", {"x": parts.get("x", None), "y": parts.get("y", None), "duration": parts["moveto"]}))

        elif "move" in parts:
            translated_actions.append(("move", {"x": parts.get("x", None), "y": parts.get("y", None), "duration": parts["move"]}))

        elif "open" in parts:
            if parts["open"] == "cmd" or parts["open"] == "explorer":
                translated_actions.append(("open", {"window": parts["open"], "folder": parts.get("param", None)}))
            elif parts["open"] == "shell":
                translated_actions.append(("open", {"window": "shell", "command": parts.get("param", None)}))
            else:
                translated_actions.append(("open", {"window": parts["open"]}))

    return translated_actions

def translate_from_callback(actions: list[tuple]) -> list[str]:
    translated_actions = []

    for action, params in actions:

        if action == "wait":
            translated_actions.append(f"wait : {params["time"]}")

        elif action == "press":
            translated_actions.append(f"press : {params["keys"]} ;; presses : {params["presses"]} ;; interval : {params["interval"]}")

        elif action == "write":
            translated_actions.append(f"write : {params["text"]} ;; interval : {params["interval"]}")

        elif action == "click":
            translated_actions.append(f"click : {params["button"]} ;; x : {params["x"]} ;; y : {params["y"]} ;; duration : {params["duration"]} ;; clicks : {params["clicks"]} ;; interval : {params["interval"]}")

        elif action == "moveto":
            translated_actions.append(f"moveto : {params["duration"]} ;; x : {params["x"]} ;; y : {params["y"]}")

        elif action == "move":
            translated_actions.append(f"move : {params["duration"]} ;; x : {params["x"]} ;; y : {params["y"]}")
        
        elif action == "open":
            additionnal_param = params.get("command", None) or params.get("folder", None)
            if additionnal_param is not None:
                translated_actions.append(f"open : {params["window"]} ;; param : {additionnal_param}")
            else:
                translated_actions.append(f"open : {params["window"]}")

    return translated_actions

def actualise(data: dict|None = None, settings: dict|None = None, abbreviation: dict|None = None, os_name="win32") -> None:
    """actualise le fichier json associé (data, settings et/ou abbreviation)"""

    if os_name == "win32":
        appdata = os.getenv("APPDATA")
        if data:
            with open(f"{appdata}\\Macro Manager\\data.json", "w") as f:
                json.dump(data, f, indent=4)
        if settings:
            with open(f"{appdata}\\Macro Manager\\settings.json", "w") as f:
                json.dump(settings, f, indent=4)
        if abbreviation:
            with open(f"{appdata}\\Macro Manager\\abbreviation.json", "w") as f:
                json.dump(abbreviation, f, indent=4)
    else:
        home = os.getenv("HOME")
        config = f"{home}/.config/Macro_Manager"
        if data:
            with open(f"{config}/data.json", "w") as f:
                json.dump(data, f, indent=4)
        if settings:
            with open(f"{config}/settings.json", "w") as f:
                json.dump(settings, f, indent=4)
        if abbreviation:
            with open(f"{config}/abbreviation.json", "w") as f:
                json.dump(abbreviation, f, indent=4)


def add_mcr(data: dict, keys: str|None, actions: list, comment: str|None = None) -> None:
    """ajoute une macro au fichier data.json (nécessite un utils.actualise pour le sauvegarder)"""

    data[str(len(data))] = {
        "keys": keys,
        "actions": actions,
        "comment": comment
    }

def add_abb(data: dict, source: str, text: str) -> None:
    """ajoute une abreviation au fichier abbreviation.json (nécessite un utils.actualise pour le sauvegarder)"""

    data[str(len(data))] = {
        "source": source,
        "text": text
    }

def remove(data: dict, nb: str|int, id=True) -> bool:
    """retire un élément d'un dictionnaire et renvoie True si réussit sinon envoie False"""

    try :
        if id: data.pop(nb)
        else: del data[nb]
        
        return True
        
    except Exception: return False
    
def delete_win32() -> bool:
    """Supprime toute l'arborescence des fichier Macro Manager, renvoie True si réussie sinon False"""

    try:
        
        path = Path.home() / "AppData" / "Roaming" / "Macro Manager"
        lnk = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Macro Manager.lnk"

        if path.exists(): shutil.rmtree(path)
        
        if lnk.exists(): os.remove(lnk)

        if not path.exists() and not lnk.exists(): return True

        else: return False

    except Exception:
        return False

def delete_linux() -> bool:
    """Supprime toute l'arborescence des fichier Macro Manager, renvoie True si réussie sinon False"""

    try:
        
        path = Path.home() / ".config" / "Macro_Manager"

        if path.exists(): shutil.rmtree(path)

        if not path.exists(): return True

        else: return False

    except Exception:
        return False