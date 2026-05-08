"""
Multisource BFS (Breadth-First Search)
--------------------------------------
Single-source BFS starts from one node.
Multisource BFS starts from many nodes at the same time.

Use case in a grid:
- 'B' = boss
- '#' = wall
- '.' = empty
- 'D' = desk

Goal:
Precompute dist[r][c] = shortest number of steps from cell (r, c)
to the nearest boss.

Key idea:
1) Put ALL bosses in the queue with distance 0.
2) Run normal BFS.
3) First time a cell gets a distance, that is its minimum distance
   to any boss (because BFS expands layer by layer).
"""

from collections import deque

INF = 10**9
DIRS_4 = ((0, 1), (1, 0), (0, -1), (-1, 0))


def boss_distances(grid: list[str]) -> list[list[int]]:
    """Return min distance from each cell to nearest 'B' using multisource BFS."""
    if not grid:
        return []

    rows, cols = len(grid), len(grid[0])
    dist = [[INF] * cols for _ in range(rows)]
    q: deque[tuple[int, int]] = deque()

    # Multi-source setup: all bosses start at distance 0.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "B":
                dist[r][c] = 0
                q.append((r, c))

    while q:
        r, c = q.popleft()
        for dr, dc in DIRS_4:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":  # walls block movement
                continue

            next_dist = dist[r][c] + 1
            if next_dist < dist[nr][nc]:
                dist[nr][nc] = next_dist
                q.append((nr, nc))

    return dist


def print_distance_grid(dist: list[list[int]]) -> None:
    for row in dist:
        print(" ".join("INF" if x >= INF else f"{x:3d}" for x in row))


def example() -> None:
    grid = [
        "D..#.",
        ".#..B",
        "..#..",
        "B...D",
    ]

    dist = boss_distances(grid)
    print("Input grid:")
    for row in grid:
        print(row)

    print("\nDistance to nearest boss (multisource BFS):")
    print_distance_grid(dist)

    # How to read "distance from desk to any boss":
    # just look up dist at desk cell(s).
    desks = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == "D"]
    for r, c in desks:
        value = dist[r][c]
        print(f"Desk at {(r, c)} -> nearest boss distance: {value if value < INF else 'INF'}")


if __name__ == "__main__":
    example()
