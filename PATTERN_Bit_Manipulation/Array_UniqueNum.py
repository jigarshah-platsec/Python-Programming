"""
https://leetcode.com/problems/single-number/

Approach 1: Seen Set. Add num, same num? Remove. Add/Remove will get rid of all dups. So rem num is Unique.
Approach 2: HashMap. same as above                      ==> Time: o(n), Space: o(n)... reduce space?
Approach 3: XOR. Dups will be gone. Remaining is Unique ==> Time: O(n), space: o(1)
Approach 4: Math.  2 * (a + b + c) - 2a - 2b - c = c  ==> 2 * (a+b+c) - (a+a+b+b+c) = c

"""
class Solution():
    def uniqueNum(self, nums):
        seen = set()

        for num in nums:
            if num in seen:
                seen.remove(num)        # Num is Dup
            else:
                seen.add(num)           # Num seen 1st time

        for num in seen:
            return num      # unique number is still left in seen Set

        return -1   # No unique num

    def uniqueNumUsingBits(self, nums):
        xor = 0

        for num in nums:
            xor = xor ^ num

        return xor

    def uniqueNumUsingMath(self, nums):
        """
        Approach 4: Math.  2 * (a + b + c) - 2a - 2b - c = c  ==> 2 * (a+b+c) - (a+a+b+b+c) = c
        """
        sumOfSet = sum(set(nums))
        sumOfList = sum(nums)

        return 2 * sumOfSet - sumOfList

s = Solution()
nums = [2,2,1]
assert(s.uniqueNumUsingMath(nums) == 1)
print(s.uniqueNumUsingMath(nums))
nums = [4,1,2,1,2]
assert(s.uniqueNumUsingMath(nums) == 4)
print(s.uniqueNumUsingMath(nums))


"""
https://leetcode.com/problems/single-number-ii/solution/

Approach Math: 3(A+B+C) = A+A+A + B+B+B + C+C+C ===> 3(A+B+C) - (A+A+A+B+B+B+C) - 2C = 0 ====> 3(A+B+C) - (A+A+A+B+B+B+C) = 2C
 
"""
class SolutionUniqueII(self, nums):
    def uniqueUsingMatch(self, nums):
        setSum = sum(set(nums))
        listSum = sum(list(nums))

        return (3 * setSum - listSum) // 2    # 3(A+B+C) - (A+A+A+B+B+B+C) = 2C

