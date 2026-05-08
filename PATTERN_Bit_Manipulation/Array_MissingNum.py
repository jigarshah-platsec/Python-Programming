"""
https://leetcode.com/problems/missing-number/
Approach 1: Sort, look for missing neighbor (next_num should be this_num + 1)   ==> O(nlogn)
Approach 2: Create a set from nums (ActualSeq), Create an expectedSeq (range 0...n+1) ===> See which one's not in set
Approach 3: Bitwise XOR: xor of expected seq, xor of actual seq, XOR will square off with original nums except missing
Approach 4: MATH: Expected seq (0...n+1) Sum and Actual Seq (0...n) sum. Diff is the num

PATTERN: BitWise Xor!
        XOR of a num with itself is 0. So the missing num will not XOR to 0
        
        XOR --> expected sequence --> 0...n
        XOR --> Given    sequence --> 0...n-1
        XOR_expected_seq XOR XOR_given_seq... So missing num will not be 0'd
"""


class Solution():
    def missingNum(self, nums):

        # Expected sequence: len(nums)+1 ---> XOR_expected
        # Actual   sequence: len(nums)   ---> XOR_actual
        xor_expected, xor_actual = 0, 0

        for i in range(len(nums)+1):
            xor_expected = xor_expected ^ i
            xor_actual = xor_actual ^ nums[i] if i != len(nums) else xor_actual     # Preventing OOB for actual loop

        # XOR_expected_seq XOR XOR_given_seq... So missing num will not be 0'd
        missingNum = xor_actual ^ xor_expected
        return missingNum

    def missingNumUsingSet(self, nums):
        actualNums = set(nums)
        expectedNums = range(len(nums)+1)

        for num in expectedNums:
            if num not in actualNums:
                return num          # Num from Expected Sequence is missing

        return -1   # No missing num

    def missingNumUsingMath(self, nums):
        """ Sum of an expected Sequence is easy to derive: sum(n) = n! = n*(n+1)//2

        Diff from Sum of expected Sequence Vs.
                  Sum of Actual   Sequence
        """
        n = len(nums)
        expectedSum = n * (n + 1) // 2
        actualSum = sum(nums)

        return expectedSum - actualSum

s = Solution()
nums = [3,0,1]
assert(s.missingNumUsingMath(nums) == 2)
print(s.missingNumUsingMath(nums))
nums = [9,6,4,2,3,5,7,0,1]
assert(s.missingNumUsingMath(nums) == 8)
print(s.missingNumUsingMath(nums))