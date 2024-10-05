def transaction(file_path):
    with open(file_path,'r') as log_file:
        log_entries= log_file.readlines()
    committed=set()
    active=set()
    redo=set()
    undo=set()
    activeCKPT=set()

    checkPoint_found= False
    after_checkPoint=False

    for entry in log_entries:
        entry=entry.strip()

        if entry.startswith("<START"):
            transaction_id= entry.split()[1].strip(">")
            active.add(transaction_id) 
         
        elif entry.startswith("<COMMIT"):
            transaction_id= entry.split()[1].strip(">")
            committed.add(transaction_id) 
            active.discard(transaction_id)
            if checkPoint_found:
                redo.add(transaction_id)
        
        
        elif entry.startswith("<CKPT"):
            checkPoint_found=True
            activeCKPT= entry.split("(")[1].split((")"))[0].split(",")    
            active = set([tx.strip() for tx in activeCKPT])
        
        elif entry.startswith("<END CKPT"):
            after_checkPoint=True    
    
    undo = active.difference(committed)
    
  
    return redo,undo

def getValue(undo,redo,getValue):
     
     with open(file_path,'r') as log_file:
        log_entries= log_file.readlines()
        
        for entry in log_entries:
            if getValue in entry:
               
                entry_parts = entry.strip("<>").split()
                transaction_id = entry_parts[0].strip("<")
               
                if transaction_id not in undo:
                    value= entry_parts[3].strip(">")
                    
                    return value
                    
                else: 
                    value=entry_parts[2] 
                    return value 
             


file_path= "undo_redo.txt"
redo,undo=transaction(file_path)
with open("result.txt", "w") as file:
    file.write("Undo the transactions: " + str(undo) + "\n")
    file.write("Redo the transactions: " + str(redo) + "\n")
    file.write("Value of A: " + str(getValue(undo, redo, " A ")) + "\n")
    file.write("Value of B: " + str(getValue(undo, redo, " B ")) + "\n")
    file.write("Value of C: " + str(getValue(undo, redo, " C ")) + "\n")
    file.write("Value of D: " + str(getValue(undo, redo, " D ")) + "\n")

print("Result has been written in result.txt")
