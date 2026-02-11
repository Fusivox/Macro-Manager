import tkinter as tk , os, json, utils, i18n, sys
from tkinter import messagebox, simpledialog, ttk
from keyboard import add_hotkey, remove_hotkey
from screeninfo import get_monitors

def ressource_path(path):
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base, path)

i18n.load_path.append(ressource_path("locales"))
i18n.set("filename_format", "{locale}.yml")
i18n.set('locale', "en")
i18n.set("fallback", "fr")

_ = i18n.t

class Application(tk.Tk):
    def __init__(self, screenName = "Main page", baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.appdata = os.getenv("APPDATA")
        with open(f"{self.appdata}\\Macro Manager\\data.json", "r") as f:
            self.data = json.load(f)

        monitor = get_monitors()

        for m in monitor:
            if m.is_primary:
                if m.width > 1920 and m.height > 1080 :
                    self.tk.call("tk", "scaling", 2)
                    self.geometry("600x400")
                else : 
                    self.tk.call("tk", "scaling", 1.75)
                    self.geometry("500x300")
        
        self.title(_("ui.title"))
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.build_menu()

        # test TTK
        """self.frame = ttk.Frame(self, padding=0)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1, minsize=50)

        self.yScorll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.yScorll.grid(row=1, column=2, sticky="ns", padx=2, pady=2)

        self.tree = ttk.Treeview(
            self.frame,
            show="headings",
            yscrollcommand=self.yScorll.set,
            selectmode="browse"
        )
        self.tree.grid(row=1, column=1, sticky="nsew", padx=1, pady=2)

        self.yScorll.config(command=self.tree.yview)

        for macro in self.data:
            self.tree.insert("", "end", values=(macro, self.data[macro]["keys"],))
        
        self.selected = ttk.Label(self, text="", wraplength=300, justify="left")
        self.selected.grid(row=1, column=2, pady=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        selected = self.tree.selection()
        Keys = _("ui.keys")
        comment = _("ui.comment")
        if selected:
            index = str(self.tree.index(selected[0]))
            self.selected.config(text=f"{Keys} : {self.data[index]["keys"]} \n\n{comment} : {self.data[index]["comment"]}" if self.data[str(index)]["comment"] != None else f"{Keys} : {self.data[index]["keys"]} \n\n ")"""

        
        
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

    def on_select(self, event):
        selection = self.listbox.curselection()
        Keys = _("ui.keys")
        comment = _("ui.comment")
        if selection:
            index = str(selection[0])
            self.selected.config(text=f"{Keys} : {self.data[index]["keys"]} \n\n{comment} : {self.data[index]["comment"]}" if self.data[str(index)]["comment"] != None else f"{Keys} : {self.data[index]["keys"]} \n\n ")
            

        
    def close(self):
        utils.actualise(self.data)
        self.destroy()

    def confirm(self):
        sure = messagebox.askokcancel(
            title=_("ui.confirm"),
            message=_("ui.dlt_confirm")
        )
        if sure :
            utils.delete()
            if not os.path.exists(f"{self.appdata}\\Macro Manager"):
                messagebox.showinfo(
                    title=_("ui.info"),
                    message=_("ui.dlt_success")
                )
                self.destroy()
            else : 
                messagebox.showerror(
                    title=_("ui.info"),
                    message=_("ui.dlt_error")
                )

    def gui_keys(self):
        msg = _("ui.key_msg")

        keys = simpledialog.askstring(
            title=_("ui.key_change"),
            prompt=f"{msg} : {self.data["0"]["keys"]}"
        )
        if keys != None and keys != "":
            try :
                test = add_hotkey(keys, lambda : None)
                remove_hotkey(test)
                self.data["0"]["keys"] = keys
                
            except Exception :
                messagebox.showerror(
                    title=_("ui.invalid_key"),
                    message=_("ui.key_eg")
                )

    def help(self):
        self.help_menu = tk.Toplevel(height=400, width=400, takefocus=True)
        self.help_menu.title(_("ui.help_title"))

    def set_lang(self, lang):
        i18n.set("locale", lang)
        self.title(_("ui.title"))
        self.refresh_menu()

    def build_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=_("ui.options"), menu=self.menu)
        self.menu_lang = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label=_("ui.lang"), menu=self.menu_lang)
        self.menu_lang.add_command(label=_("ui.en"), command=lambda: self.set_lang("en"))
        self.menu_lang.add_command(label=_("ui.fr"), command=lambda: self.set_lang("fr"))

        self.menu.add_command(label=_("ui.key"), command=self.gui_keys)
        self.menu.add_command(label=_("ui.help"), command=self.help)
        self.menu.add_separator()
        self.menu.add_command(label=_("ui.uninstall"), command=self.confirm)
        

    def refresh_menu(self):
        self.menu_bar.delete(0, "end")
        self.build_menu()