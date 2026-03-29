from collections import deque

def isCycle(graph, startNode) -> bool:
    # DFS
    recordingStack = set()

    # Start from startNode
    return DFS(graph, startNode, recordingStack)
    

def DFS(graph, cur, recordingStack) -> bool:
    if cur is None:
        return False

    if cur in recordingStack: # We are visiting this node again!
        # Remember the PATH hits a cycle 0->1->2->0 
        print("Cur in recordingStack: ", recordingStack)
        return True # CYCLE DETECTED
    
    # Remember the PATH 0->1->2
    recordingStack.add(cur)
    
    print("recordingStack: ", recordingStack)
    for conn in graph[cur]:
        return DFS(graph, conn, recordingStack)

    # No cycle
    return False
    
"""
(DFS vs Topological Sort), how do you definitively detect a cycle (deadlock)?
A) The queue becomes empty before the while loop finishes.
B) A node's in-degree drops below zero.
C) The length of the final result list is less than num_packages.
D) A node is added to the queue twice.

DFS -> recordingStack from recursive function call
topoSort -> at the end when intalled list is not equal to all num_packages needed to be installed
"""
def main():
    graph = {0: [1, 2], 1: [2], 2: []}
    assert isCycle(graph, startNode=0) == False

    graph = {0: [1], 1: [2], 2: [0]}
    assert isCycle(graph, startNode=0) == True

if __name__ == "__main__":
    main()