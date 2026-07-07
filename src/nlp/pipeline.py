from src.book import Book
from src.chapter import Chapter
from src.testament import Testament
from src.verse import Verse
from .cleaner import clean_count_verse


def process_bible(testament):
    global_frequencies = {}
    for book in testament.books.values():
        for chapter in book.chapters.values():
            for verse in chapter.verses.values():
                clean_count_verse(verse)
                for word in verse.get_frequencies():
                    if word not in global_frequencies:
                        global_frequencies[word] = verse.frequencies[word]
                    else:
                        global_frequencies[word] += verse.frequencies[word]
    return global_frequencies
