import os
import urllib.request
from datetime import *
from tkinter import *
from tkinter import messagebox
import dateparser
from bs4 import BeautifulSoup
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.index import create_in

def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase)


def getElementNoClass(text, tag):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag)

def get_schema():
    # Dentro del schema van los campos que quieras almacenar seguidos de un igual, el tipo que es y (stored=True)
    # Ejemplo title=TEXT(stored=True) y así con todos los que tenga
    return Schema(...)

def scrapping(dirname):
    # Si no existe el nombre de directorio, lo crea
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    ix = create_in(dirname, schema=get_schema())

    writer = ix.writer()

    # Recuerda que el bucle empieza por 0, por lo que debemos sumarle 1 al valor en el bucle
    numPages = 0
    url = ""

    for i in range(numPages):
        # Tratado esto en el bucle for
        read = urllib.request.urlopen(url + str(i+1))
        # Dato:
        # Las clases que tengan espacios hay que diferenciar los elementos entre los espacios con comas como tenemos aquí abajo
        # Ejemplo ['clase1', 'clase2', 'clase3'...'claseN']

        # Tras cada iteración donde obtenemos el objeto, lo escribimos

        #Aquí irían los campos del documento siguiendo el siguiente formato
        # writer.add_document(campo1 = campo1, ... , campoN = campoN)
        # Y esto iría dentro del bucle for final, como en Lunes/Semana 8
        writer.add_document(...)

        # En cambio, esto iría fuera del bucle for principal y aquí es donde le decimos al directorio que lo guarde
        writer.commit()
        messagebox.showinfo("Fin de carga", "Se ha realizado la carga de " + str(numPages))

def doNothing():
    messagebox.showinfo("Nothing", "No ha sido implementado")

def buscarPorX(dirIndex):
    def mostrar_noticias(event):
        messagebox.showinfo("Nothing", "Do nothing!")

    tLevel = Toplevel();
    tLevel.title("Buscar por X")
    frame = Frame(tLevel)
    frame.pack(side=TOP)
    label = Label(frame, text="Introduzca una palabra (o palabras) para buscar: ")
    label.pack(side=LEFT)
    entry = Entry(frame)
    entry.bind("<Return>", mostrar_noticias)
    entry.pack(side=LEFT)
    sb = Scrollbar(tLevel)
    sb.pack(side=RIGHT, fill=Y)
    lb = Listbox(tLevel, yscrollcommand=sb.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sb.config(command=lb.yview)

def ventana():
    root = Tk()
    menubar = Menu(root)
    # Este index es virtual, lo crea Whoosh para almacenar y poder indexar los datos
    dirIndex = 'dirIndex'
    # First menu
    firstMenu = Menu(menubar, tearoff=0)
    # firstMenu.add_command(label="Indexar", command=lambda: doNothing(string)
    firstMenu.add_command(label="Cargar X", command=doNothing)
    firstMenu.add_separator()
    firstMenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Indexar", menu=firstMenu)

    # Whoosh menu
    finderMenu = Menu(menubar, tearoff=0)
    finderMenu.add_command(label="Buscar por X", command=lambda: buscarPorX(dirIndex))
    finderMenu.add_command(label="Buscar por Y", command=doNothing)
    finderMenu.add_command(label="Buscar por Z", command=doNothing)
    menubar.add_cascade(label="Buscar", menu=finderMenu)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    ventana()
