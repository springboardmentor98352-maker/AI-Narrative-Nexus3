import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PyPDF2 import PdfReader
from docx import Document

#PAGE SETUP 
st.set_page_config(page_title="Narrative-Nexus", layout="centered")
st.title("🧾Text Data Collection App ")
st.write("Upload and validate text, PDF, Word, or CSV files before saving.")

#CONFIG
MAX_FILE_SIZE_MB = 5        # skip files larger than 5 MB
MIN_TEXT_LENGTH = 50        # skip text shorter than 50 characters

uploaded_files = st.file_uploader(
    "📂 Upload your files here",
    type=["txt", "pdf", "docx", "csv"],
    accept_multiple_files=True
)

data_records = []

#FILE HANDLING 
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")

        # 1️⃣ Validate file size
        file.seek(0, os.SEEK_END)
        file_size_mb = file.tell() / (1024 * 1024)
        file.seek(0)
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.warning(f"⚠️ Skipped {file.name}: file size {file_size_mb:.2f} MB > {MAX_FILE_SIZE_MB} MB")
            continue

        text = ""
        try:
            if file.name.endswith(".txt"):
                text = file.read().decode("utf-8", errors="ignore")

            elif file.name.endswith(".pdf"):
                pdf = PdfReader(file)
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)

            elif file.name.endswith(".docx"):
                doc = Document(file)
                text = "\n".join(p.text for p in doc.paragraphs)

            elif file.name.endswith(".csv"):
                df = pd.read_csv(file)
                st.write("CSV Preview:", df.head())
                text = df.to_string()
            else:
                st.warning(f"⚠️ Unsupported file type: {file.name}")
                continue

        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")
            continue

        # 2️⃣ Validate text quality
        if not text.strip():
            st.error(f"❌ {file.name} is empty or unreadable.")
            continue

        if len(text.strip()) < MIN_TEXT_LENGTH:
            st.warning(f"⚠️ {file.name} contains very little text ({len(text.strip())} chars).")
            continue

        # 3️⃣ Display preview safely
        st.text_area("Extracted Text Preview", text[:2000], height=200)
        st.info(f"✅ {file.name} looks good ({len(text)} characters).")

        # 4️⃣ Save record for export
        data_records.append({
            "file_name": file.name,
            "text_length": len(text),
            "content": text.strip(),
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

#SAVE BUTTON
if data_records:
    st.success(f"✅ {len(data_records)} validated file(s) ready to save.")

    if st.button("💾 Save Validated Texts to CSV"):
        os.makedirs("output", exist_ok=True)
        df = pd.DataFrame(data_records)
        save_path = f"output/validated_texts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(save_path, index=False, encoding="utf-8")
        st.success(f"✅ Data saved to `{save_path}`")

        st.dataframe(df[["file_name", "text_length", "uploaded_at"]])
else:
    st.info("ℹ️ Upload files to begin validation.")
