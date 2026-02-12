import json, os, ui

def make_callback(actions: list):
    def callback():
        for action, *params in actions:
            if action == "open":

                if params[0] == "gui": #("open", "gui")
                    app = ui.Application()
                    app.mainloop()

                elif params[0] == "cmd": #("open", "cmd", #dossier dans lequel cmd est ouvert None si aucun spécifié)
                    import subprocess
                    subprocess.Popen(["cmd.exe"], cwd=params[1])                

            elif action == "wait": #("wait", #temps en secondes)
                import time
                time.sleep(params[0])

            elif action == "write": #("write", "#texte a écrire")
                import pyautogui
                pyautogui.write(params[0])

            elif action == "click": #("click", #x, #y, #nb clicks ,#temps pour aller au cos)
                import pyautogui
                pyautogui.click(params[0], params[1], params[2], params[3])
                
    return callback

def actualise(data: dict):
    appdata = os.getenv("APPDATA")
    with open(f"{appdata}\\Macro Manager\\data.json", "w+") as f:
        json.dump(data, f, indent=4)

def add(data: dict, keys: str, actions: str, comment: str = None):
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
            os.rmdir(f"{appdata}\\Macro manager")
            os.remove(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk")
            return True
            
        except FileNotFoundError:
            return True

        except Exception as e :
            return False + f" {e}"
