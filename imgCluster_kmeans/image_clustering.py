import numpy as np
import matplotlib.pyplot as plt
import cv2
from imgKmeans import KMeans  # Import the custom KMeans class

# Read in the image
image = cv2.imread('rose.png')

# Change color to RGB (from BGR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image)
plt.title("Original Image")
plt.show()

# Reshaping the image into a 2D array of pixels and 3 color values (RGB)
pixel_vals = image.reshape((-1, 3))

# Convert to float type
pixel_vals = np.float32(pixel_vals)

# Number of clusters (K)
K = 5

# Apply custom KMeans
kmeans = KMeans(K=K, max_iters=100)
labels = kmeans.predict(pixel_vals)

# Plot the clusters
kmeans.plot()

# Convert data into 8-bit values
centers = np.uint8(kmeans.centroids)
segmented_data = centers[labels.astype(int)]

# Reshape data into the original image dimensions
segmented_image = segmented_data.reshape((image.shape))

# Display the clustered image
plt.imshow(segmented_image)
plt.title("Clustered Image")
plt.show()

# Save the clustered image
output_path = "clustered_imageKMean.jpg"
cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
print(f"Clustered image saved to: {output_path}")
