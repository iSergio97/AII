#Así se crean errores propios

class MiError(Exception):
    def __init__(self, valor):
        self.valor = valor


# raise MiError("El número es mayor")

for i in range(3):
    #End aquí implica la separación entre objetos que vamos a imprimir
    print(i, end=" ")

print()
print("%s %s" % ("Hola", "Mundo"))

# Para abrir archivos, usamos open junto con la ruta y las aperturas
# r = lectura
# w = write (eliminando lo que había antes)
# a = append (añadir)
# b = binario
# + = lectura y escritura
# U = universal newline)
# f = open("...")
# completo = f.read()

# Expresiones regulares
# import re

# <e> hola <b> hola1 </b> <b> hola3 </b> esto </e>
# Para sacar la parte en negritas (entre b):
# re.findAll("<b>(.+)</b>") donde (.+) te toma los valores del medio y sin los paréntesis .+ te tomaría las etiquetas también

import shelve
animales = ["piton", "mono", "camello"]
lenguajes = ["python", "mono", "perl"]
shelf = shelve.open("datos")
shelf["primera"] = animales
shelf["segunda"] = lenguajes
print(shelf)
shelf.close()