import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from preprocessing import preprocess_text #custom fn to clean txt
from similarity import compute_cosine_similarity  #custom fn to compare txt

#Page config & CSS
st.set_page_config(page_title="NarrativeNexus", layout="wide")

st.markdown("""
<style>
.main { background-color: #1e0033; color: #f2e6ff; }
.stButton>button {
    background: linear-gradient(90deg, #ff00cc, #3333ff);
    color: white;
    border-radius: 8px;
    height: 50px;
    font-size: 18px;
}
.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: #2a004d;
    color: white;
}
.section-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #2a004d;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>📘 NarrativeNexus</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>The Dynamic Text Analysis Platform</h3>", unsafe_allow_html=True)

# File upload
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.subheader("📥 Upload Files (.txt, .pdf, .docx, .csv)")
uploaded_files = st.file_uploader(
    "Upload Files",
    type=["txt", "pdf", "docx", "csv"],
    accept_multiple_files=True
)
st.markdown("</div>", unsafe_allow_html=True)

# Direct input
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.subheader("✍ Paste Text Directly")
direct_text = st.text_area("Enter text here...", height=180)
st.markdown("</div>", unsafe_allow_html=True)

# File extraction
def extract_text_from_file(file):
    try:
        if file.type == "text/plain":
            return file.read().decode("utf-8")
        
        elif file.type == "application/pdf":
            pdf = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            return "\n".join([p.text for p in doc.paragraphs])
        
        elif file.type == "text/csv":
            df = pd.read_csv(file)
            return " ".join(df.astype(str).values.flatten())
        
        else:
            return ""
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        return ""

# ANALYZE BUTTON
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
if st.button("🚀 Analyze Text"):

    all_texts = []   

    if uploaded_files:
        for f in uploaded_files:
            text = extract_text_from_file(f)
            if text.strip():
                all_texts.append(("File: "+f.name, text))
    
    if direct_text.strip():
        all_texts.append(("Direct Input", direct_text))
    
    if not all_texts:
        st.error("❌ No valid text found!")
        
    else:
        for label, text in all_texts:
            st.markdown(f"### {label}")

            # Character count before preprocessing
            st.write(f"**Original Text ({len(text)} characters):**")
            st.text(text)

            # Preprocess
            result = preprocess_text(text)
            before_text = result["before_text"]
            before_count = result["before_char_count"]
            after_text = result["after_text"]
            after_count = result["after_char_count"]
            tokens = result["tokens"]

            #Display
            st.markdown("**=== BEFORE PREPROCESSING ===**")
            st.text(before_text)
            st.write(f"Character Count: {before_count}\n")

            st.markdown("**=== AFTER PREPROCESSING ===**")
            st.text(after_text)
            st.write(f"Character Count: {after_count}\n")

            st.markdown("**=== TOKENS ===**")
            st.write(tokens)

            # Notify user that preprocessing is done
            st.success("✔ Preprocessing completed successfully!")

        
        # Compute cosine similarity
        st.subheader("📈 Cosine Similarity Matrix")
        combined_texts = [preprocess_text(t)["after_text"] for _, t in all_texts]
        similarity_matrix = compute_cosine_similarity(combined_texts)
        st.dataframe(similarity_matrix)

st.markdown("</div>", unsafe_allow_html=True)
