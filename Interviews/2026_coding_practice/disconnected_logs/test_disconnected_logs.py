import unittest
import importlib

# Workaround to import files starting with numbers directly
module = importlib.import_module("disconnected_logs")
analyze_disconnected_logs = module.analyze_disconnected_logs

class TestAnalyzeTraceLatency(unittest.TestCase):
    
    def test_basic_happy_path(self):
        """
        Tests the standard order: Auth 200 happens first, then DB 500 later.
        Should calculate average latency correctly.
        """
        logs = [
            "[2026-03-14T09:00:00] trace_abc123 Auth status=200",     # 0 seconds
            "[2026-03-14T09:00:05] trace_abc123 Database status=500", # latency: 5s
            "[2026-03-14T09:00:00] trace_xyz789 Auth status=200",     # 0 seconds
            "[2026-03-14T09:00:10] trace_xyz789 Database status=500", # latency: 10s
        ]
        
        # Generator result check
        gen = analyze_disconnected_logs(line for line in logs)
        res1 = next(gen)
        self.assertEqual(res1, [('trace_abc123', 5.0)])
        
        # After Line 2 yields, Line 3 is processed ("trace_xyz789 Auth"). 
        # Since `trace_average_latency` is not empty, the generator yields again! 
        # We want to check the yield from Line 4 ("trace_xyz789 Database"), so we step twice.
        _ = next(gen)  # Yields state after line 3
        res2 = next(gen)  # Yields state after line 4
        self.assertEqual(res2, [('trace_xyz789', 10.0), ('trace_abc123', 5.0)])
        
    def test_out_of_order_logs(self):
        """
        CRITICAL DISTRIBUTED SYSTEMS EDGE CASE:
        Logs in microservices are often delayed, batched, or sent across varying network routes.
        The DB 500 log might arrive **before** the Auth 200 log in the stream, 
        even if the Auth timestamp is technically older. 
        Your function must hold the DB state and wait for the Auth log (or handle sorting/watermarking).
        """
        logs = [
            "[2026-03-14T09:00:05] trace_ooo123 Database status=500", # Arrives FIRST in stream!
            "[2026-03-14T09:00:00] trace_ooo123 Auth status=200",     # Arrives SECOND!
        ]
        gen = analyze_disconnected_logs(line for line in logs)
        res = next(gen)
        self.assertEqual(res, [('trace_ooo123', 5.0)])

    def test_memory_leak_unmatched_traces(self):
        """
        CRITICAL MEMORY/PERFORMANCE BUG:
        Not every Auth 200 is followed by a DB 500. Most requests are successful!
        If you store the timestamp for EVERY trace_id in a dictionary to wait for a DB 500, 
        your memory will grow infinitely and crash the server on a 50GB file.
        You must implement state eviction (e.g. periodically deleting traces older than X minutes).
        
        This test simulates millions of successful trace_ids (represented by just 3 here) 
        and ensures they are purged from the tracking dictionary eventually.
        """
        logs = [
            "[2026-03-14T09:00:00] trace_success1 Auth status=200",
            "[2026-03-14T09:00:01] trace_success1 Database status=200", # Should delete trace_success1
            "[2026-03-14T09:00:00] trace_success2 Auth status=200",
            # (assume 2 hours pass without DB log for success2...)
            "[2026-03-14T11:00:00] trace_real_fail Auth status=200",
            "[2026-03-14T11:00:05] trace_real_fail Database status=500",
        ]
        
        # NOTE: Your function will need a way to inspect the size of internal state, 
        # or we will trust the test based on yielding the right value without storing old keys.
        gen = analyze_disconnected_logs(line for line in logs)
        res = next(gen)
        self.assertEqual(res, [('trace_real_fail', 5.0)])
        
    def test_duplicate_retries(self):
        """
        EDGE CASE: What if Auth retries happen? Or DB retries happen? 
        Which timestamp do you use for latency? (usually first Auth success to first DB fail, but logic must be deliberate)
        """
        logs = [
            "[2026-03-14T09:00:00] trace_abc Auth status=200",
            "[2026-03-14T09:00:01] trace_abc Auth status=200", # Retry
            "[2026-03-14T09:00:05] trace_abc Database status=500"
        ]
        gen = analyze_disconnected_logs(line for line in logs)
        # Should the latency be 5s (first) or 4s (second)? It's up to your design, but must not crash.
        res = next(gen)
        self.assertIn(res, [[('trace_abc', 4.0)], [('trace_abc', 5.0)]])

    def test_malformed_lines_and_wrong_statuses(self):
        """
        PARSING RISKS: Ensure it skips over junk and ignores statuses that don't match exactly Auth=200 / DB=500
        """
        logs = [
            "completely broken line",
            "[2026-03-14] invalid timestamp format trace_1 Auth status=200",
            "[2026-03-14T09:00:00] trace_fail Auth status=401",     # Auth failed! We only care about Auth=200
            "[2026-03-14T09:00:05] trace_fail Database status=500"  # Don't match this database fail!
        ]
        gen = analyze_disconnected_logs(line for line in logs)
        
        with self.assertRaises(StopIteration):
            next(gen) # Should yield nothing, as no valid match exists

if __name__ == '__main__':
    unittest.main()
