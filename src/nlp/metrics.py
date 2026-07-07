import math


def cosine_similarity_manual(vec_a, vec_b):
    """
    Calcula la similitud del coseno entre dos vectores numéricos.
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Los vectores deben tener la misma dimensión.")

    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0

    for a, b in zip(vec_a, vec_b):
        dot_product += a * b
        norm_a += a ** 2
        norm_b += b ** 2

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))


def generate_similarity_matrix(vectors):
    """
    Toma una lista de vectores y devuelve una matriz NxN con las similitudes.
    Esta función reemplaza a cosine_similarity() de sklearn.
    """
    n = len(vectors)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            if i == j:
                matrix[i][j] = 1.0
            else:
                sim = cosine_similarity_manual(vectors[i], vectors[j])
                matrix[i][j] = sim
                matrix[j][i] = sim

    return matrix
