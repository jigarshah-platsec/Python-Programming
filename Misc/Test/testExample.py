class Solution:
    def sum(self, a, b):
        return a + b

import unittest

class TestSolution(unittest.TestCase):
    def setUp(self):    
        # Load test data
        self.s = Solution()

    def test_sum_rightparams(self):
        self.assertEqual(self.s.sum(1, 2), 3, "wrong result")

    def test_sum_wrongparams(self):
        self.assertEqual(self.s.sum(1, 2), 3, "wrong result")




if __name__ == '__main__':
    unittest.main()