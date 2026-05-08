"""
https://leetcode.com/problems/single-number/

Approach 1: Sort and check Neighbor. (thisNum and prevNum will be same for Dup)     ==> O(nlogn)
Approach 2: Keep track of visited in set. The num already in set is dup             ==> O(n)    space: O(n)
Approach 3: Reduce space by using BIT-Array instead of set  Bits: 0....128 seen True/False ==> O(n)     space: O(1)


"""