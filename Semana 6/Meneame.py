from tkinter import *
from tkinter import  messagebox
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

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
    FECHAHORA TEXT NOT NULL,
    CONTENIDO TEXT NOT NULL
    );
    ''')

    def getElement(text, tag, clase):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all(tag, class_=[clase])

    for i in range(1, 4, 1):
        url = "https://www.meneame.net/?page=" + str(i)
        read = urllib.request.urlopen(url)
        center = getElement(read, "div", "center-content")
        for j in range(center):
            a = j.find("a")
            link = a['href']
            print(link)

print(apartado_a())