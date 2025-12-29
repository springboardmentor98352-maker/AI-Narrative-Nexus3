import streamlit as st
import pandas as pd
import io

from preprocess import (
    get_word_count,
    preprocess_text,
    preprocess_text_with_fallback,
    extract_text_from_uploaded_file,
    get_top_keywords
)

from topic_modeling import (
    split_into_documents,
    train_topic_model,
    get_topic_words
)

from sentiment_summary import (
    analyze_sentiments,
    extractive_summary
)

from reporting import (
    make_wordcloud_image,
    generate_insights_text,
    make_pdf_bytes
)

st.set_page_config(page_title="Mind Mesh Analyst", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<h1 class="app-title">Mind Mesh Analyst</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-caption">Topics · Sentiment · Summary · Insights</p>', unsafe_allow_html=True)

if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "processed_text" not in st.session_state:
    st.session_state.processed_text = ""

#Input 
st.subheader("📁 Data Import")
method = st.radio("Input Method", ["File", "Paste Text"], horizontal=True)

if method == "File":
    file = st.file_uploader("Upload file", type=["txt", "csv", "pdf", "docx"])
    if file:
        st.session_state.raw_text = extract_text_from_uploaded_file(file)
else:
    txt = st.text_area("Paste text here", height=250)
    if txt:
        st.session_state.raw_text = txt

#Raw Preview
if st.session_state.raw_text:
    st.markdown("### Raw Preview")
    st.code(st.session_state.raw_text[:800])
    st.write("Word Count:", get_word_count(st.session_state.raw_text))

#Preprocessing
if st.button("⚡ Start Pre-processing"):
    processed = preprocess_text(st.session_state.raw_text)
    if not processed.strip():
        processed = preprocess_text_with_fallback(st.session_state.raw_text)
    st.session_state.processed_text = processed
    st.success("Preprocessing completed")

# Analysis 
if st.session_state.processed_text:
    st.subheader("📊 Analysis Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Original Words", get_word_count(st.session_state.raw_text))
    col2.metric("Processed Words", get_word_count(st.session_state.processed_text))

    algo = st.selectbox("Topic Algorithm", ["LDA", "NMF"])
    n_topics = st.slider("Number of Topics", 2, 10, 5)

    if st.button("🔍 Run Analysis"):
        docs = split_into_documents(st.session_state.processed_text)

        model, vectorizer, dtm, features = train_topic_model(
            docs, algorithm=algo, n_topics=n_topics
        )

        # Topics 
        topics_df = get_topic_words(model, features)
        st.subheader("🧠 Topics")
        st.dataframe(topics_df)

        # Sentiment 
        st.subheader("😊 Sentiment Analysis")
        sent_df = analyze_sentiments(docs)
        st.dataframe(sent_df)

        # Summary 
        st.subheader("📝 Summary")
        summary = extractive_summary(st.session_state.raw_text)
        st.write(summary)

        # Keywords 
        st.subheader("🔑 Top Keywords")
        kw_df = get_top_keywords(st.session_state.processed_text)
        st.dataframe(kw_df)

        # Word Cloud 
        st.subheader("☁ Word Cloud")
        wc = make_wordcloud_image(st.session_state.processed_text.split())
        st.image(wc)

        # Insights 
        insights = generate_insights_text(
            get_word_count(st.session_state.raw_text),
            get_word_count(st.session_state.processed_text),
            topics_df,
            sent_df["compound"].mean(),
            summary
        )

        # Downloads 
        st.subheader("📥 Download Reports")

        st.download_button(
            label="📄 Download Insights (TXT)",
            data=insights.encode("utf-8"),
            file_name="insights.txt",
            mime="text/plain"
        )

        insights_csv = pd.DataFrame({
            "Metric": [
                "Original Word Count",
                "Processed Word Count",
                "Average Sentiment",
                "Summary"
            ],
            "Value": [
                get_word_count(st.session_state.raw_text),
                get_word_count(st.session_state.processed_text),
                sent_df["compound"].mean(),
                summary
            ]
        })

        st.download_button(
            label="📊 Download Insights (CSV)",
            data=insights_csv.to_csv(index=False).encode("utf-8"),
            file_name="insights.csv",
            mime="text/csv"

        )
