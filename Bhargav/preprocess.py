import re
import pandas as pd
from collections import Counter
from pypdf import PdfReader
from docx import Document

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been
before being below between both but by can could did do does doing down during
each few for from further had has have having he her here him his how i if in
into is it its itself me more most my no nor not of off on once only or other
our ours ourselves out over own same she should so some such than that the their
theirs them themselves then there these they this those through to too under
until up very was we were what when where which while who why with would you your
""".split())

def get_word_count(text):
    return len(text.split())

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 1]
    return " ".join(tokens)

def preprocess_text_with_fallback(text):
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return " ".join(text.split())

def extract_text_from_uploaded_file(f):
    ext = f.name.split(".")[-1]
    if ext == "txt":
        return f.read().decode("utf-8")
    if ext == "csv":
        df = pd.read_csv(f)
        return " ".join(df.astype(str).values.flatten())
    if ext == "pdf":
        reader = PdfReader(f)
        return " ".join(p.extract_text() or "" for p in reader.pages)
    if ext == "docx":
        doc = Document(f)
        return " ".join(p.text for p in doc.paragraphs)
    return ""

def get_top_keywords(text, n=10):
    counter = Counter(text.split())
    return pd.DataFrame(counter.most_common(n), columns=["Keyword", "Frequency"])