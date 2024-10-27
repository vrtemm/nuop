# Importing necessary libraries
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: Load the dataset
data = pd.read_csv('/Users/artemmushynskyi/Documents/NUOP/big-data-processing-technologies/module1/AAPL.csv')

# Selecting relevant columns for regression
# We use 'open', 'high', 'low', 'volume' as features to predict 'close'
data = data[['open', 'high', 'low', 'volume', 'close']]

# Check for missing values and remove any if present
data.dropna(inplace=True)

# Split data into features (X) and target (y)
X = data[['open', 'high', 'low', 'volume']]
y = data['close']

# Step 2: Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 3: Creating and training the regression model
# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict values on the test set
y_pred = model.predict(X_test)

# Step 4: Evaluating model performance with Mean Squared Error and R-squared
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R²): {r2}")

# Step 5: Plot actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel('Actual Close Prices')
plt.ylabel('Predicted Close Prices')
plt.title('Comparison of Actual vs Predicted Close Prices')
plt.show()
