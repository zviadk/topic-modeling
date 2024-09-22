import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

# Load the CSV file
df = pd.read_csv('news_data_2024_January.csv')

# Initialize a SentenceTransformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = embedding_model.encode(df['full_text'].tolist(), show_progress_bar=True)

# Define a custom CountVectorizer to remove stopwords
vectorizer = CountVectorizer(stop_words='english')

# Fit and transform the text data using CountVectorizer
vectorized_text = vectorizer.fit_transform(df['full_text'])

# Create a BERTopic model with the custom vectorizer
model = BERTopic(vectorizer_model=vectorizer)

# Fit the BERTopic model using the embeddings
topics, _ = model.fit_transform(df['full_text'], embeddings=embeddings)

# Display the topics
for idx, topic in enumerate(model.get_topic_info().head(10).values):
    print(f"Topic {idx}: {topic}")

# Get topic information
topic_info = model.get_topic_info()

# Get the number of topics
num_topics = len(topic_info) - 1  # Subtract 1 to exclude the outlier topic
print(f"Number of topics: {num_topics}")
