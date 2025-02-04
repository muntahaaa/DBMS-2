import math

dataPoints = [[3, 4], [4, 5], [2, 1], [7, 8]]

class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class KDTree:
    def __init__(self):
        self.root = None

    def buildTree(self, dataPoints, height=0):
        if not dataPoints:
            return None

        k = len(dataPoints[0])  # Number of dimensions
        axis = height % k  # Determine axis to split

        # Sort points by the current axis
        dataPoints.sort(key=lambda x: x[axis])

        # Find the median index
        mid = len(dataPoints) // 2

        # Recursively build the tree
        return TreeNode(
            value=dataPoints[mid],
            left=self.buildTree(dataPoints[:mid], height + 1),
            right=self.buildTree(dataPoints[mid + 1:], height + 1)
        )

    def insert(self, root, point, height=0):
        if root is None:
            return TreeNode(point)

        k = len(point)
        axis = height % k

        # Go left or right depending on the axis comparison
        if point[axis] < root.value[axis]:
            root.left = self.insert(root.left, point, height + 1)
        else:
            root.right = self.insert(root.right, point, height + 1)

        return root

    def printTree(self, node, level=0):
        if node is not None:
            print("  " * level + f"Node: {node.value}")
            self.printTree(node.left, level + 1)
            self.printTree(node.right, level + 1)

    def distance(self, point1, point2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

    def nearestNeighbor(self, root, target, height=0, best=None):
        if root is None:
            return best

        if best is None or self.distance(target, root.value) < self.distance(target, best):
            best = root.value

        k = len(target)
        axis = height % k


        # Determine whether to go left or right
        if target[axis] < root.value[axis]:
            best = self.nearestNeighbor(root.left, target, height + 1, best)
            # Check the other side if necessary
            if abs(target[axis] - root.value[axis]) < self.distance(target, best):
                best = self.nearestNeighbor(root.right, target, height + 1, best)
        else:
            best = self.nearestNeighbor(root.right, target, height + 1, best)
            if abs(target[axis] - root.value[axis]) < self.distance(target, best):
                best = self.nearestNeighbor(root.left, target, height + 1, best)

        return best

# Create and build the KDTree
tree = KDTree()
tree.root = tree.buildTree(dataPoints)

# Print the tree structure
print("Initial KD-Tree:")
tree.printTree(tree.root)

# Insert a new point
new_point = [6, 3]
tree.root = tree.insert(tree.root, new_point)
print("\nKD-Tree After Insertion:")
tree.printTree(tree.root)

# Find the nearest neighbor
target_point = [5, 5]
nearest = tree.nearestNeighbor(tree.root, target_point)
print(f"\nNearest neighbor to {target_point} is {nearest}")
