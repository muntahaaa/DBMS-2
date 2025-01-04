import numpy as np
from decisionTree2 import DecisionTree
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the Iris dataset
data = load_iris()
X, y = data.data, data.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Create and train the decision tree
tree = DecisionTree(max_depth=10, min_samples_split=2)
tree.fit(X_train, y_train)

# Make predictions on the test set
y_pred = tree.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Example of making a single prediction
sample = X_test[0]
print(f"Predicted label: {tree.predict([sample])[0]}")
print(f"Actual label: {y_test[0]}")
