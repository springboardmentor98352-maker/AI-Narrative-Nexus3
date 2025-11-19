import streamlit as st
from preprocessing import (
    get_word_count, 
    preprocess_text, 
    extract_text_from_uploaded_file,
    get_top_keywords
)

# Page Config
st.set_page_config(page_title="Mind Mesh Analytics", layout="wide")

# Load External CSS
try:
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Style file not found. Please upload 'style.css'.")

# App Header
st.markdown('<div class="app-title">Mind Mesh Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="app-caption">A Smart Engine for Text Understanding</div>', unsafe_allow_html=True)

# Initialize Session State
if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = ""
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = ""
# Store the last uploaded file ID to prevent redundant reloading
if 'last_uploaded_file_id' not in st.session_state:
    st.session_state['last_uploaded_file_id'] = None

# --- INPUT SECTION ---
st.subheader("📁 Data Import")
input_method = st.radio(
    "Select Input Method:",
    ('File', 'Paste Text'),
    horizontal=True,
    label_visibility="collapsed"
)

if input_method == 'File':
    uploaded_file = st.file_uploader(
        "Upload Document (Supported: .txt, .csv, .pdf, .docx)",
        type=['txt', 'csv', 'pdf', 'docx']
    )
    
    if uploaded_file is not None:
        # Check if this is a new file or the same one
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        if file_id != st.session_state['last_uploaded_file_id']:
            extracted_text = extract_text_from_uploaded_file(uploaded_file)
            if extracted_text:
                st.session_state['raw_text'] = extracted_text
                st.session_state['last_uploaded_file_id'] = file_id
                # Clear previous processing results when new file loads
                st.session_state['processed_text'] = "" 
                st.toast(f"Successfully Loaded: {uploaded_file.name}", icon="✅")
        elif st.session_state['raw_text']:
             st.success(f"✅ File Ready: {uploaded_file.name}")
    else:
        # Reset if file is removed
        if st.session_state['last_uploaded_file_id'] is not None:
            st.session_state['raw_text'] = ""
            st.session_state['processed_text'] = ""
            st.session_state['last_uploaded_file_id'] = None

else:
    text_input = st.text_area(
        "Paste Text Here",
        height=250,
        placeholder="Type or paste your content here..."
    )
    if text_input:
        st.session_state['raw_text'] = text_input

# --- ACTION BUTTON (Below Inputs) ---
st.markdown("<br>", unsafe_allow_html=True)
# Using a centered column layout for the button to make it look neat
col_btn, _ = st.columns([1, 3])
with col_btn:
    if st.button("⚡ Start Pre-processing", use_container_width=True):
        if st.session_state['raw_text']:
            st.session_state['processed_text'] = preprocess_text(st.session_state['raw_text'])
            st.toast("Processing completed successfully!", icon="🎉")
        else:
            st.error("Please provide input text first.")

st.markdown("---")

# --- RESULTS DASHBOARD ---
if st.session_state['processed_text']:
    st.subheader("📊 Analysis Dashboard")
    
    # Metrics Row
    raw_count = get_word_count(st.session_state['raw_text'])
    proc_count = get_word_count(st.session_state['processed_text'])
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Original Words", value=raw_count)
    with m_col2:
        st.metric(label="Processed Words", value=proc_count, delta=proc_count-raw_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # Content & Stats Row
    res_col1, res_col2 = st.columns([3, 2], gap="medium")
    
    with res_col1:
        st.markdown("#### 📝 Processed Text View")
        st.text_area(
            label="Output Data",
            value=st.session_state['processed_text'],
            height=450,
            key="processed_output_display"
        )
        # Download Button (Below Processed Text)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Processed Data",
            data=st.session_state['processed_text'],
            file_name="processed_data.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with res_col2:
        st.markdown("#### 🔑 Top Keywords")
        df_keywords = get_top_keywords(st.session_state['processed_text'], n=10)
        
        st.dataframe(
            df_keywords,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Keyword": st.column_config.TextColumn("Keyword", width="medium"),
                "Frequency": st.column_config.ProgressColumn(
                    "Frequency",
                    format="%d",
                    min_value=0,
                    max_value=int(df_keywords['Frequency'].max()) if not df_keywords.empty else 10
                )
            }
        )

elif st.session_state['raw_text']:
    st.info("Ready to process. Click 'Start Pre-processing' above to begin.")
