from typing import List
import unittest

class Solution:
    def makeProfit(self, prices: List[int]) -> int:
        left, right = 0, 0
        localMin, localMax = float('inf'), float('-inf')

        profit = 0
        i = 0
        while i < len(prices):

            # Find Local Min == BUY price
            while i < len(prices) and prices[i] < localMin:
                localMin = prices[i]
                i += 1
            # Left is at the index which is localMin value
            print(f"localMin: {localMin}")
            
            # Find Local Max == SELL price
            while i < len(prices) and prices[i] > localMax:
                localMax = prices[i]
                i += 1
            # right is at the index which is localMax value
            print(f"localMax: {localMax}")

            # Make txn
            profit += localMax - localMin if localMin != float('inf') and localMax != float('-inf') else 0
            print(f"Profit: {profit}, Txn Complete at: {i}")

            # Restart for next txn
            localMin, localMax = float('inf'), float('-inf')


        return profit


class TestSolution(unittest.TestCase):
    def TestMakeProfit(self):
        s = Solution()
        self.assertEqual(s.makeProfit([7,1,5,3,6,4]), 7) 
        self.assertEqual(s.makeProfit([1,2,3,4,5]), 4)
        self.assertEqual(s.makeProfit([5,4,3,2,1]), 0)

def main():
    testSolution = TestSolution()
    testSolution.TestMakeProfit()

if __name__ == "__main__":
    main()
