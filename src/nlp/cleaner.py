from src.verse import Verse
from .stopwords import STOPWORDS


def clean_count_verse(verse):
    """
    Se formatean los versos individualmente, luego se actualiza el  dict de frecuencias por palabara para cada verso.
    """
    texto_limpio = verse.content.lower()
    for caracter in [",", ":", ".", "?", "!", "¡", ";"]:
        texto_limpio = texto_limpio.replace(caracter, "")

    palabras_sucias = texto_limpio.split(" ")

    STOPWORDS_SET = set(STOPWORDS)

    clean = [
        word for word in palabras_sucias
        if word not in STOPWORDS_SET and word != ""
    ]

    verse.set_tokens(clean)
    # contar frecuencia de palabras
    for word in clean:
        if word not in verse.frequencies:
            verse.frequencies[word] = 1
        else:
            verse.frequencies[word] += 1


def clean_word(text):
    texto_limpio = text.lower()
    for caracter in [",", ":", ".", "?", "!", "¡", ";"]:
        texto_limpio = texto_limpio.replace(caracter, "")

    palabras_sucias = texto_limpio.split(" ")

    STOPWORDS_SET = set(STOPWORDS)

    clean = [
        word for word in palabras_sucias
        if word not in STOPWORDS_SET and word != ""
    ]
    return clean
