import urllib.request
from datetime import *
from tkinter import *
from tkinter import messagebox

import dateparser
# sys.path.append("Noticias")
from Noticias import *
from bs4 import BeautifulSoup
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in
import os
import sys

root = Tk()
noticias = list()


def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase)


def getElementNoClass(text, tag):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag)


def get_schema():
    return Schema(titulo=TEXT, link=TEXT,
                  categoria=TEXT, fecha=DATETIME,
                  descripcion=TEXT)


def apartado_a(dirname):

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    ix = create_in(dirname, schema=get_schema())

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
                    fecha = str(dateparser.parse(fechita))[:10]
                    format = datetime.strptime(fecha, '%Y-%m-%d')
                    if (len(descripcion) == 0):
                        descripcion = ""
                    noticia = Noticias(titulo, link, categoria, format, descripcion)
                    noticias.append(noticia)
    messagebox.showinfo("Fin de carga", "Se han cargado " + str(len(noticias)) + " noticias")
    # TODO completar apartado A con Whoosh


def ventana_principal():
    dirIndex = "index"
    cargar = Button(root, text="Cargar noticias", command=lambda: apartado_a("index"))
    cargar.pack(side=TOP)
    finderTitleDesc = Button(root, text="Buscar por título y descripción")
    finderTitleDesc.pack(side=TOP)
    finderDescrip = Button(root, text="Buscar por y descripción")
    finderDescrip.pack(side=TOP)
    finderDate = Button(root, text="Buscar fecha")
    finderDate.pack(side=TOP)
    root.mainloop()

if __name__ == '__main__':
    ventana_principal()