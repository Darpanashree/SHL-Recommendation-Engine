import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and prepare data
df = pd.read_csv("app\data\shl_products.csv")
df["combined"] = df["combined"].fillna("").astype(str)

# Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["combined"])

# Recommendation function
def recommend_assessments(query, top_n=5):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    indices = similarity.argsort()[-top_n:][::-1]
    return df.iloc[indices]["combined"].tolist()
