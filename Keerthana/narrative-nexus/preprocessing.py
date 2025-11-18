import re  #py regular expression lib used to clean txt
import nltk #natural lang toolkit used for NLP tasks
from nltk.corpus import stopwords #list outthe common wprds
from nltk.stem import WordNetLemmatizer # convert words to their baseform

#Download resources 
nltk.download("punkt")   #tokenization
nltk.download("stopwords")  #stopword list
nltk.download("wordnet")  #lemmatization

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    #BEFORE CLEANING 
    before_text = text
    before_char_count = len(before_text)

    #PHASE 1 — Cleaning
    text = text.lower()                                     # Lowercase
    text = re.sub(r"[^a-z\s]", "", text)                    # Remove punctuation & special chars
    
    tokens = nltk.word_tokenize(text)                       # Tokenize
    tokens = [t for t in tokens if t not in stop_words]     # Remove stopwords

    # PHASE 2 — Normalization
    tokens = [lemmatizer.lemmatize(t) for t in tokens]      # Lemmatization(conv words to root form )

    # PHASE 3 — Final tokenization & output
    after_text = " ".join(tokens)
    after_char_count = len(after_text)

    # Return everything for analysis
    return {
        "before_text": before_text,
        "before_char_count": before_char_count,
        "after_text": after_text,
        "after_char_count": after_char_count,
        "tokens": tokens
    }

