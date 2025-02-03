import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from kmeans import KMeans


if __name__ == "__main__":
   

    X, y = make_blobs(
        centers=3, n_samples=1000, n_features=2, shuffle=True, random_state=40
    )
    print(f"Number of samples: {X.shape[0]}, Number of features: {X.shape[1]}")

    clusters = len(np.unique(y))
    print("Number of clusters: ",clusters)

    k = KMeans(K=clusters, max_iters=150, plot_steps=True)
    y_pred = k.predict(X)

    k.plot()