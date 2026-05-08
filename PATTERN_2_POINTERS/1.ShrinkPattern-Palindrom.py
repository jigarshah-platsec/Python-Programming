""" Valid Palindrom (https://leetcode.com/problems/valid-palindrome/)
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and 
removing all non-alphanumeric characters, it reads the same forward and backward. (Alphanumeric characters include letters and numbers.)
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        DS: String, Pattern: Use of lower(), isalpha() [a-z, A-Z] and isdigit() [0-9]
        """
        
        newStr = ""
        
        for c in s.lower():
            if c.isalpha() or c.isdigit():
                newStr += c
        print(f"New String should have only AlphaNum chars: {newStr}")
        
        
        """ Pattern: 2 Pointers    begin ----->  <------- end  """
        begin, end = 0, len(newStr)-1   # Indexes
        while begin < end:
            if newStr[begin] != newStr[end]:
                return False
            begin += 1
            end -= 1
        
        return True

    def isPalindromeOptimizedSpace(self, text):
        text = text.lower()
        start, end = 0, len(text)-1
        while start < end:
            # skip non alphanumeric chars to compare
            # SRC ---> Point to an alpha
            while not (text[start].isalpha() or text[start].isdigit()):
                start += 1
        
            # Dest <--- Point to an alpha
            while not (text[end].isalpha() or text[end].isdigit()):
                end -= 1

            # Now both are alpha, compare
            if text[start] != text[end]:    # No match!
                return False
            else:                           # Match!
                start += 1
                end -= 1

        # Everything is palindrome
        return True

s = Solution()
text = "A man, a plan, a canal: Panama"
print(s.isPalindrome(text))    # Output: true Explanation: "amanaplanacanalpanama" is a palindrome.
text = "race a car"
print(s.isPalindrome(text))    # Output: false Explanation: "raceacar" is not a palindrome.
text = " "
print(s.isPalindrome(text))    # Output: true  s is an empty string "" after removing non-alphanumeric characters
text = "Abcd-cBa"
print(s.isPalindrome(text))    # Output: true  s is an empty string "" after removing non-alphanumeric characters
