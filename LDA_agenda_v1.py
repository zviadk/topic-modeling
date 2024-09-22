import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk

# Load the CSV file
df = pd.read_csv('news_data_2024_January.csv')

# Preprocess the text
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Remove stop words and punctuation, and tokenize
    tokens = [word for word in text.lower().split() if word.isalpha() and word not in stop_words]
    return ' '.join(tokens)

df['cleaned_text'] = df['full_text'].apply(preprocess)

# Vectorize the text
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['cleaned_text'])

# Apply LDA
lda = LatentDirichletAllocation(n_components=7, random_state=42)
lda.fit(X)

# Display the topics
for idx, topic in enumerate(lda.components_):
    print(f"Topic {idx}:")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])
