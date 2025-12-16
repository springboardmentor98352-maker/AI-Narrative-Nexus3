from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def lda_topic_model(texts, num_topics=5, num_words=10):
    """
    LDA Topic Modeling
    """

    doc_count = len(texts)

    vectorizer = CountVectorizer(
        stop_words="english",
        max_df=0.95,
        min_df=1 if doc_count < 5 else 2
    )

    doc_term_matrix = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=min(num_topics, doc_count),
        random_state=42
    )

    lda.fit(doc_term_matrix)

    feature_names = vectorizer.get_feature_names_out()
    topics = []

    for idx, topic in enumerate(lda.components_):
        top_words = [
            feature_names[i]
            for i in topic.argsort()[-num_words:]
        ]
        topics.append({
            "topic": f"Topic {idx + 1}",
            "words": ", ".join(top_words)
        })

    return topics
