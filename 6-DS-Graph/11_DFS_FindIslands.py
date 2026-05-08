import collections

class SolutionDFS:
    def numIslands(self, grid):
        if not grid:
            return 0

        total_islands = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':       # Explore an island from this land, mark all surronding land "1" = part of this island
                    self.dfs(grid, i, j)
                    total_islands += 1
        return total_islands

    def dfs(self, grid, i, j):
        # Base case: OOB or not land -> don't visit
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != '1':
            return
        grid[i][j] = '#'        # Mark this land VISITED to prevent visiting again through DFS
        self.dfs(grid, i + 1, j)
        self.dfs(grid, i - 1, j)
        self.dfs(grid, i, j + 1)
        self.dfs(grid, i, j - 1)


class SolutionBFS:n
    def numIslands(self, grid) -> int:
        if not grid:
            return 0

        q = collections.deque()
        total_islands = 0

        def isSafe(row, col):
            if 0 <= row < len(grid) and 0<= col < len(grid[0]) and grid[row][col] == '1':
                return True
            return False

        def BFS():
            while q:
                (row, col) = q.popleft()
                neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
                for (nrow, ncol) in neighbors:
                    if isSafe(nrow, ncol):
                        grid[nrow][ncol] = '#'
                        q.append((nrow, ncol))
        
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == '1': # Found an island, count as one island and mark all surrounding land as visited '#'
                    total_islands += 1
                    grid[row][col] = '#'
                    q.append((row, col))
                    BFS()
        

        return total_islands
