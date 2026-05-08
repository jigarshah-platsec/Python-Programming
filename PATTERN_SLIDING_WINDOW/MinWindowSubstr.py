from collections import Counter
class Solution:
    def minWindow(self, S: str, T: str) -> str:
        # Start from begin, keep moving end---> until valid constraint
        # Valid constraint = all chars in t is seen, seen = {} and counter=0
        #       When counter=0 (valid string)
                # Try minimizing str, drop unused char (begin chars not in seen)
        # New start (char[begin] ++ in seen)
        
        # Freq Map: seen = {} Prepare to use for seen chars in S
        # seen = {'A': 1, 'B': 1, 'C': 2}
        seen = Counter(T)
        counter = len(T) # countner = # of unique keys (regardless of freq)
        print(seen, counter)
        
        maxStr = ""
        start, end = 0, 0
        while end < len(S): 
            c = S[end]
            if c not in seen:  # (EXPAND --->end PAttern) # A non-important char, keep moving
                end += 1        
                continue
            
            # # seen = {'A': 1, 'B': 1, 'C': 2}
            # If a char is found and it's freq becomes 0 - counter--
            # So Counter will be 0 when {'A': 0, 'B': 0, 'C': 0}
            seen[c] -= 1
            counter -= 1
            end += 1
            if counter == 0:    # All unique keys are found in T already --- VALID ANSWER ---
                # Try triming unused char       (SHRINK ----> start PAttern)

                if len(maxStr) < len(S[start:end+1]):
                    maxStr = S[start:end+1]
                    print(f"New valid string: {S[start:end+1]}")

                # Here S[start] is in seen # Prepare for next iteration
                seen[S[start]] += 1 # Increase frequency
                counter += 1
                start += 1
            
        
        return maxStr

s = Solution()

S = "ADOBECODEBANC"; T = "ABC"
print(s.minWindow(S, T))

# S = "a"; T = "a"
# print(s.minWindow(S, T))

# S = "a"; T = "aa"
# print(s.minWindow(S, T))