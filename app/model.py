import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and prepare data
try:
    data_path = os.path.join("app", "data", "shl_products.csv")
    df = pd.read_csv(data_path)
    df["combined"] = df["combined"].fillna("").astype(str)
except FileNotFoundError:
    raise FileNotFoundError(f"Data file not found at {data_path}. Please check the file path.")
except Exception as e:
    raise Exception(f"An error occurred while loading the data: {str(e)}")

# Vectorization
try:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["combined"])
except Exception as e:
    raise Exception(f"An error occurred during vectorization: {str(e)}")

# Recommendation function
def recommend_assessments(query, top_n=5):
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    
    try:
        query_vec = vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
        if similarity.max() == 0:
            return []  # No similar items found
        indices = similarity.argsort()[-top_n:][::-1]
        return df.iloc[indices]["combined"].tolist()
    except Exception as e:
        raise Exception(f"An error occurred during recommendation: {str(e)}")
