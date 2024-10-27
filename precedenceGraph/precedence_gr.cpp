#include <bits/stdc++.h>
using namespace std;

class PrecedenceGraph {
private:
    int numtransactions;
    vector<vector<bool>> adjMat;

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

struct Action {
    int transactionId;
    char operation;
    char variable;

    Action(int tId, char op, char var) : transactionId(tId), operation(op), variable(var) {}
};

int main() {
   
    ifstream inputFile("random.txt");
    if (!inputFile) {
        cerr << "Error opening input file." << endl;
        return 1;
    }

    vector<vector<string>> schedule;
    string line;
    while (getline(inputFile, line)) {
        vector<string> transaction;
        size_t position = 0;
        string token;
        while ((position = line.find(',')) != string::npos) {
            token = line.substr(0, position);
            transaction.push_back(token);
            line.erase(0, position + 1);
        }
        transaction.push_back(line);
        schedule.push_back(transaction);
    }
    inputFile.close();

    vector<Action> SetOfActions;
    int numTransactions = schedule.size();
    int timeSteps = schedule[0].size();


    for (int j = 1; j < timeSteps; ++j) {
        for (int i = 0; i < numTransactions; ++i) {
            if (j >= schedule[i].size()) continue;

            string action = schedule[i][j];
            if (action != "-" && action != "COM") {
                char operation = action[0];
                char variable = action[2];
                int transactionID = i + 1;

                SetOfActions.push_back(Action(transactionID, operation, variable));
            }
        }
    }

    PrecedenceGraph graph(numTransactions);

    
    for (int i = 0; i < SetOfActions.size(); ++i) {
        for (int j = i + 1; j < SetOfActions.size(); ++j) {
            int id1 = SetOfActions[i].transactionId - 1;
            int id2 = SetOfActions[j].transactionId - 1;
            char op1 = SetOfActions[i].operation;
            char op2 = SetOfActions[j].operation;
            char item1 = SetOfActions[i].variable;
            char item2 = SetOfActions[j].variable;

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
