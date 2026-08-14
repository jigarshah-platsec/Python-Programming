# K Closest Points to Origin
# 
# Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
# 
# Example 1:
#   Input: points = [[1,3],[-2,2]], k = 1
#   Output: [[-2,2]]
#   Explanation: Distance of (-2,2) is sqrt(8), (1,3) is sqrt(10)
# 
# Constraints:
#   1 <= k <= points.length <= 10^4
#   -10^4 <= xi, yi <= 10^4
# 

import heapq
import math
from typing import List

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        min_heap = []
        
        for point in points:
            x, y = point[0], point[1]
            dist = math.sqrt(x*x + y*y)
            
            while len(min_heap) >= k:
                heapq.heappop(min_heap)
            
            heapq.heappush(min_heap, (dist, point))
    
        res = []
        for dist, point in min_heap:
            res.append(point)
        return res
            
            
s = Solution()
points = [[1,3],[-2,2]]
k = 1
res = s.kClosest(points, k)
print(res)