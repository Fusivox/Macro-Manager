import json, os

def make_callback(actions: list):
    def callback():
        for action, params in actions:
            if action == "open":

                if params.get("window") == "gui": #("open", {"window":"gui"})
                    import ui
                    app = ui.Application()
                    app.mainloop()

                elif params.get("window") == "cmd": #("open", {"window":"cmd", "folder":"Dossier dans lequel le cmd est ouvert si spécifié sinon celui par default"})
                    from subprocess import Popen
                    Popen(["cmd.exe"], cwd=params.get("folder", None))         

                elif params.get("window") == "explorer": #("open", {"window":"explorer", "folder":"Dossier dans lequel le navigateur de fichier est ouvert si spécifié sinon celui par default"})
                    from subprocess import Popen
                    Popen(["Explorer", params.get("folder", None)], shell=True)

            elif action == "wait": #("wait", #temps en secondes)
                from time import sleep
                sleep(params[0])

            elif action == "write": #("write", {"text":"texte a ecrire", "interval":attente entre chaque lettre})
                from pyautogui import write
                write(message=params["text"], interval=params.get("interval", 0))

            elif action == "click": #("click", {"x":si rien x curseur, "y":si rien y curseur, "clicks":par default 1, "interval":par default 0, "button":"primary(default) ou secondary ou middle" , "duration":temps pour aller au cos spécifié 0 par default})
                from pyautogui import click 
                click(x=params.get("x", None), y=params.get("y", None), clicks=params.get("clicks", 1), interval=params.get("interval", 0), button=params.get("button", "primary"), duration=params.get("duration", 0))

            elif action == "moveto": #("moveto", {"x":..., "y":..., "duration":0 par default})
                from pyautogui import moveTo
                moveTo(x=params.get("x", None), y=params.get("x", None), duration=params.get("duration", 0))

            elif action == "move": #("move", {"x":+relatif a la souris, "y":+relatif a la souris, "duration":0 par default})
                from pyautogui import move
                move(xOffset=params.get("x", 0), yOffset=params.get("y", 0), duration=params.get("duration", 0))

            elif action == "press":  #("press", {"keys":touche a appuyer, presses=nb de fois appuyer})
                from pyautogui import press
                press(keys=params["keys"], presses=params.get("presses", 1), interval=params.get("interval", 0))
                
    return callback

def actualise(data: dict|None = None, settings: dict|None = None):
    appdata = os.getenv("APPDATA")
    if data:
        with open(f"{appdata}\\Macro Manager\\data.json", "w+") as f:
            json.dump(data, f, indent=4)
    if settings:
        with open(f"{appdata}\\Macro Manager\\settings.json", "w+") as f:
            json.dump(settings, f, indent=4)


def add(data: dict, keys: str, actions: list, comment: str = None):
    data[len(data)] = {
        "keys" : keys,
        "actions" : actions,
        "comment" : comment
    }

def remove(data: dict, nb: str|int, id=True):
    try :
        if id:
            data.pop(nb)
        else : 
            del data[nb]
    except KeyError : 
        raise Exception("couldn't remove a key that doesn't exist")
    except Exception as e:
        raise Exception(f"An error occured : {e}")
    
def delete_win32():
        try :
            appdata = os.getenv("APPDATA")
            os.remove(f"{appdata}\\Macro Manager\\data.json") 
            os.remove(f"{appdata}\\Macro Manager\\settings.json")
            os.rmdir(f"{appdata}\\Macro manager")
            os.remove(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk")
            return True
            
        except FileNotFoundError:
            return True

        except Exception :
            return False
