import streamlit as st
from collection import extract_text, get_file_details
from preprocessing import preprocess_text
from model import lda_topic_model
from css import load_css
from sentiment import analyze_sentiment
import pandas as pd

def render_ui():

    #PAGE SETUP
    st.set_page_config(page_title="NarrativeNexus", layout="wide")
    st.markdown(load_css(), unsafe_allow_html=True)

    st.markdown("<h1 class='page-title'>📘 NarrativeNexus</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='page-subtitle'>Dynamic Text Analysis Platform</h3>", unsafe_allow_html=True)

    #FILE UPLOAD
    st.markdown("<div class='card-section'>", unsafe_allow_html=True)
    st.markdown("<h4 class='section-title'>📥 Upload Your Files</h4>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "",
        type=["txt", "pdf", "docx", "csv"],
        accept_multiple_files=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    #DIRECT INPUT
    st.markdown("<div class='card-section'>", unsafe_allow_html=True)
    st.markdown("<h4 class='section-title'>✍ Paste Text Directly</h4>", unsafe_allow_html=True)
    direct_text = st.text_area("", height=180)
    st.markdown("</div>", unsafe_allow_html=True)

    #PROCESS BUTTON
    st.markdown("<div class='card-section center'>", unsafe_allow_html=True)

    if st.button("🚀Analyze Text", use_container_width=True):

        all_inputs = []

        #Uploaded Files 
        if uploaded_files:
            for file in uploaded_files:
                details = get_file_details(file)
                text = extract_text(file)
                all_inputs.append((details, text))

        #Direct Text 
        if direct_text.strip():
            all_inputs.append((
                {"name": "Direct Input", "type": "text/plain",
                 "size_kb": round(len(direct_text) / 1024, 2), "extension": "txt"},
                direct_text
            ))

        if not all_inputs:
            st.error("❌ No valid input provided.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        st.markdown("</div>", unsafe_allow_html=True)

        #DISPLAY ANALYSIS 
        download_list = [] 

        for details, text in all_inputs:  

            # File title card
            st.markdown(f"<div class='file-title'>📄 {details['name']}</div>", unsafe_allow_html=True)

            with st.container():
                colA, colB, colC = st.columns([1.5, 1, 1])

                with colA:
                    st.markdown("**File Type:** " + details['type'])
                with colB:
                    st.markdown(f"**Size:** {details['size_kb']} KB")
                with colC:
                    st.markdown("**Extension:** " + details['extension'])

            #Preprocessing
            result = preprocess_text(text)

            #Statistics
            st.markdown("<h3 class='section-title'>📊 Text Statistics</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"""
                <div class='stat-card blue'>
                    <div class='stat-number'>{result['original_words']}</div>
                    <div class='stat-label'>Original Words</div>
                </div>
            """, unsafe_allow_html=True)

            col2.markdown(f"""
                <div class='stat-card purple'>
                    <div class='stat-number'>{result['original_chars']}</div>
                    <div class='stat-label'>Original Characters</div>
                </div>
            """, unsafe_allow_html=True)

            col3.markdown(f"""
                <div class='stat-card blue'>
                    <div class='stat-number'>{result['cleaned_words']}</div>
                    <div class='stat-label'>Cleaned Words</div>
                </div>
            """, unsafe_allow_html=True)

            col4.markdown(f"""
                <div class='stat-card purple'>
                    <div class='stat-number'>{result['cleaned_chars']}</div>
                    <div class='stat-label'>Cleaned Characters</div>
                </div>
            """, unsafe_allow_html=True)

            #Reduction Stats
            st.markdown("<br>", unsafe_allow_html=True)
            colr1, colr2 = st.columns(2)
            colr1.markdown(f"<div class='reduce-card'>Word Reduction: {result['word_reduction']}%</div>", unsafe_allow_html=True)
            colr2.markdown(f"<div class='reduce-card'>Character Reduction: {result['char_reduction']}%</div>", unsafe_allow_html=True)

            #Text Comparison
            st.markdown("<h3 class='section-title'>🔍 Text Comparison</h3>", unsafe_allow_html=True)

            colA, colB = st.columns(2)
            with colA:
                st.markdown("<div class='text-box-title'>⛔ Original Text</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='text-box'>{result['original_text']}</div>", unsafe_allow_html=True)

            with colB:
                st.markdown("<div class='text-box-title'>✔ Cleaned Text</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='text-box'>{result['processed_text']}</div>", unsafe_allow_html=True)

            #SENTIMENT ANALYSIS
            sentiment_result = analyze_sentiment(result["processed_text"])

            st.markdown("<h3 class='section-title'>😊 Sentiment Analysis</h3>", unsafe_allow_html=True)

            colS1, colS2, colS3, colS4 = st.columns(4)

            colS1.markdown(f"""
                <div class='stat-card blue'>
                    <div class='stat-number'>{sentiment_result['positive']}</div>
                    <div class='stat-label'>Positive</div>
                </div>
            """, unsafe_allow_html=True)

            colS2.markdown(f"""
                <div class='stat-card purple'>
                    <div class='stat-number'>{sentiment_result['neutral']}</div>
                    <div class='stat-label'>Neutral</div>
                </div>
            """, unsafe_allow_html=True)

            colS3.markdown(f"""
                <div class='stat-card blue'>
                    <div class='stat-number'>{sentiment_result['negative']}</div>
                    <div class='stat-label'>Negative</div>
                </div>
            """, unsafe_allow_html=True)

            colS4.markdown(f"""
                <div class='stat-card purple'>
                    <div class='stat-number'>{sentiment_result['compound']}</div>
                    <div class='stat-label'>Compound Score</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div class='reduce-card'>Overall Sentiment: <b>{sentiment_result['sentiment']}</b></div>",
                unsafe_allow_html=True
            )

            # Sentiment Validation Check (PER DOCUMENT)
            if abs(sentiment_result["compound"]) < 0.05:
                st.info("ℹ Sentiment confidence is low (near neutral).")

            # STORE FOR CSV + LDA
            download_list.append({
                "name": details['name'],
                "cleaned_text": result["processed_text"],
                "sentiment": sentiment_result["sentiment"],
                "compound_score": sentiment_result["compound"]
            })
   
            # Validation: ensure data exists before summary
            if not download_list:
                st.warning("No data available for sentiment summary.")
                return

        #Download CSV
        df = pd.DataFrame(download_list)
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="💾 Download Cleaned Text CSV",
            data=csv,
            file_name="cleaned_output.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.success("✔ Analysis Completed sucessfully!")

        #LDA TOPIC MODELING
        st.markdown("## 🧠 Topic Modeling (LDA)")

        processed_texts = [
            item["cleaned_text"]
            for item in download_list
            if item.get("cleaned_text")
        ]

        if len(processed_texts) >= 2:

            lda_topics = lda_topic_model(processed_texts, num_topics=5)

            for topic in lda_topics:
                st.markdown(f"**{topic['topic']}**: {topic['words']}")

        else:
            st.warning("⚠ Upload at least 2 documents for topic modeling.")

        st.success("✔ Analysis completed successfully!")
        
         # === TOPIC + SENTIMENT SUMMARY ===
        st.markdown("## 🔗 Topic + Sentiment Summary")

        avg_sentiment = sum(
            item["compound_score"] for item in download_list
        ) / len(download_list)

        overall_sentiment = (
            "Positive 😊" if avg_sentiment >= 0.05 else
            "Negative 😠" if avg_sentiment <= -0.05 else
            "Neutral 😐"
        )

        st.markdown(
            f"<div class='reduce-card'>Overall Dataset Sentiment: <b>{overall_sentiment}</b></div>",
            unsafe_allow_html=True
        )

