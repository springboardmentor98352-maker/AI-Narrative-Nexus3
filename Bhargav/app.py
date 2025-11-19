import streamlit as st
import os

st.set_page_config(layout="wide") 
from preprocessing import (
    get_word_count, 
    preprocess_text, 
    extract_text_from_uploaded_file,
    COLORS
)
try:
    with open('styles.css') as f:
        custom_css = f.read()
except FileNotFoundError:
    custom_css = f"""
    <style>
        /* Fallback CSS */
        .stApp {{ background-color: {COLORS['background']}; color: {COLORS['text']}; font-family: 'Inter', sans-serif; }}
        .app-title {{ color: {COLORS['text']}; font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }}
        .app-caption {{ color: {COLORS['text']}; font-size: 1.2rem; text-align: center; margin-bottom: 2rem; }}
        .stButton > button {{ 
            background-color: {COLORS['primary']} !important; 
            color: white !important; 
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        [data-testid="stMetric"] {{
            background-color: {COLORS['card_bg']} !important;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid {COLORS['primary']};
        }}
    </style>
    """

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<center><div class="app-title">Mind Mesh Analystics</div></center>', unsafe_allow_html=True)
st.markdown('<center><div class="app-caption">A Smart Engine for Text Understanding</center></div>', unsafe_allow_html=True)

st.subheader("Choose Your Input Method")
input_method = st.radio(
    "Select Input Source:",
    ('File Upload', 'Paste Text'),
    index=0,
    horizontal=True,
    key='input_radio'
)
# processed data
if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = ""
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = ""
data_available = False

if input_method == 'File Upload':
    uploaded_file = st.file_uploader(
        "Upload a TXT, CSV, PDF, or DOCX file",
        type=['txt', 'csv', 'pdf', 'docx'],
        accept_multiple_files=False,
        key='file_uploader'
    )
    if uploaded_file is not None:
        st.session_state['raw_text'] = extract_text_from_uploaded_file(uploaded_file)
        if st.session_state['raw_text']:
            data_available = True
            st.success(f"File '{uploaded_file.name}' loaded. Ready to process.")
else:
    pasted_text = st.text_area(
        "Paste your text here (minimum 10 characters)",
        height=200,
        key='text_area'
    )
    if pasted_text and len(pasted_text) > 10:
        st.session_state['raw_text'] = pasted_text
        data_available = True
        st.info(f"Text available for processing ({get_word_count(pasted_text)} words).")
    elif pasted_text and len(pasted_text) <= 10:
        st.warning("Please paste more substantial text.")
        st.session_state['raw_text'] = ""
st.markdown("---")

if st.button("Process Data", disabled=not data_available):
    if st.session_state['raw_text']:
        st.session_state['processed_text'] = preprocess_text(st.session_state['raw_text'])
        st.success("Data successfully processed!")
    else:
        st.warning("Please upload a file or paste text before processing.")

if st.session_state['raw_text'] or st.session_state['processed_text']:
    st.subheader("Analysis Results")
    # Calculate word counts using external function
    raw_word_count = get_word_count(st.session_state['raw_text'])
    processed_word_count = get_word_count(st.session_state['processed_text'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Original Word Count", 
            value=f"{raw_word_count:,}",
            delta=None
        )
    with col2:
        st.metric(
            label="Processed Word Count", 
            value=f"{processed_word_count:,}",
            delta=processed_word_count - raw_word_count if processed_word_count - raw_word_count != 0 else None,
            delta_color="inverse"
        )
    st.markdown("---")
    st.subheader("Raw and Processed Text Comparison")
    col_raw, col_processed = st.columns(2)
    with col_raw:
        st.markdown(f"#### Original Text ({raw_word_count} words)")
        st.code(st.session_state['raw_text'][:500] + ('...' if len(st.session_state['raw_text']) > 500 else ''), language='markdown')
        st.caption("Showing first 500 characters of the raw text.")
    with col_processed:
        st.markdown(f"#### Preprocessed Text ({processed_word_count} words)")
        st.code(st.session_state['processed_text'][:500] + ('...' if len(st.session_state['processed_text']) > 500 else ''), language='markdown')
        st.caption("Showing first 500 characters of the processed text.")
