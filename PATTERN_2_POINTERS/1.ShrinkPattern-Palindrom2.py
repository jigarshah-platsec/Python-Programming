"""
https://leetcode.com/problems/valid-palindrome/

PATTERN: 2-pointers,  left and right.... Compare strings from begin and end, should be same to be valid palindrome
"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        low, high = 0, len(s) - 1
        s = s.lower()  # Ignore case

        while low < high:
            # Find 1st low and high valid alpha (a-z) to compare
            while (low < high) and (not s[low].isalpha() and not s[low].isdigit()):
                low += 1
            while (low < high) and (not s[high].isalpha() and not s[high].isdigit()):
                high -= 1

            print("low: {}, high: {}".format(s[low], s[high]))
            # Low, High pointing to valid alpha (a-z) now, so compare
            if s[low] != s[high]:
                return False

            low += 1
            high -= 1

        return True

"""
https://leetcode.com/problems/valid-palindrome-ii/
PATTERN: 2-pointers,  left and right.... Compare strings from begin and end, should be same to be valid palindrome
If not, 2 choices.... skip ith or skip jth char.... if any choice turns to be valid palindrome, we are good!
"""


class Solution:
    def validPalindrome(self, s: str) -> bool:
        low, high = 0, len(s) - 1

        while low < high:
            if s[low] == s[high]:  # Matching till now
                low += 1
                high -= 1
            else:  # No match, try 1 skip, low+1 OR high-1
                lowSkipStr = s[:low] + s[low + 1:]
                highSkipStr = s[:high] + s[high + 1:]

                # See if either of that str is validPalindrom
                return lowSkipStr == lowSkipStr[::-1] or highSkipStr == highSkipStr[::-1]

        return True  # If entire string matches without skip



"""
https://leetcode.com/problems/valid-palindrome-iii/
PATTERN: 2-pointers,  left and right.... Compare strings from begin and end, should be same to be valid palindrome
If not, 2 choices.... skip ith or skip jth char.... if any choice turns to be valid palindrome, we are good!
From that 2 choices, pick up 1 with min skips!

Reference: DP EditDistance (Turn 1 str to reversed of that str by removing chars)
"""
class ValidPalindromK(object):
    def isValidPalindrome(self, s, k):
        mem = {}
        return self.f(s,mem) <= k
    def f(self,s,mem):
        if s in mem: return mem[s]
        i = 0
        j = len(s) - 1
        while(i < j):
            if s[i] == s[j]:
                i+=1
                j-=1
            else:
                mem[s] = 1 + min(self.f(s[i:j], mem), self.f(s[i+1:j+1], mem))
                return mem[s]
        mem[s] = 0
        return 0