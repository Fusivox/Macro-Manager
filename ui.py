import tkinter as tk , os, json, utils, i18n, sys, screeninfo, keyboard
from tkinter import messagebox, simpledialog


class Application(tk.Tk):
    def __init__(self, screenName = "Main page", baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        i18n.load_path.append(self.ressource_path("locales"))
        i18n.set("filename_format", "{locale}.yml")

        self.appdata = os.getenv("APPDATA")
        with open(f"{self.appdata}\\Macro Manager\\settings.json", "r") as f:
            self.settings = json.load(f)

        i18n.set('locale', self.settings["lang"])
        i18n.set("fallback", self.settings["fallback"])

        self._ = i18n.t

        
        with open(f"{self.appdata}\\Macro Manager\\data.json", "r") as f:
            self.data = json.load(f)

        monitor = screeninfo.get_monitors()

        for m in monitor:
            if m.is_primary:
                if m.width > 1920 and m.height > 1080 :
                    self.tk.call("tk", "scaling", 1.75)
                    self.geometry("550x350")
                else : 
                    self.tk.call("tk", "scaling", 1.5)
                    self.geometry("400x200")

        self.resizable(False, False)
        
        self.title(self._("ui.title"))
        self.iconbitmap(default=self.ressource_path("logo.ico"))
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.build_menu()
        self.build_main_ui()

    def on_select(self, event):
        self.selection = self.listbox.curselection()
        Keys = self._("ui.keys")
        comment = self._("ui.comment")
        self.rmv_button.config(state="normal", bg="SystemButtonFace")
        if self.selection:
            self.index = str(self.selection[0])
            self.selected.config(text=f"{Keys} : {self.data[self.index]["keys"]} \n\n{comment} : {self.data[self.index]["comment"]}" if self.data[self.index]["comment"] != None else f"{Keys} : {self.data[self.index]["keys"]}\n\n")
        
    def close(self):
        utils.actualise(self.data, self.settings)
        self.destroy()

    def confirm(self):
        sure = messagebox.askokcancel(
            title=self._("ui.confirm"),
            message=self._("ui.dlt_confirm")
        )
        if sure :
            dlt = utils.delete_win32()
            if dlt:
                messagebox.showinfo(
                    title=self._("ui.info"),
                    message=self._("ui.dlt_success")
                )
                self.destroy()
            else : 
                messagebox.showerror(
                    title=self._("ui.info"),
                    message=self._("ui.dlt_error")
                )

    def gui_keys(self):
        msg = self._("ui.key_msg")

        keys = simpledialog.askstring(
            title=self._("ui.key_change"),
            prompt=f"{msg} : {self.data["0"]["keys"]}"
        )
        if keys != None and keys != "":
            try :
                test = keyboard.add_hotkey(keys, lambda : None)
                keyboard.remove_hotkey(test)
                self.data["0"]["keys"] = keys
                
            except Exception :
                message = self._("ui.key_eg").format(key=keys)
                messagebox.showerror(
                    title=self._("ui.invalid_key"),
                    message=message
                )

    def help(self):
        self.help_menu = tk.Toplevel(height=400, width=400, takefocus=True)
        self.help_menu.title(self._("ui.help_title"))

    def set_lang(self, lang):
        i18n.set("locale", lang)
        self.title(self._("ui.title"))
        self.refresh_menu()

    def build_main_ui(self):
        self.yScorll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScorll.grid(row=1, column=1, sticky=tk.N+tk.S, padx=10, pady=10)

        self.txt = tk.StringVar()

        self.listbox = tk.Listbox(self, bg='white', exportselection=0, yscrollcommand=self.yScorll.set, activestyle="dotbox", listvariable=self.txt)
        self.listbox.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
        self.yScorll['command'] = self.listbox.yview

        for macro in self.data:
            self.listbox.insert(macro, self.data[macro]["keys"])

        self.selected = tk.Label(self, text="", height=10, wraplength=300, justify="left")
        self.selected.grid(row=1, column=3, padx=5)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)


        self.rmv_button = tk.Button(self, text="remove", command=lambda: self.remove(self.index), state="disabled", bg="lightgray")
        self.rmv_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.E)

        self.add_button = tk.Button(self, text="new macro", command=self.new_macro)
        self.add_button.grid(row= 2, column=3, pady=10, sticky=tk.W)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for macro in self.data:
            self.listbox.insert(macro, self.data[macro]["keys"])

    def remove(self, nb):
        utils.remove(self.data, nb)
        self.refresh_listbox()
        self.listbox.select_clear(0, tk.END)
        self.selected.config(text="")
        self.rmv_button.config(state="disabled", bg="lightgray")

    def new_macro(self):
        print("Rien pour l'instant")
        # creer une fenetre avec une entrée texte pour les touches (ou appuyer dessus ?)
        # faire une listebox ou les instructions a faire sont rangé dans l'ordre d'execution avec un boutton "add action" qui ouvre une fentre de selection d'une action avec ses parametres a choisir
        # et une derniere entrée texte pour le commentaire (par default égal a None) 

    def build_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self._("ui.options"), menu=self.menu)
        self.menu_lang = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label=self._("ui.lang"), menu=self.menu_lang)
        self.menu_lang.add_command(label=self._("ui.en"), command=lambda: self.set_lang("en"))
        self.menu_lang.add_command(label=self._("ui.fr"), command=lambda: self.set_lang("fr"))

        self.menu.add_command(label=self._("ui.key"), command=self.gui_keys)
        self.menu.add_command(label=self._("ui.help"), command=self.help)
        self.menu.add_separator()
        self.menu.add_command(label=self._("ui.uninstall"), command=self.confirm)
        

    def refresh_menu(self):
        self.menu_bar.delete(0, tk.END)
        self.build_menu()

    def ressource_path(self, path):
        base = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base, path)