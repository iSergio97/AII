from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

root = Tk()

# Apartado a
def apartado_a():
    conn = sqlite3.connect("test.db")
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS(
        MARCA TEXT NOT NULL,
        NOMBRE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        PRECIO FLOAT NOT NULL,
        PRECIOOFERTA FLOAT);
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
            conn.execute("INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?, ?)", (marca, name, href, price, floatPrice))
        else:
            conn.execute("INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?, ?)", (marca, name, href, price, 'None'))

    # productos = conn.execute("select * from productos where PRECIOOFERTA != 'None'")
    # productos
    messagebox.showinfo("OK", "Se ha completado la instrucción de forma correcta")


menubar = Menu(root)
#Añadimos el botón de almacenar
menubar.add_command(label="Almacenar", command=apartado_a)


root.config(menu=menubar)
root.mainloop()

#Apartado b