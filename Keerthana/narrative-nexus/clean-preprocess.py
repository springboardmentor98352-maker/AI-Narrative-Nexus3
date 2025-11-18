import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from PyPDF2 import PdfReader
from docx import Document

# NLP tools
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

#SETTINGS
MAX_FILE_SIZE_MB = 5
MIN_TEXT_LENGTH = 50
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

#TEXT CLEANING FUNCTION
def clean_text(text):
    text = text.lower()                                   # lowercase
    text = re.sub(r"http\S+|www\S+", "", text)            # remove URLs
    text = re.sub(r"[^a-z\s]", " ", text)                 # remove punctuation & numbers
    words = text.split()                                  # split words
    words = [w for w in words if w not in stop_words]     # remove stopwords
    words = [lemmatizer.lemmatize(w) for w in words]      # lemmatize
    return " ".join(words)

#VALIDATION FUNCTION
def validate_file(file):
    file.seek(0, os.SEEK_END)
    size = file.tell() / (1024 * 1024)
    file.seek(0)
    if size > MAX_FILE_SIZE_MB:
        return None, f"⚠️ Too large ({size:.2f} MB)"
    
    try:
        if file.name.endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")

        elif file.name.endswith(".pdf"):
            pdf = PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])

        elif file.name.endswith(".docx"):
            doc = Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
        
        elif file.name.endswith(".csv"):
            df = pd.read_csv(file)
            text = df.to_string()
        else:
            return None, "❌ Unsupported file type"

        if not text.strip():
            return None, "❌ Empty or unreadable file"

        if len(text.strip()) < MIN_TEXT_LENGTH:
            return None, f"⚠️ Too short ({len(text)} chars)"

        return text, f"✅ Valid ({len(text)} chars)"

    except Exception as e:
        return None, f"❌ Error: {e}"

#STREAMLIT UI
st.set_page_config(page_title="Narrative-Nexus", layout="centered")

st.title("🧾Text Data Collection,Cleaning & Preprocessing App")
st.write("Upload validated text files and clean them for analysis.")

uploaded_files = st.file_uploader(
    "Upload your files", 
    type=["txt", "pdf", "docx", "csv"], 
    accept_multiple_files=True
)

records = []

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        
        text, status = validate_file(file)
        st.info(status)

        if text:
            cleaned = clean_text(text)
            st.text_area("Cleaned Text Preview", cleaned[:2000], height=200)

            records.append({
                "file_name": file.name,
                "original_length": len(text),
                "clean_length": len(cleaned),
                "original_text": text,
                "clean_text": cleaned,
                "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

#SAVE BUTTON
if records:
    df = pd.DataFrame(records)

    st.divider()
    st.write("### Summary of Preprocessed Files")
    st.dataframe(df[["file_name", "original_length", "clean_length"]])

    if st.button("💾 Save Cleaned Data to CSV"):
        os.makedirs("output", exist_ok=True)
        save_path = f"output/cleaned_texts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(save_path, index=False, encoding="utf-8")
        st.success(f"Saved cleaned data to `{save_path}`")

        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_texts.csv",
            mime="text/csv"
        )