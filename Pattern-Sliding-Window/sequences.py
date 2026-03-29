"""
Shopify: Find pair of sequences
Write a program that is going to receive an array of unique integers in ascending order. You program must return a list of list of integers with the begin and the end of each sequence.
Example 1:
input: {1,3,4} output: {(1,1), (3,4)}
Example 2:
input: {1,2,3,5,6,8} output: {(1,3), (5,6), (8,8)}
"""
from typing import List


class Solution:
    def findSequences(self, nums: List[int]) -> List:
        N = len(nums)

        # Edge case: Example: []
        if N < 1:
            return []

        res = []    # res = [(1,1), (3,4)]
        begin = 0
        for i in range(1, N):   # Determine sequence by comparing with last number
            # VALID WINDOW, Keep Expanding Right -> ..
            if nums[i] == nums[i-1] + 1:
                continue

            # VALID Window Ended, Process results
            res.append((nums[begin], nums[i-1]))

            # INVALID Window: Make it VALID again by Shrinking Left -> ..
            # A new sequence begin now from i
            begin = i
        
        # Edge Case
        # At the end, either begin is in middle or last, regardless add the last sequence
        res.append((nums[begin], nums[N-1]))

        return res

s  = Solution()
print(s.findSequences([1, 3, 4]))           # output: {(1,1), (3,4)}
print(s.findSequences([1, 2, 3, 5, 6, 8]))  # output: {(1,3), (5,6), (8,8)}
print(s.findSequences([]))
print(s.findSequences([1, 2]))
print(s.findSequences([1, 5]))