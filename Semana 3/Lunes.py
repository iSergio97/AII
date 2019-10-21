from tkinter import *
from tkinter import messagebox
import sqlite3
import urllib.request

root = Tk()
conn = sqlite3.connect('test.db')


def conexion():
    try:
        conn.execute('''CREATE TABLE NOTICIAS
                 (ID INTEGER PRIMARY KEY NOT NULL,
                 TITULO           TEXT    NOT NULL,
                 LINK            TEXT     NOT NULL,
                 FECHA         TEXT);''')
        messagebox.showinfo("Aviso", "Base de datos conectada")
    except sqlite3.DatabaseError as e:
        messagebox.showinfo("Aviso", e)

def getElementByTag(text):
    return re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', text)

# Para BeautifulSoup, se debe buscar primero por la etiqueta padre y luego ir poco a poco, como he hecho aquí (buscar primero por item, luego por por title, luego por fecha y luego por link)
# En cambio, cuando haces la búsqueda completa sin BeautifulSoup, se debe hacer por al completo


def listar():
    try:
        f = urllib.request.urlopen("http://www.us.es/rss/feed/portada")
        s = f.read().decode("utf8")
        d = getElementByTag(s)
        print(d[0][0])
        print(d[0][1])
        print(d[0][3])

        for i in range(len(d)):
            conn.execute("INSERT INTO NOTICIAS VALUES  (?, ?, ?, ?)", (i, d[i][0], d[i][1], d[i][3]))
            conn.commit()

        f.close()

    except urllib.error.HTTPError as e:
        messagebox.showinfo("Aviso", "Se ha producido un error inesperado")


def entry():
    L1 = Label(root, text="Introduzca el mes (XXX)")
    L1.pack(side=LEFT)
    E1 = Entry(root, bd=5)
    E1.pack(side=RIGHT)
    def buscarPorFecha():
        fechaParametrizada = "%" + E1.get() + "%"
        fecha = conn.execute("SELECT titulo, link, fecha FROM NOTICIAS WHERE FECHA like ?", (fechaParametrizada,))
        # for row in fecha:
            # (row[0], row[1], row[2]) Esto devuelve los objetos, sólo falta añadirlos a la tabla para que se muestren por pantalla


    B = Button(root, text="Enviar", command=buscarPorFecha)
    B.pack(side=RIGHT)

    # Añadir el botón para que al hacer E1.get() se coja el valor una vez escrito algo
    root.mainloop()


menubar = Menu(root)
# Desde aquí
menubar.add_command(label="Almacenar", command=conexion)
# Hasta aquí va el botón de almacenar

# Desde aquí
menubar.add_command(label="Listar", command=listar)
# Hasta aquí va el botón de listar

# Desde aquí
menubar.add_command(label="Buscar", command=entry)
# Hasta aquí va el botón de buscar

root.config(menu=menubar)
root.mainloop()

conn.close()