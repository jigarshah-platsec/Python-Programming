"""
Valid Sudoku - INCOMPLETE
https://leetcode.com/problems/valid-sudoku/description/
"""
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rowSet, colSet, boxSet = set(), set(), set()

        rows, cols = len(board), len(board[0])
        for i in range(rows):
            for j in range(cols):
                cur = board[i][j]
                if cur != '.':  # We don't care to validate . vals
                    # Validate this cell
                    if (i, cur) in rowSet or (cur, j) in colSet or (i // 3, j // 3, cur) in boxSet:
                        return False
                    rowSet.add((i, cur))  # ROWS set =  (ROW_NUMBER, Value)
                    colSet.add((cur, j))  # COLS set =  (Value, COL_NUMBER)
                    boxSet.add((i // 3, j // 3, cur))  # BOXES set = (ROW_BOX, COL_BOX, Value)
        return True


Board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
s = Solution()
print(s.isValidSudoku(Board))