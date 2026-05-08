# Graphs: Core Foundation

## Mental Model
Nodes (vertices) connected by edges. Can be directed/undirected, weighted/unweighted.

## Key Patterns
- **Adjacency List:** The most common way to represent a graph in Python (`defaultdict(list)`).
- **DFS / BFS:** Exploring the graph. Must track `visited` nodes to prevent infinite loops.
- **Topological Sort:** Ordering of nodes in a Directed Acyclic Graph (DAG).
