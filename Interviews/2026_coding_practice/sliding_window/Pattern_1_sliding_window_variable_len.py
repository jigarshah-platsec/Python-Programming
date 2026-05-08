def longestSubString(s: str) -> int:
    localMax, globalMax = 0, 0

    

    return globalMax

"""def longestSubString(S: str) -> int:
    longest, globalLongest = 0, 0   # Local Max and Global Max to keep track of
    seen = set()                    # A Set used to Break invalid window

    left, right = 0, 0 
    for right, c in enumerate(S):
        # If window is NOT VALID, move L until window is valid
        while c in seen:
            seen.remove(S[left])
            left += 1
        
        # Window is NOW VALID
        seen.add(c)
        
        # hisab
        longest = right - left + 1                  # Local Max
        globalLongest = max(globalLongest, longest) # Global Max
        
    return globalLongest
"""

def main():
    result = longestSubString("abcabcadbc")
    assert result == 4 # "bcad" is longest substring

if __name__ == "__main__":
    main()
