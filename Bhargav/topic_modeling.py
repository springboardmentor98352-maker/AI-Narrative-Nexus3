from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

def split_into_documents(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def train_topic_model(docs, algorithm="LDA", n_topics=5):
    vectorizer = CountVectorizer(max_features=1000)
    dtm = vectorizer.fit_transform(docs)

    if algorithm == "LDA":
        model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    else:
        model = NMF(n_components=n_topics, random_state=42)

    model.fit(dtm)
    return model, vectorizer, dtm, vectorizer.get_feature_names_out()

def get_topic_words(model, features, n_words=8):
    rows = []
    for i, topic in enumerate(model.components_):
        words = [features[j] for j in topic.argsort()[-n_words:]]
        rows.append({"Topic": i, "TopWords": ", ".join(words)})
    return pd.DataFrame(rows)