def parse_log(file_path):
    log = []
    with open(file_path, 'r') as file:
        for line in file:
            log.append(line.strip())
    return log

def analyze_log(log):
    committed = set()
    active_transactions = set()
    redo_transactions = set()
    undo_transactions = set()
    elements = {}
    checkpoint_found = False
    last_checkpoint_index = -1

    for i, entry in enumerate(log):
        if entry.startswith('<START'):
            transaction = entry.split(' ')[1].strip('>')
            active_transactions.add(transaction)

        elif entry.startswith('<COMMIT'):
            transaction = entry.split(' ')[1].strip('>')
            committed.add(transaction)
            if transaction in active_transactions:
                active_transactions.remove(transaction)

        elif entry.startswith('<CKPT'):
            checkpoint_found = True
            last_checkpoint_index = i
            checkpoint_transactions = set(entry[entry.index('(')+1:entry.index(')')].split(','))

        elif '<T' in entry and '>' in entry:
            parts = entry.strip('<>').split(' ')
            transaction, element, old_value, new_value = parts[0], parts[1], parts[2], parts[3]
            if transaction not in elements:
                elements[transaction] = []
            elements[transaction].append((element, old_value, new_value))

    if checkpoint_found:
        for i in range(last_checkpoint_index + 1, len(log)):
            entry = log[i]
            if entry.startswith('<COMMIT'):
                transaction = entry.split(' ')[1].strip('>')
                redo_transactions.add(transaction)

        undo_transactions = active_transactions - committed
    else:
        redo_transactions = committed
        undo_transactions = active_transactions - committed

    return redo_transactions, undo_transactions, elements

def perform_recovery(redo_transactions, undo_transactions, elements):
    redo = {}
    undo = {}

    for transaction in undo_transactions:
        if transaction in elements:
            for update in elements[transaction]:
                element, old_value, new_value = update
                undo[element] = old_value

    for transaction in redo_transactions:
        if transaction in elements:
            for update in elements[transaction]:
                element, old_value, new_value = update
                redo[element] = new_value

   

    return redo, undo

def main():
    log_file = 'log.txt'
    log = parse_log(log_file)
    
    redo_transactions, undo_transactions, elements = analyze_log(log)
    
    redo, undo = perform_recovery(redo_transactions, undo_transactions, elements)
    
    print("Redo Transactions:", redo_transactions)
    print("Undo Transactions:", undo_transactions)
    
    print("\nRedo Phase:")
    for element, value in redo.items():
        print(f"{element} = {value}")
    
    print("\nUndo Phase:")
    for element, value in undo.items():
        print(f"{element} = {value}")

if __name__ == "__main__":
    main()
