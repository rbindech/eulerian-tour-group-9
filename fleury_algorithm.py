def run_fleury():
    # choose input.txt or terminal (CSES)
    try:
        source = open("input.txt", "r")
    except FileNotFoundError:
        source = open(0)

    def read_line():
        line = source.readline()
        if not line:
            return None
        return line.strip()

    # Read the number of nodes n and edges m
    first_line = read_line()
    if not first_line:
        exit()

    parts = first_line.split()
    n = int(parts[0])
    m = int(parts[1])

    # Initialize adjacency list with simple empty lists
    adj = []
    for i in range(n + 1):
        adj.append([])

    # Read each edge and add to adjacency list
    for i in range(m):
        edge_data = read_line().split()
        u = int(edge_data[0])
        v = int(edge_data[1])
        adj[u].append(v)
        adj[v].append(u)

    # Check Eulerian condition: all degrees must be even
    for i in range(1, n + 1):
        if len(adj[i]) % 2 != 0:
            print("IMPOSSIBLE")
            exit()

    # Function to count how many nodes can be reached from a starting node
    def count_reachable(start_node):
        # Initialize visited list with False for every node
        visited = []
        for i in range(n + 1):
            visited.append(False)

        visited[start_node] = True
        queue = [start_node]
        count = 1

        while len(queue) > 0:
            current = queue.pop(0)
            for neighbor in adj[current]:
                if visited[neighbor] == False:
                    visited[neighbor] = True
                    count = count + 1
                    queue.append(neighbor)

        return count

    # Check if the edge (u, v) is a bridge
    def is_bridge(u, v):
        # If there is only one edge left from u, we have no choice
        if len(adj[u]) == 1:
            return False

        # Count reachable nodes before removing the edge
        count_before = count_reachable(u)

        # Temporarily remove the edge
        adj[u].remove(v)
        adj[v].remove(u)

        # Count reachable nodes after removing the edge
        count_after = count_reachable(u)

        # Put the edge back
        adj[u].append(v)
        adj[v].append(u)

        # If the reachable count drops it means this edge was a bridge
        if count_before > count_after:
            return True
        else:
            return False

    #Algorithm
    curr_node = 1
    path = [curr_node]

    for step in range(m):
        # If the current node has no edges left before finishing all m edges
        if len(adj[curr_node]) == 0:
            print("IMPOSSIBLE")
            exit()

        chosen_neighbor = None

        # Try to find a neighbor connected by a non-bridge edge
        for neighbor in adj[curr_node]:
            if is_bridge(curr_node, neighbor) == False:
                chosen_neighbor = neighbor
                break

        # If all available edges are bridges pick the first one
        if chosen_neighbor is None:
            chosen_neighbor = adj[curr_node][0]

        # Move along the edge and delete it
        adj[curr_node].remove(chosen_neighbor)
        adj[chosen_neighbor].remove(curr_node)

        curr_node = chosen_neighbor
        path.append(curr_node)

    # Final check
    if curr_node == 1 and len(path) == m + 1:
        output = ""
        for node in path:
            output = output + str(node) + " "
        print("--- Fleury's algorithm ---")
        print("Eulerian circuit:")
        print(output.strip())
    else:
        print("IMPOSSIBLE")
