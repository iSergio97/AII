import os
import urllib.request
from tkinter import *
from tkinter import messagebox

import dateparser
from bs4 import BeautifulSoup
from whoosh import qparser
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser


def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase)


def getElementNoClass(text, tag):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag)


def get_schema():
    # Dentro del schema van los campos que quieras almacenar seguidos de un igual, el tipo que es y (stored=True)
    # Ejemplo title=TEXT(stored=True) y así con todos los que tenga
    return Schema(title=TEXT(stored=True), fechaHora=DATETIME(stored=True), link=TEXT(stored=True),
                  resume=TEXT(stored=True))


def scrapping(dirname):
    # Si no existe el nombre de directorio, lo crea
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    ix = create_in(dirname, schema=get_schema())

    writer = ix.writer()

    # Recuerda que el bucle empieza por 0, por lo que debemos sumarle 1 al valor en el bucle
    numPages = 2
    url = "https://www.sevilla.org/actualidad/noticias?b_start:int="

    for i in range(numPages):
        actual = i * 9
        # Tratado esto en el bucle for
        read = urllib.request.urlopen(url + str(actual))
        listado = getElement(read, 'div', ['eq-height row'])
        for j in listado:
            article = getElement(str(j), 'article', ['newsItem pos-relative height-100'])
            for l in article:
                a = l.find('a')
                link = a['href']
                div = getElement(str(a), 'div', 'newsItem__content')
                for m in div:
                    p = m.find_all('p')
                    fechaHoraText = p[0].text
                    fechaHoraDate = dateparser.parse(fechaHoraText)
                    resumen = p[1].text.strip()
                    titulo = m.find('h2').text.strip()
                    writer.add_document(title=titulo, fechaHora=fechaHoraDate, link=link, resume=resumen)

    writer.commit()
    # Dato:
    # Las clases que tengan espacios hay que diferenciar los elementos entre los espacios con comas como tenemos aquí abajo
    # Ejemplo ['clase1', 'clase2', 'clase3'...'claseN']

    # Tras cada iteración donde obtenemos el objeto, lo escribimos

    # Aquí irían los campos del documento siguiendo el siguiente formato
    # writer.add_document(campo1 = campo1, ... , campoN = campoN)
    # Y esto iría dentro del bucle for final, como en Lunes/Semana 8
    # writer.add_document(...)

    # En cambio, esto iría fuera del bucle for principal y aquí es donde le decimos al directorio que lo guarde
    # writer.commit()
    messagebox.showinfo("Fin de carga",
                        "Se ha realizado la carga de " + str(numPages) + " páginas. \nSiendo esto un total de " + str(
                            numPages * 9))


def doNothing():
    messagebox.showinfo("Nothing", "No ha sido implementado")


def buscarPorTituloFecha(dirIndex):
    def mostrar_noticias(event):
        myQuery = "[" + str(entry.get())[0::5] + "]"
        lb.delete(0, END)
        ix = open_dir(dirIndex)
        with ix.searcher() as searcher:
            query = MultifieldParser(["title", "fechaHora"], ix.schema, group=qparser.OrGroup).parse(str(entry.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['title'])
                lb.insert(END, r['fechaHora'])
                lb.insert(END, '')

    tLevel = Toplevel();
    tLevel.title("Buscar por título y fecha")
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


def buscarPorFecha(dirIndex):
    def mostrar_noticias(event):
        lb.delete(0, END)
        ix = open_dir(dirIndex)
        with ix.searcher() as searcher:
            parsear = ''
            if str(entry.get()).__contains__('Tarde'):
                entrada = str(entry.get())[0:10]
                print(entrada)
                parsear = "{" + entrada + " 4:59 TO " + entrada + " 14:59]"
                print(parsear)
            elif str(entry.get()).__contains__('Dia'):
                entrada = str(entry.get())[0:10]
                parsear = "{" + entrada + " 14:59 TO " + entrada + " 5:00]"
                print(parsear)
            query = QueryParser("fechaHora", ix.schema).parse(parsear)
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['title'])
                lb.insert(END, r['fechaHora'])
                lb.insert(END, '')

    tLevel = Toplevel();
    tLevel.title("Buscar por título y fecha")
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


def buscarPorContenidoTitulo(dirIndex):
    def mostrar_noticias(event):
        # doNothing()
        lb.delete(0, END)
        ix = open_dir(dirIndex)
        with ix.searcher() as searcher:
            parser = ''
            if str(entry.get()).__contains__(" Y "):
                parser = qparser.AndGroup
            elif str(entry.get()).__contains__(" NO "):
                parser = qparser.NotGroup
            else:
                parser = qparser.OrGroup
            query = MultifieldParser(["title", "resume"], ix.schema, group=parser).parse(str(entry.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['title'])
                lb.insert(END, r['fechaHora'])
                lb.insert(END, '')

    tLevel = Toplevel();
    tLevel.title("Buscar por etiqueta")
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
    dirIndex = 'Index'
    # First menu
    firstMenu = Menu(menubar, tearoff=0)
    # firstMenu.add_command(label="Indexar", command=lambda: doNothing(string)
    firstMenu.add_command(label="Cargar", command=lambda: scrapping(dirIndex))
    firstMenu.add_separator()
    firstMenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Indexar", menu=firstMenu)

    # Whoosh menu
    finderMenu = Menu(menubar, tearoff=0)
    finderMenu.add_command(label="Buscar por contenido y titulo", command=lambda: buscarPorContenidoTitulo(dirIndex))
    finderMenu.add_command(label="Buscar por fecha", command=lambda: buscarPorFecha(dirIndex))
    finderMenu.add_command(label="Buscar por titulo y fecha", command=lambda: buscarPorTituloFecha(dirIndex))
    menubar.add_cascade(label="Buscar", menu=finderMenu)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    ventana()
