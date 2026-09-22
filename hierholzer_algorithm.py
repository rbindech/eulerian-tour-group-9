import sys 
 
def run_hierholzer():
    # Read all tokens from standard input
    try:
        with open("input.txt", "r") as f:
            input_data = f.read().split()
    except FileNotFoundError:
        # Fallback si le fichier n'existe pas (ex: sur la plateforme de test CSES)
        input_data = sys.stdin.read().split()

    if not input_data:
        return
    #makes the data into int
    it = iter(map(int, input_data))
    
    n = next(it)  # nodes
    m = next(it)  # edges
    
    # Adjacency list storing (neighbor, edge_id)
    adj = [[] for _ in range(n + 1)]
    degree = [0] * (n + 1)
    
    for edge_id in range(m):
        u = next(it)
        v = next(it)
        adj[u].append((v, edge_id))
        adj[v].append((u, edge_id))
        degree[u] += 1
        degree[v] += 1

    
    # If any vertex has an odd degree, a closed tour is impossible.
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            print("IMPOSSIBLE")
            return

    start_node = 1
    

    used_edge = [False] * m   # list of edges visited
    curr_path = [start_node]  # Execution stack
    circuit = []              # Final result 

    # Hierholzer's Algorithm
    while curr_path:
        u = curr_path[-1] 
        
        # Pop edges that have already been traversed from another direction before
        while adj[u] and used_edge[adj[u][-1][1]]:
            adj[u].pop()
            
        if adj[u]:
            # Traverse to the next node via an unvisited edge
            v, edge_id = adj[u].pop()
            used_edge[edge_id] = True
            curr_path.append(v)
        else:
            # if the node hasn't new neighbors left add vertex to the final circuit
            circuit.append(curr_path.pop())

    
    # Check if every edges have been added
    if len(circuit) - 1 != m:
        print("IMPOSSIBLE")
        return

    # The circuit was constructed backwards so we reverse  it to get the correct path
    eulerian_circuit = circuit[::-1]
    
    print("--- Hierholzer's algorithm ---")
    print("Eulerian circuit:")
    print(*eulerian_circuit)


