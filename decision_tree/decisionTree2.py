import numpy as np
from collections import Counter 
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *,value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value=value
    
    def is_leaf_node(self):
        return self.value is not None



class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features= n_features
        self.root = None

    def fit(self,x,y):
        self.n_features = x.shape[1] if not self.n_features else min(x.shape[1], self.n_features)
        self.root = self._grow_tree(x,y, depth=0)

    def _grow_tree(self,x,y,depth): 
        n_samples, n_feats = x.shape
        n_labels = len(np.unique(y))

        #check the stopping criteria
        if(depth>= self.max_depth or n_labels==1 or n_samples< self.min_samples_split):
            leaf_value = self.most_common_label(y)
            return Node(value=leaf_value)
        feat_idxs= np.random.choice(n_feats, self.n_features, replace=False)
        
        #find the best split
        best_feature, best_threshold= self._best_split(x,y,feat_idxs)

        #create child nodes  
        left_idx, right_idx = self._split(x[:,best_feature],best_threshold)
        left = self._grow_tree(x[left_idx, :],y[left_idx],depth+1)
        right = self._grow_tree(x[right_idx, :],y[right_idx],depth+1)

        return Node(best_feature,best_threshold,left,right)
    
    def _best_split(self,x,y,feat_idxs):
        best_gain = -1
        split_idx, split_threshold = None, None 

        for feat_idx in feat_idxs:
            x_column = x[:, feat_idx]
            thresholds= np.unique(x_column)

            for thr in thresholds:
                gain = self._information_gain(y,x_column,thr)

                if gain > best_gain:
                    best_gain=gain
                    split_idx= feat_idx
                    split_threshold= thr
        
        return split_idx, split_threshold            
    
    def _information_gain(self,y,x_column,split_threshold):
        #parent entropy
        parent_entropy = self._entropy(y)
    
        #create children 
        left_idx, right_idx = self._split(x_column,split_threshold)

        if len(left_idx)==0 or len(right_idx)==0:
            return 0



        #calc weighted entropy of children
        n = len(y)
        n_left_idx, n_right_idx = len(left_idx), len(right_idx)
        entropy_left_idx , entropy_right_idx = self._entropy(y[left_idx]), self._entropy(y[right_idx])
        child_entropy = (n_left_idx/n)*entropy_left_idx + (n_right_idx/n)*entropy_right_idx


        #information gain IG
        ig = parent_entropy - child_entropy
        return ig

    def _split(self,x_column,split_threshold):
        left_idx = np.argwhere(x_column <= split_threshold).flatten()
        right_idx = np.argwhere(x_column > split_threshold).flatten()
        return left_idx, right_idx

    def _entropy(self,y):
        # counter = Counter(y)
        # entropy = 0
        # for label in counter:
        #     p = counter[label]/len(y)
        #     entropy += -p*np.log2(p)
        # return entropy
        histogram = np.bincount(y)
        ps = histogram / len(y)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def most_common_label(self,y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value

    def predict(self, x):
        return np.array([self._traverse_tree(xi, self.root) for xi in x])
     
    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right) 
