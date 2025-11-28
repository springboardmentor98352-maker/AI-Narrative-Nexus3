import streamlit as st
import pandas as pd
from preprocess import (
    get_word_count,
    preprocess_text,
    preprocess_text_with_fallback,
    extract_text_from_uploaded_file,
    get_top_keywords
)

st.set_page_config(page_title="Mind Mesh Analyst", layout="wide", initial_sidebar_state="expanded")

try:
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css not found - default styling will be used.")

st.markdown('<div class="app-title">Mind Mesh Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="app-caption">A Smart Engine for Text Understanding</div>', unsafe_allow_html=True)

if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = ""
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = ""
if 'last_uploaded_file_id' not in st.session_state:
    st.session_state['last_uploaded_file_id'] = None

st.subheader("📁 Data Import")
input_method = st.radio("Select Input Method:", ('File', 'Paste Text'), horizontal=True, label_visibility="collapsed")

uploaded_file = None
if input_method == 'File':
    uploaded_file = st.file_uploader(
        "Upload Document (Supported: .txt, .csv, .pdf, .docx)",
        type=['txt', 'csv', 'pdf', 'docx'],
        help="Upload a file. Processing will start when you click '⚡ Start Pre-processing'."
    )

    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        # Only re-extract if a different file was uploaded
        if file_id != st.session_state['last_uploaded_file_id']:
            extracted_text = extract_text_from_uploaded_file(uploaded_file)
            if extracted_text:
                st.session_state['raw_text'] = extracted_text
                st.session_state['last_uploaded_file_id'] = file_id
                st.session_state['processed_text'] = ""
                st.success(f"File Ready: {uploaded_file.name}")
            else:
                st.session_state['raw_text'] = ""
                st.session_state['processed_text'] = ""
                st.session_state['last_uploaded_file_id'] = None
                st.error("Could not extract text from the uploaded file. See notes below.")
else:
    text_input = st.text_area("Paste Text Here", height=250, placeholder="Type or paste your content here... (Processing will start when you click the button)")
    if text_input:
        st.session_state['raw_text'] = text_input
        st.session_state['processed_text'] = ""

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state['raw_text']:
    st.markdown("### Raw Text Preview (first 800 chars)")
    st.code(st.session_state['raw_text'][:800], language='text')
    st.markdown(f"**Raw word count:** {get_word_count(st.session_state['raw_text'])}")
    st.markdown("---")

col_btn, _ = st.columns([1, 3])
with col_btn:
    if st.button("⚡ Start Pre-processing", use_container_width=True):
        raw = st.session_state.get('raw_text', '').strip()
        if not raw:
            st.error("Please provide input text first (upload a file or paste text).")
        else:
            processed = preprocess_text(raw)
            if not processed.strip():
                st.warning("Standard preprocessing removed all tokens (this can happen with some PDFs). Using a fallback, less-aggressive preprocessing so you can inspect results.")
                processed = preprocess_text_with_fallback(raw)
                st.session_state['processed_text'] = processed
                st.success("Processing completed with fallback (see results).")
            else:
                st.session_state['processed_text'] = processed
                st.success("Processing completed!")
st.markdown("---")

if st.session_state['processed_text']:
    st.subheader("📊 Analysis Dashboard")

    raw_count = get_word_count(st.session_state['raw_text'])
    proc_count = get_word_count(st.session_state['processed_text'])

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Original Words", value=raw_count)
    with m_col2:
        st.metric(label="Processed Words", value=proc_count, delta=proc_count - raw_count)

    st.markdown("<br>", unsafe_allow_html=True)

    res_col1, res_col2 = st.columns([3, 2], gap="medium")

    with res_col1:
        st.markdown("#### 📝 Processed Text View")
        st.text_area(label="Output Data", value=st.session_state['processed_text'], height=420, key="processed_output_display")
        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button("📥 Download Processed Data (.txt)", data=st.session_state['processed_text'], file_name="processed_data.txt", mime="text/plain", use_container_width=True)

        proc_df = pd.DataFrame({'processed_text': [st.session_state['processed_text']]})
        csv_bytes = proc_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Processed Data (.csv)", data=csv_bytes, file_name="processed_data.csv", mime="text/csv", use_container_width=True)

    with res_col2:
        st.markdown("#### 🔑 Top Keywords")
        df_keywords = get_top_keywords(st.session_state['processed_text'], n=20)
        if df_keywords.empty:
            st.info("No keywords found in the processed text.")
        else:
            st.dataframe(df_keywords.head(10), use_container_width=True, hide_index=True)

elif st.session_state['raw_text']:
    st.info("Ready to process. Click '⚡ Start Pre-processing' above to begin.")
else:

    st.info("Upload a file or paste text to get started.")
