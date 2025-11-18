from sklearn.feature_extraction.text import TfidfVectorizer #term ferquency-inverse document frequency
from sklearn.metrics.pairwise import cosine_similarity  #how similar/close the vectors are

def compute_cosine_similarity(text_list):
    """
    Accepts: list of processed text strings 
    Returns: cosine similarity matrix
    """                                         
    vectorizer = TfidfVectorizer()                  #obj will conv all text to numer vectors
    vectors = vectorizer.fit_transform(text_list)   #fit-learns vocabulary fron texts & transform-conv text to numer
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix            #print it , visualize it n use fr analysis
