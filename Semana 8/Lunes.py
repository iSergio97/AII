from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import *
import dateparser


root = Tk()
conn = sqlite3.connect("cine.db")


def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase)


def getElementNoClass(text, tag):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag)

def apartado_a():
    conn.execute("""DROP TABLE IF EXISTS NOTICIAS""")
    conn.execute(
        """
            CREATE TABLE NOTICIAS
            (
                TITULO TEXT NOT NULL,
                LINK TEXT NOT NULL,
                CATEGORIA TEXT NOT NULL,
                FECHA DATETIME NOT NULL,
                DESCRIPCION TEXT 
            )
        """
    )

    for i in range (3):
        read = urllib.request.urlopen("http://www.sensacine.com/noticias/?page="+ str(i))

       #Las clases que tengan espacios hay que diferenciar los elementos entre los espacios con comas como tenemos aquí abajo
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
                    if not(link.endswith('.jpg')):
                        link = img["data-src"]
                for k in divMeta:
                    categoria = getElement(str(k), "div", "meta-category")[0].string[10:]
                    fechita = getElement(str(k), "div", "meta-date")[0].string
                    descripcion = getElement(str(k), "div", "meta-body")
                    fecha = str(dateparser.parse(fechita))[:10]
                    format = datetime.strptime(fecha, '%Y-%m-%d')
                    print(type(format))
                    if(len(descripcion) == 0):
                        descripcion = "NONE"

    #TODO completar apartado A con Whoosh









apartado_a()
