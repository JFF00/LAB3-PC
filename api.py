from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sklearn.decomposition import PCA

from src.testament import Testament
from src.loader import final_load
from src.nlp.pipeline import process_bible
from src.nlp.cleaner import clean_word
from src.nlp.tfidf import process_bible_objects_to_tfidf, vectorize_new_phrase
from src.nlp.metrics import cosine_similarity_manual
from src.nlp.generator import build_ngram_model, generate_text
from src.nlp.w2v import train_word2vec, generate_w2v_vectors

app = FastAPI()

NT = Testament(1, "New Testament", [])
OT = Testament(0, "Old Testament", [])
books = {}
metadata = []
vector_bible = []
vocab = []
idf = {}

ngram_models = {}
pca_results = {}

@app.on_event("startup")
def load_data():
    global books, metadata, vector_bible, vocab, idf, ngram_models, pca_results
    
    final_load(books, NT, OT)
    process_bible(OT)
    process_bible(NT)
    
    vector_bible, vocab, metadata, idf = process_bible_objects_to_tfidf([OT, NT])
    
    corpus_tokens = []
    for meta in metadata:
        book_id = next(bid for bid, bobj in books.items() if bobj.name == meta["book"])
        tokens = books[book_id].chapters[meta["chapter"]].verses[meta["verse"]].tokens
        corpus_tokens.append(tokens)

    for n in range(1, 5):
        ngram_models[n] = build_ngram_model(books, n)

    w2v_model = train_word2vec(corpus_tokens)
    vector_w2v = generate_w2v_vectors(corpus_tokens, w2v_model)

    pca_2d = PCA(n_components=2)
    pca_3d = PCA(n_components=3)

    pca_results["tfidf_2d"] = pca_2d.fit_transform(np.array(vector_bible)).tolist()
    pca_results["tfidf_3d"] = pca_3d.fit_transform(np.array(vector_bible)).tolist()
    pca_results["word2vec_2d"] = pca_2d.fit_transform(np.array(vector_w2v)).tolist()
    pca_results["word2vec_3d"] = pca_3d.fit_transform(np.array(vector_w2v)).tolist()

@app.get("/dashboard")
def get_dashboard_data(testament: Optional[str] = None, book_name: Optional[str] = None, chapter_id: Optional[str] = None):
    verse_counts = {}
    verse_lengths = {}
    global_freq = {}

    for book_id, book in books.items():
        if testament and book.testament != testament:
            continue
        if book_name and book.name != book_name:
            continue
            
        verse_counts[book.name] = 0
        total_len = 0
        
        for ch_id, chapter in book.chapters.items():
            if chapter_id and ch_id != chapter_id:
                continue
                
            for v_id, verse in chapter.verses.items():
                verse_counts[book.name] += 1
                total_len += len(verse.tokens)
                
                for word, freq in verse.frequencies.items():
                    global_freq[word] = global_freq.get(word, 0) + freq
                    
        if verse_counts[book.name] > 0:
            verse_lengths[book.name] = total_len / verse_counts[book.name]
        else:
            verse_lengths[book.name] = 0

    return {
        "verse_counts": verse_counts,
        "verse_lengths": verse_lengths,
        "frequencies": global_freq
    }

@app.get("/search")
def search_verses(query: str):
    clean = clean_word(query)
    word_vector = vectorize_new_phrase(clean, vocab, idf)
    
    resultados = []
    for i, vector_verso in enumerate(vector_bible):
        similitud = cosine_similarity_manual(word_vector, vector_verso)
        meta = metadata[i]
        
        book_id = next(bid for bid, bobj in books.items() if bobj.name == meta["book"])
        texto_original = books[book_id].chapters[meta["chapter"]].verses[meta["verse"]].content
        
        resultados.append({
            "testament": meta["testament"],
            "book": meta["book"],
            "chapter": meta["chapter"],
            "verse": meta["verse"],
            "text": texto_original,
            "similarity": similitud
        })
        
    resultados.sort(key=lambda x: x["similarity"], reverse=True)
    return resultados[:5]

@app.get("/embeddings")
def get_embeddings(method: str, dims: int):
    key = f"{method}_{dims}d"
    coords = pca_results.get(key, [])
    
    response = []
    for i, coord in enumerate(coords):
        response.append({
            "x": coord[0],
            "y": coord[1],
            "z": coord[2] if dims == 3 else 0,
            "testament": metadata[i]["testament"],
            "book": metadata[i]["book"]
        })
    return response

@app.get("/generate")
def generate(n: int, max_length: int, start_word: Optional[str] = None):
    model = ngram_models.get(n)
    if not model:
        return {"text": ""}
    text = generate_text(model, n, start_word, max_length)
    return {"text": text}