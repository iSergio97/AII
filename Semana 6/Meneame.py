from tkinter import *
from tkinter import  messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

root = Tk()

conn = sqlite3.connect("meneame.db")


# Apartado a


def apartado_a():
    conn.execute("DROP TABLE IF EXISTS MENEAME")
    conn.execute('''
    CREATE TABLE MENEAME(
    TITULO TEXT NOT NULL,
    ENLACE TEXT NOT NULL,
    NOMBREAUTOR TEXT NOT NULL,
    FECHAHORA DATETIME NOT NULL,
    CONTENIDO TEXT
    );
    ''')

    def getElement(text, tag, clase):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag, class_=clase)

    listContenido = list()
    listAuthor = list()
    listfh = list()
    listTitle = list()
    listHref = list()

    for i in range(3):
        url = "https://www.meneame.net/?page=" + str(i+1)
        read = urllib.request.urlopen(url)
        center = getElement(read, "div", "center-content")
        for j in center:
            a = j.find("h2").find("a")
            href = a["href"]
            title = a.string
            listTitle.append(title)
            listHref.append(href)
            tagAutor = getElement(str(j), "div", ['news-submitted'])
            contenido = getElement(str(j), "div", ["news-content"])
            for h in contenido:
                listContenido.append(h.string)
            for k in tagAutor:
                authorA = k.find("a")
                autor = authorA['href'].replace("/user/", "")
                listAuthor.append(autor)
                span = getElement(str(k), "span", ["ts visible"])
                data_ts = span[0]['data-ts']
                fechahora = datetime.fromtimestamp(int(data_ts))
                listfh.append(fechahora)

    for i in range(len(listAuthor)):
        titulo = listTitle[i]
        link = listHref[i]
        autor = listAuthor[i]
        fechayhora = listfh[i]
        contenidoArt = listContenido[i]
        conn.execute("INSERT INTO MENEAME VALUES (?,?,?,?,?)",
                     (titulo, link, autor, fechayhora, contenidoArt))

    messagebox.showinfo("OK", "Se han almacenado " + str(len(listfh)) + " noticias")


def apartado_1b():
    messagebox.showinfo("Aviso", "Se han añadido barras de desplazamiento tanto horizontales como verticales, pero se puede navegar empleando los botones 'INICIO' y 'FIN' del teclado y los botones de desplazamiento \n Sólo tiene que hacer click sobre una noticia y desplazarse empleando esos botones. Para navegar con las barras no es necesario realizar nada.")
    noticias = conn.execute("SELECT TITULO, NOMBREAUTOR, FECHAHORA FROM MENEAME ")
    ventana = Toplevel()

    xScrollBar = Scrollbar(ventana)
    xScrollBar.pack(side=RIGHT, fill=Y)

    yScrollBar = Scrollbar(ventana)
    yScrollBar.pack(side=BOTTOM, fill=X)

    listbox = Listbox(ventana, width=100)

    for i in noticias:
        # Así se añaden varios objetos a una sola línea
        noti = i[0] + ", " + i[1] + ", " + str(i[2])
        listbox.insert("end", noti)
        listbox.insert("end", "")

    listbox.pack(side=LEFT, fill=BOTH)
    xScrollBar.config(command = listbox.yview)
    yScrollBar.config(command=listbox.xview)



menubar = Menu(root)

#Añadimos el botón de almacenar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Almacenar", command=apartado_a)
filemenu.add_separator()
filemenu.add_command(label="Mostrar", command=apartado_1b)




menubar.add_cascade(label="Datos", menu=filemenu)
root.config(menu=menubar)
root.mainloop()


