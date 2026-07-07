from .book import Book
from .verse import Verse
from .chapter import Chapter
from .testament import Testament
import csv


def load_books(books, nt, ot):
    """
    Lee las keys de libro, su nombre, OT o NT, Genero
    """

    with open("archive/key_english.csv", "r", encoding='utf-8') as archivo:
        linea = archivo.readline().strip()
        for linea in archivo:
            l = linea.strip().split(",")
            if l[2] == "NT":
                book = Book("1", l[1], l[3])
                books[l[0]] = book
                nt.books[l[0]] = book
            elif l[2] == "OT":
                book = Book("0", l[1], l[3])
                books[l[0]] = book
                ot.books[l[0]] = book


def load_verses(books):
    """"""
    with open("archive/t_bbe.csv", "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for fila in lector:
            id_book = fila[1]
            id_chapter = fila[2]
            id_verse = fila[3]
            text = fila[4]

            # se busca el libro, luego se buscan sus capitulos, si no está se crea
            # si está se añade el verso.
            book = books.get(id_book)

            if not book:
                continue

            if id_chapter not in book.chapters:
                book.chapters[id_chapter] = Chapter(id_chapter, {})

            actual_chapter = book.chapters[id_chapter]

            verse = Verse(id_verse, text)
            actual_chapter.verses[id_verse] = verse


def final_load(books, NT, OT):
    """
    se usan las funciones de carga para crear las instancias finales.
    se crean las instancias de Testamento Nuevo y Antiguo.
    """
    load_books(books, NT, OT)
    load_verses(books)


def get_verse(testament, book, chapter, verse):
    return testament.books[book].chapters[chapter].verses[verse]


"""
print("id verso", OT.books["39"].chapters["1"].verses["1"].id, "\n",
      "verso: ", OT.books["39"].chapters["1"].verses["1"].content, "\n",
      "id_capitulo", OT.books["39"].chapters["1"].id, "\n",
      " name: ", OT.books["39"].name, "\n"
      )

"""
