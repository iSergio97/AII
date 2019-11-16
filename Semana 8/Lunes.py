# encoding:utf-8
import os
import urllib.request
from datetime import *
from tkinter import *
from tkinter import messagebox
import dateparser
# sys.path.append("Noticias")
from Noticias import *
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
    return Schema(title=TEXT(stored=True), href=ID(stored=True),
                  category=TEXT(stored=True), date=DATETIME(stored=True),
                  description=TEXT(stored=True))


def indexar(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    ix = create_in(dirname, schema=get_schema())

    writer = ix.writer()

    for i in range(3):
        read = urllib.request.urlopen("http://www.sensacine.com/noticias/?page=" + str(i))

        # Las clases que tengan espacios hay que diferenciar los elementos entre los espacios con comas como tenemos aquí abajo
        div2 = getElement(read, "div", ["col-left"])
        for a in div2:
            div = getElement(str(a), "div", ["card", "news-card"])
            for j in div:
                figure = getElement(str(j), "figure", "thumbnail")
                divMeta = getElement(str(j), "div", "meta")
                for k in figure:
                    img = k.find("img")
                    titulo = img["alt"]
                    link = img["src"]
                    if not (link.endswith('.jpg')):
                        link = img["data-src"]
                for k in divMeta:
                    categoria = getElement(str(k), "div", "meta-category")[0].string[10:]
                    fechita = getElement(str(k), "div", "meta-date")[0].string
                    descripcion = getElement(str(k), "div", "meta-body")
                    if (len(descripcion) == 0):
                        descripcion = ""
                    else:
                        descripcion = descripcion[0].string

                    fecha = str(dateparser.parse(fechita))[:10]
                    format = datetime.strptime(fecha, '%Y-%m-%d')
                    writer.add_document(title=titulo, href=link, category=categoria, date=format, description=descripcion)
    writer.commit()
    messagebox.showinfo("Fin de carga", "Se han cargado " + str(i+1) + " páginas")


def ventana_principal():
    dirIndex = "index"
    root = Tk()
    menubar = Menu(root)
    # TKinter, parte del desplegable de indexar
    cargarMenu = Menu(menubar, tearoff=0)
    cargarMenu.add_command(label="Cargar noticias", command=lambda: indexar(dirIndex))
    cargarMenu.add_separator()
    cargarMenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Indexar", menu=cargarMenu)

    #TKinter, parte del menu de finder
    finderMenu = Menu(menubar, tearoff=0)
    finderMenu.add_command(label="Buscar por título y descripción", command=lambda: finderTitleAndDescrip(dirIndex))
    finderMenu.add_command(label="Buscar por descripción", command=doNothing)
    finderMenu.add_command(label="Buscar por fecha", command=doNothing)
    menubar.add_cascade(label="Buscar noticias", menu=finderMenu)

    root.config(menu=menubar)
    root.mainloop()


def doNothing():
    messagebox.showinfo("Nothing", "Do nothing!")


def finderTitleAndDescrip(dirIndex):
    def mostrar_noticias(event):
        messagebox.showinfo("Nothing", "Do nothing!")


    tLevel = Toplevel()
    tLevel.title("Buscar por título y descripción")
    frame = Frame(tLevel)
    frame.pack(side=TOP)
    label = Label(frame, text="Introduzca una palabra para buscar: ")
    label.pack(side=LEFT)
    entry = Entry(frame)
    entry.bind("<Return>", mostrar_noticias)
    entry.pack(side=LEFT)
    sb = Scrollbar(tLevel)
    sb.pack(side=RIGHT, fill=Y)
    lb = Listbox(tLevel, yscrollcommand=sb.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sb.config(command=lb.yview)

if __name__ == '__main__':
    ventana_principal()
