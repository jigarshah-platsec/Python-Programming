"""
Regular Binday Search
"""


def BinarySearch(array, valueToFind):
    low = 0
    high = len(array) - 1
    while low < high:
        mid = (low + high) / 2 # mid = (low+hign)<<1
        if array[mid] == valueToFind:
            print "Found value {0} at index: {1}".format(valueToFind, mid)
            return mid
        elif array[mid] < valueToFind:
            print "search in RIGHT half"
            low = mid + 1
        else:
            print "search in LEFT half"
            high = mid - 1
    print "Value {0} not found".format(valueToFind)
    return -1   # not found


"""Tweaked Binday Search:

If multiple values are same as valueToFind, 
return the lowest index instead of 1st hit in binary search

"""
def BinarySearch_LowestIndex(array, valueToFind):
    low = 0
    high = len(array) - 1
    result = -1 # not found by default

    while low < high:
        mid = (low + high) / 2
        if array[mid] == valueToFind:
            print "Found value {0} at index: {1}... Still searching lower index".format(valueToFind, mid)
            result = mid        # Store this result and still continue to look for lower index
            high = mid - 1              ###### Tweak from regular BinarySearch: CONTINUE SEARCHING ON LEFT HALF
        elif array[mid] < valueToFind:
            print "search in right half"
            low = mid + 1
        else:
            print "search in left half"
            high = mid - 1
    return result


def BinarySearch_HighestIndex(array, valueToFind):
    low = 0
    high = len(array) - 1
    result = -1  # not found by default

    while low < high:
        mid = (low + high) / 2  # mid = (low+hign)<<1
        if array[mid] == valueToFind:
            print "Found value {0} at index: {1}... Still searching higher index".format(valueToFind, mid)
            result = mid
            low = mid + 1              ###### Tweak from regular BinarySearch: CONTINUE SEARCHING ON RIGHT HALF
        elif array[mid] < valueToFind:
            print "search in right half"
            low = mid + 1
        else:
            print "search in left half"
            high = mid - 1
    return result  # not found


"""
https://leetcode.com/problems/search-in-rotated-sorted-array
Search in Rotated Sorted Array

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
"""
def BinarySearch_SortedRotatedArray(array, valueToFind):
    low = 0
    high = len(array)-1

    while low <= high:
        mid = (low + high) >> 1
        if array[mid] == valueToFind:
            return mid

        if array[low] <= array[mid]:
            # LEFT half is Sorted. Perform regular ops
            if array[low] <= valueToFind <= array[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            # RIGHT half is sorted. Perform regular ops but inverted
            if array[mid] <= valueToFind <= array[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1

"""
Find pair of elements in array that sums to given sum value
"""
def FindPairWithSum(array, sumToFind, low, high):
    while low <= high:
        currentSum = array[low] + array[high]
        if currentSum == sumToFind:
            return low, high
        elif currentSum < sumToFind:
            low += 1
        else:
            high -= 1
    return -1, -1

"""
https://www.geeksforgeeks.org/find-triplets-array-whose-sum-equal-zero/
Find all triplets with zero sum
Input : arr[] = {0, -1, 2, -3, 1}
Output : 0 -1 1
         2 -3 1

Input : arr[] = {1, -2, 1, 0, 5}
Output : 1 -2  1
"""
def threeSum(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    result = []
    d = dict((nums[i], i) for i in xrange(len(nums)))
    print "Dict {number --> Index}"
    print d
    nums = sorted(nums)
    targetSum = 0

    for i in xrange(len(nums)-1):
        low = i + 1
        high = len(nums) - 1

        while low < high:
            currentSum = nums[i] + nums[low] + nums[high]
            if currentSum == 0:
                result.append([nums[i], nums[low], nums[high]])
            elif currentSum < 0:
                # Go higher, RIGHT side
                low += 1
            else:
                # Go lower, LEFT side
                high -= 1
        return result


def main():
    """
    a = [1, 3, 5, 6, 8, 10, 10, 10, 12]
    valueToFind = 10
    result = BinarySearch(a, valueToFind)
    if result == -1:
        print "Value {0} Not found".format(valueToFind)
    else:
        print "Found {0} at location Index {1}".format(valueToFind, result)

    result = BinarySearch_LowestIndex(a, valueToFind)
    if result == -1:
        print "Value {0} Not found".format(valueToFind)
    else:
        print "Found {0} at location Index {1}".format(valueToFind, result)

    result = BinarySearch_HighestIndex(a, valueToFind)
    if result == -1:
        print "Value {0} Not found".format(valueToFind)
    else:
        print "Found {0} at location Index {1}".format(valueToFind, result)

    sumToFind = 14
    low, high = FindPairWithSum(a, sumToFind, 0, len(a)-1)
    if low == -1 or high == -1:
        print "Sum {0} Not found".format(sumToFind)
    else:
        print "Sum {0} found at pair of index {1} and {2}".format(sumToFind, low, high)

    sumToFind = 16
    for i in xrange(0, len(a)-1):
        low, high = FindPairWithSum(a, sumToFind-i, i, len(a)-1)
        if low != -1 and high != -1:
            print "Sum {0} found at index {1} {2}".format(sumToFind, low, high)


    index = BinarySearch_SortedRotatedArray([4, 5, 6, 7, 0, 1, 2, 3], 0)
    print "Index found: {0}".format(index)
    index = BinarySearch_SortedRotatedArray([4, 5, 6, 7, 0, 1, 2, 3], 7)
    print "Index found: {0}".format(index)
    index = BinarySearch_SortedRotatedArray([5 ,1, 3], 5)
    print "Index found: {0}".format(index)
    index = BinarySearch_SortedRotatedArray([5, 1, 3], 1)
    print "Index found: {0}".format(index)
    index = BinarySearch_SortedRotatedArray([5, 1, 3], 3)
    print "Index found: {0}".format(index)
    index = BinarySearch_SortedRotatedArray([5, 1, 3], 0)
    print "Index found: {0}".format(index)
    """

    print threeSum([-1, 0, 1, 2, -1, -4])

if __name__ == "__main__":
    main()

