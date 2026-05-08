"""
You are given a matrix where each cell can have values

D - your desk
B - Boss's desk (can be multiple)
S - Snack (can be multiple)
. - empty
# - wall

first question -> Find if it's possible to get a snack from your desk without disturbing any boss.
BFS

second question ->
If the snack has a noise value K. K represnt the number of empty spaces the noise can travel through. find if its' possible to get the snack without disturbing any boss' through noise.

sol. first do multisource bfs from All B's and store min distance of a cell from any B's. then do a BFS from D to S such that you do not use any points where dist(cell) <= k from B

third question ->

Find the maximum value of K for which you can get the snack without distrubing any B's.

Binary Search on K with the solution of 2nd.
"""
from collections import deque

def is_safe(matrix, point) -> bool:
    row, col = point
    rows, cols = len(matrix), len(matrix[0])
    if not (0 <= row < rows and 0 <= col < cols):
        return False
    return matrix[row][col] not in {"B", "#", "W"}


def BFS(matrix) -> bool:
    if not matrix:
        return False

    queue = deque()
    visited = set()
    has_snack = any("S" in row for row in matrix)

    # Multi-source BFS: start from all desks.
    for row, row_data in enumerate(matrix):
        for col, cell in enumerate(row_data):
            if cell == "D":
                queue.append((row, col))
                visited.add((row, col))

    if not queue or not has_snack:
        return False

    # Move only forward directions: right, down, diagonal down-right.
    directions = [(0, 1), (1, 0), (1, 1)]

    while queue:
        row, col = queue.popleft()
        if matrix[row][col] == "S":
            return True

        for d_row, d_col in directions:
            nxt = (row + d_row, col + d_col)
            if nxt in visited:
                continue
            if not is_safe(matrix, nxt):
                continue
            visited.add(nxt)
            queue.append(nxt)

    return False



def main():
    matrix = ["D..#", "B#..", ".#BS", "..#."]     # D=Desk, B=Boss, #=Wall, S=Snack --- Reach from Desk to Snack, avoid Boss and Wall
    assert BFS(matrix) == True

if __name__ == "__main__":
    main()