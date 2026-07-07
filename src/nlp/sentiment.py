import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon', quiet=True)


def analyze_sentiment(books):
    sia = SentimentIntensityAnalyzer()
    verse_sentiments = []

    for book_id, book in books.items():
        for chapter_id, chapter in book.chapters.items():
            for verse_id, verse in chapter.verses.items():
                score = sia.polarity_scores(verse.content)["compound"]

                verse_sentiments.append({
                    "book": book.name,
                    "chapter": chapter_id,
                    "verse": verse_id,
                    "score": score,
                    "content": verse.content
                })

    df_sentiments = pd.DataFrame(verse_sentiments)

    book_sentiments = df_sentiments.groupby(
        "book")["score"].mean().reset_index()
    chapter_sentiments = df_sentiments.groupby(["book", "chapter"])[
        "score"].mean().reset_index()

    return df_sentiments, book_sentiments, chapter_sentiments
