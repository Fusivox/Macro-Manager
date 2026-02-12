import json, os

def make_callback(actions : list):
    def callback():
        for action in actions:
            exec(action)
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
        
        except Exception as e:
            return False + f" {e}"
        
