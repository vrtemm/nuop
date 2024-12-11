# Importing necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
import string

# Download stopwords
nltk.download('stopwords')

# Step 1: Load the dataset
print("Step 1: Loading the dataset...")
# Replace 'spam.csv' with the path to your dataset
data = pd.read_csv('/Users/artemmushynskyi/Documents/NUOP/big-data-processing-technologies/module2/spam.csv', encoding='latin-1')

# Keeping only the necessary columns
data = data[['v1', 'v2']]
data.columns = ['label', 'message']

# Checking for missing values
if data.isnull().sum().any():
    print("Warning: Dataset contains missing values. Handling them...")
    data.dropna(inplace=True)

# Mapping labels to binary values
data['label'] = data['label'].map({'ham': 0, 'spam': 1})
print("Dataset loaded successfully.")

# Step 2: Text preprocessing
print("Step 2: Preprocessing the text...")
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = ''.join([char for char in text if not char.isdigit()])
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    return ' '.join(words)

data['message'] = data['message'].apply(preprocess_text)
print("Text preprocessing completed.")

# Step 3: Feature extraction
print("Step 3: Extracting features...")
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['message'])
y = data['label']
print("Feature extraction completed.")

# Step 4: Splitting the dataset
print("Step 4: Splitting the dataset...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("Dataset split into training and testing sets.")

# Step 5: Training the Naive Bayes classifier
print("Step 5: Training the Naive Bayes classifier...")
model = MultinomialNB()
model.fit(X_train, y_train)
print("Model training completed.")

# Step 6: Making predictions
print("Step 6: Making predictions...")
y_pred = model.predict(X_test)

# Step 7: Evaluating the model
print("Step 7: Evaluating the model...")
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print("\nClassification Report:\n", report)

# Save results to a file
with open("classification_report.txt", "w") as file:
    file.write(f"Accuracy: {accuracy}\n\n")
    file.write(f"Classification Report:\n{report}\n")
print("Results saved to 'classification_report.txt'.")

# Step 8: Test on custom messages
print("Step 8: Testing on custom messages...")
custom_messages = ["Congratulations! You've won a free ticket to Bahamas.", 
                   "Hey, are we meeting for lunch today?"]
custom_preprocessed = [preprocess_text(msg) for msg in custom_messages]
custom_vectors = vectorizer.transform(custom_preprocessed)
predictions = model.predict(custom_vectors)
for msg, pred in zip(custom_messages, predictions):
    print(f"Message: '{msg}' => Prediction: {'Spam' if pred == 1 else 'Not Spam'}")

# Optional: Interactive testing
while True:
    user_message = input("\nEnter a message to classify (or 'exit' to quit): ")
    if user_message.lower() == 'exit':
        break
    user_preprocessed = preprocess_text(user_message)
    user_vector = vectorizer.transform([user_preprocessed])
    user_prediction = model.predict(user_vector)
    print(f"Message: '{user_message}' => Prediction: {'Spam' if user_prediction[0] == 1 else 'Not Spam'}")
