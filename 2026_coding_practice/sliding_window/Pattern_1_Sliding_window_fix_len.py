from typing import List
def maxSumOfSubArray(A: List[int], windowSize: int) -> int:
    if len(A) < windowSize:
        return 0

    localSum, globalSum = 0, 0
    left, right = 0, windowSize-1

    # Python: Use Slice to get sum of WindowSize
    #   cloneA = A[:]
    #   localSum = cloneA[left:right]

    for right, val in enumerate(A):
        # Expand the window until a fix len (WindowSize)
        if right < windowSize:
            localSum += val
            continue

        print("right:", right, "localSum", localSum)
        # Window is Valid now
        # Hisab
        localSum -= A[left]
        localSum += A[right]
        globalSum = max(globalSum, localSum)
        
        # Move Fixed window by 1
        left += 1
        right += 1
        

    print("At Last --> left:", left, "right: ", right)
    return globalSum
    

def main():
    A = [3, 1, 4, 5, 2, 1, 3, 9, 2]
    result = maxSumOfSubArray(A, 3)
    print(result)
    assert result == 14 # [3, 9, 2]


if __name__ == "__main__":
    main()