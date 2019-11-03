from tkinter import *
from tkinter import  messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

root = Tk()

conn = sqlite3.connect("vinos.db")

def apartado_a():
    conn.execute("DROP TABLE IF EXISTS VINO")
    conn.execute('''
    CREATE TABLE VINO(
    NOMBRE TEXT NOT NULL,
    PRECIO NUMBER NOT NULL,
    DENORIGEN TEXT NOT NULL,
    TIPOS TEXT NOT NULL,
    SCORE NUMBER
    );
    ''')

    listTitle = list()
    listPrecios = list()
    listOrigenes = list()
    listaUvas = list()
    def getElement(text, tag, clase):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag, class_=clase)

    def getElementNoClass(text, tag):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag)

    for i in range(0, 51, 50):
        url = "https://www.vinissimus.com/es/vinos/tinto/index.html?start=" + str(i)
        read = urllib.request.urlopen(url)
        tr = getElementNoClass(read, "tr")
        for j in tr:
            td = j.find_all("td")
            prices = j.find_all("span")
            for k in prices[3]:
                price = k.string
                priceFinal = re.findall(r'[0-9]{0,2}\,[0-9]{0,2}', price)[0]
                priceFinal = priceFinal + " €"
                listPrecios.append(priceFinal)
            for k in prices:
                denOrigenes = getElement(str(k), "span", "type")
                for l in denOrigenes:
                    listOrigenes.append(l.string.strip())
            for k in prices:
                uvas = getElement(str(k), "span", "grape")
                for l in uvas:
                    listaUvas.append(l.string.strip())
            for k in td[1]:
                h3 = getElementNoClass(str(k), "h3")
                for l in h3:
                    a = l.find("a")
                    listTitle.append(a.string)
