import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

nltk.download("vader_lexicon")
nltk.download("punkt")

def analyze_sentiments(docs):
    sia = SentimentIntensityAnalyzer()
    data = []
    for d in docs:
        score = sia.polarity_scores(d)
        data.append(score)
    return pd.DataFrame(data)

def extractive_summary(text, max_sentences=5):
    sentences = sent_tokenize(text)
    return " ".join(sentences[:max_sentences])