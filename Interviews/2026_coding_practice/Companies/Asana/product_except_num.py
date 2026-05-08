""" 238. Product of Array Except Self
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.

 Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""
import heapq
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        maxHeap = []

        # Save only K in Heap
        for i, point in enumerate(points):
            dist = point[0]*point[0] + point[1]*point[1]
            if len(maxHeap) >= k:
                heapq.heappop(maxHeap)
            heapq.heappush(maxHeap, (-dist, point))


        # Top K elements from MinHeap
        res = []
        for (dist, point) in maxHeap:
            res.append(point)
        return res

