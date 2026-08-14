"""
Plaid: API Response Cache with TTL
==================================
Dict + DLL sorted by expiry (soonest-to-expire sits at head.next).

  cache[(item_id, product)] -> Node
  Node: key, data, expiry, prev, next
  Dummy head / dummy tail: no None checks on insert or remove.

  Part 1  put / get / evict_expired
  Part 2  refresh_if_stale + product default TTLs
  Part 3  capacity: if full, drop the node that expires soonest (head.next)

Expiry: valid while timestamp <= created + ttl
  put(t=1000, ttl=60) -> expiry=1060
  get(1060) hit,  get(1061) miss   (expired iff expiry < now)

Complexity
  get              O(1)
  put              O(n)   scan DLL to splice in expiry order  (not LRU — TTLs differ)
  evict_expired    O(k)   k expired nodes are always a prefix of the list
  capacity evict   O(1)   always head.next
"""

DEFAULT_TTL = {
    "balance": 30,
    "transactions": 3600,   # 1 hour
    "identity": 86400,      # 1 day
}


class Node:
    def __init__(self, key=None, data=None, expiry=0):
        self.key = key          # (item_id, product) — needed so eviction can drop the dict entry
        self.data = data
        self.expiry = expiry
        self.prev = None
        self.next = None


class PlaidCache:
    def __init__(self, capacity=None):
        self.cache = {}              # (item_id, product) -> Node
        self.capacity = capacity     # None = unlimited
        # sentinels: head.expiry = -inf, tail.expiry = +inf  → walk never hits None
        self.head = Node(expiry=float("-inf"))
        self.tail = Node(expiry=float("inf"))
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Unlink from DLL. O(1) because we already hold the node pointer."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_sorted(self, new_node):
        """Splice node so the list stays sorted by expiry. O(n). Tail (+inf) always stops the walk."""
        cur = self.head.next
        while cur.expiry < new_node.expiry:
            cur = cur.next

        # We are at position to insert a new node
        prev = cur.prev
        prev.next = new_node
        new_node.prev = prev
        new_node.next = cur
        cur.prev = new_node

    def evict_expired(self, timestamp):
        """Pop from the front while expiry < now. Sorted list ⇒ stop at the first still-valid node."""
        cur = self.head.next
        while cur is not self.tail and cur.expiry < timestamp:
            nxt = cur.next
            self._remove(cur)
            del self.cache[cur.key]
            cur = nxt

    def put(self, item_id, product, data, ttl, timestamp):
        key = (item_id, product)
        if key in self.cache:                    # overwrite: size does not grow
            node = self.cache[key]
            self._remove(node)
            del self.cache[key]

        # Part 3: expired entries shouldn't count toward capacity
        if self.capacity is not None:
            self.evict_expired(timestamp)
            if len(self.cache) >= self.capacity:
                oldest = self.head.next          # soonest expiry == smallest remaining TTL
                if oldest is not self.tail:
                    self._remove(oldest)
                    del self.cache[oldest.key]

        new_node = Node(key, data, expiry = timestamp + ttl)
        self.cache[key] = new_node
        self._insert_sorted(new_node)

    def get(self, item_id, product, timestamp):
        key = (item_id, product)
        if key not in self.cache:
            return None
        node = self.cache[key]
        return node.data

    def refresh_if_stale(self, item_id, product, fetch_fn, timestamp):
        data = self.get(item_id, product, timestamp)
        if data is not None:
            return data
        data = fetch_fn()
        self.put(item_id, product, data, DEFAULT_TTL[product], timestamp)
        return data


# --- Part 1 ---
cache = PlaidCache()
cache.put("item_1", "balance", {"amount": 100}, ttl=60, timestamp=1000)
assert cache.get("item_1", "balance", timestamp=1050) == {"amount": 100}
assert cache.get("item_1", "balance", timestamp=1060) == {"amount": 100}
assert cache.get("item_1", "balance", timestamp=1061) is None

# overwrite same key, new TTL
cache.put("item_1", "balance", {"amount": 200}, ttl=10, timestamp=1000)
assert cache.get("item_1", "balance", timestamp=1010) == {"amount": 200}
assert cache.get("item_1", "balance", timestamp=1011) is None

# --- Part 2 ---
calls = {"n": 0}

def fetch():
    calls["n"] += 1
    return {"amount": 50}

cache = PlaidCache()
assert cache.refresh_if_stale("item_1", "balance", fetch, timestamp=0) == {"amount": 50}
assert cache.refresh_if_stale("item_1", "balance", fetch, timestamp=29) == {"amount": 50}  # still fresh
assert calls["n"] == 1
assert cache.refresh_if_stale("item_1", "balance", fetch, timestamp=31) == {"amount": 50}  # stale, refetch
assert calls["n"] == 2

# --- Part 3 ---
# remaining TTL = expiry - now, so "expires soonest" == smallest expiry == head.next
c = PlaidCache(capacity=2)
c.put("a", "balance", "A", ttl=100, timestamp=0)   # expires 100
c.put("b", "balance", "B", ttl=50, timestamp=0)    # expires 50  → front
c.put("c", "balance", "C", ttl=80, timestamp=0)    # full → drop B
assert c.get("b", "balance", timestamp=0) is None
assert c.get("a", "balance", timestamp=0) == "A"
assert c.get("c", "balance", timestamp=0) == "C"

print("ok")
