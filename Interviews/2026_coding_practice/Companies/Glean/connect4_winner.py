"""
Connect 4 winner check (interview-friendly).

Key idea:
After each move, only check lines that pass through the newly placed piece.
Directions to check:
  - horizontal  (0, 1)
  - vertical    (1, 0)
  - diag down   (1, 1)
  - diag up     (1, -1)
"""

from typing import List, Optional, Tuple


class Connect4:
    ROWS = 6
    COLS = 7
    EMPTY = "."
    DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

    def __init__(self, rows: int = ROWS, cols: int = COLS) -> None:
        self.rows = rows
        self.cols = cols
        self.board: List[List[str]] = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]

    def drop_piece(self, col: int, player: str) -> Optional[Tuple[int, int]]:
        """
        Drop a piece in a column.
        Returns (row, col) where piece lands, or None if column is full/invalid.
        """
        if not (0 <= col < self.cols):
            return None
        if len(player) != 1 or player == self.EMPTY:
            raise ValueError("Player token must be one non-empty character.")

        for row in range(self.rows - 1, -1, -1):  # bottom -> top
            if self.board[row][col] == self.EMPTY:
                self.board[row][col] = player
                return row, col
        return None

    def has_winner(self, row: int, col: int, player: str) -> bool:
        """Check whether last move at (row, col) creates a connect-4."""
        for d_row, d_col in self.DIRS:
            total = 1  # include current piece
            total += self._count_one_direction(row, col, d_row, d_col, player)
            total += self._count_one_direction(row, col, -d_row, -d_col, player)
            if total >= 4:
                return True
        return False

    def _count_one_direction(self, row: int, col: int, d_row: int, d_col: int, player: str) -> int:
        count = 0
        r, c = row + d_row, col + d_col
        while self._in_bounds(r, c) and self.board[r][c] == player:
            count += 1
            r += d_row
            c += d_col
        return count

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def render(self) -> str:
        return "\n".join(" ".join(row) for row in self.board)


def play_move(game: Connect4, col: int, player: str) -> bool:
    """Utility for interviews: drop + win-check in one call."""
    placed = game.drop_piece(col, player)
    if placed is None:
        raise ValueError(f"Invalid move: column {col} is full or out of bounds.")
    row, placed_col = placed
    return game.has_winner(row, placed_col, player)


def main() -> None:
    game = Connect4()
    moves = [
        (0, "X"),
        (0, "O"),
        (1, "X"),
        (1, "O"),
        (2, "X"),
        (2, "O"),
        (3, "X"),  # X wins horizontally on bottom row
    ]

    winner = None
    for col, player in moves:
        if play_move(game, col, player):
            winner = player
            break

    print(game.render())
    print(f"\nWinner: {winner}" if winner else "\nNo winner yet.")


if __name__ == "__main__":
    main()
