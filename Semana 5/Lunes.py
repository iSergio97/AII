from tkinter import  *
from tkinter import messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

root = Tk()

conn = sqlite3.connect("test.db")
conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
conn.execute('''CREATE TABLE PRODUCTOS(
MARCA TEXT NOT NULL,
NOMBRE TEXT NOT NULL,
LINK TEXT NOT NULL,
PRECIO TEXT NOT NULL,
PRECIOOFERTA TEXT
''')

def getElement(text, tag, clase):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(tag, class_=clase, id=True)

read = urllib.request.urlopen("añadirURL")