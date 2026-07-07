from gensim.models import Word2Vec
import numpy as np

def train_word2vec(corpus_tokens, vector_size=100, window=5, min_count=1):
    model = Word2Vec(sentences=corpus_tokens, vector_size=vector_size, window=window, min_count=min_count, workers=4)
    return model

def get_verse_embedding(tokens, model):
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if len(vectors) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

def generate_w2v_vectors(corpus_tokens, model):
    vectors = []
    for tokens in corpus_tokens:
        vectors.append(get_verse_embedding(tokens, model))
    return vectors