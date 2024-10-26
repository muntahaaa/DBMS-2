#include <bits/stdc++.h>
using namespace std;

class PrecedenceGraph {
private:
    int numtransactions;
    vector<vector<bool>> adjMat;
    unordered_map<int, set<int>> conflictOperation;

    bool isCyclic() {
        vector<int> inDegree(numtransactions, 0);

        for (int i = 0; i < numtransactions; ++i) {
            for (int j = 0; j < numtransactions; ++j) {
                if (adjMat[i][j]) {
                    inDegree[j]++;
                }
            }
        }
        queue<int> q;
        for (int i = 0; i < numtransactions; ++i) {
            if (inDegree[i] == 0) {
                q.push(i);
            }
        }
        int count = 0;

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            count++;

            for (int i = 0; i < numtransactions; ++i) {
                if (adjMat[node][i]) {
                    inDegree[i]--;
                    if (inDegree[i] == 0) {
                        q.push(i);
                    }
                }
            }
        }
        return count != numtransactions;
    }

public:
    PrecedenceGraph(int n) : numtransactions(n) {
        adjMat = vector<vector<bool>>(n, vector<bool>(n, false));
    }

    void addEdge(int from, int to) {
        adjMat[from][to] = true;
    }

    void printGraph() {
        cout << "Adjacency matrix of precedence graph:\n";
        for (int i = 0; i < numtransactions; ++i) {
            for (int j = 0; j < numtransactions; ++j) {
                cout << adjMat[i][j] << " ";
            }
            cout << "\n";
        }
    }

    bool isSerializable() {
        return !isCyclic();
    }
};

int main() {
    string filename = "schedule.txt";
    int numTransactions;
    int numOperations;
    
    ifstream inputFile(filename);
    if (!inputFile) {
        cerr << "Error opening file\n";
        return 1;
    }
    
   
    inputFile >> numTransactions >> numOperations;

  
    vector<tuple<int, char, char>> schedule(numOperations);
    PrecedenceGraph graph(numTransactions);

  
    for (int i = 0; i < numOperations; ++i) {
        int transactionID;
        char operation, item;
        inputFile >> transactionID >> operation >> item;
        schedule[i] = make_tuple(transactionID - 1, operation, item);
    }
    inputFile.close();

  
    for (int i = 0; i < numOperations; ++i) {
        for (int j = i + 1; j < numOperations; ++j) {
            int id1 = get<0>(schedule[i]);
            int id2 = get<0>(schedule[j]);
            char op1 = get<1>(schedule[i]);
            char op2 = get<1>(schedule[j]);
            char item1 = get<2>(schedule[i]);
            char item2 = get<2>(schedule[j]);

            if (id1 != id2 && item1 == item2 &&
                (op1 == 'R' && op2 == 'W' || op1 == 'W' && op2 == 'W' || op1 == 'W' && op2 == 'R')) {
                graph.addEdge(id1, id2);
            }
        }
    }

   
    graph.printGraph();
    if (graph.isSerializable()) {
        cout << "The transaction is conflict serializable.\n";
    } else {
        cout << "The transaction is not conflict serializable.\n";
    }

    return 0;
}
