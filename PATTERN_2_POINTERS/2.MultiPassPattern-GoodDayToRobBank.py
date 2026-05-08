"""
https://leetcode.com/problems/find-good-days-to-rob-the-bank/
"""
from typing import List

class Solution:
    def goodDaysToRobBank(self, security: List[int], time: int) -> List[int]:
        N = len(security)
        
        print(f"security: {security}")
        prefixCount, suffixCount = [1], [1]
        cnt = 1
        for i, num in enumerate(security):
            # Check if num in DESCENDING order
            if i == 0:  # skip first
                continue
            
            if num <= security[i-1]:
                cnt += 1    # Keep increasing DESCENDING order count
            else:   
                cnt = 1     # Restart
            prefixCount.append(cnt)
        
        print(f"prefixCount: {prefixCount}")
        cnt = 1
        for i in range(N-1, -1, -1):
            # Check if num in ASCENDING order
            if i == N-1:    # skip last
                continue
            num = security[i]
            if num <= security[i+1]:
                cnt += 1    # Keep increasing ASCENDING order count
            else:
                cnt = 1     # restart
            suffixCount.append(cnt)

            suffixCount = list(reversed(suffixCount))
        print(f"SuffixCount: {suffixCount}")

        res = []
        for i, num in enumerate(security):
            if i - time >= 0 and i + time < N:   # Within boundry
                if prefixCount[i] >= time and suffixCount[i] >= time:
                    res.append(i)
        
        return res
        
        
s = Solution()

security = [5,3,3,3,5,6,2]
time = 2    ## Output: [2,3]
print(s.goodDaysToRobBank(security, time))

security = [1,1,1,1,1]
time = 0        ## Output: [0,1,2,3,4]
print(s.goodDaysToRobBank(security, time))

security = [1,2,3,4,5,6]
time = 2      ## Output: []
print(s.goodDaysToRobBank(security, time))

            
            