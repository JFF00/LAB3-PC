from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix


def dummy_tokenizer(text):
    return text


def train_and_evaluate_classifier(books):
    X_text = []
    y_labels = []

    for book_id, book in books.items():
        for chapter_id, chapter in book.chapters.items():
            for verse_id, verse in chapter.verses.items():
                if verse.tokens:
                    X_text.append(verse.tokens)
                    y_labels.append(book.name)

    print("Total verses for training:", len(X_text))

    vectorizer = TfidfVectorizer(
        analyzer=dummy_tokenizer,
        lowercase=False
    )

    X_tfidf = vectorizer.fit_transform(X_text)

    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y_labels, test_size=0.2, random_state=42
    )

    model = MultinomialNB()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)

    print("Accuracy:", accuracy)

    return model, vectorizer, accuracy, conf_matrix
