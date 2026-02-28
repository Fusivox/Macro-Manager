import tkinter as tk , os, json, utils, i18n, sys, keyboard
from tkinter import messagebox, simpledialog, filedialog

if sys.platform == "win32": 
    name = "Main Page"
    macro_appdata = f"{os.getenv("APPDATA")}\\Macro Manager\\"
    platform = "win32"
if sys.platform == "linux": 
    name = None
    macro_appdata = f"{os.getenv("HOME")}/.config/Macro_Manager/"
    platform = "linux"

class Application(tk.Tk):
    def __init__(self, screenName = name, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        i18n.load_path.append(self.ressource_path("locales"))
        i18n.set("filename_format", "{locale}.yml")

        self.appdata = os.getenv("APPDATA") if platform == "win32" else os.getenv("HOME")
        with open(f"{macro_appdata}settings.json", "r") as f:
            self.settings = json.load(f)

        i18n.set('locale', self.settings["lang"])
        i18n.set("fallback", self.settings["fallback"])

        self._ = i18n.t
        
        with open(f"{macro_appdata}data.json", "r") as f:
            self.data = json.load(f)
        with open(f"{macro_appdata}abbreviation.json", "r") as f:
            self.abbreviation = json.load(f)

        self.tk.call("tk", "scaling", 1.75)
        self.geometry("550x350")
                
        self.resizable(False, False)
        
        self.title(self._("ui.title"))
        if platform == "win32": self.iconbitmap(default=self.ressource_path("logo.ico"))
        else: self.iconphoto(False, tk.PhotoImage(file=self.ressource_path("logo.png")))
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.help_running = False
        self.current_menu = "main"
        
        self.build_menu()
        self.build_main_ui()

    def on_select(self, event) -> None:
        """change le texte basé sur l'elements selectionné pour le menu macro"""

        self.selection = self.listbox.curselection()
        Keys = self._("ui.keys")
        comment = self._("ui.comment")
        self.rmv_button.config(state="normal", bg=self.rmv_button.master.cget("bg"))
        self.edit_button.config(state="normal", bg=self.rmv_button.master.cget("bg"))
        if self.selection:
            self.index = str(self.selection[0])
            self.selected.config(text=f"{Keys} : {self.data[self.index]["keys"]} \n\n{comment} : {self.data[self.index]["comment"]}" if self.data[self.index]["comment"] is not None else f"{Keys} : {self.data[self.index]["keys"]}\n\n")

    def abb_on_select(self, event) -> None:
        """change le texte basé sur l'elements selectionné pour le menu abbreviation"""

        self.abb_selection = self.abb_listbox.curselection()
        source = self._("ui.source")
        text = self._("ui.text")
        self.abb_rmv_button.config(state="normal", bg=self.rmv_button.master.cget("bg"))
        if self.abb_selection:
            self.abb_index = str(self.abb_selection[0])
            self.abb_selected.config(text=f"{source} : {self.abbreviation[self.abb_index]["source"]} \n\n{text} : {self.abbreviation[self.abb_index]["text"]}")
        
    def close(self) -> None:
        """ferme l'appli mais actualise tout les fichier json avant"""

        utils.actualise(self.data, self.settings, self.abbreviation, platform)
        self.destroy()

    def confirm(self) -> None:
        """demande de confirmation avant de suppr l'appli completement"""

        sure = messagebox.askokcancel(
            title=self._("ui.confirm"),
            message=self._("ui.dlt_confirm")
        )
        if sure :
            dlt = utils.delete_win32() if platform == "win32" else utils.delete_linux()
            if dlt:
                messagebox.showinfo(
                    title=self._("ui.info"),
                    message=self._("ui.dlt_success")
                )
                self.destroy()
                exit()
            else : 
                messagebox.showerror(
                    title=self._("ui.info"),
                    message=self._("ui.dlt_error")
                )

    def gui_keys(self) -> None:
        """change les touches pour ouvrir l'ui de l'app"""

        msg = self._("ui.key_msg")

        keys = simpledialog.askstring(
            title=self._("ui.key_change"),
            prompt=f"{msg} : {self.data["0"]["keys"]}"
        )
        if keys is not None and keys != "":
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

    def help(self) -> None:
        """ouvre le menu d'aide"""

        if not self.help_running:
            self.help_running = True
            self.help_menu = tk.Toplevel(height=400, width=400)
            self.help_menu.title(self._("ui.help_title"))
            self.help_menu.resizable(False, False)
            self.help_menu.focus_set()
            self.help_menu.transient(self)
            self.help_menu.protocol("WM_DELETE_WINDOW", self.close_help)

    def close_help(self) -> None:
        "ferme le menu d'aide"

        self.help_running = False
        self.help_menu.destroy()

    def set_lang(self, lang: str, fallback: str) -> None:
        """change la langue de l'app"""

        i18n.set("locale", lang)
        self.settings["lang"] = lang
        self.settings["fallback"] = fallback
        utils.actualise(settings=self.settings, os_name=platform)
        self.title(self._("ui.title"))
        self.refresh_ui()

    def build_main_ui(self) -> None:
        """construit l'ui du menu macro"""

        self.yScorll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScorll.grid(row=1, column=1, sticky=tk.N+tk.S, padx=10, pady=10)

        self.listbox = tk.Listbox(self, bg='white', exportselection=0, yscrollcommand=self.yScorll.set, activestyle="dotbox",)
        self.listbox.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
        self.yScorll['command'] = self.listbox.yview

        self.build_listbox()

        self.selected = tk.Label(self, text="", height=10, wraplength=300, justify="left")
        self.selected.grid(row=1, column=3, padx=5)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.rmv_button = tk.Button(self, text=self._("ui.rmv"), command=lambda: self.remove("data", self.index), state="disabled", bg="lightgray")
        self.rmv_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.E)

        self.add_button = tk.Button(self, text=self._("ui.new"), command=self.new_macro)
        self.add_button.grid(row=2, column=3, pady=10, sticky=tk.W)

        self.edit_button = tk.Button(self, text=self._("ui.edit"), command=self.edit_macro, state="disabled", bg="lightgray")
        self.edit_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

    def build_abb_ui(self) -> None:
        """construit l'ui du menu abbreviation"""

        self.abb_yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.abb_yScroll.grid(row=1, column=1, sticky=tk.N+tk.S, padx=10, pady=10)

        self.abb_listbox = tk.Listbox(self, bg='white', exportselection=0, yscrollcommand=self.abb_yScroll.set, activestyle="dotbox")
        self.abb_listbox.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
        self.abb_yScroll['command'] = self.abb_listbox.yview

        self.abb_build_listbox()

        self.abb_selected = tk.Label(self, text="", height=10, wraplength=300, justify=tk.LEFT)
        self.abb_selected.grid(row=1, column=3, padx=5)

        self.abb_listbox.bind("<<ListboxSelect>>", self.abb_on_select)

        self.abb_rmv_button = tk.Button(self, text=self._("ui.rmv"), command=lambda: self.remove("abb", self.abb_index), state="disabled", bg="lightgray")
        self.abb_rmv_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.E)

        self.abb_add_button = tk.Button(self, text=self._("ui.abb_new"), command=self.new_abbreviation)
        self.abb_add_button.grid(row= 2, column=3, pady=10, sticky=tk.W)

    def build_listbox(self, refresh: bool = False) -> None:
        """creer la listhox des macro existante"""

        if refresh : self.listbox.delete(0, tk.END)
        for macro in self.data:
            self.listbox.insert(macro, self.data[macro]["keys"]) if self.data[macro]["keys"] is not None else self.listbox.insert(macro, self._("ui.no_key"))

    def abb_build_listbox(self, refresh: bool = False) -> None:
        """creer la listbox des abbreviations existante"""

        if refresh : self.abb_listbox.delete(0, tk.END)
        for abb in self.abbreviation:
            self.abb_listbox.insert(abb, self.abbreviation[abb]["source"])

    def remove(self, source: str, nb) -> None:
        """retire un éléments du fichier json séléctionné (data ou abb pour abbreviation)"""

        if source == "data" :
            rmv = utils.remove(self.data, nb)
            self.data = {str(i): self.data[keys] for i, keys in enumerate(sorted(self.data.keys()))}
            print(f">Debug : {self.data}")
            if rmv:
                self.build_listbox(refresh=True)
                self.listbox.select_clear(0, tk.END)
                self.selected.config(text="")
                self.rmv_button.config(state="disabled", bg="lightgray")
                self.edit_button.config(state="disabled", bg="lightgray")

        elif source == "abb" :
            rmv = utils.remove(self.abbreviation, nb)
            self.abbreviation = {str(i): self.abbreviation[keys] for i, keys in enumerate(sorted(self.abbreviation.keys()))}
            print(f">Debug : {self.abbreviation}")
            if rmv:
                self.abb_build_listbox(refresh=True)
                self.abb_listbox.select_clear(0, tk.END)
                self.abb_selected.config(text="")
                self.abb_rmv_button.config(state="disabled", bg="lightgray")

    def new_macro(self) -> None:
        """creer une fenetre avec une entrée texte pour les touches qui peut être mis a None dans le cas ou c'est une action utile dans le task scheduler (future ajout) mais qu'on ne veut pas sous forme de macro
        c'est une listebox ou les instructions a faire sont rangé dans l'ordre d'execution avec un boutton "add action" qui ouvre une fentre de selection d'une action avec ses parametres a choisir
        et une derniere entrée texte pour le commentaire (par default égal a None)""" 

        self.nmcr_menu = tk.Toplevel(self, width=300, height=400)
        self.nmcr_menu.title(self._("ui.nmcr_title"))

        self.nmcr_menu.grab_set()
        self.nmcr_menu.focus_set()
        self.nmcr_menu.transient(self)
        self.nmcr_menu.resizable(False, False)

        keys_txt = f"{self._("ui.keys")} : "
        keys_lbl = tk.Label(self.nmcr_menu, text=keys_txt, justify=tk.RIGHT)
        keys_lbl.grid(row=0, column=0, padx=10, pady=10)


        keys = tk.Entry(self.nmcr_menu, justify=tk.CENTER, exportselection=0)
        keys.grid(row=0, column=1, sticky=tk.E+tk.W, padx=10, pady=10)
        
        mcr_yScroll = tk.Scrollbar(self.nmcr_menu, orient=tk.VERTICAL)
        mcr_yScroll.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E, padx=10, pady=10)

        mcr_listbox = tk.Listbox(self.nmcr_menu, bg='white', exportselection=0, yscrollcommand=mcr_yScroll.set, activestyle="dotbox")
        mcr_listbox.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
        mcr_yScroll['command'] = mcr_listbox.yview

        com_txt = f"{self._("ui.comment")} : "
        com_lbl = tk.Label(self.nmcr_menu, text=com_txt, justify=tk.RIGHT)
        com_lbl.grid(row=2, column=0, padx=10, pady=10)

        comment = tk.Entry(self.nmcr_menu, exportselection=0)
        comment.grid(row=2, column=1, sticky=tk.E+tk.W, padx=10, pady=10)

        def create_macro() -> None:
            """creer et sauvegarde dans le fichier json la macro a partir des parametres renseigné (keys, actions et comment)"""

            _key = keys.get() or None                                   # mets a None si y'a rien d'ecrit (parce que sinon tkinter renvoie "" et c'est relou)
            _comment = comment.get() or None
            _actions = list(mcr_listbox.get(0, tk.END))                 # creer une liste avec les actions dans la listbox, on stocke un syntaxe utilisateur plus simple a comprendre pour la convertir en syntaxe programme avec translate_callback
            _actions = utils.translate_callback(_actions)               # transforme la syntaxe utilisateur en syntaxe programme
            if len(_actions) > 0:                                       # Si aucune actions ça fait rien et ferme juste la fenetre 
                utils.add_mcr(self.data, _key, _actions, _comment)
                utils.actualise(data=self.data, os_name=platform)                    
                if _key is not None :                                   # Initialise la macro si des touches sont définis
                    callback = utils.make_callback(_actions)
                    keyboard.add_hotkey(_key, callback)  

                self.build_listbox(refresh=True)
            self.nmcr_menu.destroy()

        def add_action() -> None:
            """permet d'ajouter une action a la macro actuellement en creation"""

            actions = ["open", "wait", "write", "click", "moveto", "move", "press"]           # liste des actions possible (a actualiser en même temps que le fonction make_callback dans utils)
            
            def close() -> None: 
                """ferme le menu pour ajouter une action et rends le focus au menu de creation de macro"""

                self.nmcr_menu.focus_set()
                self.nmcr_menu.grab_set()
                add_action_menu.destroy()

            def ask_params() -> None:
                """demande les parametres de l'actions en train d'être creer"""

                selected_action = actions_list.get(actions_list.curselection()[0])
                title = self._("ui.params_title").format(action=selected_action)
                print(f">Debug : {selected_action}")

                def init_params_menu() -> None:
                    """creer la fenetre de base pour renseigner les parametres de l'action en train d'être creer"""

                    global params_menu
                    params_menu = tk.Toplevel(add_action_menu, width=300, height=400)
                    params_menu.title(title)
                    params_menu.grab_set()
                    params_menu.focus_set()
                    params_menu.transient(add_action_menu)
                    params_menu.resizable(False, False)

                def close_params_menu() -> None:
                    """ferme la fenetre pour renseigner les parametres de l'action en train d'être creer et rends le focus a la fenetre pour ajouter une action"""

                    add_action_menu.grab_set()
                    add_action_menu.focus_set()
                    params_menu.destroy()

                if selected_action == "wait":
                    time = simpledialog.askfloat(title=self._("ui.wait_title"), prompt=self._("ui.wait"))
                    if time is not None : mcr_listbox.insert(tk.END, f"{selected_action} : {time}") 

                else:
                    init_params_menu()

                    if selected_action == "write": 

                        text_label = tk.Label(params_menu, text=f"{self._("ui.text")} :", justify=tk.RIGHT)
                        text_label.grid(row=0, column=0, padx=10, pady=10)

                        text_entry = tk.Entry(params_menu, exportselection=0)
                        text_entry.grid(row=0, column=1, sticky=tk.E+tk.W, padx=10, pady=10)

                        interval_label = tk.Label(params_menu, text=f"{self._("ui.interval")} :", justify=tk.RIGHT)
                        interval_label.grid(row=1, column=0, padx=10, pady=10)

                        interval_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        interval_entry.grid(row=1, column=1, padx=10, pady=10)

                        def add_write() -> None:
                            """ajoute aux actions la fonction write avec les parametres renseigné"""

                            interval = utils.convert(interval_entry.get() or 0)
                            if isinstance(interval, (int, float)) and len(text_entry.get()) > 0:

                                write_command = f"{selected_action} : {text_entry.get()}"
                                if interval != 0:
                                    write_command += f" ;; interval : {interval}"

                                mcr_listbox.insert(tk.END, write_command)

                                close_params_menu()
                                
                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_write)
                        validate_button.grid(row=2, column=1, padx=10, pady=10)

                    elif selected_action == "click":
                        
                        button_label = tk.Label(params_menu, text=f"{self._("ui.button")} :", justify=tk.RIGHT)
                        button_label.grid(row=0, column=0, padx=10, pady=10)

                        buttonlist = (self._("primary"), self._("secondary"), self._("middle"))
                        buttonvar = tk.StringVar()
                        buttonvar.set(buttonlist[0])

                        button_entry = tk.OptionMenu(params_menu, buttonvar, *buttonlist)
                        button_entry.grid(row=0, column=1, padx=10, pady=10)

                        x_label = tk.Label(params_menu, text=f"{self._("ui.x")} :", justify=tk.RIGHT)
                        x_label.grid(row=1, column=0, padx=10, pady=10)

                        x_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=1)
                        x_entry.grid(row=1, column=1, padx=10, pady=10)

                        y_label = tk.Label(params_menu, text=f"{self._("ui.y")} :", justify=tk.RIGHT)
                        y_label.grid(row=1, column=2, padx=10, pady=10)

                        y_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=1)
                        y_entry.grid(row=1, column=3, padx=10, pady=10)

                        clicks_label = tk.Label(params_menu, text=f"{self._("ui.clicks")} :", justify=tk.RIGHT)
                        clicks_label.grid(row=2, column=0, padx=10, pady=10)

                        clicks_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=1)
                        clicks_entry.grid(row=2, column=1, padx=10, pady=10)

                        interval_label = tk.Label(params_menu, text=f"{self._("ui.interval")} :", justify=tk.RIGHT)
                        interval_label.grid(row=2, column=2, padx=10, pady=10)

                        interval_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        interval_entry.grid(row=2, column=3, padx=10, pady=10)

                        duration_label = tk.Label(params_menu, text=f"{self._("ui.duration")} :", justify=tk.RIGHT)
                        duration_label.grid(row=3, column=0, padx=10, pady=10)

                        duration_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        duration_entry.grid(row=3, column=1, padx=10, pady=10)

                        def add_click() -> None:
                            """ajoute aux actions la fonction click avec les parametres renseigné"""

                            button = buttonvar.get()
                            x, y = utils.convert(x_entry.get() or None) , utils.convert(y_entry.get() or None)
                            duration = utils.convert(duration_entry.get() or 0)
                            interval = utils.convert(interval_entry.get() or 0)
                            clicks = utils.convert(clicks_entry.get() or 1)

                            if isinstance(clicks, (int, float)) and isinstance(interval, (int, float)) and isinstance(duration, (int, float)) and (isinstance(x, (float, int)) or x is None) and (isinstance(y, (float, int)) or y is None) and (x is not None or y is not None): 
                                
                                click_command = f"{selected_action} : {button}"
                                if x is not None:
                                    click_command += f" ;; x : {x}"
                                if y is not None:
                                    click_command += f" ;; y : {y}"
                                if duration != 0:
                                    click_command += f" ;; duration : {duration}"
                                if interval != 0:
                                    click_command += f" ;; interval : {interval}"
                                if clicks != 1:
                                    click_command += f" ;; clicks : {clicks}"

                                mcr_listbox.insert(tk.END, click_command)

                                close_params_menu()
                            
                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_click)
                        validate_button.grid(row=4, column=3, padx=10, pady=10)

                    elif selected_action == "moveto":

                        x_label = tk.Label(params_menu, text=f"{self._("ui.x")} :", justify=tk.RIGHT)
                        x_label.grid(row=0, column=0, padx=10, pady=10)

                        x_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=1)
                        x_entry.grid(row=0, column=1, padx=10, pady=10)

                        y_label = tk.Label(params_menu, text=f"{self._("ui.y")} :", justify=tk.RIGHT)
                        y_label.grid(row=0, column=2, padx=10, pady=10)

                        y_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=1)
                        y_entry.grid(row=0, column=3, padx=10, pady=10)

                        duration_label = tk.Label(params_menu, text=f"{self.i("ui.duration")} :", justify=tk.RIGHT)
                        duration_label.grid(row=1, column=0, padx=10, pady=10)

                        duration_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        duration_entry.grid(row=1, column=1, padx=10, pady=10)

                        def add_moveto() -> None:
                            """ajoute aux actions la fonction move avec les parametres renseigné"""

                            x, y = utils.convert(x_entry.get() or None), utils.convert(y_entry.get() or None)
                            duration = utils.convert(duration_entry.get() or 0)

                            if isinstance(duration, (int, float)) and (isinstance(x, (float, int)) or x is None) and (isinstance(y, (float, int)) or y is None) and (x is not None or y is not None): 

                                moveto_command = f"{selected_action} : {duration}"
                                if x is not None:
                                    moveto_command += f" ;; x : {x}"
                                if y is not None:
                                    moveto_command += f" ;; y : {y}"

                                mcr_listbox.insert(tk.END, moveto_command)

                                close_params_menu()

                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_moveto)
                        validate_button.grid(row=2, column=3, padx=10, pady=10)

                    elif selected_action == "move":
                        
                        x_label = tk.Label(params_menu, text=f"{self._("ui.x")} :", justify=tk.RIGHT)
                        x_label.grid(row=0, column=0, padx=10, pady=10)

                        x_entry = tk.Spinbox(params_menu, exportselection=0, from_=-1000000, to=1000000, increment=1)
                        x_entry.grid(row=0, column=1, padx=10, pady=10)

                        y_label = tk.Label(params_menu, text=f"{self._("ui.y")} :", justify=tk.RIGHT)
                        y_label.grid(row=0, column=2, padx=10, pady=10)

                        y_entry = tk.Spinbox(params_menu, exportselection=0, from_=-1000000, to=1000000, increment=1)
                        y_entry.grid(row=0, column=3, padx=10, pady=10)

                        duration_label = tk.Label(params_menu, text=f"{self.i("ui.duration")} :", justify=tk.RIGHT)
                        duration_label.grid(row=1, column=0, padx=10, pady=10)

                        duration_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        duration_entry.grid(row=1, column=1, padx=10, pady=10)

                        def add_move() -> None:
                            """ajoute aux actions la fonction move avec les parametres renseigné"""

                            x, y = utils.convert(x_entry.get() or None), utils.convert(y_entry.get() or None)
                            duration = utils.convert(duration_entry.get() or 0)

                            if isinstance(duration, (int, float)) and (isinstance(x, (float, int)) or x is None) and (isinstance(y, (float, int)) or y is None) and (x is not None or y is not None): 

                                move_command = f"{selected_action} : {duration}"
                                if x is not None:
                                    move_command += f" ;; x : {x}"
                                if y is not None:
                                    move_command += f" ;; y : {y}"

                                mcr_listbox.insert(tk.END, move_command)

                                close_params_menu()

                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_move)
                        validate_button.grid(row=2, column=3, padx=10, pady=10)

                    elif selected_action == "press":

                        press_label = tk.Label(params_menu, text=f"{self._("ui.press")} :", justify=tk.RIGHT)
                        press_label.grid(row=0, column=0, padx=10, pady=10)

                        press_entry = tk.Entry(params_menu, exportselection=0)
                        press_entry.grid(row=0, column=1, sticky=tk.E+tk.W, padx=10, pady=10)

                        presses_label = tk.Label(params_menu, text=f"{self._("ui.presses")} :", justify=tk.RIGHT)
                        presses_label.grid(row=1, column=0, padx=10, pady=10)

                        presses_entry = tk.Spinbox(params_menu, exportselection=0, from_=1, to=1000000, increment=1)
                        presses_entry.grid(row=1, column=1, padx=10, pady=10)

                        interval_label = tk.Label(params_menu, text=f"{self._("ui.interval")} :", justify=tk.RIGHT)
                        interval_label.grid(row=2, column=0, padx=10, pady=10)

                        interval_entry = tk.Spinbox(params_menu, exportselection=0, from_=0, to=1000000, increment=0.1)
                        interval_entry.grid(row=2, column=1, padx=10, pady=10)

                        def add_press():
                            """ajoute aux actions la fonction press avec les parametres renseigné"""

                            interval = utils.convert(interval_entry.get() or 0)
                            presses = utils.convert(presses_entry.get() or 1)
                            key = press_entry.get().strip().lower()
                            if isinstance(interval, (float, int)) and isinstance(presses, (int, float)) and key in utils.POSSIBLE_KEYS:

                                press_command = f"{selected_action} : {key}"
                                if presses != 1:
                                    press_command += f" ;; presses : {presses}"
                                    if interval != 0:
                                        press_command += f" ;; interval : {interval}"

                                mcr_listbox.insert(tk.END, press_command)

                                close_params_menu()

                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_press)
                        validate_button.grid(row=3, column=1, padx=10, pady=10)

                    elif selected_action == "open":
                        
                        path_label = tk.Label(params_menu, text=f"{self._("ui.path")} :", justify=tk.RIGHT)
                        path_label.grid(row=0, column=0, padx=10, pady=10)

                        pathvar = tk.StringVar()
                        path_entry = tk.Entry(params_menu, exportselection=0, textvariable=pathvar)
                        path_entry.grid(row=0, column=1, padx=10, pady=10)


                        def browse_file():
                            """ouvre une fenetre de recherche de fichier et mets son chemin dans l'entry"""

                            path = filedialog.askopenfilename(
                                title=self._("ui.files"),
                                filetypes=[(self._("ui.file_type"), "*.*")]
                            )
                            if path: pathvar.set(path)

                        browsefile_button = tk.Button(params_menu, text=self._("ui.browse"), command=browse_file)
                        browsefile_button.grid(row=0, column=2, padx=10, pady=10)

                        param_label = tk.Label(params_menu, text=f"{self._("ui.add_param")} :", justify=tk.RIGHT)
                        param_label.grid(row=1, column=0, padx=10, pady=10)

                        paramvar = tk.StringVar()
                        param_entry = tk.Entry(params_menu, exportselection=0, textvariable=paramvar)
                        param_entry.grid(row=1, column=1, padx=10, pady=10)

                        def browse_folder():
                            """ouvre une fenetre de recherche de dossier et mets son chemin dans l'entry"""

                            path = filedialog.askdirectory(
                                title=self._("ui.folder")
                            )
                            if path: paramvar.set(path)

                        browseparam_button = tk.Button(params_menu, text=self._("ui.browse"), command=browse_folder)
                        browseparam_button.grid(row=1, column=2, padx=10, pady=10)

                        def add_open():
                            """ajoute aux actions la fonction open avec les parametres renseigné"""

                            path = pathvar.get().strip() or None
                            additional_param = paramvar.get().strip() or None

                            if path is not None:

                                if path.lower() == "cmd" or path.lower() == "shell":
                                    
                                    if platform == "win32":
                                        open_command = f"{selected_action} : cmd"
                                    else:
                                        open_command = f"{selected_action} : shell"

                                    if additional_param is not None:
                                        open_command += f" ;; param : {additional_param}"

                                else : open_command = f"{selected_action} : {path}"

                                mcr_listbox.insert(tk.END, open_command)
                                
                                close_params_menu()

                        validate_button = tk.Button(params_menu, text=self._("ui.choose_act"), command=add_open)
                        validate_button.grid(row=2, column=2, padx=10, pady=10)

            add_action_menu = tk.Toplevel(self.nmcr_menu, width=300, height=400)
            add_action_menu.title(self._("ui.add_action"))

            add_action_menu.grab_set()
            add_action_menu.focus_set()
            add_action_menu.transient(self.nmcr_menu)
            add_action_menu.resizable(False, False)
            add_action_menu.protocol("WM_DELETE_WINDOW", close)

            actions_list_yScorll = tk.Scrollbar(add_action_menu, orient=tk.VERTICAL)
            actions_list_yScorll.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E, padx=10, pady=10)

            actions_list = tk.Listbox(add_action_menu, bg='white', exportselection=0, yscrollcommand=actions_list_yScorll.set, activestyle="dotbox")
            actions_list.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
            actions_list_yScorll['command'] = actions_list.yview

            for action in actions:
                actions_list.insert(tk.END, action)

            choose_button = tk.Button(add_action_menu, text=self._("ui.choose_act"), command=ask_params)
            choose_button.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

        add_button = tk.Button(self.nmcr_menu, text=self._("ui.naction"), justify=tk.LEFT, command=add_action)
        add_button.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)

        create_button = tk.Button(self.nmcr_menu, text=self._("ui.nmcr"), justify=tk.RIGHT, command=create_macro)
        create_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)

    def edit_macro(self) -> None:
        """creation de la même fenetre que pour le new_macro mais avec les cases prérempli avec les data associé a la macro séléctionné (a faire apres que le new_macro soit complétement fait)
        faut juste faire que les StringVar contiennet le data[id]["keys"] et data[id]["comment"] pour les Entry et faire un for act in actions mcr_listbox.insert(act, -Synthaxe choisi-)"""

        return 0
    
    def new_abbreviation(self) -> None:
        """demande les parametres d'une nouvelle abreviation puis l'ajoute ou remplace si elle existe deja"""

        self.nabb_menu = tk.Toplevel(self, width=300, height=400)
        self.nabb_menu.title(self._("ui.nabb_title"))

        self.nabb_menu.grab_set()
        self.nabb_menu.focus_set()
        self.nabb_menu.transient(self)
        self.nabb_menu.resizable(False, False)

        source_txt = f"{self._("ui.source")} : "
        source_lbl = tk.Label(self.nabb_menu, text=source_txt, justify=tk.RIGHT)
        source_lbl.grid(row=0, column=0, padx=10, pady=10)

        source_entry = tk.Entry(self.nabb_menu, justify=tk.CENTER, exportselection=0)
        source_entry.grid(row=0, column=1, padx=20, pady=10)

        abb_txt = f"{self._("ui.text")} : "
        abb_lbl = tk.Label(self.nabb_menu, text=abb_txt, justify=tk.RIGHT)
        abb_lbl.grid(row=1, column=0, padx=10, pady=10)

        abb_entry = tk.Entry(self.nabb_menu, justify=tk.CENTER, exportselection=0)
        abb_entry.grid(row=1, column=1, padx=10, pady=10)

        def add_act() -> None:
            """ajoute l'abbreviation a partir des parametres renseigné dans le menu"""

            source = source_entry.get()
            abb = abb_entry.get()
            print(f">Debug : {source}\n>Debug : {self.abbreviation}")

            for id in self.abbreviation:
                print(f">Debug : {self.abbreviation[id]}")
                if source == self.abbreviation[id]["source"] :
                    self.abbreviation[id]["text"] = abb          # si il existe deja une abreviations avec ce "declancheur" ça l'enleve 
                    keyboard.remove_abbreviation(source)
                    
                    break

            else:
                utils.add_abb(self.abbreviation, source, abb)
                                                                                    # ajoute l'abreviations et actualise le json puis l'initialise pour l'utiliser direct     

            utils.actualise(abbreviation=self.abbreviation, os_name=platform)  
            keyboard.add_abbreviation(source, abb)

            self.abb_build_listbox(refresh=True)
            self.nabb_menu.destroy()
        
        add_button = tk.Button(self.nabb_menu, text=self._("ui.nabb"), command=add_act)
        add_button.grid(row=3, column=0, padx=10, pady=10)

        self.build_menu()

    def refresh_ui(self, switch: bool = False) -> None:
        """clear l'ui actuel et le reconstruit par default
        l'argument switch permet de passer entre le main ui (pour les macros) et le abb ui (pour les abreviations)"""

        for widget in self.winfo_children() :
            widget.destroy()

        if self.current_menu == "main":
            
            if switch: 
                self.current_menu = "abb"
                self.build_abb_ui()

            else: self.build_main_ui()

        elif self.current_menu == "abb":
            
            if switch: 
                self.current_menu = "main"
                self.build_main_ui()
                
            else: self.build_abb_ui()

        self.build_menu()


    def build_menu(self) -> None:
        """construit le menu en haut de l'app"""

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self._("ui.options"), menu=self.menu)
        self.menu_lang = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label=self._("ui.lang"), menu=self.menu_lang)
        self.menu_lang.add_command(label=self._("ui.en"), command=lambda: self.set_lang("en", "fr"))
        self.menu_lang.add_command(label=self._("ui.fr"), command=lambda: self.set_lang("fr", "en"))

        self.menu.add_command(label=self._("ui.key"), command=self.gui_keys)
        self.menu.add_command(label=self._("ui.help"), command=self.help)
        self.menu.add_separator()
        self.menu.add_command(label=self._("ui.uninstall"), command=self.confirm)

        if self.current_menu == "main":
            self.menu_bar.add_command(label=self._("ui.htk"), command=lambda: self.refresh_ui(switch=True))
        elif self.current_menu == "abb":
            self.menu_bar.add_command(label=self._("ui.abb"), command=lambda: self.refresh_ui(switch=True))

    def refresh_menu(self) -> None:
        """clear le menu puis le reconstruit"""

        self.menu_bar.delete(0, tk.END)
        self.build_menu()

    def ressource_path(self, path: str) -> str:
        """permet a l'exe de trouver le chemin du fichier/ressource renseigné"""

        base = getattr(sys, '_MEIPASS', os.path.abspath("."))

        return os.path.join(base, path)