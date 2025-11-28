# preprocessing.py (replace your existing file)
import pandas as pd
import re
from collections import Counter
import streamlit as st

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during',
    'each', 'few', 'for', 'from', 'further',
    'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how',
    'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself',
    'let\'s', 'me', 'more', 'most', 'my', 'myself',
    'no', 'nor', 'not',
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'she', 'should', 'so', 'some', 'such',
    'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up',
    'very',
    'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'why', 'with', 'would',
    'you', 'your', 'yours', 'yourself', 'yourselves'
}

def get_word_count(text: str) -> int:
    if not text:
        return 0
    return len(text.split())

def get_top_keywords(text: str, n: int = 10) -> pd.DataFrame:
    if not text:
        return pd.DataFrame(columns=['Keyword', 'Frequency'])
    words = text.split()
    counter = Counter(words)
    most_common = counter.most_common(n)
    return pd.DataFrame(most_common, columns=['Keyword', 'Frequency'])

def preprocess_text(text: str) -> str:
    """
    Aggressive cleaning (default): lowercase, remove apostrophes, drop non-alpha,
    remove stopwords and tokens <=1 char.
    Returns empty string if nothing remains.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"'", "", text)
    text = re.sub(r'[^a-z\s]', ' ', text)   # keep only letters and spaces
    tokens = text.split()
    cleaned = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return ' '.join(cleaned)

def preprocess_text_with_fallback(text: str) -> str:
    """
    Less aggressive fallback:
     - lowercase
     - remove only control chars
     - collapse whitespace
     - remove purely symbol tokens
     - keep tokens even if stopword removal would eliminate everything
    """
    if not text:
        return ""
    text = text.lower()
    # remove control characters
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # replace weird punctuation with spaces, but keep letters and numbers
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 0 and not all(ch in '0123456789' for ch in t)]
    # remove single-character tokens except digits (we already removed all-digit tokens)
    tokens = [t for t in tokens if len(t) > 1]
    if not tokens:
        # as last resort, collapse whitespace and return original-ish text
        normalized = re.sub(r'\s+', ' ', text).strip()
        return normalized
    return ' '.join(tokens)

def extract_text_from_uploaded_file(uploaded_file) -> str:
    """
    Extract text from .txt, .csv, .pdf, .docx
    Returns string (may be empty). Does not raise.
    """
    if uploaded_file is None:
        return ""

    uploaded_file.seek(0)
    file_extension = uploaded_file.name.split('.')[-1].lower()
    text = ""

    try:
        if file_extension == 'txt':
            raw = uploaded_file.getvalue()
            if isinstance(raw, bytes):
                text = raw.decode('utf-8', errors='ignore')
            else:
                text = str(raw)

        elif file_extension == 'csv':
            df = pd.read_csv(uploaded_file, dtype=str, keep_default_na=False)
            # join cells with spaces
            text = ' '.join(df.fillna('').astype(str).values.flatten())

        elif file_extension == 'pdf':
            if not PdfReader:
                st.error("PDF extraction requires 'pypdf' to be installed. Install with: pip install pypdf")
                return ""
            try:
                reader = PdfReader(uploaded_file)
                pages_text = []
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    pages_text.append(page_text)
                text = "\n".join(pages_text).strip()
                if not text:
                    # sometimes extract_text returns empty because of encoding; return empty and let UI show it
                    st.warning("PDF was read but no extractable text was found on pages. This can happen with scanned PDFs or unusual encodings.")
                    return ""
            except Exception as e:
                st.error(f"Error extracting PDF text: {e}")
                return ""

        elif file_extension == 'docx':
            if not Document:
                st.error("DOCX extraction requires 'python-docx' to be installed. Install with: pip install python-docx")
                return ""
            try:
                doc = Document(uploaded_file)
                paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
                text = "\n".join(paragraphs)
            except Exception as e:
                st.error(f"Error reading DOCX: {e}")
                return ""

        else:
            st.error(f"Unsupported file type: .{file_extension}")
            return ""
    except Exception as e:
        st.error(f"Unexpected error reading file: {e}")
        return ""

    return text