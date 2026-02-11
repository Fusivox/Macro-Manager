import os

try :
    appdata = os.getenv("APPDATA")
    os.remove(f"{appdata}\\Macro Manager\\data.json") 
    os.rmdir(f"{appdata}\\Macro manager") 
    os.remove(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk")

    if not os.path.exists(f"{appdata}\\Macro manager") and not os.path.exists(f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Macro Manager.lnk"):
        print("Succesfully Uninstalled")

    else : print("Something went wrong, Uninstallation failed")

except FileNotFoundError:
    print("Couldn't delete something that doesn't exist")

except Exception as e:
    print(f"Something went wrong : {e}")

