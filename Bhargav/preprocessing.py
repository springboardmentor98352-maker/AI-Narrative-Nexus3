import pandas as pd
import re
from collections import Counter
import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    from docx import Document
except ImportError:
    Document = None

COLORS = {
    'background': '#2C2B30',
    'card_bg': '#4F4F51',
    'text': '#D6D6D6',
    'accent_pink': '#F2C4CE',
    'accent_coral': '#F58F7C'
}

STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at', 
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 
    'can', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 
    'each', 'few', 'for', 'from', 'further', 
    'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 
    'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 
    'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 
    'no', 'nor', 'not', 
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 
    'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 
    'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too', 
    'under', 'until', 'up', 
    'very', 
    'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 
    'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves'
}

def get_word_count(text: str) -> int:
    """Calculates the total number of words in the text."""
    if not text:
        return 0
    return len(text.split())

def get_top_keywords(text: str, n: int = 10) -> pd.DataFrame:
    """
    Generates a DataFrame of the top N most frequent words.
    Since text is already preprocessed (stopwords removed), we just count.
    """
    if not text:
        return pd.DataFrame(columns=['Keyword', 'Frequency'])

    words = text.split()    
    counter = Counter(words)
    most_common = counter.most_common(n)
    return pd.DataFrame(most_common, columns=['Keyword', 'Frequency'])

def preprocess_text(text: str) -> str:
    if not text:
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove apostrophes (preserve contractions as single words)
    text = re.sub(r"'", "", text)
    
    # 3. Remove special characters and numbers (replace with space to avoid merging separate words)
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # 4. Tokenize and Remove Stopwords
    tokens = text.split()
    cleaned_tokens = [word for word in tokens if word not in STOPWORDS and len(word) > 1]
    
    # 5. Join back
    processed_text = ' '.join(cleaned_tokens)
    
    return processed_text

def extract_text_from_uploaded_file(uploaded_file) -> str:
    """
    Extracts text content from TXT, CSV, PDF, and DOCX files.
    """
    if uploaded_file is None:
        return ""

    uploaded_file.seek(0)

    file_extension = uploaded_file.name.split('.')[-1].lower()
    text = ""

    try:
        if file_extension == 'txt':
            text = uploaded_file.getvalue().decode("utf-8")
        
        elif file_extension == 'csv': 
            df = pd.read_csv(uploaded_file)
            text = ' '.join(df.astype(str).values.flatten())

        elif file_extension == 'pdf':
            if PdfReader:
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                st.error("PDF support missing. Please install 'pypdf'.")
            
        elif file_extension == 'docx':
            if Document:
                document = Document(uploaded_file)
                text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            else:
                st.error("DOCX support missing. Please install 'python-docx'.")
        else:
            st.error(f"Unsupported file type: {file_extension}")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
    return text