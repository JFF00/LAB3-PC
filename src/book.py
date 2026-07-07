class Book:
    def __init__(self, testament: str, name: str, genre: str):
        self.testament = testament
        self.name = name
        self.chapters = {}  # {numero_capitulo: Objeto Capitulo}
        self.genre = genre
