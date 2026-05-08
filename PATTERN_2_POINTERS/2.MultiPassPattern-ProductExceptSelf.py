from math import prod
from typing import List

"""
Pattern: Multi-Pass L -----> & <------- R 
L = Prefix L Running Multiplier
R = Suffix R Running Multiplier
Result = Multiplier of (Prefix L * Suffix R)

Next Q: Trapping Rain Water!
"""
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        N = len(nums)
        L, R, res = [1]*N, [1]*N, [1]*N

        # L -----> Traverse front
        # Left Product at i is: Prefix product of i-1 * previous num
        for i in range(1, N):
            L[i] = L[i-1] * nums[i-1]

        # <---------R Traverse back 
        # Right Product at i is: Prefix product until i+1 * previous num
        for i in range(N-2, -1, -1):
            R[i] = R[i+1] * nums[i+1]


        # L[i] has product of all numbers till i
        # R[i] has product of all numbers till i
        # Result is simply L[i] (prefix product of all L) * R[i] (prefix product of all R)
        for i in range(N):
            res[i] = L[i] * R[i]

        return res

    def productExceptSelfOptimized(self, nums: List[int]) -> List[int]:
        """ 
        Optimized version O(1) space
        L ----> 
        Result while R <-------
        """
        N = len(nums)
        res = [1]*N

        # L -----> Traverse front
        # Left Product at i is: Prefix product of i-1 * previous num
        for i in range(1, N):
            res[i] = res[i-1] * nums[i-1]
        print(res)
            
        # <---------R Traverse back 
        # Right Product at i is: Prefix product until i+1 * previous num
        rMax = 1
        for i in range(N-1, -1, -1):
            # Result at i is: L prefix product till now (res[i]) * Right prefix product till now (rMax)
            res[i] = res[i] * rMax
            
            # Update max R prefix product to carry forward
            rMax = rMax * nums[i]
            print(res[i], rMax)

        return res

def productExceptSum(nums):
  N = len(nums)

  # ----> L Prefix
  L = [1] * N
  for i in range(1, N):
    L[i] = L[i-1] * nums[i-1]
  print(f"Left: {L}")

  # <---- R Prefix
  RMul = 1
  # Total
  res = [1] * N
  for i in range(N-1, -1, -1):
    # Res here is the LeftPrefix * RightPrefix
    res[i] = L[i] * RMul

    # RightPrefix is now ThisNum*LastRightPrefix
    RMul = nums[i] * RMul

  return res

nums = [8, 10, 2]
print(productExceptSum(nums)) # [20, 16, 80]
nums = [2, 7, 3, 4]
print(productExceptSum(nums)) # [84, 24, 56, 42]
nums = [4, 5, 1, 8, 2]
print(productExceptSum(nums)) # [80, 64, 320, 40, 160]
