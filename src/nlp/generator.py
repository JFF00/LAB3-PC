import random
from collections import defaultdict, Counter


def build_ngram_model(books, n):
    model = defaultdict(Counter)

    for book_id, book in books.items():
        for chapter_id, chapter in book.chapters.items():
            for verse_id, verse in chapter.verses.items():
                if n == 1:
                    tokens = verse.tokens + ["<END>"]
                    for word in tokens:
                        model[tuple()][word] += 1
                else:
                    tokens = ["<START>"] * (n - 1) + verse.tokens + ["<END>"]
                    for i in range(len(tokens) - n + 1):
                        history = tuple(tokens[i:i + n - 1])
                        target = tokens[i + n - 1]
                        model[history][target] += 1
    return model


def generate_text(model, n, start_word=None, max_length=20):
    if n == 1:
        current_history = tuple()
        words = []
        if start_word:
            words.append(start_word)
    else:
        if start_word:
            # Buscamos todos los historiales válidos que terminen con nuestra palabra inicial
            posibles_inicios = [hist for hist in model.keys() if len(
                hist) > 0 and hist[-1] == start_word]

            if posibles_inicios:
                # Elegimos uno al azar para darle variedad
                current_history = random.choice(posibles_inicios)
                # Extraemos las palabras reales de ese historial para nuestra frase final
                words = [w for w in current_history if w != "<START>"]
            else:
                # Si la palabra no existe en ningún contexto, forzamos un inicio normal
                current_history = tuple(["<START>"] * (n - 1))
                words = [start_word]
        else:
            current_history = tuple(["<START>"] * (n - 1))
            words = []

    # Ajustamos el límite según lo que ya escribimos
    for _ in range(max_length - len(words)):
        if current_history not in model or not model[current_history]:
            break

        choices = list(model[current_history].keys())
        weights = list(model[current_history].values())
        next_word = random.choices(choices, weights=weights)[0]

        if next_word == "<END>":
            break

        if next_word != "<START>":
            words.append(next_word)

        if n > 1:
            current_history = tuple(list(current_history[1:]) + [next_word])

    return " ".join(words)
