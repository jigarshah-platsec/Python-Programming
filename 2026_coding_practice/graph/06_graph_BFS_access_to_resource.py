""" INVERTED GRAPH {child_user: {parent_group1, parent_group2, ...}} --> {"bob": [sre_group, admin_group], "alice": [dev_group, audit_group]}
why you inverted the graph (User-centric search)

Practice Problem: The Transitive Group CheckerScenario: You are building an authorization engine.
Groups can contain other groups (nested).
Circular references are possible (e.g., Devs $\rightarrow$ OnCall $\rightarrow$ Devs).

Function:
def has_access(user, required_group, memberships) that returns True if the user is a member of the required group, directly or indirectly.
Input Data: A list of (parent_group, child_member) tuples.
"""

from collections import deque, defaultdict
from typing import List, Tuple, Dict, Set

class MembershipEngine:
    def __init__(self, memberships: List[Tuple[str, str]]):     # [("admin_group", "dev_group"), ...]
        # Optimization: Build an "Inverted Graph" (Member -> Parent Groups)
        # This allows us to search UP from the user, which is usually 
        # much smaller than searching DOWN from a root group.
        self.parent_groups = defaultdict(list)
        
        for parent_group, member in memberships:
            self.parent_groups[member].append(parent_group)

    def has_access(self, user: str, required_group: str) -> bool:
        # Edge Case: The user IS the group (e.g. checking direct mapping)
        if user == required_group:
            return True
        
        # BFS on Graph
        queue = deque()
        visited = set()  
        
        visited.add(user)       # Mark visited BEFORE adding in queue to prevent DUPS in Qs from future nodes pointing to this conn 
        queue.append(user)      # begin with given "member"

        while queue:
            current_group = queue.popleft()

            # Happy Path! If we reached the target group, we found a path
            if current_group == required_group:
                return True

            # Keep looking! Traverse UP to the parent groups
            for parent_group in self.parent_groups[current_group]:
                if parent_group not in visited:
                    visited.add(parent_group)  # Mark visited BEFORE queueing - prevent adding them in queue/visit again!
                    queue.append(parent_group)

        return False

# --- Test ---
"""
► 1. In a standard BFS for Access Control, when is the exact right moment to add a node to the visited set to prevent massive queue duplication?
A) Immediately after popping it from the queue.
B) Immediately before appending it to the queue.
C) After checking if it matches the target group.
D) At the very end of the while loop.
"""
def main():
    # Graph: 
    # Admins -> Devs -> Alice
    # Admins -> SREs -> Bob
    # Devs -> Audit -> Admins (Cycle!)
    memberships = [
        ("admin_group", "dev_group"),
        ("dev_group", "alice"),
        ("sre_group", "bob"),
        ("admin_group", "sre_group"),
        ("dev_group", "audit_group"), 
        ("audit_group", "admin_group") 
    ]
    
    engine = MembershipEngine(memberships)
    
    # Test 1: Alice -> Devs -> Admins (True)
    assert engine.has_access("alice", "admin_group") == True
    print("Alice is Admin: PASS")

    # Test 2: Bob -> SREs -> Devs (False)
    assert engine.has_access("bob", "dev_group") == False
    print("Bob is NOT Dev: PASS")
    
    # Test 3: Cycle Safety
    assert engine.has_access("alice", "audit_group") == True
    print("Cycle handled: PASS")

if __name__ == "__main__":
    main()