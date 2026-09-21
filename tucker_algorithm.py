"""Tucker's algorithm for an undirected Eulerian circuit.

The first element of ``nodes`` is considered the starting vertex.
"""

from graph_network import nodes, edges


class DisjointSet:
    """Track which initial circuits have already been merged."""

    def __init__(self, count):
        self.parent = list(range(count))
        self.size = [1] * count

    def find(self, item):
        """Return the representative of the set containing ``item``."""

        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, first, second):
        """Merge two sets and return True only if they were different."""

        first_root = self.find(first)
        second_root = self.find(second)

        if first_root == second_root:
            return False

        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root

        self.parent[second_root] = first_root
        self.size[first_root] += self.size[second_root]
        return True


def build_tucker_circuit(number_of_nodes, indexed_edges):
    """Build a circuit on a zero-based graph, or return None.

    Tucker's algorithm first pairs the incident edges at every vertex. These
    pairings split the graph into edge-disjoint circuits. Circuits that meet at
    the same original vertex are then merged by crossing two local pairs.
    """

    number_of_edges = len(indexed_edges)
    adjacency = [[] for _ in range(number_of_nodes)]

    # An undirected edge e is represented by two half-edges:
    #   2*e     leaves its first endpoint;
    #   2*e + 1 leaves its second endpoint.
    # The opposite half-edge is always obtained with h ^ 1.
    destination = [0] * (2 * number_of_edges)

    for edge_id, (first, second) in enumerate(indexed_edges):
        first_half = 2 * edge_id
        second_half = first_half + 1

        adjacency[first].append(first_half)
        adjacency[second].append(second_half)
        destination[first_half] = second
        destination[second_half] = first

    # A closed Eulerian circuit requires an even degree at every vertex.
    if any(len(incident_edges) % 2 != 0 for incident_edges in adjacency):
        return None

    # Every edge must be reachable from the starting vertex (index 0).
    reachable = [False] * number_of_nodes
    reachable[0] = True
    stack = [0]

    while stack:
        current_node = stack.pop()

        for half_edge in adjacency[current_node]:
            neighbour = destination[half_edge]

            if not reachable[neighbour]:
                reachable[neighbour] = True
                stack.append(neighbour)

    if any(
        adjacency[node] and not reachable[node]
        for node in range(number_of_nodes)
    ):
        return None

    # With no edge, the starting vertex itself is the trivial circuit.
    if number_of_edges == 0:
        return [0]

    # partner[h] gives the half-edge paired with h at the same vertex.
    partner = [-1] * (2 * number_of_edges)

    for incident_edges in adjacency:
        for index in range(0, len(incident_edges), 2):
            first_half = incident_edges[index]
            second_half = incident_edges[index + 1]

            partner[first_half] = second_half
            partner[second_half] = first_half

    # Identify the separate circuits created by the initial pairings.
    circuit_of_edge = [-1] * number_of_edges
    circuit_count = 0

    for edge_id in range(number_of_edges):
        if circuit_of_edge[edge_id] != -1:
            continue

        current_half = 2 * edge_id

        while circuit_of_edge[current_half // 2] == -1:
            circuit_of_edge[current_half // 2] = circuit_count

            # Traverse current_half, arrive through current_half ^ 1,
            # then leave through the half-edge paired with it.
            current_half = partner[current_half ^ 1]

        circuit_count += 1

    circuits = DisjointSet(circuit_count)

    # Merge different circuits meeting at the same vertex.
    for incident_edges in adjacency:
        if not incident_edges:
            continue

        anchor_first = incident_edges[0]
        anchor_second = incident_edges[1]
        anchor_circuit = circuit_of_edge[anchor_first // 2]

        for index in range(2, len(incident_edges), 2):
            other_first = incident_edges[index]
            other_second = incident_edges[index + 1]
            other_circuit = circuit_of_edge[other_first // 2]

            # Crossing two pairs from the same merged circuit could split it.
            if not circuits.union(anchor_circuit, other_circuit):
                continue

            # Before crossing:
            #   anchor_first <-> anchor_second
            #   other_first  <-> other_second
            #
            # After crossing:
            #   anchor_first  <-> other_first
            #   anchor_second <-> other_second
            partner[anchor_first] = other_first
            partner[other_first] = anchor_first
            partner[anchor_second] = other_second
            partner[other_second] = anchor_second

            # The pair (anchor_first, other_first) becomes the new anchor.
            anchor_second = other_first

    # A connected Eulerian graph must now contain one merged circuit.
    final_root = circuits.find(0)

    if any(
        circuits.find(circuit) != final_root
        for circuit in range(circuit_count)
    ):
        return None

    # Follow the final pairings to materialize the Eulerian circuit.
    start_half = adjacency[0][0]
    current_half = start_half
    route = [0]
    used_edges = [False] * number_of_edges

    for _ in range(number_of_edges):
        edge_id = current_half // 2

        if used_edges[edge_id]:
            return None

        used_edges[edge_id] = True
        current_node = destination[current_half]
        route.append(current_node)

        arriving_half = current_half ^ 1
        current_half = partner[arriving_half]

    if (
        route[-1] != 0
        or current_half != start_half
        or not all(used_edges)
    ):
        return None

    return route


def run_tucker():
    """Run Tucker's algorithm on the graph imported from graph_network."""

    print("\n--- Tucker's Algorithm ---")

    if not nodes:
        print("IMPOSSIBLE: the graph contains no starting node.")
        return None

    if len(set(nodes)) != len(nodes):
        raise ValueError("The nodes list must not contain duplicates.")

    # The first element of nodes is the common starting node (post office).
    start_node = nodes[0]
    ordered_nodes = [start_node] + [node for node in nodes if node != start_node]
    node_to_index = {
        node: index
        for index, node in enumerate(ordered_nodes)
    }

    try:
        indexed_edges = [
            (node_to_index[first], node_to_index[second])
            for first, second in edges
        ]
    except KeyError as error:
        raise ValueError(
            f"Edge endpoint {error.args[0]!r} is missing from nodes."
        ) from error

    indexed_route = build_tucker_circuit(
        len(ordered_nodes),
        indexed_edges,
    )

    if indexed_route is None:
        print("IMPOSSIBLE: the graph has no Eulerian circuit.")
        return None

    route = [ordered_nodes[index] for index in indexed_route]

    print("Eulerian circuit:")
    print(" -> ".join(map(str, route)))
    return route


if __name__ == "__main__":
    run_tucker()
