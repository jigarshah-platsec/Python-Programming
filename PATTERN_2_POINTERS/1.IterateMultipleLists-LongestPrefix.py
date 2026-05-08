"""
Strings: Longest Common Prefix
https://leetcode.com/problems/longest-common-prefix/
"""

class Solution:
    def longestCommonPrefix(self, strs):
        # Edge case     If no strings,             Example: []
        if len(strs) == 0:
            return ""

        # Edge case:    If there is only 1 string, Example: [[]] or [["Jigar"]]
        if len(strs) == 1:
            return strs[0]

        # Find the shortest str to iterate all other strings with
        shortestStr = min(strs, key=len)

        # Iterate through shortestStr and find if that char exists in all other strs at same index
        for i, c in enumerate(shortestStr):
            # all other strs
            for other in strs:
                if c != other[i]:  # No match == until now is the longest common prefix
                    return shortestStr[:i]
                else:              # Match == continue to look for next char
                    continue
        
        # Everything matched
        return shortestStr

s = Solution()
strs = ["flower","flow","flight"]   # Output: "fl"
print(s.longestCommonPrefix(strs))
strs = ["dog","racecar","car"]      # Output: ""
print(s.longestCommonPrefix(strs))
