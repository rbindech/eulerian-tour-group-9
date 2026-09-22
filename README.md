# Eulerian Circuit Algorithms - Mail Delivery

## Identity

**Informatics ITS Graph Theory Class - Group [GROUP NUMBER]**

| Name | Student ID |
| --- | --- |
| Rida Bindech | 5999261011 |
| Emmanuel Santini | 5999261124 |
| Calixte Berthier | 5999261123 |

## Project Overview

This project solves the [CSES Mail Delivery problem](https://cses.fi/problemset/task/1691). A mail carrier must start at the post office, traverse every street exactly once, and return to the post office.

The city is represented as an undirected graph:

- Crossings are vertices (`nodes`).
- Streets are undirected edges (`edges`).
- The first element of `nodes` is the starting vertex (the post office).

The project implements and compares three algorithms for constructing an Eulerian circuit:

1. Fleury's Algorithm
2. Hierholzer's Algorithm
3. Tucker's Algorithm

An Eulerian circuit exists when:

- every vertex with a non-zero degree belongs to the same connected component as the starting vertex; and
- every vertex has an even degree.

If one of these conditions is not satisfied, the algorithms report that an Eulerian circuit is impossible.

## Algorithms

### 1. Fleury's Algorithm

Fleury's algorithm constructs the final circuit one edge at a time. At the current vertex, it avoids choosing a bridge whenever another unused edge is available. A bridge is an edge whose removal would disconnect the remaining graph.

Avoiding bridges prevents the algorithm from entering a part of the graph too early and leaving unused edges inaccessible. However, repeatedly testing whether an edge is a bridge makes the typical implementation relatively slow.

- **Typical time complexity:** `O(E^2)`
- **Space complexity:** `O(V + E)`

### 2. Hierholzer's Algorithm

Hierholzer's algorithm starts from the post office and follows arbitrary unused edges until it closes a circuit. If unused edges remain, it starts another circuit from a vertex already present in the current circuit and splices the new circuit into the existing one.

With an adjacency list, edge identifiers, and a stack, every edge is processed only once.

- **Time complexity:** `O(V + E)`
- **Space complexity:** `O(V + E)`

### 3. Tucker's Algorithm

Tucker's algorithm first pairs the incident edges at every vertex. Because every degree is even, all incident edges can be paired. These local pairings decompose the graph into edge-disjoint circuits.

When two different circuits pass through the same original vertex, Tucker's algorithm crosses two local pairs to merge the circuits. A disjoint-set union structure (DSU) records which circuits have already been merged and prevents a completed circuit from being split again. After all circuits have been merged, the final pairings are followed from the post office to produce one Eulerian circuit.

- **Time complexity in this implementation:** `O(V + E * alpha(E))`
- **Space complexity:** `O(V + E)`

Here, `alpha` is the inverse Ackermann function and grows so slowly that the implementation is practically linear.


## Project Structure

```text
.
|-- input.txt                #Input for sample run
|-- fleury_algorithm.py              # Fleury's algorithm
|-- hierholzer_algorithm.py          # Hierholzer's algorithm
|-- tucker_algorithm.py     # Tucker's algorithm
|-- main.py                # Runs all three algorithms
|-- README.md
|-- report.pdf           # Step-by-step analysis and comparison
```

## Prerequisites

- Python 3.10 or later
- No external Python packages are required

Verify the Python installation with:

```bash
python3 --version
```

On Windows, the command may be:

```bash
python --version
```

## Input Format

The algorithms read the graph input directly from `input.txt` using the standard CSES Mail Delivery format.

- First line: Two space-separated integers $n$ (number of vertices) and $m$ (number of edges).
- Next $m$ lines: Two space-separated integers $u$ and $v$, representing an undirected edge between vertex $u$ and vertex $v$.:

```text
5 6
1 2
2 3
3 1
1 4
4 5
5 1
```

## How to Run

Place all Python files in the same directory and run:

```bash
python3 main.py
```

On Windows, use:

```bash
python main.py
```

The `main.py` file can call the algorithms as follows:

```python
from fleury_algorithm import run_fleury
from hierholzer_algorithm import run_hierholzer
from tucker_eulerian_algorithm import run_tucker


def main():
    run_fleury()
    run_hierholzer()
    run_tucker()


if __name__ == "__main__":
    main()
```

## Sample Run Result

One possible execution on the sample graph is:

```text
--- Fleury's algorithm ---
Eulerian circuit:
1 2 3 1 4 5 1

--- Hierholzer's Algorithm ---
Eulerian circuit:
1 -> 3 -> 5 -> 4 -> 2 -> 3 -> 6 -> 2 -> 1

--- Tucker's Algorithm ---
Eulerian circuit:
1 -> 2 -> 4 -> 5 -> 3 -> 6 -> 2 -> 3 -> 1
```

The three outputs do not need to be identical. A result is valid when it:

- starts and ends at the post office;
- uses every edge exactly once; and
- contains exactly `E + 1` vertices.

## AI Tools Usage Disclosure

OpenAI ChatGPT/Codex was used during this project to:

- clarify the differences between Fleury's, Hierholzer's, and Tucker's algorithms;
- assist with the design, commenting, testing, and debugging of the Tucker implementation; and
- help draft and organize this README.

## References

- Course material: *Graph Traversal 1 - Eulerian Tour, Graph Theory Week 3*
- [CSES Problem Set - Mail Delivery](https://cses.fi/problemset/task/1691)
