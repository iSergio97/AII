import dateparser
fecha = dateparser.parse("lunes, 1 de noviembre de 2019")
print(str(fecha)[:10])

for i in range (3):
    print("http://www.sensacine.com/noticias/?page=" + str(i))