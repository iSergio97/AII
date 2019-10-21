from tkinter import *
from tkinter import messagebox
import sqlite3
import urllib.request as req
from bs4 import BeautifulSoup

conn = sqlite3.connect("test.db")
conn.execute("DROP TABLE IF EXISTS PARTIDO")
conn.execute('''CREATE TABLE PARTIDO(
    LOCAL TEXT NOT NULL,
    VISITANTE TEXT NOT NULL,
    GOLES_L TEXT NOT NULL,
    GOLES_V TEXT NOT NULL,
    JORNADA TEXT NOT NULL)
    ''')

text = req.urlopen("https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/")
soup = BeautifulSoup(text, "html.parser")
# Nunca, nunca, nunca hagas un print a una página web seria porque tienen mil scripts metidos como texto y es una mierda

jornada = soup.find_all("table", class_="tabla-datos")

# Así saco el equipo local y visitante del primer partido de la primera jornada
local = jornada[0].find("span", class_="nombre-equipo").string
tdVisitante = jornada[0].find("td", class_="col-equipo-visitante")
visitante = tdVisitante.find("span", class_="nombre-equipo").string
