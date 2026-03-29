from collections import defaultdict
import collections
import heapq

""" GRAPHS
Study: https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/#introDFSnBFS
"""
class Graph(object):
    def __init__(self):
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)

    # Directed graph
    def add_edge(self, src, dest):
        self.graph[src].append(dest)

    # Un-Directed graph
    def add_edge_undirected(self, src, dest):
        self.graph[src].append(dest)
        self.graph[dest].append(src)

    # Weighted directed graph
    def add_edge_weighted(self, src, dest, weight=1):
        self.graph[src].append((dest, weight))

    # Weighted Undirected graph
    def add_edge_weighted_undirected(self, src, dest, weight=1):
        self.graph[src].append((dest, weight))
        self.graph[dest].append((src, weight))

    # Topological sort: Build Pre-Requisties for dependancies of Dest --- To resolve Dest, Src has to be resolved first!
    def add_edge_topological(self, src, dest):
        self.graph[src].append(dest)
        self.indegree[dest] += 1

    """
    DFS for connected graph
    Study: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    """
    def dfs_connected_graph(self, root):
        visited = {}
        # Start from 1 Node....
        self.dfs_recur(root, visited)

    """
    DFS for disconnected graph
    Study: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    """
    def dfs_disconnected_graph(self):
        visited = {}

        # Start from ALL Node....
        for root in self.graph:
            if root not in visited:
                self.dfs_recur(root, visited)


    """
    DFS: Recursive function to visit a node and all it's connections
    """
    def dfs_recur(self, node, visited):
        # PreOrder: Mark this node visited (=process) BEFORE visiting connections
        visited[node] = True
        print((node,))

        # Children: Recursively visit all children of this node
        for (conn, weight) in self.graph[node]:
            if conn not in visited:
                self.dfs_recur(conn, visited)

        # PostOrder: Mark this node visited (=process) AFTER visiting connections
        # TRICK: Helpful in Installing/Processing component AFTER installing all dependancies! Install all deps (conns) then process the root node
        # visited[node] = True

    """
    Detect cycle
    Read: https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
    """
    def is_cycle(self):
        visited = {}            # used to mark node visited, to prevent DFS endless loop
        recordingStack = set()     # used to keep memory of PATH for DFS calls, (1)->(2)->(3)->(1) then recStack at 

        # disconnected graph, so start with ALL nodes
        for root in self.graph:
            if root not in visited:
                if self.is_cycle_recur(root, visited, recordingStack):
                    return True
        return False

    def is_cycle_recur(self, node, visited, recordingStack):
        # Check if we came here through DFS from any parent node (1)->(2)->(3)->(1) then recStack is (1, 2, 3) so 1 already exists and we came again to visit 1 from 3 !
        if node in recordingStack:
            return True         # CYCLE DETECTED !

        # START of recording stack: for DFS(parent)
        recordingStack.add(node)
        
        # Mark current node as visited and
        visited[node] = True

        # Visit all connections
        for (conn, weight) in self.graph[node]:
            # IN-BETWEEN: recStack! = Cycle -
            # We are re-visiting this node (conn) from the same dfs stack of original node
            if conn not in visited:
                self.is_cycle_recur(conn, visited, recordingStack)

        # END of recording stack: for DFS(parent)
        recordingStack.remove(node)
        return False        # No CYCLE detected in this DFS(parent) path


    """
    Find Path from Src to Dest
    Not Minimum Path from Src->Dest required, any path!
    Read: https://www.geeksforgeeks.org/find-if-there-is-a-path-between-two-vertices-in-a-given-graph/
    """
    def find_path(self, src, dest):
        visited = {}
        for node in list(self.graph.keys()):
            if node not in visited:
                if self.find_path_dfs(node, src, dest, visited):
                    return True
        return False

    def dfs_recur(self, node, src, dest, visited):
        # PreOrder: Mark this node visited
        visited[node] = True

        # Now visit all connections
        for (conn, weight) in self.graph[node]:
            """
            TRICK!!! During DFS if the target node is found from source == PATH is found. exit!!!
            """
            if conn == dest:
                return True

            if conn not in visited:
                if self.dfs_recur(conn, src, dest, visited):
                    return True

        # Everything is visited, but target not found yet
        return False

    """
    BFS for connected Graph
    Study: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/

► 1. In a standard BFS for Access Control, when is the exact right moment to add a node to the visited set to prevent massive queue duplication?
A) Immediately after popping it from the queue.
B) Immediately before appending it to the queue.
C) After checking if it matches the target group.
D) At the very end of the while loop.
    """
    def bfs_connected_graph(self, root):
        q = collections.deque()
        visited = set()

        q.append(root)      # Start from root node!

        while q:            # Keep going till there is any left node in Q
            node = q.popleft()     # Visit the 1st node from queue

            if node in visited: # Already visited node
                continue        # No need to visit again and add it's connections to queue
            
            # PreOrder
            # # At C) Visit the node BEFORE it's connections
            visited.add(node)
            print((node,))

            # # At L) & R) Add all connections of this node in queue to be visited later: Visiting children is deferred!
            for conn in self.graph[node]:
                if conn not in visited:
                    q.append(conn)          # QUEUE UP to visit later!

    """
    BFS for WEIGHTED Dis-connected Graph
    Study: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    """
    def bfs_connected_graph(self):
        q = collections.deque()
        visited = set()

        # q.append(root)      # Connected graph will Start from root node! but 
        # # disconnected graph has multiple root (indegree=0) nodes
        for root in self.graph:
            q.append(root)


        while q:            # Keep going till there is any left node in Q
            node = q.popleft()     # Visit the 1st node from queue

            if node in visited: # Already visited node
                continue        # No need to visit again and add it's connections to queue
            
            # PreOrder
            # # At C) Visit the node BEFORE it's connections
            visited.add(node)
            print((node,))

            # # At L) & R) Add all connections of this node in queue to be visited later: Visiting children is deferred!
            for conn in self.graph[node]:
                if conn not in visited:
                    q.append(conn)          # QUEUE UP to visit later!

    def printGraph(self):
        return sorted(list(self.graph.items()), key=lambda x: x[0])
