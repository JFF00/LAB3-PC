class Testament:
    def __init__(self, id, name, books):
        self.id = id
        self.name = name  # Old / New
        self.books = {}  # {id_libro:Objeto Libro}

    def get_books(self):
        return self.books
