import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, ndcg_score, mean_squared_error
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from scipy.spatial.distance import cdist

# Step 1: Load and preprocess data
checkins_data = pd.read_csv(
    "/Users/artemmushynskyi/Documents/NUOP/algorithms-and-technologies-for-building-recommender-systems/module2/loc-gowalla_totalCheckins.txt",
    sep="\t", header=None,
    names=["user_id", "timestamp", "latitude", "longitude", "location_id"]
)

edges_data = pd.read_csv(
    "/Users/artemmushynskyi/Documents/NUOP/algorithms-and-technologies-for-building-recommender-systems/module2/loc-gowalla_edges.txt",
    sep="\t", header=None,
    names=["user_id_1", "user_id_2"]
)

# checkins_data = checkins_data.sample(frac=0.1, random_state=42)

# Extract unique locations and their coordinates
location_coords = checkins_data[['location_id', 'latitude', 'longitude']].drop_duplicates()

# Step 2: Content-based recommendations
def content_based_recommendations(location_id, num_recommendations=5):
    """Recommend locations based on geographic proximity."""
    target_location = location_coords[location_coords['location_id'] == location_id]
    if target_location.empty:
        return []
    distances = cdist(location_coords[['latitude', 'longitude']],
                      target_location[['latitude', 'longitude']], metric='euclidean')
    location_coords['distance'] = distances
    similar_locations = location_coords.sort_values(by='distance').head(num_recommendations)
    return similar_locations['location_id'].tolist()

# Step 3: Collaborative filtering
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(checkins_data[['user_id', 'location_id']].assign(interaction=1), reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Train the SVD model
svd_model = SVD(n_factors=20, random_state=42)
svd_model.fit(trainset)

def collaborative_recommendations(user_id, num_recommendations=5):
    """Recommend locations using collaborative filtering."""
    unique_locations = checkins_data['location_id'].unique()
    predictions = [svd_model.predict(user_id, loc) for loc in unique_locations]
    predictions.sort(key=lambda x: x.est, reverse=True)
    return [pred.iid for pred in predictions[:num_recommendations]]

# Step 4: Hybrid recommendations
def hybrid_recommendations(user_id, location_id=None, num_recommendations=5):
    """Combine content-based and collaborative filtering recommendations."""
    collaborative = collaborative_recommendations(user_id, num_recommendations)
    content_based = content_based_recommendations(location_id, num_recommendations) if location_id else []
    return list(set(collaborative + content_based))[:num_recommendations]

# Step 5: Evaluation of recommendations
def evaluate_recommendations():
    """Evaluate recommendation quality using metrics."""
    true_labels = []
    predicted_labels = []
    for user_id in checkins_data['user_id'].unique():
        true_locations = checkins_data[checkins_data['user_id'] == user_id]['location_id'].values
        recommendations = hybrid_recommendations(user_id, num_recommendations=5)
        true_labels.append([1 if loc in true_locations else 0 for loc in recommendations])
        predicted_labels.append([1] * len(recommendations))  # Assume all recommendations are relevant

    # Compute evaluation metrics
    precision = precision_score(true_labels, predicted_labels, average='macro', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='macro', zero_division=0)
    ndcg = ndcg_score(true_labels, predicted_labels)
    rmse = np.sqrt(mean_squared_error(true_labels, predicted_labels))

    # Print metrics
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"NDCG: {ndcg}")
    print(f"RMSE: {rmse}")

# Example: Run evaluation
evaluate_recommendations()
