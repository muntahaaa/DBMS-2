# Load transaction data from the text file
def load_transactions(filename):
    transactions = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            transaction_id = parts[0]
            items = parts[1:]
            transactions[transaction_id] = set(items)
    return transactions

# Get the support count for itemsets
def get_support_count(transactions, itemset):
    count = 0
    for items in transactions.values():
        if itemset.issubset(items):
            count += 1
    return count

# Generate candidates of k-itemsets
def generate_candidates(prev_frequent_itemsets, k):
    candidates = set()
    prev_items = list(prev_frequent_itemsets)
    for i in range(len(prev_items)):
        for j in range(i + 1, len(prev_items)):
            candidate = prev_items[i].union(prev_items[j])
            if len(candidate) == k:
                candidates.add(candidate)
    return candidates

# Apriori algorithm main function
def apriori(transactions, min_support):
    # Step 1: Generate 1-itemsets and filter based on min support
    items = set(item for trans in transactions.values() for item in trans)
    one_itemsets = [frozenset({item}) for item in items]

    
    frequent_itemsets = []
    k = 1
    current_frequent_itemsets = {frozenset(itemset) for itemset in one_itemsets if get_support_count(transactions, itemset) >= min_support}

    
    # Add initial frequent itemsets
    frequent_itemsets.append(current_frequent_itemsets)
    
    # Step 2: Generate k-itemsets for k > 1
    while current_frequent_itemsets:
        k += 1
        candidates = generate_candidates(current_frequent_itemsets, k)
        current_frequent_itemsets = {itemset for itemset in candidates if get_support_count(transactions, itemset) >= min_support}
        
        if current_frequent_itemsets:
            frequent_itemsets.append(current_frequent_itemsets)
    
    return frequent_itemsets

# Generate association rules from frequent itemsets
def generate_association_rules(frequent_itemsets, transactions, min_support):
    rules = []
    for k_itemsets in frequent_itemsets[1:]:  # Skip 1-itemsets
        for itemset in k_itemsets:
            for consequent in itemset:
                antecedent = itemset - {consequent}
                if antecedent:
                    support_antecedent = get_support_count(transactions, antecedent)
                    support_itemset = get_support_count(transactions, itemset)
                    
                    if support_antecedent > 0:
                        confidence = support_itemset / support_antecedent
                        rules.append((antecedent, consequent, confidence))
    return rules

# Main
if __name__ == "__main__":
    transactions = load_transactions("transactions.txt")
    min_support = 3
    
    # Step 1-5: Generate frequent itemsets using the Apriori algorithm
    frequent_itemsets = apriori(transactions, min_support)
    
    # Step 6: Generate association rules
    association_rules = generate_association_rules(frequent_itemsets, transactions, min_support)
    
    # Display results
    print("Frequent Itemsets:")
    for i, itemsets in enumerate(frequent_itemsets):
        print(f"{i+1}-itemsets:", itemsets)
    
    print("\nAssociation Rules:")
    for antecedent, consequent, confidence in association_rules:
        print(f"{set(antecedent)} -> {consequent}, confidence: {confidence:.2f}")
