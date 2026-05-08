"""
Shrinking 2 pointers pattern! Multiple Pass L ---->   <-----R  then result ------> Pattern

https://leetcode.com/problems/trapping-rain-water/

"""
from audioop import reverse
from typing import List
"""
Pattern: Multi-Pass L --->  <---- R 
L = Prefix L Running Max
R = Suffix R Running Max
Result = maxWaterCanBeFilled = min(L, R) 

Previous Q: Product Except Self
"""
class Solution:
    """ Pattern: Multi-Pass L (Max) --->  <---- R (Max)
    
    """
    def trap(self, height: List[int]) -> int:
        N = len(height)
        leftMax = [0]*N
        rightMax = [0]*N
        
        leftMax[0] = height[0]
        for i in range(1, N):
            leftMax[i] = max(leftMax[i-1], height[i])
        
        rightMax[N-1] = height[N-1]
        for i in range(N-2, -1, -1):
            rightMax[i] = max(rightMax[i+1], height[i])
            
        print(f"leftMax: {leftMax}")
        print(f"rightMax: {rightMax}")
        
        # Add water from either L bar or R bar depending on which has less Max
        res = 0
        for i in range(N):
            # At i -> look at LeftMax height and RightMax height
            # Fill water: that can be trappped at this point is (Lmax-Rmax) and some height may already be tehre, so
            water = min(leftMax[i], rightMax[i]) - height[i]
            res += water
        
        return res
    
    def trapRainWater(self, heights):
        N = len(heights)
        Lmax, Rmax = [], []

        curMax = 0
        for i, height in enumerate(heights):
            curMax = max(curMax, height)
            Lmax.append(curMax)
        print(f"Lmax: {Lmax}")
        
        curMax = 0
        for i, height in enumerate(reversed(heights)):
            curMax = max(curMax, height)
            Rmax.append(curMax)
        Rmax = list(reversed(Rmax))
        
        print(f"Rmax: {Rmax}")

        # Calc result: Add water in available space
        # Available space = min(Lmax and Rmax) at this point
        water = 0
        for i in range(N):
            availableSpace = min(Lmax[i], Rmax[i])
            if heights[i] < availableSpace:
                print(f"Adding water at i: {i} L={Lmax[i]} and R={Rmax[i]}")
                water += availableSpace - heights[i]
        
        return water

s = Solution()
heights = [1,0,2,1,0,1,4]
print(s.trapRainWater(heights))     # Total = 5