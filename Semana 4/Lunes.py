# Primera práctica de la asignatura AII

from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

root = Tk()
conn = sqlite3.connect('test.db')
conn.execute("DROP TABLE IF EXISTS FORO")
conn.execute('''CREATE TABLE FORO(
    TITULO TEXT PRIMARY KEY NOT NULL,
    LINK TEXT NOT NULL,
    AUTOR TEXT NOT NULL,
    NUMRESPUESTAS TEXT NOT NULL,
    NUMVISITAS TEXT NOT NULL,
    FECHAHORA TEXT NOT NULL);''')

def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase, id=True)


read = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General")
li = getElement(read, "li", "threadbit")
print(len(li))
for i in li:
    a = i.find("a", class_="title")
    # De ambas formas se puede obtener el elemento. Con la primera obtengo el valor de la etiqueta (lo que está entre las llaves <a...> </a>)
    # Y con la segunda se obtiene el elemento de la etiqueta
    title = a.string
    href = a["href"]
    div = i.find("div", class_="author")
    etiquetaA = div.find('a')
    author = etiquetaA.string
    titleEtiqueta = etiquetaA["title"]
    fechayhora = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4} [0-9]{2}:[0-9]{2}', titleEtiqueta)[0]
    print(fechayhora)
    numRespuestas = 0 # TODO
    numVisitas = 0 # TODO
    # conn.execute("INSERT INTO FORO VALUES (?, ?, ?, ?, ?, ?)", (title, href, author, numRespuestas, numVisitas, fechayhora))








'''
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

'''
'''
def BuscarPorPalabra():
    def buscaPalabra(event):
        conn = sqlite3.connect("test.db")
        conn.text_factory = str
        s = "%" + en.get() + "%"
        cursor = conn.execute("SELECT TITULO, AUTOR, FECHAHORA FROM FORO WHERE TITULO LIKE ?""", (s,))
        imprimir_etiqueta(cursor)
        conn.close()
   
    v = TopLevel()
    lb1 = Label(v, text = "Introduzca una palabra: ")
    lb1.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", buscaPorPalabra)
    en.pack(side = LEFT)

def BuscarPorFecha():
    def buscaFecha(event):
        conn = sqlite3.connect("test.db")
        conn.text_factory = str
        s = "%" + en.get() + "%"
        cursor = conn.execute("SELECT TITULO, AUTOR, FECHAHORA FROM FORO WHERE FECHAHORA LIKE ?""", (s,))
        imprimir_etiqueta(cursor)
        conn.close()
   
    v = TopLevel()
    lb1 = Label(v, text = "Introduzca una fecha: ")
    lb1.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", buscaPorFecha)
    en.pack(side = LEFT)


def ventana_principal():
    root = Tk()
    menubar = Menu(root)
    searchmenu = Menu(menubar, tearoff = 0)
    searchmenu.add_command(label="Buscar Por Palabra", command = BuscarPorPalabra)
    searchmenu.add_command(label="Buscar por Fecha", command = BuscarPorFecha)
    

if __name__ == "__main__":
    ventana_principal()




    

    '''        