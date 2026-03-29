from .Tree import createBinaryTreeFromList

"""
Validate Binary Search Tree
"""
class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        minRange = 0
        maxRange = float('inf')
        return self.isValidBST_Util(root, minRange, maxRange)

    def isValidBST_Util(self, root, minRange, maxRange):
        # Base Case: Empty tree is BST
        if root is None:
            return True

        # Constraint for root
        if root.val < minRange or root.val > maxRange:
            return False

        # Same constraint for L & R
        return self.isValidBST_Util(root.left, minRange, root.val-1) and \
               self.isValidBST_Util(root.right, root.val+1, maxRange)

def check_binary_search_tree_util(root, min, max):
    # Empty tree is BST
    if root is None:
        return True

    # Constraint for BST min<root.key<max
    if root.key < min or root.key > max:
        return False

    # Constraint for LST and RST
    return check_binary_search_tree_util(root.left, min, root.key - 1) and \
           check_binary_search_tree_util(root.right, root.key + 1, max)


def check_binary_search_tree(root):
    min = -65535
    max = 65535
    return check_binary_search_tree_util(root, min, max)


def test_isBST(TreeNodes):
    # Build a tree from given List
    root = createBinaryTreeFromList(TreeNodes)
    assert check_binary_search_tree(root) is True
    print("This is BST: ", True)


def main():
    TreeNodes = [1, 2, 3, 4, 5, 6, 7]
    """
    test_isBST(TreeNodes)
    TreeNodes = [3, 2, 1, 4, 5, 6, 7]
    test_isBST(TreeNodes)
    TreeNodes = [1, 2, 3, 4, 5, 7, 6, 8]
    test_isBST(TreeNodes)
    TreeNodes = [1, 2, 5, 10, 12, 15, 20]
    test_isBST(TreeNodes)
    """
    root = createBinaryTreeFromList(TreeNodes)
    s = Solution()
    s.isValidBST(root)


if __name__ == "__main__":
    main()
