from collections import defaultdict, deque

def find_patch_order(num_packages, dependencies) -> list:
    # 1. Initialize In-Degree for ALL nodes (0 to N-1)
    # This fixes Trap #2 (Isolated nodes are now tracked)
    indegree = {i: 0 for i in range(num_packages)}
    graph = defaultdict(list)

    # 2. Build Graph
    for dest, src in dependencies:
        graph[src].append(dest)
        indegree[dest] += 1
    
    # 3. Initialize Queue with nodes that have NO dependencies
    q = deque()
    for node, curIndegree in indegree.items():
        if curIndegree == 0:
            q.append(node)
    
    result = []

    while q:
        node = q.popleft()
        result.append(node)

        for child in graph[node]:
            # 4. TRAP #1 FIX: Decrement count instead of blind appending
            indegree[child] -= 1
            
            # Only add to queue if ALL dependencies are satisfied
            if indegree[child] == 0:
                q.append(child)

    # 5. Safety Check: Did we install everything?
    if len(result) != num_packages:
        return [] # Cycle detected! (e.g. A->B->A)

    return result

# --- Comprehensive Test Suite ---
"""
(Topological Sort), how do you definitively detect a cycle (deadlock)?
A) The queue becomes empty before the while loop finishes.
B) A node's in-degree drops below zero.
C) The length of the final result list is less than num_packages.
D) A node is added to the queue twice.
"""
def main():
    print("Running Tests...")

    # Test 1: Standard Dependency Tree
    # 0 -> 1 -> 3
    # 0 -> 2 -> 3
    n = 4
    deps = [[1, 0], [2, 0], [3, 1], [3, 2]]
    # Valid outputs: [0, 1, 2, 3] OR [0, 2, 1, 3]
    order = find_patch_order(n, deps)
    print(f"Test 1 (Standard): {order}")
    assert order == [0, 1, 2, 3] or order == [0, 2, 1, 3]

    # Test 2: Disconnected Components (Two separate clusters)
    # 0 -> 1
    # 2 -> 3
    n = 4
    deps = [[1, 0], [3, 2]]
    # Valid: [0, 2, 1, 3], [2, 0, 3, 1], etc.
    # Key check: 0 before 1, AND 2 before 3.
    order = find_patch_order(n, deps)
    print(f"Test 2 (Disconnected): {order}")
    assert order.index(0) < order.index(1)
    assert order.index(2) < order.index(3)
    assert len(order) == 4

    # Test 3: Cycle Detection (The Deadlock)
    # 0 -> 1 -> 0
    n = 2
    deps = [[1, 0], [0, 1]]
    order = find_patch_order(n, deps)
    print(f"Test 3 (Cycle): {order}")
    assert order == []  # Must return empty list

    # Test 4: Single Node (No dependencies)
    n = 1
    deps = []
    order = find_patch_order(n, deps)
    print(f"Test 4 (Single): {order}")
    assert order == [0]

    # Test 5: Linear Chain
    # 0 -> 1 -> 2 -> 3
    n = 4
    deps = [[1, 0], [2, 1], [3, 2]]
    order = find_patch_order(n, deps)
    print(f"Test 5 (Linear): {order}")
    assert order == [0, 1, 2, 3]

    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    main()