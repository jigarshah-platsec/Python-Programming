# Data Structure Design: Core Foundation

## Mental Model
Combining multiple basic data structures to achieve specific time/space complexity goals.

## Key Patterns
- **LRU Cache:** Combining a HashMap (for $O(1)$ lookups) and a Doubly Linked List (for $O(1)$ ordering updates).
- **Insert/Delete/GetRandom $O(1)$:** Combining a HashMap (value -> index) and a List (for $O(1)$ random access).
