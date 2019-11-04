class Tema:
    def __init__(self, titulo, link, autor, fecha, numRespuestas, numVisitas):
        self.titulo = titulo
        self.link = link
        self.autor = autor
        self.fecha = fecha
        self.numRespuestas = numRespuestas
        self.numVisitas = numVisitas


        def titulo(self):
            return self.titulo

        def link(self):
            return self.link

        def fecha(self):
            return self.fecha

        def autor(self):
            return self.autor

        def numVisitas(self):
            return self.numVisitas

        def numRespuestas(self):
            return self.numRespuestas

        def __str__(self):
            tema = str(titulo) + "," + str(link)  + "," + fecha  + "," + str(autor)  + "," + numVisitas  + "," + numRespuestas
            return tema