from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from decisionTree2 import DecisionTree

data = datasets.load_breast_cancer()
x = data.data
y = data.target

x_train, x_test, y_train, y_test = train_test_split(
    x,y,test_size=0.2,random_state=1234)

clf = DecisionTree()
clf.fit(x_train,y_train)
predictions = clf.predict(x_test)

def accuracy(y_test, y_pred):
    accuracy = np.sum(y_test == y_pred) / len(y_test)
    return accuracy
acc = accuracy(y_test, predictions)
print("Accuracy:", acc)
