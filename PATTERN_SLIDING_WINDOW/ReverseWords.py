class Solution:
    def reverseWords(self, text):
    
        def reverseStr(s):
            s = list(s)
            start, end = 0, len(s)-1
            while start < end:
                s[start], s[end] = s[end], s[start]
                start += 1
                end -= 1
            return "".join(s)

        N = len(text)
        start, end = 0, 0
        text = list(text)
        
        resStr = ""
        while end < N:
            if text[end].isalpha():
                end += 1
                continue
            elif text[end] == " ": # word ending here
                if start == end:    # get rid of more spaces in betwee
                    start += 1
                    end += 1
                    continue
                reversedWord = reverseStr(text[start:end])
                resStr += reversedWord
                resStr += " "
                end += 1
                start = end     # Lookup for new word
            else:
                print(f"Not expected char: {text[end]}")
        # Last word
        reversedWord = reverseStr(text[start:N])
        resStr += reversedWord
        
        # resStr contains all reveversed words, now reveserse str
        start, end = 0, len(reversedWord)-1
        reversedStr = reverseStr(resStr)
        return reversedStr

s = Solution()
print(s.reverseWords("Apple is Banana"))    # regular spacing
print(s.reverseWords("Apple  is  Banana"))  # more spaces in between
print(s.reverseWords("  Apple is Banana"))  # leading spaces
print(s.reverseWords("Apple is Banana"  ))  # Trailing spaces
