import tkinter as tk
from tkinter import messagebox
from screeninfo import get_monitors

def test():
    messagebox.showinfo(
        title="Informations",
        message="New file created"
    )


root = tk.Tk()
root.title("tkinter test tk")
root.geometry("400x300")

menu_bar = tk.Menu(root)

menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

menu_fichier.add_command(label="Nouveau", command=test)
menu_fichier.add_command(label="Ouvrir")
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=root.destroy)

menu_edition = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Édition", menu=menu_edition)

menu_couleurs = tk.Menu(menu_edition, tearoff=0)
menu_edition.add_cascade(label="Couleurs", menu=menu_couleurs)

menu_couleurs.add_command(label="Rouge")
menu_couleurs.add_command(label="Vert")
menu_couleurs.add_command(label="Bleu")

root.config(menu=menu_bar)

yScroll = tk.Scrollbar(root, orient=tk.VERTICAL)
yScroll.grid(row=10, column=11, sticky=tk.N+tk.S)

contenu = tk.StringVar()

listeboxe = tk.Listbox(root, bg="white", exportselection=0, yscrollcommand=yScroll.set, activestyle="dotbox", listvariable=contenu)
listeboxe.grid(row=10, column=10, sticky=tk.N+tk.S+tk.E+tk.W, padx=10, pady=10)
yScroll['command'] = listeboxe.yview

for i in range(20):
    listeboxe.insert(i, f"ligne numéro {i+1}")


info = tk.Label(root, text="No value selected", height=2)
info.grid(row=10, column=12, padx=5)

def on_select(event):
    selection = listeboxe.curselection()
    if selection:
        index = selection[0]
        info.config(text=f"item number {index+1} has been selected")

listeboxe.bind("<<ListboxSelect>>", on_select)

root.mainloop()

monitor = get_monitors()

for m in monitor :
    if m.is_primary :
        print(f"Resolution: {m.width}x{m.height}")

import tkinter as tk
from tkinter import ttk


def test():
    print("Nouveau fichier")


root = tk.Tk()
root.title("tkinter test ttk")
root.geometry("400x300")

# =======================
# MENU (reste en tk)
# =======================
menu_bar = tk.Menu(root)

menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_fichier.add_command(label="Nouveau", command=test)
menu_fichier.add_command(label="Ouvrir")
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=root.destroy)

menu_edition = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Édition", menu=menu_edition)

menu_couleurs = tk.Menu(menu_edition, tearoff=0)
menu_edition.add_cascade(label="Couleurs", menu=menu_couleurs)
menu_couleurs.add_command(label="Rouge")
menu_couleurs.add_command(label="Vert")
menu_couleurs.add_command(label="Bleu")

root.config(menu=menu_bar)

# =======================
# CONTENU PRINCIPAL
# =======================
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

# Scrollbar ttk
yscroll = ttk.Scrollbar(frame, orient=tk.VERTICAL)
yscroll.grid(row=0, column=0, sticky="ns")

# Treeview (remplace Listbox)
tree = ttk.Treeview(
    frame,
    columns=("value",),
    show="headings",
    yscrollcommand=yscroll.set,
    selectmode="browse"
)
tree.heading("value", text="Liste")
tree.grid(row=0, column=0, sticky="nsew")

yscroll.config(command=tree.yview)

# Remplissage
for i in range(20):
    tree.insert("", "end", values=(f"ligne numéro {i+1}",))

# Label info
info = ttk.Label(root, text="No value selected")
info.grid(row=1, column=0, pady=5)

# Sélection
def on_select(event):
    selected = tree.selection()
    if selected:
        index = tree.index(selected[0])
        info.config(text=f"item number {index+1} has been selected")

tree.bind("<<TreeviewSelect>>", on_select)

root.mainloop()
