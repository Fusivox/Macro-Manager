import tkinter as tk , os, json, utils, i18n, sys, screeninfo, keyboard
from tkinter import messagebox, simpledialog

if sys.platform == "win32": name = "Main Page"
if sys.platform == "linux": name = None

class Application(tk.Tk):
    def __init__(self, screenName = name, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
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
        with open(f"{self.appdata}\\Macro Manager\\abbreviation.json", "r") as f:
            self.abbreviation = json.load(f)

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
        if sys.platform == "win32": self.iconbitmap(default=self.ressource_path("logo.ico"))
        else: self.iconphoto(False, tk.PhotoImage(file="logo.png"))
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.help_running = False
        self.current_menu = "main"
        
        self.build_menu()
        self.build_main_ui()

    def on_select(self, event):
        self.selection = self.listbox.curselection()
        Keys = self._("ui.keys")
        comment = self._("ui.comment")
        self.rmv_button.config(state="normal", bg="SystemButtonFace")
        if self.selection:
            self.index = str(self.selection[0])
            self.selected.config(text=f"{Keys} : {self.data[self.index]["keys"]} \n\n{comment} : {self.data[self.index]["comment"]}" if self.data[self.index]["comment"] is not None else f"{Keys} : {self.data[self.index]["keys"]}\n\n")

    def abb_on_select(self, event):
        self.abb_selection = self.abb_listbox.curselection()
        source = self._("ui.source")
        text = self._("ui.text")
        self.abb_rmv_button.config(state="normal", bg="SystemButtonFace")
        if self.abb_selection:
            self.abb_index = str(self.abb_selection[0])
            self.abb_selected.config(text=f"{source} : {self.abbreviation[self.abb_index]["source"]} \n\n{text} : {self.abbreviation[self.abb_index]["text"]}")
        
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

    def help(self):
        if not self.help_running:
            self.help_running = True
            self.help_menu = tk.Toplevel(height=400, width=400)
            self.help_menu.title(self._("ui.help_title"))
            self.help_menu.resizable(False, False)
            self.help_menu.focus_set()
            self.help_menu.transient(self)
            self.help_menu.protocol("WM_DELETE_WINDOW", self.help_false)

    def help_false(self):
        self.help_running = False
        self.help_menu.destroy()

    def set_lang(self, lang):
        i18n.set("locale", lang)
        self.title(self._("ui.title"))
        self.refresh_ui()

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

        self.rmv_button = tk.Button(self, text=self._("ui.rmv"), command=lambda: self.remove("data", self.index), state="disabled", bg="lightgray")
        self.rmv_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.E)

        self.add_button = tk.Button(self, text=self._("ui.new"), command=self.new_macro)
        self.add_button.grid(row= 2, column=3, pady=10, sticky=tk.W)

    def build_abb_ui(self):
        self.abb_yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.abb_yScroll.grid(row=1, column=1, sticky=tk.N+tk.S, padx=10, pady=10)

        self.abb_txt = tk.StringVar()

        self.abb_listbox = tk.Listbox(self, bg='white', exportselection=0, yscrollcommand=self.abb_yScroll.set, activestyle="dotbox", listvariable=self.abb_txt)
        self.abb_listbox.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=10)
        self.abb_yScroll['command'] = self.abb_listbox.yview

        for abb in self.abbreviation:
            self.abb_listbox.insert(abb, self.abbreviation[abb]["source"])

        self.abb_selected = tk.Label(self, text="", height=10, wraplength=300, justify="left")
        self.abb_selected.grid(row=1, column=3, padx=5)

        self.abb_listbox.bind("<<ListboxSelect>>", self.abb_on_select)

        self.abb_rmv_button = tk.Button(self, text=self._("ui.rmv"), command=lambda: self.remove("abb", self.abb_index), state="disabled", bg="lightgray")
        self.abb_rmv_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.E)

        self.abb_add_button = tk.Button(self, text=self._("ui.abb_new"), command=self.new_abbreviation)
        self.abb_add_button.grid(row= 2, column=3, pady=10, sticky=tk.W)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for macro in self.data:
            self.listbox.insert(macro, self.data[macro]["keys"])

    def abb_refresh_listbox(self):
        self.abb_listbox.delete(0, tk.END)
        for abb in self.abbreviation:
            self.abb_listbox.insert(abb, self.abbreviation[abb]["text"])

    def remove(self, source : str, nb):
        if source == "data" :
            rmv = utils.remove(self.data, nb)
            self.data = {str(i): self.data[keys] for i, keys in enumerate(sorted(self.data.keys()))}
            print(f">Debug : {self.data}")
            if rmv:
                self.refresh_listbox()
                self.listbox.select_clear(0, tk.END)
                self.selected.config(text="")
                self.rmv_button.config(state="disabled", bg="lightgray")

        elif source == "abb" :
            rmv = utils.remove(self.abbreviation, nb)
            self.abbreviation = {str(i): self.abbreviation[keys] for i, keys in enumerate(sorted(self.abbreviation.keys()))}
            print(f">Debug : {self.abbreviation}")
            if rmv:
                self.abb_refresh_listbox()
                self.abb_listbox.select_clear(0, tk.END)
                self.abb_selected.config(text="")
                self.abb_rmv_button.config(state="disabled", bg="lightgray")

    def new_macro(self):
        # creer une fenetre avec une entrée texte pour les touches (ou appuyer dessus ?)
        # faire une listebox ou les instructions a faire sont rangé dans l'ordre d'execution avec un boutton "add action" qui ouvre une fentre de selection d'une action avec ses parametres a choisir
        # et une derniere entrée texte pour le commentaire (par default égal a None) 
        self.nmcr_menu = tk.Toplevel(self, width=300, height=400)
        self.nmcr_menu.title(self._("ui.nmcr_title"))

        self.nmcr_menu.grab_set()
        self.nmcr_menu.focus_set()
        self.nmcr_menu.transient(self)
        self.nmcr_menu.resizable(False, False)

    def new_abbreviation(self):
        self.nabb_menu = tk.Toplevel(self, width=300, height=400)
        self.nabb_menu.title(self._("ui.nabb_title"))

        self.nabb_menu.grab_set()
        self.nabb_menu.focus_set()
        self.nabb_menu.transient(self)
        self.nabb_menu.resizable(False, False)

        #ajouter deux entrée texte pour l'abbreviation et pour le texte et le bouton "add"

    def switch_ui(self):
        for widget in self.winfo_children() :
            widget.destroy()

        if self.current_menu == "main":
            self.current_menu = "abb"
            self.build_abb_ui()

        elif self.current_menu == "abb":
            self.current_menu = "main"
            self.build_main_ui()

        self.build_menu()

    def refresh_ui(self):
        for widget in self.winfo_children() :
            widget.destroy()

        if self.current_menu == "main":
            self.build_main_ui()

        elif self.current_menu == "abb":
            self.build_abb_ui()

        self.refresh_menu()


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

        if self.current_menu == "main":
            self.menu_bar.add_command(label=self._("ui.abb"), command=self.switch_ui)
        elif self.current_menu == "abb":
            self.menu_bar.add_command(label=self._("ui.htk"), command=self.switch_ui)

    def refresh_menu(self):
        self.menu_bar.delete(0, tk.END)
        self.build_menu()

    def ressource_path(self, path):
        base = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base, path)