from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

root = Tk()

conn = sqlite3.connect("test.db")


# Apartado a
def apartado_a():
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS(
        MARCA TEXT NOT NULL,
        NOMBRE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        PRECIOANTIGUO FLOAT NOT NULL,
        PRECIOFINAL FLOAT);
    ''')

    def getElement(text, tag):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag, id=True)

    read = urllib.request.urlopen("https://www.ulabox.com/campaign/productos-sin-gluten#gref")

    article = getElement(read, "article")

    for i in article:
        a = i.find("a")
        href = a['href']
        marca = i['data-product-brand']
        name = i['data-product-name']
        price = i['data-price']
        offeredPrice = i.find('del')
        if offeredPrice != None:
            offeredPrice = offeredPrice.string
            priceSplited = offeredPrice.split()
            priceSplited[0]
            floatPrice = float(priceSplited[0].replace(",", "."))
            conn.execute("INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?, ?)", (marca, name, href, floatPrice, float(price)))
        else:
            conn.execute("INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?, ?)", (marca, name, href, 'None', float(price)))

    # productos = conn.execute("select * from productos where preciofinal")

    messagebox.showinfo("OK", "Se ha completado la instrucción de forma correcta")




def apartado_b():
    marcas = conn.execute("SELECT DISTINCT MARCA from PRODUCTOS ")
    marcasString= list()
    for i in marcas:
        marcasString.append(i[0])

    def queryDB():
        query = conn.execute("SELECT NOMBRE,PRECIOFINAL FROM PRODUCTOS WHERE MARCA= (?)", (w.get(),))
        ventana = Toplevel()
        listbox = Listbox(ventana, width=100)
        listbox
        for i in query:
            # Así se añaden varios objetos a una sola línea
            producto = i[0] + ", " + str(i[1])
            listbox.insert("end", producto)
            listbox.insert("end", "")
        listbox.pack(expand=YES)

    button = Button(root, text="Buscar productos de esa marca", command=queryDB)
    button.pack(side=RIGHT)
    w = Spinbox(values=marcasString, state="readonly")
    w.pack()



menubar = Menu(root)
#Añadimos el botón de almacenar
menubar.add_command(label="Almacenar", command=apartado_a)

menubar.add_command(label="Marcas", command=apartado_b)
root.config(menu=menubar)
root.mainloop()

#Apartado b