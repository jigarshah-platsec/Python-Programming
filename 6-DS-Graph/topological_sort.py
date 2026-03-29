"""
https://leetcode.com/problems/course-schedule-ii/solution/

https://leetcode.com/problems/course-schedule-ii/discuss/59321/Python-dfs-bfs-solutions-with-comments.
"""

from collections import defaultdict

class Graph(object):
    def __init__(self):
        self.graph = defaultdict(list)

    # Directed graph
    def add_edge(self, src, dest):
        self.graph[src].append(dest)

"""
(Topological Sort), how do you definitively detect a cycle (deadlock)?
A) The queue becomes empty before the while loop finishes.
B) A node's in-degree drops below zero.
C) The length of the final result list is less than num_packages.
D) A node is added to the queue twice.
"""
class Solution():
    """
    BFS using minHeap queue
    """
    def topologicalSort_BFS(self, edges):
        graph = Graph()
        indegree = defaultdict(int)
        topoOrder = list()

        # Building graph ---- With InDegree
        for edge in edges:
            src, dest = edge[0], edge[1]
            graph.add_edge(src, dest)

            # Building indegree #dict{Vertex: Indegree} #= number of dependancies before this can resolve}
            indegree[dest] += 1
        print(("InDegree: {0}".format(indegree)))

        # BFS: TOPOLOGICAL Order.... Node with indegree=0 to be visited. All other nodes (dependants) indegree to be reduced
        q = [node for node, iVal in list(indegree.items()) if iVal == 0]  # Start with Node with indegree=0 (No dependency)
        resolved = 0
        while q:
            print(("Queue: {0}".format(q)))
            print(("Indegree: {0}".format(indegree)))
            node = q.pop()
            resolved += 1   # This dependency is resolved
            topoOrder.append(node)

            # Now resolve all that was dependent on this
            for conn in graph.graph[node]:
                indegree[conn] -= 1      # This has now 1 less dependency
                if indegree[conn] == 0:  # If no dependency, then queue it to resolve
                    q.append(conn)

        return topoOrder

    """
    DFS: Using RecStack (PostOrder traversal)
    https://www.geeksforgeeks.org/python-program-for-topological-sorting/
    """
    def topologicalSort_DFS(self, edges):
        graph = defaultdict(list)
        visited = set()
        stack = []

        # Building graph
        for edge in edges:
            src, dest = edge[0], edge[1]
            graph[src].append(dest)

        for node in list(graph.keys()):
            if node not in visited:
                self.visit(graph, node, visited, stack)
        print("Topological sort order of Graph: ")
        return stack

    def visit(self, graph, node, visited, stack):
        visited.add(node)

        for conn in graph[node]:
            if conn not in visited:
                self.visit(graph, conn, visited, stack)

        # TRICK: POST PROCESSING. The core node is visited last! But it should be installed first!
        stack.insert(0, node)


s = Solution()
# edges = [[1,0]]
# print(s.topologicalSort_BFS(edges, 2))
# print(s.topologicalSort(edges, 2))
#
# edges = [[1,0],[0,1]]
# print(s.topologicalSort_BFS(edges, 2))
# print(s.topologicalSort(edges, 2))
#
edges = [['A', 'B'], ['A', 'C'], ['B', 'D']]
print((s.topologicalSort_BFS(edges)))
print((s.topologicalSort_DFS(edges)))
#
# edges = [[1, 0], [2, 0], [3, 1], [3, 2]]
# print(s.topologicalSort_BFS(edges, 3))
# print(s.topologicalSort(edges, 3))
