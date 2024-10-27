import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load and preprocess data
click_data = pd.read_csv('/Users/artemmushynskyi/Documents/NUOP/algorithms-and-technologies-for-building-recommender-systems/module1/clicks_sample.csv')[['user_id', 'click_article_id']].drop_duplicates()
articles_metadata = pd.read_csv('/Users/artemmushynskyi/Documents/NUOP/algorithms-and-technologies-for-building-recommender-systems/module1/articles_metadata.csv')[['article_id', 'category_id', 'words_count']]

# Create user-item matrix
user_article_matrix = click_data.pivot_table(index='user_id', columns='click_article_id', aggfunc='size', fill_value=0)

# Calculate cosine similarity between articles
article_similarity = cosine_similarity(user_article_matrix.T)

# Function to get recommendations
def recommend_articles(article_idx, num_recommendations=5):
    similar_indices = np.argsort(-article_similarity[article_idx])[1:num_recommendations+1]
    return articles_metadata.iloc[similar_indices][['article_id', 'category_id', 'words_count']]

# Example: Recommend articles similar to a specific article
print(recommend_articles(0))
