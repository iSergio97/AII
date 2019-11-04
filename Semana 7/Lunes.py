from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import *

# from . import Tema Falla Revisar porqué



root = Tk()
conn = sqlite3.connect("derecho.db")

def apartado_a():
    conn.execute("""DROP TABLE IF EXISTS TEMAS""")
    conn.execute("""DROP TABLE IF EXISTS RESPUESTA""")
    conn.execute(
        """
            CREATE TABLE TEMAS
            (
                TITULO TEXT NOT NULL,
                LINK TEXT NOT NULL PRIMARY KEY,
                AUTOR TEXT NOT NULL,
                FECHA DATETIME NOT NULL,
                NUMRESPUESTAS NUMBER NOT NULL,
                NUMVISITAS NUMBER NOT NULL
            )
        """
    )

    conn.execute(
        """
            CREATE TABLE RESPUESTA
            (
                AUTOR TEXT NOT NULL,
                FECHA DATETIME NOT NULL,
                TEXTO TEXT NOT NULL,
                LINK TEXT NOT NULL,
                FOREIGN KEY (LINK) REFERENCES TEMAS(LINK)
            )
        """
    )

    def getElement(text, tag, clase):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag, class_=clase)

    def getElementNoClass(text, tag):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag)

    read = urllib.request.urlopen("https://foros.derecho.com/foro/34-Derecho-Inmobiliario")

    li = getElement(read, "li", ["threadbit"])

    for i in li:
        div = getElement(str(i), "div", ["inner"])
        ul = getElement(str(i), "ul", "threadstats td alt")
        for j in ul:
            numRespuestas = int(j.find("a").string.replace(",", "."))
        for j in ul:
            numVisitas = j.find_all("li")[1].string[8:]
            numVisitas = int(numVisitas.replace(",", ""))
        for j in div:
            a = j.find("a")
            titulo = a["title"]
            link = a["href"]
            div2 = j.find("div")
            for k in div2:
                span = k.find("span")
                if span != -1:
                    autor = span.find('a').string
                    fechaStr = list(span.strings)[2][2:]
                    fecha = datetime.strptime(fechaStr, "%d/%m/%Y %H:%S")

                    conn.execute("INSERT INTO TEMAS VALUES (?, ?, ?, ?, ?, ?)", (titulo, link, autor, fecha, numRespuestas, numVisitas))


    numTemas = conn.execute("SELECT COUNT(*) FROM TEMAS")

    mensaje = "Se ha completado la instrucción de forma correcta, guardando " + str(numTemas.fetchone()[0]) + " temas"
    messagebox.showinfo("OK", mensaje)










menubar = Menu(root)

# Añadimos botón de inicio
indexMenu = Menu(menubar, tearoff=0)
indexMenu.add_command(label="Indexar", command=apartado_a)
indexMenu.add_separator()
indexMenu.add_command(label="Salir", command = root.quit)
menubar.add_cascade(label="Inicio", menu=indexMenu)

root.config(menu=menubar)
root.mainloop()