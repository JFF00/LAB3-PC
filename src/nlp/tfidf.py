import math
from collections import Counter


def compute_tf(doc_tokens):
    # En sklearn, el TF inicial es simplemente el conteo bruto.
    # La normalización por longitud se hace al final sobre el vector completo.
    if not doc_tokens:
        return {}
    return dict(Counter(doc_tokens))


def compute_idf(corpus):
    idf_dict = {}
    total_docs = len(corpus)
    df_dict = {}

    for doc_tokens in corpus:
        for word in set(doc_tokens):
            df_dict[word] = df_dict.get(word, 0) + 1

    # Aplicamos la fórmula Smoothed IDF de sklearn para evitar negativos
    for word, df in df_dict.items():
        idf_dict[word] = math.log((total_docs + 1) / (df + 1)) + 1.0

    return idf_dict


def generate_tfidf_vectors(corpus):
    vocabulario = sorted(list(set(word for doc in corpus for word in doc)))
    idf = compute_idf(corpus)
    vectores_tfidf = []

    for doc in corpus:
        tf = compute_tf(doc)
        vector_doc = []

        # 1. Calculamos el TF-IDF crudo
        for word in vocabulario:
            if word in tf:
                valor_tfidf = tf[word] * idf.get(word, 0.0)
            else:
                valor_tfidf = 0.0

            vector_doc.append(valor_tfidf)

        # 2. Aplicamos Normalización L2 (Obligatorio para replicar sklearn)
        # Esto asegura que todos los vectores tengan la misma escala geométrica
        norma = math.sqrt(sum(v ** 2 for v in vector_doc))
        if norma > 0:
            vector_doc = [v / norma for v in vector_doc]

        vectores_tfidf.append(vector_doc)

    return vectores_tfidf, vocabulario, idf


def process_bible_objects_to_tfidf(testaments_list):
    """
    Recorre la jerarquía de clases (Testament -> Book -> Chapter -> Verse)
    para armar el corpus y calcular el TF-IDF.
    """
    corpus_tokens = []
    metadatos_versos = []

    for testament in testaments_list:
        for book in testament.books:
            for chapter in testament.books[book].chapters:
                for verse in testament.books[book].chapters[chapter].verses:
                    corpus_tokens.append(
                        testament.books[book].chapters[chapter].verses[verse].tokens)
                    metadatos_versos.append({
                        "testament": testament.name,
                        "book": testament.books[book].name,
                        "chapter": testament.books[book].chapters[chapter].id,
                        "verse": testament.books[book].chapters[chapter].verses[verse].id
                    })

    vectores_finales, vocabulario, idf = generate_tfidf_vectors(corpus_tokens)

    return vectores_finales, vocabulario, metadatos_versos, idf


def vectorize_new_phrase(phrase_tokens, vocabulario_global, idf_global):
    """
    Convierte una frase nueva en un vector TF-IDF compatible con el corpus original.
    """
    # 1. Calculamos el TF de tu frase
    tf = compute_tf(phrase_tokens)
    vector_frase = []

    # 2. Mapeamos tu frase usando el vocabulario estricto de la Biblia
    for word in vocabulario_global:
        if word in tf:
            # Si usaste la palabra y existe en la Biblia, calculamos su peso
            valor_tfidf = tf[word] * idf_global.get(word, 0.0)
        else:
            # Si la palabra no está en tu frase, o no existe en la Biblia, es 0
            valor_tfidf = 0.0

        vector_frase.append(valor_tfidf)

    # 3. Normalización L2 obligatoria para que la similitud del coseno funcione
    norma = math.sqrt(sum(v ** 2 for v in vector_frase))
    if norma > 0:
        vector_frase = [v / norma for v in vector_frase]

    return vector_frase
