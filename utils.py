import json, os

def make_callback(actions):
    def callback():
        for action in actions:
            exec(action)
    return callback

def actualise(data):
    with open("Python/Macro manager/data.json", "w+") as f:
        json.dump(data, f, indent=4)

def add(data, keys, actions, comment):
    data[len(data)] = {
        "keys" : keys,
        "actions" : actions,
        "comment" : comment
    }

def remove(data, nb, id=True):
    try :
        if id:
            data.pop(nb)
        else : 
            del data[nb]
    except KeyError : 
        raise Exception("couldn't remove a key that doesn't exist")
    except Exception as e:
        raise Exception(f"An error occured : {e}")
    
def delete():
        try :
            appdata = os.getenv("APPDATA")
            os.remove(f"{appdata}\\Macro Manager\\data.json") 
            os.rmdir(f"{appdata}\\Macro manager")
            os.remove(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk")
            
        except Exception as e :
            raise e
