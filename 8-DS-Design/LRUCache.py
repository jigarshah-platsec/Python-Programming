"""
https://www.kunxi.org/blog/2014/05/lru-cache-in-python/
https://leetcode.com/problems/lru-cache/solution/
"""

import collections

""" ❖ The Architecture:
Node Class: Stores key, value, prev, and next.
Dictionary: Maps key ➔ Node Instance.
Dummy Head & Tail: Two "sentinel" nodes that stay fixed. They eliminate if node.next is None checks, keeping the code clean and fast.


Hashmap + Doubly Linked-List
LRU HashMap ---> {key: Node}  -> O(1) access

Time Complexity: Every operation is strictly $O(1)$.Space Complexity: $O(capacity)$ to store the nodes and the hash map.
"""
class Node:
    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # key -> Node (This is your "Pointer Map")
        
        # Sentinel nodes to avoid null checks
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        """Standard DLL removal: O(1)"""
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add(self, node):
        """Always add to the right (most recent): O(1)"""
        prev, nxt = self.tail.prev, self.tail
        prev.next = node.next = nxt
        node.prev, nxt.prev = prev, node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node) # Move to 'Most Recent' position
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add(new_node)
        
        if len(self.cache) > self.cap:
            # Remove the 'Least Recently Used' (The one after head)
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]

"""
Concurrency: In a production multi-threaded environment (like LinkedIn's Feed service), 
you would wrap the _remove and _add operations in a Threading Lock OR 
"""
import threading

class ThreadSafeLRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.lock = threading.Lock() # The Guard
        # ... DLL head/tail initialization ...

    def get(self, key):
        with self.lock: # Atomic block: No one else can get/put
            if key in self.cache:
                node = self.cache[key]
                self._move_to_recent(node)
                return node.value
            return -1

    def put(self, key, value):
        with self.lock: # Atomic block
            # ... update/add node logic ...
"""
Concurrency: In a production multi-threaded environment (like LinkedIn's Feed service), 
use a Read-Write Lock to prevent two threads from corrupting the pointers simultaneously.
"""
class RWLock:
    def __init__(self):
        self.lock = threading.Lock()
        self.readers = 0

    def acquire_read(self):
        with self.lock:
            self.readers += 1

    def release_read(self):
        with self.lock:
            self.readers -= 1

    def acquire_write(self):
        self.lock.acquire() # Exclusive hold

    def release_write(self):
        self.lock.release()

""" Sharding
❖ The Staff-Level Optimization:
If the interviewer asks how to scale this further, propose Sharding.

Instead of one giant LRU Cache with one lock, create 16 smaller caches (buckets).

Use hash(key) % 16 to decide which bucket to use.

Now, you have 16 independent locks. Threads hitting different buckets don't block each other. This is how high-performance systems like Memcached or Redis handle concurrency.
"""

"""
Using UnOrdered Map (Dictionary)
"""
class LRUCache_UnOrderedMap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.mostRecent = 0     # Marker for most recent get/put entry that keeps higher number to keep cache for last entry, refreshed
        self.cache = {}
        self.lru = {}

    def get(self, key):
        if key in self.cache:
            self.lru[key] = self.mostRecent
            self.mostRecent += 1
            return self.cache[key]
        return -1

    def set(self, key, value):
        if len(self.cache) > self.capacity:
            # Find the LRU entry to purge       # mostRecent = min number
            old_key = min(self.lru.keys(), key=self.mostRecentKey)
            self.cache.pop(old_key)
            self.lru.pop(old_key)
        self.cache[key] = value
        self.lru[key] = self.mostRecent
        self.mostRecent += 1
    
    def mostRecentKey(self, k):
        return self.lru[k]

"""
Using UnOrdered Map (Dictionary)
MostRecent is always on the top
LeastRecent is always in the bottom
"""
class LRUCache_OrderedMap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)     # Pop and Push this value to make it MostRecent
            self.cache[key] = value
            print("get returns", value)
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        try:
            self.cache.pop(key)         # Key exists, Update
        except KeyError:
            if len(self.cache) >= self.capacity:    # Full
                print("purge")
                self.cache.popitem(last=False)      # Purge old entry (LeastRecent is always in the bottom)
        print("set sets", value)
        self.cache[key] = value                     # set New entry






def main():
    lru = Solution(2)
    print(list(filter(lambda x: x, [lru.set(1, 1),lru.set(2, 2), lru.set(3, 3), lru.get(1), lru.get(2), lru.get(3)])))


    lru = LRUCacheOptimized(2)
    print(list(filter(lambda x: x, [lru.set(1, 1),lru.set(2, 2),lru.set(1, 1), lru.set(3, 3),lru.get(3), lru.get(1)])))