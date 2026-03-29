"""
Day 2: Sliding Window (The Rate Limiter)
Why this matters:
Security Engineers constantly deal with "noisy neighbors" or DDoS attempts. You need to verify if a specific user/IP has exceeded N requests in the last T seconds.

The "Staff" Level Trap:
A Junior engineer uses a simple counter that resets every minute (Fixed Window). This is bad because a burst of traffic at 00:59 and 01:01 could double the allowed limit.
A Staff engineer uses a Sliding Window, which is smooth and accurate.

The Data Structure: collections.deque

Why? We need to remove old timestamps from the left (oldest) and add new ones to the right (newest).

Performance: popleft() is O(1). A standard list pop(0) is O(N). Using deque shows you understand performance at scale.

Practice Problem: API Rate Limiter
Scenario:
Implement a RateLimiter class.

Rule: A client can make at most 3 requests every 10 seconds.

Input: A stream of requests (client_id, timestamp).

Output: True (Allowed) or False (Blocked).
"""
from collections import defaultdict, deque
class RateLimiter():
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        """ 
        Initialize a map of DeQueues
        history = {"user_1": [1, 2, 2, ...],
                    "user_2": [1, 2, 2, ...]
                    }
        """
        self.history = defaultdict(deque)

    def should_allow(self, user: str, currenttime: int):
        print(self.history[user])
        user_history_queue = self.history[user]

        # Clean up the queue first, delete old timestamps
        while user_history_queue and (user_history_queue[0] <= (currenttime - self.time_window)):
            user_history_queue.popleft()

        # Now Queue is ready to recieve new requests, if not full with max requests
        if len(user_history_queue) >= self.max_requests:
            return False
        
        user_history_queue.append(currenttime)
        return True
    

def main():
    # Test Case: 3 requests allowed every 10 seconds
    limiter = RateLimiter(max_requests=3, time_window=10)

    print("--- Starting Rate Limiter Test ---")

    # Time: 1s (Request 1) -> OK
    print(f"T=1: {limiter.should_allow('user_1', 1)}") 

    # Time: 2s (Request 2) -> OK
    print(f"T=2: {limiter.should_allow('user_1', 2)}")

    # Time: 2s (Request 3) -> OK
    print(f"T=2: {limiter.should_allow('user_1', 2)}")

    # Time: 3s (Request 4) -> BLOCKED (3 requests in window [1, 2, 2])
    print(f"T=3: {limiter.should_allow('user_1', 3)}") 

    # Time: 12s (Request 5) -> OK 
    # Why? The window is now [2, 12]. The request at T=1 expired.
    print(f"T=12: {limiter.should_allow('user_1', 12)}")


    assert limiter.should_allow('user_1', 3) == False
    # assert limiter.should_allow('user_1', 12) == True
    print("\nTest Passed! Logic is solid.")

if __name__ == "__main__":
    main()