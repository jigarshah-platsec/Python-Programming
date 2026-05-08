import unittest
import json
import importlib

# Handling the module import with the missing 's' in the filename
try:
    module = importlib.import_module("json_log_procesor")
    json_log_processor = module.json_log_processor
except ImportError:
    raise ImportError("Could not find json_log_procesor.py. Make sure the filename matches!")

class TestJsonLogProcessor(unittest.TestCase):

    def check_result(self, res):
        """Helper to cleanly parse the result whether it is yielded as a dict or a JSON string."""
        if isinstance(res, str):
            return json.loads(res)
        return res

    def test_single_batch_exact_size(self):
        """
        Tests that it successfully processes exactly one batch and yields the correct count.
        """
        logs = [
            '{"tenant_id": "tenant_A", "http_status": 403}',
            '{"tenant_id": "tenant_B", "http_status": 200}', # Should not be counted
            '{"tenant_id": "tenant_A", "http_status": 403}',
        ]
        
        # Batch size is 3. We have exactly 3 logs.
        gen = json_log_processor((log for log in logs), batch_size=3)
        res = self.check_result(next(gen))
        
        self.assertEqual(res.get("tenant_A"), 2)
        self.assertNotIn("tenant_B", res)
        
        # Generator should be exhausted
        with self.assertRaises(StopIteration):
            next(gen)

    def test_multiple_batches_and_memory_wipe(self):
        """
        Tests that memory is wiped clean between batches.
        """
        logs = [
            # Batch 1
            '{"tenant_id": "tenant_A", "http_status": 403}',
            '{"tenant_id": "tenant_A", "http_status": 403}',
            
            # Batch 2
            '{"tenant_id": "tenant_A", "http_status": 403}', # Should start fresh from 1
            '{"tenant_id": "tenant_B", "http_status": 403}',
        ]
        
        gen = json_log_processor((log for log in logs), batch_size=2)
        
        res1 = self.check_result(next(gen))
        self.assertEqual(res1.get("tenant_A"), 2)
        
        res2 = self.check_result(next(gen))
        self.assertEqual(res2.get("tenant_A"), 1, "Memory was not wiped clean! It accumulated counts from Batch 1.")
        self.assertEqual(res2.get("tenant_B"), 1)

    def test_partial_final_batch(self):
        """
        Tests that if the stream ends before a full batch is reached,
        it yields whatever remaining counts it has (the partial batch).
        """
        logs = [
            '{"tenant_id": "tenant_x", "http_status": 403}',
            '{"tenant_id": "tenant_x", "http_status": 500}',
        ]
        
        gen = json_log_processor((log for log in logs), batch_size=5)
        res = self.check_result(next(gen))
        self.assertEqual(res.get("tenant_x"), 1)
        
        with self.assertRaises(StopIteration):
            next(gen)

    def test_string_vs_int_status(self):
        """
        JSON numbers might sometimes be parsed as strings. Ensures robustness.
        """
        logs = [
            '{"tenant_id": "tenant_str", "http_status": "403"}',
            '{"tenant_id": "tenant_int", "http_status": 403}',
        ]
        gen = json_log_processor((log for log in logs), batch_size=2)
        res = self.check_result(next(gen))
        self.assertEqual(res.get("tenant_str"), 1)
        self.assertEqual(res.get("tenant_int"), 1)

    def test_malformed_json_handling(self):
        """
        Should survive bad JSON and keep processing without crashing.
        """
        logs = [
            '{"tenant_id": "tenant_A", "http_status": 403}',
            'not a valid json string',
            '{"tenant_id": "tenant_A", "http_status": 403}',
        ]
        gen = json_log_processor((log for log in logs), batch_size=3)
        res = self.check_result(next(gen))
        
        self.assertEqual(res.get("tenant_A"), 2)

if __name__ == "__main__":
    unittest.main()
