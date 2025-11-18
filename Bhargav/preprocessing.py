import pandas as pd
import re
import io
import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    from docx import Document
except ImportError:
    Document = None

def get_word_count(text: str) -> int:
    """
    Calculates the number of words in a given string by splitting on whitespace.
    """
    if not text:
        return 0
    # Splits by any whitespace character
    return len(text.split())

def preprocess_text(text: str) -> str:
    """
    Performs basic text preprocessing:
    1. Converts to lowercase.
    2. Removes punctuation and numbers.
    3. Removes extra whitespace.
    """
    # 1. Convert to lowercase
    processed_text = text.lower()
    # 2. Remove punctuation and numbers (keep only letters and whitespace)
    processed_text = re.sub(r'[^a-z\s]', ' ', processed_text)
    # 3. Remove extra whitespace and trim
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    return processed_text

def extract_text_from_uploaded_file(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> str or None:
    """
    Reads the content of various supported file types (TXT, CSV, PDF, DOCX).
    """
    file_extension = uploaded_file.name.split('.')[-1].lower()
    text = ""

    try:
        if file_extension == 'txt':
            text = uploaded_file.getvalue().decode("utf-8")
        
        elif file_extension == 'csv':
            # FIX: Convert all cells to string and join values to avoid counting separators/newlines 
            df = pd.read_csv(uploaded_file)
            
            # Combine all non-NaN values from all cells into a single, space-separated string.
            text = ' '.join(df.astype(str).values.flatten())

        elif file_extension == 'pdf':
            if PdfReader:
                reader = PdfReader(uploaded_file)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            else:
                st.warning("Install 'pypdf' for PDF support. Using mock content.")
                text = f"Mock PDF Content: File '{uploaded_file.name}' placeholder text for analysis."
            
        elif file_extension == 'docx':
            if Document:
                document = Document(uploaded_file)
                text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            else:
                st.warning("Install 'python-docx' for DOCX support. Using mock content.")
                text = f"Mock DOCX Content: File '{uploaded_file.name}' placeholder text for analysis."
        
        else:
            st.error(f"Unsupported file type: {file_extension}")
            return None

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None
    return text
COLORS = {
    'primary': '#51E2F5',    
    'secondary': '#FFA8B6',  
    'background': '#EDF7F6', 
    'card_bg': '#9DF9EF',    
    'text': '#A28089',       }