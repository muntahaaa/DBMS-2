import numpy as np
from decisionTree3 import DecisionTree
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# Load dataset
data = load_iris()
X, y = data.data, data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Train and test with Gini index
tree_gini = DecisionTree(criterion="gini", max_depth=10)
tree_gini.fit(X_train, y_train)
y_pred_gini = tree_gini.predict(X_test)
accuracy_gini = accuracy_score(y_test, y_pred_gini)
print(f"Gini Accuracy: {accuracy_gini:.2f}")

# Train and test with Entropy
tree_entropy = DecisionTree(criterion="entropy", max_depth=10)
tree_entropy.fit(X_train, y_train)
y_pred_entropy = tree_entropy.predict(X_test)
accuracy_entropy = accuracy_score(y_test, y_pred_entropy)
print(f"Entropy Accuracy: {accuracy_entropy:.2f}")
