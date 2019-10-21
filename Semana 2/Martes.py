# Páginas visitadas:
# https://tutorialspoint.com/sqlite/sqlite_python.htm SQLITE
# https://www.tutorialspoint.com/python3/python_gui_programming.htm TKINTER
# from tkinter import *
from tkinter import *


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


root = Tk()
menubar = Menu(root)
# Desde aquí
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
# Hasta aquí corresponde con el botón de file
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
# Desde aqui
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
# Hasta aquí corresponde con el botón de edit

helpmenu = Menu(menubar, tearoff=0)
# Desde aquí
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
# Hasta aquí corresponde con el botón de help

root.config(menu=menubar)
root.mainloop()
