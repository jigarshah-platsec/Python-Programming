import os
import sys
import unittest

# Ensure the local directory is in Python's path so IDEs (e.g., Pylance) and execution can find it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rate_limit import window, rate_limit

class TestRateLimiter(unittest.TestCase):

    def setUp(self):
        # Clear the global sliding window state before each test
        # so test cases do not leak state to each other
        window.clear()

    def test_allows_requests_under_threshold(self):
        # Allow 3 requests before hitting a threshold of 3
        for i in range(3):
            req = {"IP": "1.1.1.1", "timestamp": str(i)}
            self.assertTrue(rate_limit(req, window_size_seconds=5, threshold=3))

    def test_blocks_requests_over_threshold(self):
        # Allow the first 3 requests
        for i in range(3):
            req = {"IP": "1.1.1.1", "timestamp": str(i)}
            rate_limit(req, window_size_seconds=5, threshold=3)
        
        # 4th request must fail within the same 5 second window
        req_fail = {"IP": "1.1.1.1", "timestamp": "3"}
        with self.assertRaisesRegex(Exception, "RATE LIMIT OFFENDER IP: 1.1.1.1"):
            rate_limit(req_fail, window_size_seconds=5, threshold=3)

    def test_sliding_window_evicts_old_requests(self):
        # Fill window up to threshold
        for i in range(3):
            req = {"IP": "1.1.1.1", "timestamp": str(i)} # Times: 0, 1, 2
            rate_limit(req, window_size_seconds=5, threshold=3)

        # normally 4th request would fail.
        # but if we wait > 5 seconds, old requests fall out of the window.
        
        # At t=6, t=0 evicts (6 - 0 = 6, which is > 5)
        req_wait = {"IP": "1.1.1.1", "timestamp": "6"} 
        self.assertTrue(rate_limit(req_wait, window_size_seconds=5, threshold=3))
        
        # Now window has times: 1, 2, 6. Next request at t=7 evicts t=1
        req_wait2 = {"IP": "1.1.1.1", "timestamp": "7"}
        self.assertTrue(rate_limit(req_wait2, window_size_seconds=5, threshold=3))

    def test_multiple_ips(self):
        # Each IP should have its own rate limit counter tracked independently
        for i in range(3):
            req1 = {"IP": "1.1.1.1", "timestamp": str(i)}
            req2 = {"IP": "2.2.2.2", "timestamp": str(i)}
            self.assertTrue(rate_limit(req1, window_size_seconds=5, threshold=3))
            self.assertTrue(rate_limit(req2, window_size_seconds=5, threshold=3))
            
        # Both are at their limit
        with self.assertRaises(Exception):
            rate_limit({"IP": "1.1.1.1", "timestamp": "3"}, window_size_seconds=5, threshold=3)
            
        with self.assertRaises(Exception):
            rate_limit({"IP": "2.2.2.2", "timestamp": "3"}, window_size_seconds=5, threshold=3)
            
    def test_handles_case_insensitive_ip_key(self):
        # Ensure that it handles the lowercase "ip" instead of "IP" correctly
        req = {"ip": "3.3.3.3", "timestamp": "1"}
        self.assertTrue(rate_limit(req, window_size_seconds=5, threshold=3))

if __name__ == '__main__':
    unittest.main()
